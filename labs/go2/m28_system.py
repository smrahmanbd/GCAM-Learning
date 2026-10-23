"""Module 2.8 - The system together: a tiny one-region power-and-land toy IAM.

Each 5-year step: electricity demand grows with income -> technologies share the market by a
logit on cost (with the carbon price) -> bioenergy with CCS needs land, and land gets dearer
the more is used (a second market, solved together) -> emissions -> warming added by this
sector (TCRE). Compare Reference, a carbon price and an emissions cap. Illustrative only.
Run:  python m28_system.py
"""
import numpy as np
from scipy.optimize import brentq

years = np.arange(2025, 2101, 5)
techs = ["coal", "gas", "solar", "bio_ccs"]
cost0 = np.array([60.0, 70.0, 80.0, 110.0])           # $/MWh before carbon price
ef = np.array([0.9, 0.4, 0.0, -0.8])                  # tCO2/MWh (bio with CCS removes CO2)
decline = np.array([0.0, 0.0, 0.015, 0.005])          # yearly cost decline (assumed, not learned)
LAND_COST = 0.08                                      # $/MWh added per million ha of energy crops

def bio_land(gen_twh):                                # Mha = TWh * 3.6 PJ/TWh / 0.35 eff / 180 GJ/ha
    return gen_twh * 3.6 / 0.35 / 180

def step(t, cp, demand):
    def mix(land_adder):
        c = cost0 * (1 - decline) ** t + ef * cp
        c[3] += land_adder
        x = np.maximum(c, 5.0) ** -6.0
        return x / x.sum()
    # land market: find the land price adder consistent with the land the mix uses
    g = lambda a: a - LAND_COST * bio_land(demand * mix(a)[3])
    a = brentq(g, 0, 1e4)
    s = mix(a)
    return s, demand * s

def run(price_path):
    cum, out = 0.0, []
    for y, cp in zip(years, price_path):
        t = y - 2025
        demand = 30000 * 1.02 ** t                     # TWh
        s, gen = step(t, cp, demand)
        co2 = float(gen @ ef) / 1000                   # Gt (TWh x t/MWh = Mt)
        cum += co2 * 5
        out.append(dict(year=int(y), co2=co2, solar=s[2], bio_land=bio_land(gen[3]), dT=0.45 * cum / 1000))
    return out

ref = run(np.zeros(len(years)))
tax = run(25 * 1.05 ** (years - 2025))
i50 = list(years).index(2050)
target = 0.5 * ref[0]["co2"]
p0 = brentq(lambda p: run(p * 1.05 ** (years - 2025))[i50]["co2"] - target, 0.01, 5000)
cap = run(p0 * 1.05 ** (years - 2025))
for name, r in (("Reference", ref), ("Carbon price", tax), ("Cap -50% by 2050", cap)):
    print(f"{name:<17} 2050: CO2 {r[i50]['co2']:6.2f} Gt, solar share {r[i50]['solar']:.2f}, "
          f"bio land {r[i50]['bio_land']:6.1f} Mha | warming added by 2100 {r[-1]['dT']:.2f} C")
print(f"The cap is met by a carbon price starting at {p0:.1f} $/t in 2025 and growing 5%/yr:"
      " a price and a cap are two doors to the same room.")
