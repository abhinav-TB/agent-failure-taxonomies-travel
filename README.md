# How Well Do Agent Failure Taxonomies Travel?

Verified computational revision, 18 October 2026. Authors: Abhinav Tharamel Baiju and Tejaswini Viswanath.

This repository contains a descriptive audit of 384 released agent-failure annotations: 200 AgentErrorBench trajectories and 184 Who&When rows from 139 questions. It maps them to a 13-class operational scheme and audits label quality. Dataset, task, system and annotation protocols are confounded; different frequencies do not establish that a taxonomy cannot transfer.

## Current results

| Analysis | N | chi-square | df | p | Cramer's V |
|---|---:|---:|---:|---:|---:|
| Dataset, all rows |384|160.47627|12|4.20062e-28|.646457|
| Dataset, mapped only |322|158.92614|11|2.22072e-28|.702538|
| Domain, mapped only |322|185.29192|33|4.10612e-23|.437965|

Who&When: GROUNDING36 (19.6%), TOOL_FORMAT10 (5.4%), UNMAPPABLE35 (19.0%). The prior 37 TOOL_FORMAT /8 UNMAPPABLE counts are historical. The 27-row rule correction, reasons and original labels are retained. See [revision notes](REVISION_NOTES.md) for evidence limits, strict coding sensitivity and cluster assumptions.

## Reproduce

Run the entire sequence with `python3 analysis/reproduce_all.py`, or run the steps below individually.

Python 3.11+; pinned tested dependency versions are in requirements.txt. From repository root:

```sh
python3 -m pip install -r requirements.txt
python3 analysis/count_taxonomy.py
python3 analysis/run_analysis.py
python3 analysis/verify_release.py
python3 analysis/sensitivity.py
python3 analysis/permutation_check.py
python3 analysis/cluster_analysis.py
python3 analysis/model_sensitivity.py
python3 analysis/make_figures.py
```

The resampling scripts use seed7, plus-one Monte Carlo p-values, 100000 row permutations and 20000 cluster/model-stratified permutations or question bootstraps. Cluster tests condition on multiplicity. Grounding bootstrap plurality is 86.655% with ties /83.465% uniquely; percentile interval14.136%-25.275%. Full outputs are in analysis/.

## Files

- coding/whowhen_184_coding.csv: original coder labels, original consensus and corrected labels/notes.
- coding/recoding_audit_27.csv: source-linked audit of exactly 27 changes.
- data/raw/ and data/work/: released snapshots and generated machine-readable coded rows with cluster IDs.
- analysis/: scripts, mapping and generated results/validation.
- figures/: regenerated vectorPDF and 300dpiPNG outputs.
- manuscript/: synchronized TeX, bibliography, six sequential figures and current manuscript PDF.
- PREREGISTRATION.md: historical author-provided plan, preserved unchanged. New robustness analyses are retrospective.
- SCHEME_PROVENANCE.md: operational-scheme provenance limits; no unsupported 24-source synthesis claim.
- DATA_SOURCES.md and LICENSE.md: upstream source hashes and rights.

## Archive and submission

[Zenodo v1.1](https://doi.org/10.5281/zenodo.23072906) preserves the earlier preprint and computations (H1=192.53). It must not be cited as a matching archive of this revision. The current complete materials are packaged as Supplemental Data S1 for journal submission. A new Zenodo version can archive this exact revision later; no new DOI is claimed here. Cite the specific version you used and the upstream datasets/papers.

Original analysis artifacts: MIT. Manuscript: CC BY4.0. Third-party source material retains upstream terms; the Who&When page supplied no explicit dataset license. See LICENSE.md rather than assuming MIT applies to the underlying data. AI assistance and authors' remaining verification duties are disclosed in the manuscript and revision notes.
