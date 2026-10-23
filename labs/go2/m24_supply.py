"""Module 2.4 - Energy supply: levelised cost, resource supply curve, learning.

Toy numbers only. Run:  python m24_supply.py
"""
import numpy as np

# 1. Levelised cost of electricity (LCOE) = capital recovery + fixed O&M + fuel + carbon
def crf(r, n):                                  # capital recovery factor
    return r * (1 + r) ** n / ((1 + r) ** n - 1)

def lcoe(capex, fom, cf, fuel_price=0.0, eff=1.0, ef=0.0, carbon=0.0, r=0.07, n=30):
    """capex $/kW, fom $/kW-yr, cf capacity factor, fuel $/GJ, eff output/input, ef tCO2/GJ fuel, carbon $/t."""
    mwh = cf * 8.76                              # MWh produced per kW per year
    cap = (capex * crf(r, n) + fom) / mwh        # $/MWh
    fuel = fuel_price * 3.6 / eff                # 3.6 GJ per MWh
    co2 = ef * 3.6 / eff * carbon
    return cap + fuel + co2

gas = dict(capex=1000, fom=25, cf=0.55, fuel_price=6, eff=0.55, ef=0.0561)
solar = dict(capex=900, fom=15, cf=0.22)
for carbon in (0, 50, 100):
    print(f"carbon {carbon:>3} $/t: gas {lcoe(**gas, carbon=carbon):5.1f} $/MWh, solar {lcoe(**solar):5.1f} $/MWh")

# 2. Graded resource supply curve: cheap grades first, price rises as you use more.
grades = [(0, 3.0), (500, 4.5), (1000, 7.0), (1500, 12.0)]   # (cumulative EJ, extraction cost $/GJ)
def resource_price(cum_ej):
    for (q0, c0), (q1, c1) in zip(grades, grades[1:]):
        if cum_ej <= q1:
            return c0 + (c1 - c0) * (cum_ej - q0) / (q1 - q0)
    return grades[-1][1]
print("resource price at 200, 800, 1400 EJ:", [round(float(resource_price(q)), 2) for q in (200, 800, 1400)], "$/GJ")

# 3. Learning curve: cost falls by the learning rate for each doubling of capacity.
def learn(c0, lr, doublings):
    return c0 * (1 - lr) ** doublings
print("solar capex after 3 doublings at 20%:", round(learn(900, 0.20, 3), 1), "$/kW")
