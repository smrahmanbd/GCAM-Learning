"""
gcam_transport_toy.py -- a stand-alone passenger-transport model that mimics GCAM's structure.

WHAT IT MIMICS (GCAM 9.1, gcam-core tag gcam-v9.1; file paths are relative to gcam-core/)
  * Nesting: trn_pass -> {Walk, Cycle, Passenger Rail, Domestic Aviation, road}
             road  -> trn_pass_road     -> {Bus, LDV}
             LDV   -> trn_pass_road_LDV -> {2W and 3W, 4W}
             4W    -> trn_pass_road_LDV_4W -> {Car}   (GCAM also has Mini Car and Large Car and Truck)
    Sources: input/gcamdata/inst/extdata/energy/A54.sector.csv,
             A54.tranSubsector_logit_revised.csv, A54.globaltech_passthru_revised.csv,
             energy/mappings/UCD_techs_revised.csv
  * Logit types and exponents
      - competition among modes (supplysector level): relative-cost logit; trn_pass -2,
        trn_pass_road -4, trn_pass_road_LDV -4 (A54.sector.csv; a blank logit.type defaults to
        relative-cost-logit in input/gcamdata/R/xml.R lines 207-208)
      - competition among technologies inside a mode (tranSubsector level): absolute-cost logit;
        Car -8, 2W and 3W -8, Bus -3, Passenger Rail -1, Domestic Aviation -6
        (A54.tranSubsector_logit_revised.csv)
      - absolute-cost logit: share_i ~ sw_i * exp(beta * p_i / p0), where p0 is the cost of the
        most expensive calibrated option in the calibration year
        (cvs/objects/functions/source/absolute_cost_logit.cpp, lines 111-124;
         cvs/objects/util/base/source/calibrate_share_weight_visitor.cpp, lines 136-162)
      - relative-cost logit: share_i ~ sw_i * p_i ** gamma (relative_cost_logit.cpp)
  * Technology cost per passenger-km = (non-fuel cost per vkm + fuel price x intensity) / load factor
    (cvs/objects/technologies/source/tran_technology.cpp, getTotalInputCost / getEnergyCost)
  * Mode (subsector) price = share-weighted technology cost + time value when addTimeValue = 1
    time value = wage x time-value-multiplier / speed, wage = GDP per capita / (40 h x 50 weeks)
    (cvs/objects/sectors/source/tran_subsector.cpp lines 175-214; multipliers and addTimeValue
     from A54.tranSubsector_VOTT_revised.csv)
  * Sector price = share-weighted subsector price (cvs/objects/sectors/source/sector.cpp 324-339)
  * Service demand D_t = D_{t-1} (Y_t/Y_{t-1})^income (P_t/P_{t-1})^price (N_t/N_{t-1}),
    trn_pass price elasticity -1.25 and income elasticity 1.0 (A54.demand.csv)
  * Share-weight calibration to base-year output, anchored on the largest option
    (calibrate_share_weight_visitor.cpp); new technologies get share-weights from an
    assumption path like A54.globaltranTech_shrwt_revised.csv (BEV 0 until 2025, 1 from 2030;
    FCEV 0 in 2030 rising to 0.5 in 2050 -- linear here, GCAM uses an s-curve)

WHAT IT DOES NOT DO: vintages and retirement, the solver (no fuel-price feedback), freight,
international aviation and shipping, several LDV size classes, fuel-preference elasticities.

NUMBERS: illustrative. Car, bus, rail and aviation costs, intensities, load factors and speeds are
rounded from the "Middle East" rows of UCD_trn_data_CORE.csv and OTAQ_trn_data_EMF37.csv
(Compact Car for cars; capital annualised at 10% over 10 years, 14,000 vkm/yr, as in
R/zenergy_L154.transportation_UCD.R). Money is 2005$ (GCAM 9.1 uses 1975$ internally:
1975$ = 0.341 x 2005$ with gcamdata's gdp_deflator). Base-year activity, fuel prices, 2W and
BEV-bus costs are invented. This is a teaching model, not GCAM output.

Run:  python gcam_transport_toy.py        (writes toy_results.csv next to this file)
"""
import csv
import math
import os

