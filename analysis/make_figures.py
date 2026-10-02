"""Regenerate all six paper figures with a consistent, publication-clean design.
- Canonical class order everywhere (review item 9):
  PLAN, TOOL_SELECT, TOOL_FORMAT, TOOL_EXEC, OBS_MISREAD, GROUNDING,
  VERIFICATION, MEMORY, COORDINATION, LOOP, GIVE_UP, OTHER
  (+ NO_RECOVERY noted as zero everywhere; UNMAPPABLE only where relevant)
- Horizontal bars, larger fonts, uncrowded legends, single-column sizing.
- Fig 1 (full-width placement) and Fig 6 (residual heatmap) use wide-short
  layouts: Fig 6 transposes domains to rows / classes to columns.
Reads: data/work/coded.csv. Writes: figures/fig{1..6}_*.png
"""
import os
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.colors import TwoSlopeNorm

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
coded = pd.read_csv(f"{BASE}/data/work/coded.csv")

ORDER = ["PLAN", "TOOL_SELECT", "TOOL_FORMAT", "TOOL_EXEC", "OBS_MISREAD",
         "GROUNDING", "VERIFICATION", "MEMORY", "COORDINATION", "LOOP",
         "GIVE_UP", "OTHER"]
DPI = 200
plt.rcParams.update({
    "font.size": 10, "axes.titlesize": 11, "axes.labelsize": 10,
    "xtick.labelsize": 9, "ytick.labelsize": 9, "legend.fontsize": 9,
    "figure.dpi": DPI, "savefig.dpi": DPI,
})
for spine in ["top", "right"]:
    plt.rcParams[f"axes.spines.{spine}"] = False

DS_COLORS = {"AgentErrorBench": "#3b6ea5", "Who&When": "#d98a2b"}
DOM_COLORS = {"alfworld": "#3b6ea5", "webshop": "#4ca64c",
              "gaia": "#9b59b6", "multi-agent": "#d98a2b"}
DOM_LABEL = {"alfworld": "embodied (ALFWorld)", "webshop": "web (WebShop)",
             "gaia": "general (GAIA)", "multi-agent": "multi-agent (Who&When)"}
MODEL_COLORS = {"GPT-4o": "#3b6ea5", "Qwen3-8B": "#4ca64c",
                "Llama3.3-70B-Turbo": "#d64545"}

def grouped_hbar(ax, categories, groups, props, colors, xlabel):
    """Horizontal grouped bars. props: dict group -> list aligned to categories."""
    y = np.arange(len(categories))
    n = len(groups)
    h = 0.8 / n
    for i, g in enumerate(groups):
        off = (i - (n - 1) / 2) * h
        ax.barh(y + off, props[g], height=h * 0.92, label=g, color=colors[g],
                edgecolor="white", linewidth=0.5)
    ax.set_yticks(y)
    ax.set_yticklabels(categories, fontsize=9)
    ax.set_xlabel(xlabel)
    ax.invert_yaxis()
    ax.legend(frameon=True, facecolor="white", framealpha=0.9, edgecolor="0.8", loc="lower right", ncols=1)
    ax.grid(axis="x", alpha=0.25, linestyle="--")

def present(sub, order):
    vc = sub["unified"].value_counts(normalize=True)
    return [vc.get(c, 0.0) for c in order]

# ---- Fig 1: by dataset (incl. UNMAPPABLE) — wide & short (full-width placement) ----
cats1 = ORDER + ["UNMAPPABLE"]
groups = ["AgentErrorBench", "Who&When"]
props = {g: present(coded[coded.dataset == g], cats1) for g in groups}
fig, ax = plt.subplots(figsize=(10.0, 2.9))
x = np.arange(len(cats1)); w = 0.38
for i, g in enumerate(groups):
    ax.bar(x + (i - 0.5) * w, [props[g][j] for j in range(len(cats1))],
           width=w, label=g, color=DS_COLORS[g])
ax.set_xticks(x); ax.set_xticklabels(cats1, fontsize=8, rotation=28, ha="right")
ax.set_ylabel("proportion", fontsize=10)
ax.legend(frameon=True, fontsize=8, loc="upper right")
fig.subplots_adjust(left=0.07, right=0.99, top=0.94, bottom=0.26)
fig.savefig(f"{BASE}/figures/fig1_dist_by_dataset.png"); plt.close(fig)

# ---- Fig 2: by domain (labeled records) ----
dom = coded[coded.unified != "UNMAPPABLE"]
dorder = ["alfworld", "webshop", "gaia", "multi-agent"]
props = {d: present(dom[dom.domain == d], ORDER) for d in dorder}
fig, ax = plt.subplots(figsize=(4.0, 4.4))
grouped_hbar(ax, ORDER, [DOM_LABEL[d] for d in dorder],
             {DOM_LABEL[d]: props[d] for d in dorder},
             {DOM_LABEL[d]: DOM_COLORS[d] for d in dorder},
             "proportion of domain's failures")
ax.set_title("Failure-class distribution by domain", pad=8)
fig.tight_layout(pad=0.6)
fig.savefig(f"{BASE}/figures/fig2_dist_by_domain.png"); plt.close(fig)

