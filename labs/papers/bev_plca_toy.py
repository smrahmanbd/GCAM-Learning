"""
A toy time-adjusted prospective LCA (pLCA) of passenger cars.

Teaching companion to:
  Simaitis, J., Lupton, R., Vagg, C., Butnar, I., Sacchi, R. & Allen, S. (2025).
  Battery electric vehicles show the lowest carbon footprints among passenger cars
  across 1.5-3.0 degC energy decarbonisation pathways.
  Communications Earth & Environment 6, 476. https://doi.org/10.1038/s43247-025-02447-2

What this is
  A deliberately small model that reproduces the *logic* of the paper:
    footprint per km = (production + end-of-life) / lifetime km
                       + average over the use years of (energy per km x carbon per unit of energy)
  and compares a "typical" static LCA (all stages use 2025 energy) with a
  time-adjusted pLCA (each year of driving uses that year's energy mix from a scenario).

What this is NOT
  The paper used TIAM-UCL scenarios, premise, ecoinvent 3.9.1, carculator and
  brightway2. Every number below is ILLUSTRATIVE, chosen so the toy lands close to
  the paper's headline figures (e.g. BEV ~32-47% below HEV; breakeven ~50-90k km).
  Do not cite these numbers as results.

Run:  python3 bev_plca_toy.py          (prints the worked solutions)
Needs: Python 3.8+ only (numpy/matplotlib optional for the plot at the end).
"""
import json
import random

# ---------------------------------------------------------------------------
# 1. Parameters (illustrative, Medium SUV = size factor 1.0)
# ---------------------------------------------------------------------------
YEARS = [2025, 2030, 2035, 2040, 2045, 2050]

PARAMS = {
    "powertrains": ["BEV", "PHEV", "HEV", "FCEV"],
    # cradle-to-gate production, t CO2e per vehicle (2025 build, Medium SUV)
    "production_t": {"BEV": 15.0, "PHEV": 10.0, "HEV": 7.5, "FCEV": 12.5},
    "eol_t": 0.3,                      # end of life, t CO2e (cut-off: no recycling credit)
    # energy use per km (Medium SUV, WLTP-like)
    "kwh_per_km": {"BEV": 0.235, "PHEV": 0.17, "HEV": 0.0, "FCEV": 0.0},
    "litre_per_km": {"BEV": 0.0, "PHEV": 0.028, "HEV": 0.060, "FCEV": 0.0},
    "kgh2_per_km": {"BEV": 0.0, "PHEV": 0.0, "HEV": 0.0, "FCEV": 0.0105},
    # diesel
    "diesel_exhaust_kg_per_l": 2.68,   # fossil CO2 at the tailpipe
    "diesel_supply_kg_per_l": 0.55,    # well-to-tank, fossil diesel
    "biodiesel_supply_kg_per_l": 1.0,  # well-to-tank, biodiesel (its tailpipe CO2 is biogenic = 0)
    # sizes scale production and energy use
    "sizes": {"Small": 0.75, "Medium": 0.9, "Medium SUV": 1.0, "Large SUV": 1.2},
    # 2025 life-cycle carbon intensity of electricity, kg CO2e/kWh, the 16 TIAM-UCL regions (illustrative)
    "grid_2025": {"AFR": 0.50, "AUS": 0.47, "CAN": 0.12, "CHI": 0.56, "CSA": 0.15, "EEU": 0.62,
                  "FSU": 0.38, "IND": 0.64, "JPN": 0.40, "MEA": 0.48, "MEX": 0.38, "ODA": 0.43,
                  "SKO": 0.40, "UK": 0.18, "USA": 0.34, "WEU": 0.20},
    "region_names": {"AFR": "Africa", "AUS": "Australia & NZ", "CAN": "Canada", "CHI": "China",
                     "CSA": "Central & South America", "EEU": "Eastern Europe", "FSU": "Former Soviet Union",
                     "IND": "India", "JPN": "Japan", "MEA": "Middle East", "MEX": "Mexico",
                     "ODA": "Other developing Asia", "SKO": "South Korea", "UK": "United Kingdom",
                     "USA": "United States", "WEU": "Western Europe"},
    "scenarios": ["No scenario", "No climate action", "Baseline (NDCs)", "Ambitious (<2 °C)", "Very ambitious (1.5 °C)"],
    "rcp": {"No scenario": "static 2025", "No climate action": "SSP2-RCP6.0", "Baseline (NDCs)": "SSP2-RCP4.5",
            "Ambitious (<2 °C)": "SSP2-RCP2.6", "Very ambitious (1.5 °C)": "SSP2-RCP1.9"},
    # grid intensity as a fraction of the region's 2025 value, at YEARS
    "grid_factor": {
        "No scenario":             [1, 1, 1, 1, 1, 1],
        "No climate action":       [1, .93, .87, .82, .77, .72],
        "Baseline (NDCs)":         [1, .78, .62, .52, .45, .40],
        "Ambitious (<2 °C)":       [1, .75, .55, .40, .28, .18],
        "Very ambitious (1.5 °C)": [1, .55, .28, .12, .05, .0],
    },
    # biodiesel share of diesel supply at YEARS
    "bio_share": {
        "No scenario":             [0, 0, 0, 0, 0, 0],
        "No climate action":       [0, .02, .04, .06, .08, .10],
        "Baseline (NDCs)":         [0, .04, .08, .12, .16, .20],
        "Ambitious (<2 °C)":       [0, .08, .16, .25, .33, .40],
        "Very ambitious (1.5 °C)": [0, .12, .28, .42, .52, .60],
    },
    # hydrogen, kg CO2e per kg H2 at YEARS (global; 1.5 °C goes negative through BECCS)
    "h2_kg_per_kg": {
        "No scenario":             [13, 13, 13, 13, 13, 13],
        "No climate action":       [13, 12.5, 12, 11.5, 11, 10.5],
        "Baseline (NDCs)":         [13, 12, 10, 8, 6.5, 5],
        "Ambitious (<2 °C)":       [13, 11.5, 9, 6.5, 4.5, 3.5],
        "Very ambitious (1.5 °C)": [13, 3, -10, -20, -25, -28],
    },
    # a car built in 2035 instead of 2025
    "production_2035_factor": 0.77,
    "efficiency_2035_factor": {"BEV": 0.95, "PHEV": 0.85, "HEV": 0.93, "FCEV": 0.93},
}
P = PARAMS