YEARS = list(range(2020, 2101, 5))
BASE = 2020

# ---------------------------------------------------------------- helpers
def interp(points, year):
    """Linear interpolation in a {year: value} dict, flat outside the range."""
    ys = sorted(points)
    if year <= ys[0]:
        return points[ys[0]]
    if year >= ys[-1]:
        return points[ys[-1]]
    for a, b in zip(ys, ys[1:]):
        if a <= year <= b:
            return points[a] + (points[b] - points[a]) * (year - a) / (b - a)


EF = {"refined liquids enduse": 19.6 * 44 / 12 / 1000,   # tCO2 per GJ (A_PrimaryFuelCCoef.csv: 19.6 kgC/GJ)
      "delivered gas": 14.2 * 44 / 12 / 1000,            # 14.2 kgC/GJ
      "elect_td_trn": 0.0, "H2 LDV": 0.0, "H2 MHDV": 0.0}  # emissions counted where power/H2 is made

# ---------------------------------------------------------------- scenario settings
SCENARIOS = {
    "Reference":      dict(),
    "BEV-low":        dict(bev_cost_mult=0.70),          # BEV non-fuel cost -30% from 2030
    "Carbon-price":   dict(carbon=True),                 # 50 $/tCO2 in 2025, +5%/yr
    "Fast-wage":      dict(gdp_growth=0.03),             # GDP per capita +3%/yr instead of +2%/yr
    "LF-up":          dict(car_lf_2050=2.60),            # car occupancy rises instead of falling
}


def fuel_price(fuel, year, sc):
    base = {"refined liquids enduse": interp({2020: 15.0, 2050: 18.0}, year),
            "delivered gas": 8.0,
            "elect_td_trn": 30.0,
            "H2 LDV": interp({2020: 45.0, 2050: 30.0}, year),
            "H2 MHDV": interp({2020: 40.0, 2050: 28.0}, year)}[fuel]        # 2005$/GJ, illustrative
    if sc.get("carbon") and year >= 2025:
        # carbon price in 2005$/tCO2: 50 in 2025 (or sc["carbon_start"]) rising 5%/yr
        base += EF[fuel] * sc.get("carbon_start", 50.0) * 1.05 ** (year - 2025)
    return base


def gdp_pc(year, sc):                      # thousand 2005$ per person (illustrative)
    return 18.0 * (1 + sc.get("gdp_growth", 0.02)) ** (year - BASE)


def population(year):                      # million people (illustrative logistic)
    return 260.0 + 140.0 * (1 - math.exp(-0.025 * (year - BASE)))


