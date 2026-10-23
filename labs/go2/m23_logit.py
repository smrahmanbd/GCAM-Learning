"""Module 2.3 - Choice: the logit.

GCAM shares a market among technologies with a logit (GCAM v8.2 docs, 'Economic Choice').
Relative-cost form:  share_i = w_i * c_i^g / sum_j (w_j * c_j^g),  g < 0 (the logit exponent).
Absolute-cost form:  share_i = w_i * exp(b * c_i) / sum_j (w_j * exp(b * c_j)).
Toy numbers (lab 4/7 costs). Run:  python m23_logit.py
"""
import numpy as np

def relative_logit(costs, g, w=None):
    c = np.asarray(costs, float); w = np.ones_like(c) if w is None else np.asarray(w, float)
    x = w * c ** g
    return x / x.sum()

def absolute_logit(costs, b, w=None):
    c = np.asarray(costs, float); w = np.ones_like(c) if w is None else np.asarray(w, float)
    x = w * np.exp(b * c)
    return x / x.sum()

techs, costs = ["coal", "gas", "solar"], [60, 70, 80]
for g in (-1, -4, -10):
    print(f"relative logit, exponent {g:>3}: ", {k: round(float(v), 3) for k, v in zip(techs, relative_logit(costs, g))})

# Share weights calibrate the base year: they make the logit reproduce observed shares.
observed = np.array([0.30, 0.50, 0.20])
g = -4
w = observed / (np.array(costs, float) ** g)
w = w / w[0]
print("calibrated share weights:", {k: round(float(v), 3) for k, v in zip(techs, w)},
      "-> reproduces", [round(float(v), 3) for v in relative_logit(costs, g, w)])

# Nested logit: electricity first chooses fossil vs renewable, then within each nest.
fossil = relative_logit([60, 70], -6)          # coal vs gas inside the fossil nest
fossil_cost = (np.array([60, 70]) * fossil).sum()  # nest cost = share-weighted average (simplification)
top = relative_logit([fossil_cost, 80], -3)    # fossil nest vs solar
print(f"nested: fossil nest {top[0]:.3f} (coal {top[0] * fossil[0]:.3f}, gas {top[0] * fossil[1]:.3f}), solar {top[1]:.3f}")
