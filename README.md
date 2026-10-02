# How Well Do Agent Failure Taxonomies Travel?

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.23072906.svg)](https://doi.org/10.5281/zenodo.23072906)

Code and data supplement for **"How Well Do Agent Failure Taxonomies Travel?
A Cross-Dataset Empirical Analysis of Failure Labels in Public Agent Trajectory
Datasets"** (Abhinav Tharamel Baiju and Tejaswini Viswanath).

> **Cite the Zenodo record, not this repo:**
> Baiju, A. T. & Viswanath, T. (2026).
> *How Well Do Agent Failure Taxonomies Travel? A Cross-Dataset Empirical
> Analysis of Failure Labels in Public Agent Trajectory Datasets* (v1.1).
> Zenodo. https://doi.org/10.5281/zenodo.23072906
>
> The Zenodo archive is the permanent, versioned record. This repository is a
> browsable mirror for discovery and reuse.

## What this is

384 agent failures from two public benchmarks — **AgentErrorBench** (200) and
**Who&When** (184) — hand-coded onto one frozen 13-class unified failure
scheme (`PLAN`, `OBS_MISREAD`, `TOOL_FORMAT`, `MEMORY`, `GROUNDING`,
`UNMAPPABLE`, `VERIFICATION`, `TOOL_EXEC`, `OTHER`, `TOOL_SELECT`,
`COORDINATION`, `LOOP`, `GIVE_UP`), plus a **label-noise audit** of the
upstream datasets (13.5% empty labels; inconsistent label strings; README/code
taxonomy-size mismatch).

Headline result: failure profiles differ strongly by benchmark
(χ²=192.53, df=12, p=1.13×10⁻³⁴, Cramer's V=0.708) — single-dataset taxonomies
don't travel.

## Contents

| Path | What it is |
|---|---|
| `PREREGISTRATION.md` | Preregistration frozen 2026-09-26 |
| `DATA_SOURCES.md` | Upstream identifiers, access dates, sha256 hashes |
| `data/work/agenterrorbench_annotations.csv` | 200-row AgentErrorBench annotation snapshot |
| `data/work/whowhen_reasons.csv` | 184-row Who&When reason snapshot |
| `data/raw/agenterrorbench/Label/*.json` | Raw AgentErrorBench label files (200 trajectories) |
| `data/raw/agentdebug/detector/error_definitions.py` | Verbatim taxonomy definition file |
| `coding/whowhen_184_coding.csv` | 184-row coding: both coders' labels, agreement flag, consensus, adjudication notes |
| `analysis/` | All analysis scripts (`run_analysis.py`, `sensitivity.py`, `permutation_check.py`, `make_figures.py`, `count_taxonomy.py`), `mapping.md` |
| `figures/` | The six paper figures as PNGs |

## Reproducing the results

Python 3.10+ with `pandas`, `numpy`, `scipy`, `matplotlib`. From the repo root:

```
python3 analysis/count_taxonomy.py    # taxonomy-size audit
python3 analysis/run_analysis.py      # confirmatory stats (H1–H3, label-noise audit)
python3 analysis/sensitivity.py       # sensitivity of contested codings
python3 analysis/permutation_check.py # Monte Carlo permutation checks
python3 analysis/make_figures.py      # regenerate figures
```

## License

- Analysis code, codings, mappings, docs: **MIT** (© 2026 Abhinav Tharamel Baiju and Tejaswini Viswanath)
- Redistributed upstream files under `data/raw/` remain under their original terms
  (AgentDebug: MIT; Who&When source states no explicit license — see `LICENSE.md`)

## Upstream sources

- AgentErrorBench via [AgentDebug](https://github.com/ulab-uiuc/AgentDebug) (arXiv:2509.25370)
- [Who&When](https://huggingface.co/datasets/Kevin355/Who_and_When) (arXiv:2505.00212)

If you reuse the upstream data, cite the original datasets and papers too.
