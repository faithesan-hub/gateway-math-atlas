"""Step 4: figures.

Plain-language note: draws the report's charts from the processed tables.
Every figure carries a DRAFT stamp until you have verified the numbers;
run with --final only after the verification checklist is complete.

Run:  python code/04_figures.py            (draft)
      python code/04_figures.py --final    (after verification)
"""
import csv
import statistics as st
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.ticker import PercentFormatter

import build_lib as b

FINAL = "--final" in sys.argv
FIG = b.ROOT / "report" / "figures"
FIG.mkdir(parents=True, exist_ok=True)

# reference palette (dataviz skill), validated light: slot1 blue, slot2 orange
COL = {"CA": "#2a78d6", "TX": "#eb6834"}
INK, INK2, GRID, SURF = "#0b0b0b", "#52514e", "#e4e3df", "#fcfcfb"
TITLE = {"CA": "California community colleges\nPassed transfer-level math in the first year (CCCCO 502C)",
         "TX": "Texas community colleges\nPassed a college-level math course within 2 years (THECB C18UC)"}

plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 9, "axes.edgecolor": GRID,
                     "axes.labelcolor": INK2, "xtick.color": INK2, "ytick.color": INK2,
                     "figure.facecolor": SURF, "axes.facecolor": SURF})


def stamp(fig):
    if not FINAL:
        fig.text(0.99, 0.995, "DRAFT - not yet verified", ha="right", va="top", fontsize=8,
                 color="#b00020", weight="bold")


def style(ax):
    for s in ["top", "right", "left"]:
        ax.spines[s].set_visible(False)
    ax.grid(axis="x", color=GRID, linewidth=0.8)
    ax.set_axisbelow(True)


cols = b.read_csv(b.OUT / "atlas_v1_colleges.csv")
long = b.read_csv(b.OUT / "atlas_v1_long.csv")

# Figure 1: distribution of college rates, one panel per state (measures differ; not ranked against each other)
fig, axes = plt.subplots(2, 1, figsize=(7.5, 5.2))
for ax, s in zip(axes, ["CA", "TX"]):
    cs = [c for c in cols if c["state"] == s and c["small_cohort"] == "0" and c["latest_rate"] != ""]
    rates = sorted(float(c["latest_rate"]) for c in cs)
    ys = [0.5 + 0.35 * ((i * 0.618) % 1 - 0.5) for i in range(len(rates))]  # deterministic jitter
    ax.scatter(rates, ys, s=28, color=COL[s], edgecolor=SURF, linewidth=1.5, zorder=3)
    if rates:
        m = st.median(rates)
        ax.axvline(m, color=INK2, linewidth=1, linestyle=(0, (3, 3)))
        ax.text(m, 0.98, f" median {m*100:.0f}%", color=INK, fontsize=8, va="top", transform=ax.get_xaxis_transform())
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_yticks([])
    ax.xaxis.set_major_formatter(PercentFormatter(1.0, decimals=0))
    ax.set_title(f"{TITLE[s]}  ·  {len(rates)} colleges, latest cohort", loc="left", fontsize=9, color=INK)
    style(ax)
axes[1].set_xlabel("Share of the starting cohort who passed (each dot is one college)")
fig.text(0.01, 0.005, "Sources: CCCCO Data Vista; THECB Accountability System. The two states define the measure "
         "differently, so rates are not comparable across states.", fontsize=7, color=INK2)
fig.tight_layout(rect=(0, 0.03, 1, 1))
stamp(fig)
fig.savefig(FIG / "fig1_distribution.png", dpi=200)
plt.close(fig)

# Figure 2: rate vs Pell share, small multiples
fig, axes = plt.subplots(1, 2, figsize=(7.5, 3.6), sharey=False)
for ax, s in zip(axes, ["CA", "TX"]):
    cs = [c for c in cols if c["state"] == s and c["small_cohort"] == "0" and c["pct_pell_2021_22"] not in ("",)]
    x = [float(c["pct_pell_2021_22"]) for c in cs]
    y = [float(c["latest_rate"]) for c in cs]
    ax.scatter(x, y, s=22, color=COL[s], edgecolor=SURF, linewidth=1.5, zorder=3)
    ax.set_title({"CA": "California (1-year measure)", "TX": "Texas (2-year measure)"}[s], loc="left", fontsize=9, color=INK)
    ax.xaxis.set_major_formatter(PercentFormatter(1.0, decimals=0))
    ax.yaxis.set_major_formatter(PercentFormatter(1.0, decimals=0))
    ax.set_xlabel("Pell recipients, share of undergrads (2021-22)")
    ax.grid(color=GRID, linewidth=0.8)
    ax.set_axisbelow(True)
    for sp in ["top", "right"]:
        ax.spines[sp].set_visible(False)
axes[0].set_ylabel("Passed gateway math (latest cohort)")
fig.tight_layout(rect=(0, 0.04, 1, 1))
stamp(fig)
fig.savefig(FIG / "fig2_pell.png", dpi=200)
plt.close(fig)

# Figure 3: pooled state rate by cohort (sum of matched colleges), one panel per state
fig, axes = plt.subplots(1, 2, figsize=(7.5, 3.0))
for ax, s in zip(axes, ["CA", "TX"]):
    years = sorted({r["cohort"] for r in long if r["state"] == s})
    vals = []
    for y in years:
        rs = [r for r in long if r["state"] == s and r["cohort"] == y and r["completed_n"] != ""]
        vals.append(sum(int(r["completed_n"]) for r in rs) / sum(int(r["cohort_n"]) for r in rs))
    ax.plot(years, vals, color=COL[s], linewidth=2, marker="o", markersize=5, markeredgecolor=SURF)
    for y, v in zip(years, vals):
        ax.annotate(f"{v*100:.1f}%", (y, v), textcoords="offset points", xytext=(0, 7), ha="center", fontsize=7.5, color=INK)
    ax.set_ylim(0, max(vals) * 1.35 if vals else 1)
    ax.yaxis.set_major_formatter(PercentFormatter(1.0, decimals=0))
    ax.set_title({"CA": "California, by fall cohort", "TX": "Texas, by entering cohort"}[s], loc="left", fontsize=9, color=INK)
    ax.grid(axis="y", color=GRID, linewidth=0.8)
    ax.set_axisbelow(True)
    for sp in ["top", "right"]:
        ax.spines[sp].set_visible(False)
fig.tight_layout(rect=(0, 0.05, 1, 1))
stamp(fig)
fig.savefig(FIG / "fig3_trend.png", dpi=200)
plt.close(fig)
print("figures written:", sorted(p.name for p in FIG.glob("*.png")))
