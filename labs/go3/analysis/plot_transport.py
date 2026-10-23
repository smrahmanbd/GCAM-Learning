"""plot_transport.py - standard transport figures from the tidy CSVs (read_transport.py output).

Figures (analysis/out/figures/):
  mode_shares_2050.png    passenger-km by mode, 2050, one bar per scenario
  co2_paths.png           direct transport CO2 by scenario, 2020-2100 (MtCO2)
  fuel_mix_<scen>.png     final energy by fuel over time for each scenario (stacked area)
  lmdi_<comparison>.png   LMDI effects as a waterfall (needs decompose_lmdi.py first)
Colours are distinguished by hatching or labels as well as colour. Synthetic data unless you ran --db.
Run: python plot_transport.py
"""
import os
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "out", "figures"); os.makedirs(OUT, exist_ok=True)
svc = pd.read_csv(os.path.join(HERE, "out", "service_by_mode.csv"))
en = pd.read_csv(os.path.join(HERE, "out", "energy_by_mode_fuel.csv"))
co2 = pd.read_csv(os.path.join(HERE, "out", "co2_transport.csv"))
SYN = " (synthetic sample data)" if svc.region.str.contains("toy").any() else ""
COL = ["#0b3954", "#0f8a8a", "#c4502e", "#4f8a2c", "#c27a1a", "#6a56a8", "#8d4a5a", "#7a7a8a"]
HATCH = ["", "//", "..", "xx", "\\\\", "++", "--", "oo"]

# 1. mode shares 2050
m = svc[svc.year == 2050].pivot_table(index="scenario", columns="mode", values="value", aggfunc="sum")
m = m.div(m.sum(axis=1), axis=0) * 100
fig, ax = plt.subplots(figsize=(8, 4.5)); left = 0
for i, c in enumerate(m.columns):
    ax.barh(m.index, m[c], left=left, color=COL[i % 8], hatch=HATCH[i % 8], edgecolor="white", label=c); left = left + m[c]
ax.set_xlabel("share of passenger-km in 2050 (%)"); ax.set_title("Mode shares, 2050" + SYN)
ax.legend(ncol=4, fontsize=8, loc="upper center", bbox_to_anchor=(0.5, -0.15)); fig.tight_layout()
fig.savefig(os.path.join(OUT, "mode_shares_2050.png"), dpi=130); plt.close(fig)

# 2. CO2 paths (MTC -> MtCO2)
fig, ax = plt.subplots(figsize=(7, 4))
for i, (sc, g) in enumerate(co2.groupby("scenario")):
    g = g.groupby("year").value.sum() * 44 / 12
    ax.plot(g.index, g.values, color=COL[i % 8], lw=2.5, ls=["-", "--", ":", "-.", "-"][i % 5], label=sc)
    ax.annotate(sc, (g.index[-1], g.values[-1]), fontsize=8, xytext=(3, 0), textcoords="offset points")
ax.set_ylabel("direct CO2 (Mt per year)"); ax.set_title("Passenger transport CO2" + SYN); ax.set_xlim(2020, 2112)
ax.grid(alpha=.3); fig.tight_layout(); fig.savefig(os.path.join(OUT, "co2_paths.png"), dpi=130); plt.close(fig)

# 3. fuel mix per scenario
for sc, g in en.groupby("scenario"):
    p = g.pivot_table(index="year", columns="fuel", values="value", aggfunc="sum").fillna(0)
    fig, ax = plt.subplots(figsize=(7, 4))
    ax.stackplot(p.index, p.T.values, labels=p.columns, colors=COL[:len(p.columns)])
    ax.set_ylabel("EJ"); ax.set_title(f"Final energy by fuel: {sc}{SYN}"); ax.legend(fontsize=8, loc="upper left")
    fig.tight_layout(); fig.savefig(os.path.join(OUT, f"fuel_mix_{sc}.png"), dpi=130); plt.close(fig)

# 4. LMDI waterfalls
lp = os.path.join(HERE, "out", "lmdi_results.csv")
if os.path.exists(lp):
    for _, r in pd.read_csv(lp).iterrows():
        steps = [("start", r.co2_start), ("activity", r.activity), ("structure", r.structure),
                 ("intensity", r.intensity), ("carbon", r.carbon)]
        fig, ax = plt.subplots(figsize=(6.5, 3.8)); level = 0
        for i, (k, v) in enumerate(steps):
            if k == "start":
                ax.bar(i, v, color="#7a7a8a"); level = v
            else:
                ax.bar(i, v, bottom=level, color="#c4502e" if v > 0 else "#0f8a8a"); level += v
            ax.text(i, max(level, level - v) + 1, f"{v:+.1f}" if k != "start" else f"{v:.1f}", ha="center", fontsize=8)
        ax.bar(len(steps), r.co2_end, color="#0b3954"); ax.text(len(steps), r.co2_end + 1, f"{r.co2_end:.1f}", ha="center", fontsize=8)
        tops = [r.co2_start]; lv = r.co2_start
        for _, v in steps[1:]:
            lv += v; tops.append(max(lv, lv - v))
        ax.set_ylim(0, max(tops + [r.co2_end]) * 1.15)
        ax.set_xticks(range(len(steps) + 1), [s[0] for s in steps] + ["end"]); ax.set_ylabel("MtCO2")
        ax.set_title(r.comparison + SYN, fontsize=9); fig.tight_layout()
        name = "".join(ch if ch.isalnum() else "_" for ch in r.comparison).strip("_")
        fig.savefig(os.path.join(OUT, f"lmdi_{name}.png"), dpi=130); plt.close(fig)
print("figures:", sorted(os.listdir(OUT)))
