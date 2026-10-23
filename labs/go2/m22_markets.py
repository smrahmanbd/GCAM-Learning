"""Module 2.2 - Markets, equilibrium and solving.

Part A solves one market by searching for the price where supply = demand (the lab 4 market).
Part B solves three linked markets at once with Broyden's method, the same family of
method GCAM's solver uses (GCAM v8.2 docs, 'Solution and Computation').
Toy numbers only. Run:  python m22_markets.py
"""
import numpy as np
from scipy.optimize import brentq, root

# ---- Part A: one market (lab 4): demand 1000 - 4p, supply 6 (p - 0.9 tax) ----
def excess(p, tax):                     # excess demand = demand - supply
    return (1000 - 4 * p) - 6 * (p - 0.9 * tax)

for tax in (0, 50):
    p = brentq(excess, 0, 500, args=(tax,))
    print(f"One market, tax {tax:>2}: price {p:6.1f}, quantity {1000 - 4 * p:6.1f}")

# ---- Part B: three linked markets: oil, electricity, biomass ----
# Demand for each good depends on all three prices (substitution), supply on its own price.
# Excess demand must be ~0 in every market at the same time.
def excess3(p, carbon=0.0):
    oil, elec, bio = p
    oil_cost = oil + 0.07 * carbon            # carbon price raises the cost of burning oil
    d_oil = 100 * (oil_cost / 10) ** -0.6 * (elec / 30) ** 0.3          # cheaper electricity -> less oil
    d_elec = 80 * (elec / 30) ** -0.5 * (oil_cost / 10) ** 0.3
    d_bio = 20 * (bio / 5) ** -0.8 * (oil_cost / 10) ** 0.5             # biofuel competes with oil
    s_oil = 100 * (oil / 10) ** 1.2
    s_elec = 80 * (elec / 30) ** 1.0 * (bio / 5) ** -0.2                # some power from biomass
    s_bio = 20 * (bio / 5) ** 1.5
    return np.array([d_oil - s_oil, d_elec - s_elec, d_bio - s_bio])

# Solve in log-prices so prices stay positive; relative excess demand keeps markets comparable.
def f(logp, carbon):
    p = np.exp(logp)
    return excess3(p, carbon) / np.array([100, 80, 20])

for carbon in (0, 50):
    sol = root(f, x0=np.log([8, 25, 6]), args=(carbon,), method="broyden1", options={"fatol": 1e-10})
    p = np.exp(sol.x)
    print(f"Three markets, carbon {carbon:>2}: prices oil {p[0]:.2f}, electricity {p[1]:.2f}, "
          f"biomass {p[2]:.2f}; converged={sol.success}; max |excess| = {abs(excess3(p, carbon)).max():.1e}")
