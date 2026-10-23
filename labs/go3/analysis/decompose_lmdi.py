"""decompose_lmdi.py - LMDI-I additive decomposition of passenger-transport CO2.

  CO2 = sum over modes m of  A x S_m x I_m x C_m
    A   activity          total passenger-km (all modes, incl. walk and cycle)
    S_m structure         mode share of passenger-km
    I_m energy intensity  EJ per passenger-km of mode m
    C_m carbon intensity  tCO2 per EJ of mode m (direct, from the fuel mix)
  Effect of factor X = sum_m L(CO2_m^1, CO2_m^0) x ln(X_m^1 / X_m^0),
  L(a, b) = (a - b) / (ln a - ln b) (logarithmic mean; L(a, a) = a). The four effects add up
  EXACTLY to the change in CO2 (Ang 2005, Energy Policy 33:867-871; Ang 2015 Energy Policy 86:233-238).
  Zero values are replaced by 1e-12 (Ang & Liu 2007 recommend a small number), so modes with no
  direct CO2 (rail on electricity) contribute nothing.

Two uses: over time (2020 -> 2050 within a scenario) and across scenarios (Reference -> policy in 2050).
Direct emission factors (tCO2/GJ): refined liquids 19.6 kgC/GJ, gas 14.2 kgC/GJ (gcam-core
input/gcamdata/inst/extdata/energy/A_PrimaryFuelCCoef.csv), electricity and hydrogen 0 at the tailpipe.
Input: analysis/out/{service_by_mode,energy_by_mode_fuel}.csv from read_transport.py.
Run: python decompose_lmdi.py   (writes out/lmdi_results.csv)
"""
import math, os
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
EF = {"refined liquids enduse": 19.6 * 44 / 12 / 1000, "delivered gas": 14.2 * 44 / 12 / 1000}  # tCO2/GJ
EPS = 1e-12


def L(a, b):
    a, b = max(a, EPS), max(b, EPS)
    return a if abs(a - b) < 1e-15 else (a - b) / (math.log(a) - math.log(b))


def factors(svc, en, scen, year):
    s = svc[(svc.scenario == scen) & (svc.year == year)].groupby("mode").value.sum()
    e = en[(en.scenario == scen) & (en.year == year)].copy()
    e["co2"] = e.apply(lambda r: r.value * 1e3 * EF.get(r.fuel, 0.0), axis=1)     # EJ -> Mt CO2
    ej = e.groupby("mode").value.sum(); co2 = e.groupby("mode").co2.sum()
    A = s.sum(); out = {}
    for m in ej.index:
        out[m] = dict(A=A, S=s[m] / A, I=ej[m] / s[m], C=(co2[m] / ej[m]) if ej[m] > 0 else 0.0, CO2=co2[m])
    return out


def lmdi(f0, f1):
    eff = dict(activity=0.0, structure=0.0, intensity=0.0, carbon=0.0)
    for m in set(f0) | set(f1):
        a = f0.get(m, dict(A=1, S=EPS, I=EPS, C=EPS, CO2=0.0)); b = f1.get(m, dict(A=1, S=EPS, I=EPS, C=EPS, CO2=0.0))
        if a["CO2"] <= 0 and b["CO2"] <= 0:
            continue
        w = L(b["CO2"], a["CO2"])
        for k, x in (("activity", "A"), ("structure", "S"), ("intensity", "I"), ("carbon", "C")):
            eff[k] += w * math.log(max(b[x], EPS) / max(a[x], EPS))
    tot0 = sum(v["CO2"] for v in f0.values()); tot1 = sum(v["CO2"] for v in f1.values())
    eff.update(co2_start=tot0, co2_end=tot1, change=tot1 - tot0, residual=tot1 - tot0 - sum(eff[k] for k in ("activity", "structure", "intensity", "carbon")))
    return eff


def main():
    svc = pd.read_csv(os.path.join(HERE, "out", "service_by_mode.csv"))
    en = pd.read_csv(os.path.join(HERE, "out", "energy_by_mode_fuel.csv"))
    rows = []
    for sc in sorted(svc.scenario.unique()):
        rows.append(dict(comparison=f"{sc}: 2020 -> 2050", **lmdi(factors(svc, en, sc, 2020), factors(svc, en, sc, 2050))))
    for sc in sorted(svc.scenario.unique()):
        if sc != "Reference":
            rows.append(dict(comparison=f"2050: Reference -> {sc}", **lmdi(factors(svc, en, "Reference", 2050), factors(svc, en, sc, 2050))))
    df = pd.DataFrame(rows)
    pd.set_option("display.width", 160)
    print(df.round(2).to_string(index=False))
    print(f"\nlargest |residual| = {df.residual.abs().max():.2e} Mt (LMDI is exact up to rounding)")
    df.to_csv(os.path.join(HERE, "out", "lmdi_results.csv"), index=False)


if __name__ == "__main__":
    main()
