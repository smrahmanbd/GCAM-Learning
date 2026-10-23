"""Module 2.6 - Land, food and bioenergy.

GCAM shares land among uses with a logit on profit per hectare (positive exponent)
(GCAM v8.2 docs, 'Land' / 'Economic Choice'). Toy numbers (week 9 worked example).
Run:  python m26_land.py
"""
import numpy as np

def profit(price, cost, yield_t):              # $ per hectare
    return (price - cost) * yield_t

def land_shares(profits, exponent=1.0, w=None):
    p = np.maximum(np.asarray(profits, float), 1e-9)
    w = np.ones_like(p) if w is None else np.asarray(w, float)
    x = w * p ** exponent
    return x / x.sum()

for grass_price in (40, 60, 90):
    pr = [profit(200, 120, 3), profit(grass_price, 30, 10)]
    s = land_shares(pr)
    print(f"grass ${grass_price}/t: profits wheat {pr[0]:.0f}, grass {pr[1]:.0f} $/ha -> shares wheat {s[0]:.3f}, grass {s[1]:.3f}")

# Land needed for bioenergy: EJ / (t/ha x GJ/t)
for ej, y in ((10, 10), (100, 10), (100, 5)):
    mha = ej * 1e9 / (y * 18) / 1e6
    print(f"{ej:>3} EJ at {y:>2} t/ha -> {mha:6.1f} million ha")