# ---------------------------------------------------------------- technologies
# per technology: fuel, non-fuel cost (2005$/vkm), intensity (MJ/vkm), load factor (pers/veh),
# share-weight path for non-calibrated technologies
def techs(year, sc):
    car_lf = interp({2020: 2.33, 2050: sc.get("car_lf_2050", 2.00)}, year)
    bev_mult = sc.get("bev_cost_mult", 1.0) if year >= 2030 else 1.0
    car = {
        "Liquids":        dict(fuel="refined liquids enduse", nf=interp({2020: .6345, 2030: .6747, 2050: .7652}, year),
                               mj=interp({2020: 3.322, 2030: 3.101, 2050: 2.718}, year), lf=car_lf),
        "Hybrid Liquids": dict(fuel="refined liquids enduse", nf=interp({2020: .6629, 2030: .7081, 2050: .7872}, year),
                               mj=interp({2020: 2.581, 2030: 2.454, 2050: 2.226}, year), lf=car_lf),
        "NG":             dict(fuel="delivered gas", nf=interp({2020: .6599, 2030: .7017, 2050: .7958}, year),
                               mj=interp({2020: 3.355, 2030: 3.132, 2050: 2.745}, year), lf=car_lf),
        "BEV":            dict(fuel="elect_td_trn", nf=bev_mult * interp({2020: .7407, 2030: .6894, 2050: .7652}, year),
                               mj=interp({2020: 1.026, 2030: 1.019, 2050: 1.005}, year), lf=car_lf,
                               sw={2020: 0, 2025: 0, 2030: 1}),
        "FCEV":           dict(fuel="H2 LDV", nf=interp({2020: .8050, 2030: .7280, 2050: .7799}, year),
                               mj=interp({2020: 1.572, 2030: 1.518, 2050: 1.418}, year), lf=car_lf,
                               sw={2020: 0, 2030: 0, 2050: 0.5}),
    }
    bus = {
        "Liquids": dict(fuel="refined liquids enduse", nf=1.6319, mj=interp({2020: 7.908, 2050: 7.884}, year), lf=25.0),
        "NG":      dict(fuel="delivered gas", nf=1.7609, mj=interp({2020: 7.908, 2050: 7.884}, year), lf=25.0),
        "BEV":     dict(fuel="elect_td_trn", nf=interp({2020: 2.00, 2050: 1.70}, year), mj=3.0, lf=25.0,
                        sw={2020: 0, 2025: 0, 2050: 1}),
    }
    two_w = {
        "Liquids": dict(fuel="refined liquids enduse", nf=0.12, mj=1.0, lf=1.3),
        "BEV":     dict(fuel="elect_td_trn", nf=interp({2020: 0.14, 2050: 0.11}, year), mj=0.30, lf=1.3,
                        sw={2020: 0, 2025: 0, 2030: 1}),
    }
    rail = {"Electric": dict(fuel="elect_td_trn", nf=16.005, mj=53.197, lf=1152.0)}
    air = {"Liquids": dict(fuel="refined liquids enduse", nf=13.77, mj=interp({2020: 366.5, 2050: 310.6}, year),
                           lf=interp({2020: 148.8, 2050: 161.6}, year))}
    return {"Car": car, "Bus": bus, "2W and 3W": two_w, "Passenger Rail": rail, "Domestic Aviation": air}


TECH_EXP = {"Car": -8, "Bus": -3, "2W and 3W": -8, "Passenger Rail": -1, "Domestic Aviation": -6}
# mode-level settings: time-value multiplier, addTimeValue, speed (km/h)
MODES = {
    "Walk":              dict(vott=1.066, add=1, speed=lambda y: 4.8),
    "Cycle":             dict(vott=1.066, add=1, speed=lambda y: 15.0),
    "Passenger Rail":    dict(vott=0.80, add=1, speed=lambda y: 42.0),
    "Domestic Aviation": dict(vott=1.244, add=1, speed=lambda y: 197.0),
    "Bus":               dict(vott=0.808, add=1, speed=lambda y: interp({2020: 22, 2050: 24, 2100: 25}, y)),
    "2W and 3W":         dict(vott=0.82, add=1, speed=lambda y: 30.0),
    "4W":                dict(vott=0.82, add=1, speed=lambda y: interp({2020: 35, 2050: 40, 2100: 42}, y)),
    "road":              dict(vott=1.0, add=0, speed=lambda y: 1.0),
    "LDV":               dict(vott=1.0, add=0, speed=lambda y: 1.0),
}
NEST = {  # sector: (logit exponent, children)
    "trn_pass":          (-2, ["Walk", "Cycle", "Passenger Rail", "Domestic Aviation", "road"]),
    "trn_pass_road":     (-4, ["Bus", "LDV"]),
    "trn_pass_road_LDV": (-4, ["2W and 3W", "4W"]),
}
CHILD_SECTOR = {"road": "trn_pass_road", "LDV": "trn_pass_road_LDV", "4W": "Car"}

# base-year (2020) passenger-km, billion (illustrative)
BASE_PKM = {"Walk": 70.0, "Cycle": 25.0, "Passenger Rail": 6.0, "Domestic Aviation": 55.0,
            "Bus": {"Liquids": 157.0, "NG": 3.0}, "2W and 3W": {"Liquids": 45.0},
            "Car": {"Liquids": 1120.0, "Hybrid Liquids": 20.0, "NG": 10.0}}


