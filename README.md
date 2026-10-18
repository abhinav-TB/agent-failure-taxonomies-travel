# How Well Do Agent Failure Taxonomies Travel?

Verified computational revision, 18 October 2026. Authors: Abhinav Tharamel Baiju and Tejaswini Viswanath.

This repository contains a descriptive audit of 384 released agent-failure annotations: 200 AgentErrorBench trajectories and 184 Who&When rows from 139 questions. It maps them to a 13-class operational scheme and audits label quality. Dataset, task, system and annotation protocols are confounded; different frequencies do not establish that a taxonomy cannot transfer.

## Current results

| Analysis | N | chi-square | df | p | Cramer's V |
|---|---:|---:|---:|---:|---:|
| Dataset, all rows |384|167.28917|12|1.71022e-29|.660037|
| Dataset, mapped only |312|161.37669|11|6.98044e-29|.719189|
| Domain, mapped only |312|189.81124|33|6.19835e-24|.450322|

The strict primary rule requires explicit evidence of malformed call syntax, argument structure, or a schema violation for TOOL_FORMAT. Who&When has GROUNDING36 (19.6%), TOOL_FORMAT0, and UNMAPPABLE45 (24.5%). The 37 original TOOL_FORMAT consensus assignments were conservatively recoded as UNMAPPABLE; original coder labels, original consensus, and the previous broader revision are preserved. These are retrospective rule corrections, not a new independent human annotation round. The earlier broader revision had TOOL_FORMAT10 and UNMAPPABLE35. Original second-coder labels have UNMAPPABLE34; the exact unmappable share is coding-sensitive. See [revision notes](REVISION_NOTES.md).

## Mapping coverage

All384 records are accounted for. Substantive coverage is173/200(86.5%) for AgentErrorBench and139/184(75.5%) for Who&When, or312/384(81.25%) overall. All observed nonempty normalized AgentErrorBench native labels have explicit crosswalks. Its vocabulary crosswalk reaches only7 of13 substantive classes; zeros in the other classes do not establish absent mechanisms. See analysis/MAPPING_COVERAGE.md and its machine-readable tables. All45 unresolved reasons are enumerated, not forced into residual classes.

## Reproduce

Run the entire sequence with `python3 analysis/reproduce_all.py`, or run the steps below individually.

Python 3.11+; pinned tested dependency versions are in requirements.txt. From repository root:

```sh
python3 -m pip install -r requirements.txt
python3 analysis/count_taxonomy.py
python3 analysis/run_analysis.py
python3 analysis/verify_release.py
python3 analysis/coverage_audit.py
python3 analysis/sensitivity.py
python3 analysis/permutation_check.py
python3 analysis/cluster_analysis.py
python3 analysis/model_sensitivity.py
python3 analysis/make_figures.py
```

The resampling scripts use seed7, plus-one Monte Carlo p-values, 100000 row permutations and 20000 cluster/model-stratified permutations or question bootstraps. Cluster tests condition on multiplicity. Grounding bootstrap plurality is 86.655% with ties /83.465% uniquely; percentile interval14.136%-25.275%. Full outputs are in analysis/.

## Files

- coding/whowhen_184_coding.csv: original coder labels, original consensus and corrected labels/notes.
- coding/recoding_audit_37.csv: complete strict-rule audit. coding/recoding_audit_27.csv preserves the earlier partial correction.
- data/raw/ and data/work/: released snapshots and generated machine-readable coded rows with cluster IDs.
- analysis/: scripts, mapping and generated results/validation.
- figures/: regenerated vectorPDF and 300dpiPNG outputs.
- Manuscript files are maintained separately and are not distributed in this repository.
- PREREGISTRATION.md: historical author-provided plan, preserved unchanged. New robustness analyses are retrospective.
- SCHEME_PROVENANCE.md: operational-scheme provenance limits; no unsupported 24-source synthesis claim.
- DATA_SOURCES.md and LICENSE.md: upstream source hashes and rights.

## Archive and submission

[Zenodo v1.1](https://doi.org/10.5281/zenodo.23072906) preserves the earlier preprint and computations (H1=192.53). It must not be cited as a matching archive of this revision. The current complete materials are packaged as Supplemental Data S1 for journal submission. A new Zenodo version can archive this exact revision later; no new DOI is claimed here. Cite the specific version you used and the upstream datasets/papers.

Original analysis artifacts: MIT. Third-party source material retains upstream terms; the Who&When page supplied no explicit dataset license. See LICENSE.md rather than assuming MIT applies to the underlying data.
