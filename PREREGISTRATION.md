# How Well Do Agent Failure Taxonomies Travel? — Preregistration

**Study:** Cross-dataset empirical analysis of failure labels in public LLM-agent trajectory datasets.
**Date:** 2026-09-26. **Analyst:** the authors (Abhinav Tharamel Baiju and Tejaswini Viswanath).
**Status:** Analysis plan fixed BEFORE confirmatory statistics are computed. EDA for data
understanding is permitted; all hypothesis tests below are pre-specified.

## Research questions

- **RQ1.** What is the distribution of native failure labels within each public dataset?
- **RQ2.** After mapping native labels to one unified scheme, which failure categories dominate
  *across* datasets, and which are dataset- or domain-specific?
- **RQ3.** Do identically-named failure categories mean the same thing across datasets?
  (definition comparison + label-shift quantification)
- **RQ4.** Do failure-label distributions differ significantly by agent domain
  (web navigation vs. embodied vs. multi-agent collaboration)?

## Datasets (all public, no human subjects)

1. **AgentErrorBench** (ulab-uiuc/AgentDebug, GitHub) — annotated failure trajectories from
   ALFWorld, GAIA, WebShop with AgentErrorTaxonomy labels.
2. **Who&When** (HuggingFace `Kevin355/Who_and_When`) — failure logs from 127 multi-agent
   systems, annotated with responsible agent + decisive step + reason.
3. **API-Bank dialogues** (AlibabaResearch/DAMO-ConvAI) — 314 annotated tool-use dialogues,
   if labels are present; else used only for qualitative context.

## Unified coding scheme

Native labels are mapped to the 13-class unified scheme developed for the companion systematic
review. The 13 class definitions are reproduced in Table 2 of the paper, and the mapping
guidance appears in `analysis/mapping.md`. Any native label that cannot be mapped without guessing is coded
`UNMAPPABLE` and reported (not silently dropped).

## Pre-specified analyses

1. Per-dataset label distributions (counts, proportions, 95% Wilson CIs).
2. Chi-square test of independence: unified-category × dataset (α = 0.05). If significant,
   standardized residuals to identify over/under-represented cells.
3. Domain comparison (RQ4): same test with domain (web / embodied / multi-agent) as the grouping.
4. Label-shift audit (RQ3): for each pair of datasets sharing a category name, compare the
   datasets' written definitions and report Jensen–Shannon divergence between the conditional
   distributions of sub-labels/trajectory features where available.
5. Coverage: proportion of trajectories whose native label maps cleanly vs. `UNMAPPABLE`, per dataset.

## Hypotheses (directional; tested by analyses 2–3)

- **H1:** Failure-label distributions differ significantly across datasets (chi-square p < 0.05).
- **H2:** Planning/reasoning failures form the plurality in web-navigation datasets but not in
  multi-agent datasets (where coordination/communication failures dominate).
- **H3:** At least 15% of native labels are `UNMAPPABLE` without definitional guesswork,
  evidencing taxonomy incomparability.

## Falsification / limits

- If H1 fails (no significant difference), the paper reports taxonomy convergence, not divergence.
- If a dataset cannot be obtained or lacks usable labels, it is dropped and the paper's scope
  is reduced transparently; no substitute data is invented.
- All code, mapping tables, and data snapshots are released for reproducibility.

## What this preregistration does NOT cover

Exploratory findings from EDA will be clearly labeled as exploratory in the paper.
No p-hacking: only the tests above count as confirmatory.

## Timeline / provenance (added 2026-09-27)

- **2026-09-26 18:49 UTC** — this analysis plan frozen (file creation timestamp).
  Research questions, hypotheses (H1–H3), datasets, and statistical tests
  above were fixed at this point.
- **2026-09-26 20:28 UTC** — confirmatory analysis script
  (`analysis/run_analysis.py`) first written, after the freeze. All
  hypothesis-test statistics in the paper come from this script.
- **2026-09-27** — post-freeze additions, all clearly marked as such in the
  paper: permutation robustness checks (`analysis/permutation_check.py`; a
  vectorization bug in the first version was found and fixed the same day,
  verified against an independent reimplementation), sensitivity analyses of
  the contested Who&When codings (`analysis/sensitivity.py`), and the
  exploratory per-model comparison (not preregistered).
- Exploratory data understanding (loading the datasets, RQ1-style
  distributions) was performed before the freeze, as permitted above; no
  hypothesis test was run before the freeze.

**Note:** this is the public copy of the preregistration frozen 2026-09-26;
the statistical content above is unchanged.