# ---------------------------------------------------------------- logit functions
def rel_shares(prices, sws, g):
    w = {k: (sws[k] * prices[k] ** g if sws[k] > 0 else 0.0) for k in prices}
    t = sum(w.values())
    return {k: v / t for k, v in w.items()}


def abs_shares(costs, sws, beta, p0):
    w = {k: (sws[k] * math.exp(beta * costs[k] / p0) if sws[k] > 0 else 0.0) for k in costs}
    t = sum(w.values())
    return {k: v / t for k, v in w.items()}


def run(name, sc):
    cal = {}                     # calibrated share-weights and base costs (from the base year)
    rows, demand_prev, price_prev = [], None, None
    for year in YEARS:
        T = techs(year, sc)
        wage = gdp_pc(year, sc) * 1000 / (40 * 50)        # 2005$ per hour
        tech_cost, tech_share, mode_money = {}, {}, {}
        # 1) technology level (absolute-cost logit inside each mode)
        for mode, tt in T.items():
            costs = {k: (v["nf"] + fuel_price(v["fuel"], year, sc) * v["mj"] / 1000) / v["lf"] for k, v in tt.items()}
            tech_cost[mode] = costs
            if year == BASE:
                base = BASE_PKM[mode] if isinstance(BASE_PKM[mode], dict) else {list(tt)[0]: BASE_PKM[mode]}
                calk = {k: base.get(k, 0.0) for k in tt}
                tot = sum(calk.values())
                p0 = max(costs[k] for k in tt if calk[k] > 0)            # most expensive calibrated option
                anchor = max(calk, key=calk.get)
                sws = {}
                for k in tt:
                    if calk[k] > 0:   # inverse of the absolute logit (calibrate_share_weight_visitor.cpp)
                        sws[k] = (calk[k] / tot) / (calk[anchor] / tot) * math.exp(TECH_EXP[mode] / p0 * (costs[anchor] - costs[k]))
                    else:
                        sws[k] = 0.0
                cal[mode] = dict(p0=p0, sw=sws)
            sws = {k: (interp(v["sw"], year) if "sw" in v and cal[mode]["sw"][k] == 0 else cal[mode]["sw"][k]) for k, v in tt.items()}
            sh = abs_shares(costs, sws, TECH_EXP[mode], cal[mode]["p0"])
            tech_share[mode] = sh
            mode_money[mode] = sum(sh[k] * costs[k] for k in costs)
        mode_money["Walk"] = mode_money["Cycle"] = 0.0      # non-motorised: no money cost
        mode_money["4W"] = mode_money["Car"]                # pass-through: 4W sector holds only Car

        def mode_price(m):
            md = MODES[m]
            tv = wage * md["vott"] / md["speed"](year) if md["add"] else 0.0
            return mode_money[m] + tv

        # 2) nests from the bottom up (relative-cost logit among modes)
        sector_price, mode_sh = {}, {}
        for sector in ["trn_pass_road_LDV", "trn_pass_road", "trn_pass"]:
            g, kids = NEST[sector]
            prices = {}
            for k in kids:
                prices[k] = sector_price[CHILD_SECTOR[k]] if k in ("road", "LDV") else mode_price(k)
            if year == BASE:
                def base_out(k):
                    if k == "road": return base_out("Bus") + base_out("LDV")
                    if k == "LDV": return base_out("2W and 3W") + base_out("4W")
                    if k == "4W": return sum(BASE_PKM["Car"].values())
                    v = BASE_PKM[k]
                    return sum(v.values()) if isinstance(v, dict) else v
                outs = {k: base_out(k) for k in kids}
                anchor = max(outs, key=outs.get)
                cal[sector] = {k: (outs[k] / outs[anchor]) * (prices[anchor] / prices[k]) ** g for k in kids}
            sh = rel_shares(prices, cal[sector], g)
            mode_sh[sector] = sh
            sector_price[sector] = sum(sh[k] * prices[k] for k in kids)
        P = sector_price["trn_pass"]

        # 3) total passenger demand (billion pkm)
        if year == BASE:
            D = sum(BASE_PKM[m] if not isinstance(BASE_PKM[m], dict) else sum(BASE_PKM[m].values()) for m in BASE_PKM)
        else:
            y_ratio = gdp_pc(year, sc) / gdp_pc(year - 5, sc)
            D = demand_prev * y_ratio ** 1.0 * (P / price_prev) ** -1.25 * population(year) / population(year - 5)
        demand_prev, price_prev = D, P

        # 4) pkm by mode and technology, energy and CO2
        top, road, ldv = mode_sh["trn_pass"], mode_sh["trn_pass_road"], mode_sh["trn_pass_road_LDV"]
        mode_pkm = {"Walk": D * top["Walk"], "Cycle": D * top["Cycle"], "Passenger Rail": D * top["Passenger Rail"],
                    "Domestic Aviation": D * top["Domestic Aviation"], "Bus": D * top["road"] * road["Bus"],
                    "2W and 3W": D * top["road"] * road["LDV"] * ldv["2W and 3W"],
                    "Car": D * top["road"] * road["LDV"] * ldv["4W"]}
        energy, co2 = {}, 0.0
        for m, pk in mode_pkm.items():
            rows.append((name, year, "service output by mode", m, pk, "billion pkm"))
            rows.append((name, year, "mode share", m, pk / D, "fraction"))
            if m in T:
                for k, s in tech_share[m].items():
                    v = T[m][k]
                    ej = pk * s / v["lf"] * v["mj"] / 1000              # billion vkm x MJ/vkm = PJ -> EJ
                    energy[v["fuel"]] = energy.get(v["fuel"], 0.0) + ej
                    co2 += ej * 1e3 * EF[v["fuel"]]                      # EJ -> PJ = million GJ; x t/GJ = Mt
                    rows.append((name, year, "tech share", f"{m}|{k}", s, "fraction"))
        rows.append((name, year, "service output", "trn_pass", D, "billion pkm"))
        rows.append((name, year, "service price", "trn_pass", P, "2005$/pkm"))
        for f, e in sorted(energy.items()):
            rows.append((name, year, "final energy by fuel", f, e, "EJ"))
        rows.append((name, year, "CO2 (direct)", "trn_pass", co2, "MtCO2"))
    return rows


