"""Module 2.5 - Energy demand: service demand and a mode choice with the cost of time.

Service demand grows with income and falls with price (elasticities).
Transport modes compete on a generalised cost: money cost + time cost (value of time x hours).
GCAM's transport sector uses the same idea (GCAM v8.2 docs, 'Energy Demand'). Toy numbers.
Run:  python m25_demand.py
"""
import numpy as np

def service_demand(base, income_ratio, price_ratio, inc_el=0.6, price_el=-0.3):
    return base * income_ratio ** inc_el * price_ratio ** price_el

print("passenger-km if income doubles, price same:", round(service_demand(100, 2, 1), 1))
print("...and if fuel makes travel 50% dearer:     ", round(service_demand(100, 2, 1.5), 1))

# Mode choice: generalised cost per passenger-km = money cost + wage-based value of time / speed
modes = {"walk": (0.00, 5), "bus": (0.05, 15), "rail": (0.12, 30), "car": (0.30, 60)}   # $/pkm, door-to-door km/h
def mode_shares(wage, g=-3.0):
    vot = 0.5 * wage                              # value of time: half the wage, a common assumption
    gc = np.array([m + vot / s for m, s in modes.values()])
    x = gc ** g
    return {k: round(float(v), 3) for k, v in zip(modes, x / x.sum())}, [round(float(v), 3) for v in gc]

for wage in (2, 10, 40):                          # $ per hour
    sh, gc = mode_shares(wage)
    print(f"wage {wage:>2} $/h -> generalised cost {gc} -> shares {sh}")