# ---- Fig 3: by model (AgentErrorBench labeled only) ----
mod = coded[(coded.dataset == "AgentErrorBench") & (coded.unified != "UNMAPPABLE")]
models = ["GPT-4o", "Qwen3-8B", "Llama3.3-70B-Turbo"]
nz = [c for c in ORDER if (mod["unified"] == c).any()]
props = {m: present(mod[mod.llm == m], nz) for m in models}
fig, ax = plt.subplots(figsize=(4.0, 3.6))
grouped_hbar(ax, nz, models, props, MODEL_COLORS,
             "proportion of model's labeled failures")
ax.set_title("Failure-class distribution by model", pad=8)
fig.tight_layout(pad=0.6)
fig.savefig(f"{BASE}/figures/fig3_dist_by_model.png"); plt.close(fig)

# ---- Fig 4: empty-label rate by model ----
aeb = coded[coded.dataset == "AgentErrorBench"]
rates, ns = [], []
for m in models:
    s = aeb[aeb.llm == m]; n = len(s)
    rates.append((s["unified"] == "UNMAPPABLE").sum() / n); ns.append(n)
fig, ax = plt.subplots(figsize=(3.5, 2.3))
y = np.arange(len(models))
bars = ax.barh(y, rates, height=0.55,
               color=[MODEL_COLORS[m] for m in models], edgecolor="white")
ax.set_yticks(y); ax.set_yticklabels([f"{m}\n(n={n})" for m, n in zip(models, ns)],
                                 fontsize=9)
ax.set_xlabel("unmappable (empty-label) rate", fontsize=10)
ax.invert_yaxis(); ax.grid(axis="x", alpha=0.25, linestyle="--")
for b, r in zip(bars, rates):
    ax.text(b.get_width() + 0.012, b.get_y() + b.get_height() / 2,
            f"{r:.1%}", va="center", fontsize=10)
ax.set_xlim(0, max(rates) * 1.32)
ax.set_title("Empty failure labels by model", pad=8)
fig.subplots_adjust(left=0.34, right=0.86, top=0.88, bottom=0.22)
fig.savefig(f"{BASE}/figures/fig4_empty_by_model.png"); plt.close(fig)

# ---- Fig 5: native AgentErrorBench label frequencies ----
nat = aeb["native"].value_counts()
top = nat.head(14)
fig, ax = plt.subplots(figsize=(3.5, 3.4))
y = np.arange(len(top))
bars = ax.barh(y, top.values, height=0.6, color="#3b6ea5", edgecolor="white")
ax.set_yticks(y)
ax.set_yticklabels([t.replace(".", ".\u200b") for t in top.index], fontsize=8.5)
ax.set_xlabel("count (n=200 annotations)")
ax.invert_yaxis(); ax.grid(axis="x", alpha=0.25, linestyle="--")
for b, v in zip(bars, top.values):
    ax.text(b.get_width() + 0.9, b.get_y() + b.get_height() / 2,
            str(v), va="center", fontsize=9)
ax.set_xlim(0, top.values.max() * 1.18)
ax.set_title("Most frequent native labels", pad=8)
fig.subplots_adjust(left=0.55, right=0.9, top=0.9, bottom=0.14)
fig.savefig(f"{BASE}/figures/fig5_native_labels.png"); plt.close(fig)

# ---- Fig 6: standardized residuals heatmap — domains as rows,
# classes as columns; wide & short; no internal title (caption covers it) ----
ctd = pd.crosstab(dom["unified"], dom["domain"])
ctd = ctd.reindex([c for c in ORDER if c in ctd.index])
exp = np.outer(ctd.sum(axis=1), ctd.sum(axis=0)) / ctd.sum().sum()
res = (ctd.values - exp) / np.sqrt(exp)
dcols = ["alfworld", "webshop", "gaia", "multi-agent"]
res = pd.DataFrame(res, index=ctd.index, columns=list(ctd.columns))
res = res[dcols].T
res.index = [DOM_LABEL[d] for d in dcols]
fig, ax = plt.subplots(figsize=(9.6, 2.75))
norm = TwoSlopeNorm(vmin=-4.5, vcenter=0, vmax=4.5)
im = ax.imshow(res.values, cmap="RdBu_r", norm=norm, aspect="auto")
ax.set_xticks(range(len(res.columns)))
ax.set_xticklabels(res.columns, fontsize=9, rotation=28, ha="right")
ax.set_yticks(range(len(res.index))); ax.set_yticklabels(res.index, fontsize=9)
for i in range(res.shape[0]):
    for j in range(res.shape[1]):
        v = res.values[i, j]
        ax.text(j, i, f"{v:+.1f}", ha="center", va="center", fontsize=8,
                color="white" if abs(v) > 2.6 else "black")
cbar = fig.colorbar(im, ax=ax, shrink=0.9, pad=0.015)
cbar.set_label("standardized residual", fontsize=9)
for spine in ["top", "right", "left", "bottom"]:
    ax.spines[spine].set_visible(False)
ax.tick_params(left=False, bottom=False)
fig.subplots_adjust(left=0.22, right=0.88, top=0.96, bottom=0.30)
fig.savefig(f"{BASE}/figures/fig6_residuals.png"); plt.close(fig)

print("figures written:",
      sorted(os.path.basename(p) for p in
             [f"{BASE}/figures/fig{i}_" for i in range(1, 7)]))
for i, f in enumerate(
        ["fig1_dist_by_dataset.png", "fig2_dist_by_domain.png",
         "fig3_dist_by_model.png", "fig4_empty_by_model.png",
         "fig5_native_labels.png", "fig6_residuals.png"], 1):
    p = f"{BASE}/figures/{f}"
    print(i, f, os.path.getsize(p), "bytes")
