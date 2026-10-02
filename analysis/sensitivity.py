"""NOTE: this copy reads the 184-row coding table
at coding/whowhen_184_coding.csv (column coder2_label) instead of the
working filename; analysis logic is unchanged. See README.md.
Sensitivity analyses for the contested Who&When coding decisions (round 2).

Reviewer concern: the primary analyst's guide maps bare "code is incorrect"
reasons to TOOL_FORMAT (37/184 Who&When consensus rows), but the independent
second coder judged 34 such reasons too vague to map at all (UNMAPPABLE).
Adjudication held the guide default for 27 of those rows (consensus TOOL_FORMAT)
and held UNMAPPABLE for 8 rows.

This script reports coder-specific distributions and re-runs the headline
tests under three alternative labelings:
  S1 (ambiguous-as-unmappable): rows where coder2=UNMAPPABLE -> UNMAPPABLE;
      all else = consensus labels.
  S2 (second-coder labels): all 184 Who&When rows use coder 2's labels.
  S3 (contested TOOL_FORMAT -> UNMAPPABLE): the 27 TOOL_FORMAT-vs-UNMAPPABLE
      rows use coder 2's UNMAPPABLE; all else = consensus labels.

For each scenario (+ primary consensus) it recomputes H1 (full and
labeled-only variants) and the domain test. Writes SENSITIVITY_RESULTS.md.
"""
import os
import importlib.util
import numpy as np
import pandas as pd
from scipy.stats import chi2_contingency

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

spec = importlib.util.spec_from_file_location("wc", f"{BASE}/analysis/whowhen_coding.py")
wc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(wc)

coded = pd.read_csv(f"{BASE}/data/work/coded.csv")
c2 = pd.read_csv(f"{BASE}/coding/whowhen_184_coding.csv").set_index("row_id")["coder2_label"]

ww_idx = coded[coded.dataset == "Who&When"].index
coder1 = pd.Series({i: wc.CODING[i][0] for i in range(184)})
consensus = coded.loc[ww_idx, "unified"].reset_index(drop=True)
consensus.index = range(184)

# agreement check
agree = (coder1 == c2).sum()
po = agree / 184
c1c = coder1.value_counts(normalize=True)
c2c = c2.value_counts(normalize=True)
pe = sum(c1c.get(k, 0) * c2c.get(k, 0) for k in set(c1c.index) | set(c2c.index))
kappa = (po - pe) / (1 - pe)
print(f"coder1 vs coder2 agreement: {agree}/184 = {po:.1%}, kappa={kappa:.3f}")
ambig = (c2 == "UNMAPPABLE")
print(f"rows where coder2=UNMAPPABLE: {ambig.sum()}")
tf_contested = (coder1 == "TOOL_FORMAT") & (c2 == "UNMAPPABLE")
print(f"contested TOOL_FORMAT rows: {tf_contested.sum()}")

def cramers_v(chi2, n, r, c):
    return float(np.sqrt(chi2 / (n * (min(r, c) - 1))))

def run_tests(ww_labels, name):
    """ww_labels: Series of 184 unified labels for Who&When."""
    cc = coded.copy()
    cc.loc[ww_idx, "unified"] = ww_labels.values
    res = {"scenario": name}
    # H1 full (incl UNMAPPABLE)
    ct = pd.crosstab(cc["unified"], cc["dataset"])
    x2, p, dof, _ = chi2_contingency(ct)
    res["H1_full"] = (f"chi2={x2:.2f}, df={dof}, p={p:.2g}, "
                      f"V={cramers_v(x2, len(cc), *ct.shape):.3f}")
    # H1 labeled-only
    lab = cc[cc.unified != "UNMAPPABLE"]
    ctl = pd.crosstab(lab["unified"], lab["dataset"])
    x2l, pl, dofl, _ = chi2_contingency(ctl)
    res["H1_labeled"] = (f"n={len(lab)}, chi2={x2l:.2f}, df={dofl}, p={pl:.2g}, "
                         f"V={cramers_v(x2l, len(lab), *ctl.shape):.3f}")
    # Domain (excl UNMAPPABLE)
    ctd = pd.crosstab(lab["unified"], lab["domain"])
    x2d, pd_, dofd, _ = chi2_contingency(ctd)
    res["domain"] = f"n={len(lab)}, chi2={x2d:.2f}, df={dofd}, p={pd_:.2g}"
    # Who&When TOOL_FORMAT share
    w = ww_labels
    res["ww_TOOL_FORMAT"] = f"{(w=='TOOL_FORMAT').sum()}/184 ({(w=='TOOL_FORMAT').mean():.1%})"
    res["ww_top1"] = f"{w.value_counts().index[0]} ({w.value_counts().iloc[0]}/184)"
    return res

scenarios = {
    "primary (consensus)": consensus,
    "S1 coder2-UNMAPPABLE rows->UNMAPPABLE": consensus.mask(ambig, "UNMAPPABLE"),
    "S2 coder-2 labels": c2,
    "S3 contested TOOL_FORMAT->UNMAPPABLE": consensus.mask(tf_contested, "UNMAPPABLE"),
}

rows = [run_tests(lab, name) for name, lab in scenarios.items()]

out = ["# Sensitivity analyses — contested Who&When coding decisions\n"]
out.append("## Coder-specific distributions (Who&When, n=184)\n")
out.append("| class | coder 1 (primary analyst) | coder 2 (independent) | consensus (analysis) |")
out.append("|---|---|---|---")
allc = sorted(set(coder1) | set(c2) | set(consensus))
for cl in allc:
    out.append(f"| {cl} | {(coder1==cl).sum()} | {(c2==cl).sum()} | {(consensus==cl).sum()} |")
out.append("")
out.append(f"Inter-annotator agreement: {agree}/184 = {po:.1%}, Cohen's kappa = {kappa:.3f} (substantial). "
           f"{ambig.sum()} rows have coder2=UNMAPPABLE against a coder-1 substantive class "
           f"({tf_contested.sum()} of those are TOOL_FORMAT-vs-UNMAPPABLE: bare 'code is incorrect' reasons).\n")
out.append("## Headline tests under each labeling\n")
for r in rows:
    out.append(f"### {r['scenario']}")
    out.append(f"- H1 (full): {r['H1_full']}")
    out.append(f"- H1 (labeled-only): {r['H1_labeled']}")
    out.append(f"- Domain: {r['domain']}")
    out.append(f"- Who&When TOOL_FORMAT share: {r['ww_TOOL_FORMAT']}; top class: {r['ww_top1']}")
    out.append("")

with open(f"{BASE}/analysis/SENSITIVITY_RESULTS.md", "w") as f:
    f.write("\n".join(out))
print("\n".join(out))