def interp(series, year):
    """Linear interpolation on the 5-year grid; held flat after 2050."""
    if year <= YEARS[0]:
        return series[0]
    if year >= YEARS[-1]:
        return series[-1]
    i = int((year - YEARS[0]) // 5)
    f = (year - YEARS[i]) / 5
    return series[i] + f * (series[i + 1] - series[i])


def energy_intensities(region, scenario, year):
    """Carbon per unit of each energy carrier in a given year."""
    grid = P["grid_2025"][region] * interp(P["grid_factor"][scenario], year)
    b = interp(P["bio_share"][scenario], year)
    exhaust = P["diesel_exhaust_kg_per_l"] * (1 - b)
    supply = P["diesel_supply_kg_per_l"] * (1 - b) + P["biodiesel_supply_kg_per_l"] * b
    h2 = interp(P["h2_kg_per_kg"][scenario], year)
    return grid, exhaust, supply, h2


def footprint(pt, region="CHI", scenario="Ambitious (<2 °C)", size="Medium SUV",
              km=200_000, lifetime=15, build_year=2025, breakdown=False):
    """Life-cycle g CO2e per km. scenario='No scenario' gives the typical static LCA."""
    s = P["sizes"][size]
    prod = P["production_t"][pt] * s * (P["production_2035_factor"] if build_year >= 2035 else 1)
    eff = s * (P["efficiency_2035_factor"][pt] if build_year >= 2035 else 1)
    kwh, lit, h2kg = P["kwh_per_km"][pt] * eff, P["litre_per_km"][pt] * eff, P["kgh2_per_km"][pt] * eff
    km_per_year = km / lifetime
    elec = fuel_supply = exhaust = hyd = 0.0
    for y in range(lifetime):                        # time adjustment: each year uses its own mix
        yr = build_year + y + 0.5
        g, ex, sup, h = energy_intensities(region, scenario, yr)
        elec += km_per_year * kwh * g
        fuel_supply += km_per_year * lit * sup
        exhaust += km_per_year * lit * ex
        hyd += km_per_year * h2kg * h
    parts = {  # kg CO2e over the life
        "Production": prod * 1000, "Electricity": elec, "Diesel supply": fuel_supply,
        "Exhaust": exhaust, "Hydrogen": hyd, "End of life": P["eol_t"] * 1000,
    }
    gkm = {k: v / km * 1000 for k, v in parts.items()}  # g CO2e per km
    return gkm if breakdown else sum(gkm.values())


def breakeven_km(region, scenario, size="Medium SUV", lifetime=15, build_year=2025):
    """Smallest total mileage at which a BEV beats an HEV (bisection on km)."""
    f = lambda km: footprint("BEV", region, scenario, size, km, lifetime, build_year) - \
        footprint("HEV", region, scenario, size, km, lifetime, build_year)
    lo, hi = 1_000, 1_000_000
    if f(hi) > 0:
        return None
    for _ in range(60):
        mid = (lo + hi) / 2
        lo, hi = (mid, hi) if f(mid) > 0 else (lo, mid)
    return hi


def monte_carlo(n=5000, seed=1, scenarios=None):
    """Comparative (dependent) Monte Carlo: every powertrain sees the SAME sampled inputs."""
    rng = random.Random(seed)
    scenarios = scenarios or P["scenarios"]
    rows = []
    for _ in range(n):
        inp = dict(region=rng.choice(list(P["grid_2025"])), scenario=rng.choice(scenarios),
                   size=rng.choice(list(P["sizes"])), km=rng.uniform(100_000, 300_000),
                   lifetime=rng.randint(10, 20))
        rows.append({**inp, **{pt: footprint(pt, **inp) for pt in P["powertrains"]}})
    return rows


def mean(xs):
    xs = list(xs)
    return sum(xs) / len(xs)


# ---------------------------------------------------------------------------
# 2. Worked solutions (match the exercises on papers/bev-plca.html)
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    print("Exercise 1 - typical static LCA vs time-adjusted pLCA, China, Medium SUV, 200,000 km, 15 years")
    for pt in P["powertrains"]:
        st = footprint(pt, "CHI", "No scenario")
        pl = footprint(pt, "CHI", "Ambitious (<2 °C)")
        print(f"  {pt:5s} static {st:6.1f}  pLCA {pl:6.1f} g/km  change {100 * (pl / st - 1):+5.1f}%")

    print("\nExercise 2 - where does a BEV's footprint come from? (China, <2 °C)")
    for k, v in footprint("BEV", breakdown=True).items():
        print(f"  {k:14s} {v:6.1f} g/km")

    print("\nExercise 3 - breakeven mileage, Medium SUV, 15 years (average over 16 regions)")
    for sc in P["scenarios"]:
        bes = [breakeven_km(r, sc) for r in P["grid_2025"]]
        bes = [b for b in bes if b]
        print(f"  {sc:25s} mean {mean(bes) / 1000:5.0f}k km   worst {max(bes) / 1000:5.0f}k km")

    print("\nExercise 4 - comparative Monte Carlo, 5000 samples")
    rows = monte_carlo()
    for sc in P["scenarios"]:
        r = [x for x in rows if x["scenario"] == sc]
        b, h, f = mean(x["BEV"] for x in r), mean(x["HEV"] for x in r), mean(x["FCEV"] for x in r)
        share = 100 * mean(1 if x["BEV"] < x["HEV"] else 0 for x in r)
        print(f"  {sc:25s} BEV {b:5.0f} HEV {h:5.0f} FCEV {f:5.0f} g/km  BEV<HEV in {share:5.1f}%  "
              f"BEV {100 * (1 - b / h):4.0f}% below HEV")

    print("\nExercise 5 - a car built in 2035 (China, <2 °C)")
    for pt in P["powertrains"]:
        print(f"  {pt:5s} 2025 build {footprint(pt):6.1f}  2035 build {footprint(pt, build_year=2035):6.1f} g/km")

    print("\nExercise 6 - PHEV utility factor: how much does driver behaviour matter? (CHI, <2 °C)")
    base_k, base_l = P["kwh_per_km"]["PHEV"], P["litre_per_km"]["PHEV"]
    for uf in (0.2, 0.47, 0.8):
        P["kwh_per_km"]["PHEV"] = 0.36 * uf          # kWh/km in electric mode x share of km
        P["litre_per_km"]["PHEV"] = 0.053 * (1 - uf)  # L/km in fuel mode x share of km
        print(f"  utility factor {uf:.2f}: PHEV {footprint('PHEV'):6.1f}  vs BEV {footprint('BEV'):6.1f} "
              f"and HEV {footprint('HEV'):6.1f} g/km")
    P["kwh_per_km"]["PHEV"], P["litre_per_km"]["PHEV"] = base_k, base_l

    with open(__file__.replace(".py", "_params.json"), "w") as fh:
        json.dump(PARAMS, fh, indent=1, ensure_ascii=False)
