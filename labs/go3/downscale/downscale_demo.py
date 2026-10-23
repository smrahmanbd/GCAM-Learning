"""downscale_demo.py - from a GCAM region to countries: two downscaling methods on SYNTHETIC data.

Problem: GCAM reports transport energy for "Middle East", but a ministry asks about one country.
  Method 1, proportional: each country keeps its base-year share of the regional total.
  Method 2, convergence (inspired by DSCALE, Sferra et al. 2026, Geoscientific Model Development 19,
           doi:10.5194/gmd-19-3157-2026): each country's energy intensity (energy per unit of GDP)
           moves from its own base-year value toward the regional intensity, closing the gap
           log-linearly by a convergence year; country GDP follows its own projection; the
           results are then rescaled every year so countries add up exactly to the GCAM regional
           total (harmonisation). DSCALE itself does much more (several convergence criteria,
           sector detail, emissions with an optimisation step); this demo shows only the idea.
Data: six invented countries ("Country A".."Country F") in an invented region; the regional total
is the toy model's Reference passenger-transport final energy (sample_data). Nothing here is real.
Run: python downscale_demo.py   (writes downscale_results.csv and downscale_demo.png)
"""
import math, os
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = os.path.dirname(os.path.abspath(__file__))
en = pd.read_csv(os.path.join(HERE, "..", "analysis", "sample_data", "transport_final_energy_by_mode_and_fuel.csv"))
REG = en[en.scenario == "Reference"].groupby("Year").value.sum()        # EJ, regional total
YEARS = list(REG.index)

# invented base-year data: GDP (billion $), GDP growth (%/yr), transport energy (EJ) in 2020
C = pd.DataFrame({
    "country": ["Country A", "Country B", "Country C", "Country D", "Country E", "Country F"],
    "gdp0":    [800, 420, 180, 160, 75, 40],
    "growth":  [0.025, 0.030, 0.020, 0.022, 0.035, 0.040],
    "energy0": [0.80, 0.45, 0.25, 0.16, 0.12, 0.07]})
C["energy0"] *= REG[2020] / C.energy0.sum()           # make 2020 add up to the regional total
CONV_YEAR = 2100

rows = []
for y in YEARS:
    t = y - 2020
    gdp = C.gdp0 * (1 + C.growth) ** t
    # method 1: proportional
    prop = REG[y] * C.energy0 / C.energy0.sum()
    # method 2: convergence of energy intensity toward the regional intensity, then harmonise
    ei0 = C.energy0 / C.gdp0
    reg_ei = REG[y] / gdp.sum()
    w = min(1.0, t / (CONV_YEAR - 2020))
    ei = np.exp((1 - w) * np.log(ei0) + w * math.log(reg_ei))
    raw = ei * gdp
    conv = raw * REG[y] / raw.sum()                    # harmonised to the GCAM regional total
    for i, c in enumerate(C.country):
        rows.append(dict(year=y, country=c, gdp=gdp[i], proportional_EJ=prop[i], convergence_EJ=conv[i],
                         convergence_unharmonised_EJ=raw[i]))
df = pd.DataFrame(rows)
df.to_csv(os.path.join(HERE, "downscale_results.csv"), index=False)

chk = df.groupby("year")[["proportional_EJ", "convergence_EJ"]].sum().sub(REG, axis=0).abs().max().max()
print(f"Regional totals reproduced by both methods: max error {chk:.1e} EJ")
show = df[df.year.isin([2020, 2050, 2100])].pivot_table(index="country", columns="year",
                                                       values=["proportional_EJ", "convergence_EJ"]).round(3)
print(show.to_string())
harm = df[df.year == 2050].convergence_EJ.sum() / df[df.year == 2050].convergence_unharmonised_EJ.sum()
print(f"Harmonisation factor in 2050 (GCAM total / sum of unharmonised country values): {harm:.3f}")

fig, ax = plt.subplots(1, 2, figsize=(11, 4), sharey=True)
for a, col, title in ((ax[0], "proportional_EJ", "Proportional (fixed 2020 shares)"),
                      (ax[1], "convergence_EJ", "Intensity convergence + harmonisation")):
    p = df.pivot(index="year", columns="country", values=col)
    a.stackplot(p.index, p.T.values, labels=p.columns,
                colors=["#0b3954", "#0f8a8a", "#c4502e", "#4f8a2c", "#c27a1a", "#6a56a8"])
    a.set_title(title + " (synthetic)", fontsize=10); a.set_xlabel("year")
ax[0].set_ylabel("passenger transport final energy (EJ)"); ax[1].legend(fontsize=8, loc="upper left")
fig.tight_layout(); fig.savefig(os.path.join(HERE, "downscale_demo.png"), dpi=130)
print("wrote downscale_results.csv and downscale_demo.png")