if __name__ == "__main__":
    allrows = []
    for name, sc in SCENARIOS.items():
        allrows += run(name, sc)
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "toy_results.csv")
    with open(out, "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["scenario", "year", "variable", "item", "value", "unit"])
        for r in allrows:
            w.writerow([r[0], r[1], r[2], r[3], f"{r[4]:.6g}", r[5]])
    # tidy summary table
    get = {(r[0], r[1], r[2], r[3]): r[4] for r in allrows}
    print(f"{'scenario':<13}{'year':>5}{'pkm(bn)':>9}{'car%':>7}{'bus%':>6}{'rail%':>6}{'air%':>6}"
          f"{'BEV%car':>8}{'FCEV%car':>9}{'liqEJ':>7}{'elecEJ':>7}{'CO2 Mt':>8}")
    for name in SCENARIOS:
        for year in (2020, 2030, 2050, 2075, 2100):
            g = lambda v, i: get.get((name, year, v, i), 0.0)
            print(f"{name:<13}{year:>5}{g('service output', 'trn_pass'):9.0f}{100 * g('mode share', 'Car'):7.1f}"
                  f"{100 * g('mode share', 'Bus'):6.1f}{100 * g('mode share', 'Passenger Rail'):6.1f}"
                  f"{100 * g('mode share', 'Domestic Aviation'):6.1f}{100 * g('tech share', 'Car|BEV'):8.1f}"
                  f"{100 * g('tech share', 'Car|FCEV'):9.1f}{g('final energy by fuel', 'refined liquids enduse'):7.2f}"
                  f"{g('final energy by fuel', 'elect_td_trn'):7.2f}{g('CO2 (direct)', 'trn_pass'):8.0f}")
    print(f"\nWrote {out}")
