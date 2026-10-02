# Data sources and version identifiers

All datasets are public. The analysis pipeline reads only the derived
extraction files in `data/work/` (snapshots included here); upstream
provenance is documented below. Accessed 2026-09-26.

## D1. AgentErrorBench (n=200 annotated failure trajectories)

- **Upstream:** Google Drive folder linked from https://github.com/ulab-uiuc/AgentDebug
  (README badge: arXiv:2509.25370).
- **Raw files used:** `Label/alfworld_labels.json` (100 trajectories),
  `Label/gaia_labels.json` (50), `Label/webshop_labels.json` (50) — included
  in this archive under `data/raw/agenterrorbench/Label/` (the confirmatory
  script re-derives codings from these for fidelity).
  - alfworld_labels.json sha256: `a21e3a6f217851f7583c8d2f6553b05f02e168b8519f9a8ae704df061b89bbb1`
  - gaia_labels.json sha256: `c463d7fc598ecad15ffeac52cb85e20d5deb1a4694763a98d4294f0a95b749c8`
  - webshop_labels.json sha256: `2b4dd5d291131fe99e4ec05ba4a8368a1baec42eef051e0833772ab24eb17af7`
- **Taxonomy definitions:** `detector/error_definitions.py` in the same repository —
  included in this archive under `data/raw/agentdebug/detector/`.
  The file contains **18 distinct label strings across 19 module-qualified
  pairs** (`hallucination` is defined under both `memory` and `reflection`);
  the repository README text claims "17 error types across 5 modules". This
  README/code size mismatch is a reported finding (paper §4.3); reproduce it
  with `python3 analysis/count_taxonomy.py`.
  - error_definitions.py sha256: `415ced442e998133d23526d05064eef908a8e4df50519d7355af12e838d9d9bb`
- **Included snapshot:** `data/work/agenterrorbench_annotations.csv` — 200-row
  extraction of raw annotation values (trajectory id, model, task type,
  critical-failure module, native failure-type string, reasoning text).
  - sha256: `0c569af9be16cc32642a65063d9e565b6843fd87a31c01bec2038d0e6c01c558`

## D2. Who&When (n=184 multi-agent failures with free-text attributions)

- **Upstream:** Hugging Face dataset `Kevin355/Who_and_When` (public, ungated;
  tags: arxiv:2505.00212).
- **Raw files used:** `Algorithm-Generated.parquet` (126 rows),
  `Hand-Crafted.parquet` (58 rows).
- **Included snapshot:** `data/work/whowhen_reasons.csv` — 184-row extraction
  (row id, source split, mistake agent, free-text mistake reason).
  - sha256: `6552d5558761b95757a5122c46e8c88f4390b6eae0bc905a398ba796ac317ac3`

## D3. API-Bank — excluded from confirmatory analysis

Source `https://github.com/AlibabaResearch/DAMO-ConvAI` contains API
documentation and simulated exception strings but no trajectory-level failure
annotations; it could not be mapped to the unified scheme without inventing
labels, so it was dropped per the preregistration's falsification clause.
Not included in this archive.

## Coding and mapping artifacts (author-created)

- `coding/whowhen_184_coding.csv` — 184 rows: free-text reason, both coders'
  labels (`coder1_label`, `coder2_label`), agreement flag, consensus label,
  adjudication note (empty where coders agreed).
  - sha256: `ed8e6da24bb11b45655f51d79429e257fb56b4e0a5d87344d4f2427690ee0231`
- `analysis/consensus_overrides.csv` — 25 rows where the consensus label
  differs from coder 1 (machine-readable form of the adjudication outcome).
  - sha256: `e5014995ae0a89a863d710e3d0160b62d3fe4ebe1a544a18d923ab954360a96e`
- `analysis/mapping.md` — full native-to-unified mapping rationale table
  (AgentErrorBench strings; Who&When coding guide is in
  `analysis/whowhen_coding.py`).
- Inter-annotator agreement: 128/184 (69.6%), Cohen's kappa = 0.662; 56
  disagreements adjudicated to consensus (31 held coder 1, 24 coder 2,
  1 a third reading).
