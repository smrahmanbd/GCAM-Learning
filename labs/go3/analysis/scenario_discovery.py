"""scenario_discovery.py - which uncertain inputs lead to high 2050 transport CO2?

Input: analysis/sample_data/ensemble.csv (300 toy runs; replace with your own GCAM ensemble table:
one row per run, input columns + an outcome column).
Method (as in course lab 13 and Lamontagne et al. 2018, Earth's Future 6:488-504):
  1. label runs "high" if the outcome is in the top quarter;
  2. fit a shallow classification tree (scikit-learn, max_depth 3) to see which inputs split them;
  3. a PRIM-style box search (Friedman & Fisher 1999): peel 5% of runs at a time from the input
     edge that most raises density, stop at coverage >= 0.8; report coverage and density:
       coverage = high runs inside the box / all high runs
       density  = high runs inside the box / all runs inside the box
Run: python scenario_discovery.py   (writes out/scenario_discovery.txt)
"""
import os
import numpy as np
import pandas as pd
from sklearn.tree import DecisionTreeClassifier, export_text

HERE = os.path.dirname(os.path.abspath(__file__))
df = pd.read_csv(os.path.join(HERE, "sample_data", "ensemble.csv"))
X_COLS = ["bev_cost_mult", "car_lf_2050", "gdp_growth", "carbon_start_usd_tco2"]
Y = "co2_2050_mtco2"
thr = df[Y].quantile(0.75)
df["high"] = df[Y] > thr
lines = [f"{len(df)} runs; 'high' = 2050 CO2 above {thr:.1f} Mt (top quarter): {df.high.sum()} runs", ""]

tree = DecisionTreeClassifier(max_depth=3, min_samples_leaf=10, random_state=0).fit(df[X_COLS], df.high)
lines += ["Classification tree (max_depth 3):", export_text(tree, feature_names=X_COLS, decimals=3)]
imp = sorted(zip(X_COLS, tree.feature_importances_), key=lambda t: -t[1])
lines += ["Feature importance: " + ", ".join(f"{k} {v:.2f}" for k, v in imp), ""]

# PRIM-style peeling
box = {c: [df[c].min(), df[c].max()] for c in X_COLS}
inside = np.ones(len(df), bool); alpha = 0.05; path = []
def stats(mask):
    h = df.high[mask].sum(); return h / df.high.sum(), (h / mask.sum() if mask.sum() else 0)
while True:
    cov, den = stats(inside); path.append((cov, den, {k: tuple(v) for k, v in box.items()}))
    best = None
    for c in X_COLS:
        vals = df.loc[inside, c]
        for side, q in (("lo", vals.quantile(alpha)), ("hi", vals.quantile(1 - alpha))):
            m = inside & ((df[c] >= q) if side == "lo" else (df[c] <= q))
            if m.sum() == inside.sum() or m.sum() < 15:
                continue
            c2, d2 = stats(m)
            if c2 >= 0.8 and (best is None or d2 > best[0]):
                best = (d2, c, side, q, m)
    if best is None:
        break
    d2, c, side, q, m = best
    box[c][0 if side == "lo" else 1] = q; inside = m
cov, den, b = path[-1]
restricted = {k: v for k, v in b.items() if (v[0] > df[k].min() + 1e-9) or (v[1] < df[k].max() - 1e-9)}
lines += [f"PRIM-style box after {len(path) - 1} peels: coverage {cov:.2f}, density {den:.2f} "
          f"(base rate {df.high.mean():.2f})", "Restricted inputs:"]
lines += [f"  {k}: {v[0]:.3f} to {v[1]:.3f}  (full range {df[k].min():.3f} to {df[k].max():.3f})" for k, v in restricted.items()]
txt = "\n".join(lines); print(txt)
os.makedirs(os.path.join(HERE, "out"), exist_ok=True)
open(os.path.join(HERE, "out", "scenario_discovery.txt"), "w").write(txt + "\n")
