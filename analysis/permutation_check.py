"""Corrected permutation_check.py — Monte Carlo permutation robustness checks.

Bug fixed 2026-09-27: the original vectorized implementation pooled all
permutations' label indices into a single bincount before reshaping, so each
"permutation" received ~1/m of the pooled counts and the null statistics were
near zero (0/100000 exceedances for every test). The fix offsets each
permutation's flat indices by perm_idx*R*C so bincount produces per-permutation
(R x C) tables. Verified against an independent plain-loop implementation
(different seed): model test p=0.0017 (loop, seed=123, 20k) vs p=0.00196
(vectorized, seed=7, 100k).

Replicates the three reported tests from run_analysis.py, then computes
permutation p-values (100,000 label permutations each, seed=7, Pearson
chi-square statistic, labels permuted uniformly with group sizes fixed).
Writes results to analysis/PERMUTATION_RESULTS.md
"""
import os
import numpy as np
import pandas as pd
from scipy.stats import chi2_contingency

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
coded = pd.read_csv(f"{BASE}/data/work/coded.csv")

def chi2_of(counts):
    """Pearson chi-square statistic from an (R x C) count matrix."""
    n = counts.sum()
    row = counts.sum(axis=1, keepdims=True)
    col = counts.sum(axis=0, keepdims=True)
    exp = row @ col / n
    mask = exp > 0
    return float((((counts - exp) ** 2)[mask] / exp[mask]).sum())

def perm_p(groups, labels, n_perm=100_000, seed=7):
    """Permutation p-value: shuffle labels uniformly, keep group sizes fixed.

    Statistic: Pearson chi-square. Sampling: n_perm independent uniform
    permutations of the label vector (np.random.default_rng(seed)).
    Returns (observed_chi2, dof, p_value, exceedance_count).
    """
    rng = np.random.default_rng(seed)
    g, labs = np.asarray(groups), np.asarray(labels)
    ug, gc = np.unique(g, return_inverse=True)
    ul, lc = np.unique(labs, return_inverse=True)
    R, C = len(ug), len(ul)
    obs_counts = np.zeros((R, C), dtype=float)
    np.add.at(obs_counts, (gc, lc), 1)
    obs = chi2_of(obs_counts)
    dof = (R - 1) * (C - 1)
    ge = 0
    # vectorized in chunks for speed
    chunk = 5000
    for start in range(0, n_perm, chunk):
        m = min(chunk, n_perm - start)
        # m independent uniform permutations of the label codes
        perms = np.argsort(rng.random((m, len(lc))), axis=1)
        pl = lc[perms]  # (m, N)
        # per-permutation flat indices: offset each perm by perm_idx*R*C
        # (FIX: without the offset, bincount pools all perms into one table)
        off = np.arange(m)[:, None] * R * C
        idx = (off + gc[None, :] * C + pl).ravel()
        cnt = np.bincount(idx, minlength=m * R * C).reshape(m, R, C).astype(float)
        n = cnt.sum(axis=(1, 2), keepdims=True)
        row = cnt.sum(axis=2, keepdims=True)
        col = cnt.sum(axis=1, keepdims=True)
        exp = row @ col / n
        with np.errstate(divide="ignore", invalid="ignore"):
            terms = np.where(exp > 0, (cnt - exp) ** 2 / np.where(exp > 0, exp, 1), 0.0)
        stats = terms.sum(axis=(1, 2))
        ge += int((stats >= obs).sum())
    p = (ge + 1) / (n_perm + 1)
    return obs, dof, p, ge

out = ["# Monte Carlo permutation robustness checks (100,000 permutations each)\n"]
out.append("Method: seed=7, Pearson chi-square statistic, labels permuted uniformly "
           "with group sizes fixed; p=(exceedances+1)/(100000+1).\n")

# H1: unified x dataset (full 384, incl. UNMAPPABLE)
ct = pd.crosstab(coded["unified"], coded["dataset"])
chi2, p_asymp, dof, _ = chi2_contingency(ct)
obs, df_, p_perm, ge = perm_p(coded["dataset"], coded["unified"])
out.append(f"## H1 — unified x dataset (n=384)\n- asymptotic: chi2={chi2:.2f}, df={dof}, p={p_asymp:.3g}")
out.append(f"- permutation: chi2={obs:.2f}, df={df_}, p_perm={p_perm:.3g} "
           f"({ge}/100000 permutations >= observed)")
assert abs(chi2 - 192.53) < 0.05, f"H1 replication failed: {chi2}"
out.append("")

# H1 labeled-only variant (excl. UNMAPPABLE, n=349)
lab = coded[coded.unified != "UNMAPPABLE"].copy()
ctl = pd.crosstab(lab["unified"], lab["dataset"])
chi2l, p_asympl, dofl, _ = chi2_contingency(ctl)
obsl, df_l, p_perml, gel = perm_p(lab["dataset"], lab["unified"])
out.append(f"## H1 (labeled-only) — unified x dataset (n={len(lab)})\n- asymptotic: chi2={chi2l:.2f}, df={dofl}, p={p_asympl:.3g}")
out.append(f"- permutation: chi2={obsl:.2f}, df={df_l}, p_perm={p_perml:.3g} "
           f"({gel}/100000 permutations >= observed)")
assert abs(chi2l - 182.53) < 0.05, f"H1 labeled-only replication failed: {chi2l}"
out.append("")

# Domain: unified x domain, excluding UNMAPPABLE (n=349)
dom = coded[coded.unified != "UNMAPPABLE"].copy()
ctd = pd.crosstab(dom["unified"], dom["domain"])
chi2d, pd_asymp, dofd, _ = chi2_contingency(ctd)
obsd, dfd_, pd_perm, ged = perm_p(dom["domain"], dom["unified"])
out.append(f"## Domain — unified x domain (n={len(dom)})\n- asymptotic: chi2={chi2d:.2f}, df={dofd}, p={pd_asymp:.3g}")
out.append(f"- permutation: chi2={obsd:.2f}, df={dfd_}, p_perm={pd_perm:.3g} "
           f"({ged}/100000 permutations >= observed)")
assert abs(chi2d - 210.07) < 0.05, f"domain replication failed: {chi2d}"
out.append("")

# Model: unified x llm on AgentErrorBench labeled records only
mod = coded[(coded.dataset == "AgentErrorBench") & (coded.unified != "UNMAPPABLE")].copy()
ctm = pd.crosstab(mod["unified"], mod["llm"])
chi2m, pm_asymp, dofm, _ = chi2_contingency(ctm)
obsm, dfm_, pm_perm, gem = perm_p(mod["llm"], mod["unified"])
out.append(f"## Model — unified x llm, AgentErrorBench labeled (n={len(mod)})\n- asymptotic: chi2={chi2m:.2f}, df={dofm}, p={pm_asymp:.4g}")
out.append(f"- permutation: chi2={obsm:.2f}, df={dfm_}, p_perm={pm_perm:.4g} "
           f"({gem}/100000 permutations >= observed)")
assert abs(chi2m - 30.72) < 0.05, f"model replication failed: {chi2m}"
out.append("")

out.append("Conclusion: permutation p-values agree with the asymptotic results — "
           "every association remains significant at alpha=0.05. Note the model "
           "comparison's permutation p (0.0020) is close to its asymptotic p "
           "(0.0022); an earlier version of this script contained a vectorization "
           "bug that reported p<1e-5 for all three tests.")
with open(f"{BASE}/analysis/PERMUTATION_RESULTS.md", "w") as f:
    f.write("\n".join(out))
print("\n".join(out))
