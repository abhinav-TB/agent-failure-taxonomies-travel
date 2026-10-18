"""Retrospective dependence sensitivity, not a prespecified confirmatory test.

Unit/estimand: annotation-row proportions with questions resampled as intact
clusters. Cluster-label permutations are restricted by multiplicity; two-row
questions occur only in Who&When and cannot exchange dataset/domain labels
with singleton clusters. Thus only size-one clusters exchange group labels.
This conditional reference test still assumes exchangeability of independent
clusters within a size stratum. Observational benchmark differences do not
support a causal taxonomy claim. The bootstrap treats the 139 released
questions as an empirical population; it does not cover annotation error.
"""
from pathlib import Path
import json
import numpy as np
import pandas as pd
from permutation_check_helpers import pearson

BASE = Path(__file__).resolve().parents[1]
SEED, N_PERM, N_BOOT = 7, 20_000, 20_000

def cluster_permutation(frame, group):
    cats = sorted(frame.unified.unique())
    groups = sorted(frame[group].unique())
    clusters = list(frame.groupby("cluster_id", sort=True))
    counts = np.array([part.unified.value_counts().reindex(cats, fill_value=0).values for _, part in clusters])
    gc = np.array([groups.index(part[group].iloc[0]) for _, part in clusters])
    assert all(part[group].nunique() == 1 for _, part in clusters)
    sizes = counts.sum(axis=1)
    strata = [np.flatnonzero(sizes == size) for size in np.unique(sizes)]
    def statistic(labels):
        table = np.zeros((len(groups), len(cats)))
        np.add.at(table, labels, counts)
        return pearson(table)
    observed = statistic(gc)
    rng = np.random.default_rng(SEED)
    ge = 0
    for _ in range(N_PERM):
        labels = gc.copy()
        for idx in strata:
            labels[idx] = rng.permutation(gc[idx])
        ge += statistic(labels) >= observed - 1e-10
    return dict(observed=float(observed), p=(ge+1)/(N_PERM+1), exceedances=int(ge),
                clusters=len(clusters), multiplicities={str(s):int((sizes==s).sum()) for s in np.unique(sizes)})

def main():
    coded = pd.read_csv(BASE / "data/work/coded.csv")
    ww = coded[coded.dataset == "Who&When"]
    assert len(ww) == 184 and ww.cluster_id.nunique() == 139
    aeb = coded[coded.dataset == "AgentErrorBench"]
    assert aeb.record_id.nunique() == 200
    # Released identifiers are unique trajectories, not demonstrated unique tasks.
    result = {"seed":SEED, "permutations":N_PERM, "bootstrap_resamples":N_BOOT,
              "cluster_definition":"Who&When question_ID; AgentErrorBench trajectory_id (underlying task repeats unresolved)",
              "h1":cluster_permutation(coded, "dataset"),
              "domain":cluster_permutation(coded[coded.unified != "UNMAPPABLE"], "domain")}
    cats = sorted(ww.unified.unique())
    counts = np.array([part.unified.value_counts().reindex(cats, fill_value=0).values
                       for _,part in ww.groupby("cluster_id",sort=True)])
    rng = np.random.default_rng(SEED)
    total = np.array([counts[rng.integers(0,len(counts),len(counts))].sum(axis=0) for _ in range(N_BOOT)])
    props = total / total.sum(axis=1,keepdims=True)
    mapped = [i for i,c in enumerate(cats) if c != "UNMAPPABLE"]
    ground = cats.index("GROUNDING")
    # Ties count as a plurality; strict uniqueness is reported separately.
    mx = total[:,mapped].max(axis=1)
    result["grounding_plurality_including_ties"] = float((total[:,ground] == mx).mean())
    result["grounding_unique_plurality"] = float(((total[:,ground] == mx) & ((total[:,mapped] == mx[:,None]).sum(axis=1)==1)).mean())
    result["bootstrap"]={c:dict(share=float((ww.unified==c).mean()),
                                 low=float(np.quantile(props[:,cats.index(c)],.025)),
                                 high=float(np.quantile(props[:,cats.index(c)],.975)))
                         for c in ["GROUNDING","COORDINATION"]}
    (BASE / "analysis/CLUSTER_RESULTS.json").write_text(json.dumps(result,indent=2)+"\n")
    print(json.dumps(result,indent=2))

if __name__ == "__main__": main()
