# License and provenance

This supplementary archive contains three kinds of material, covered
separately below. See `DATA_SOURCES.md` for exact upstream sources,
file hashes, and access dates.

## 1. Manuscript

The paper PDF (`agent-failure-taxonomies-preprint.pdf` on Zenodo) is
released under the **Creative Commons Attribution 4.0 International
(CC BY 4.0)** license, matching the Zenodo record license.

Copyright 2026 Abhinav Tharamel Baiju and Tejaswini Viswanath.

## 2. Original analysis artifacts

All files authored for this study are released under the **MIT License**:

- everything under `analysis/` (scripts, `mapping.md`,
  `PREREGISTRATION.md`, `consensus_overrides.csv`, figures),
- `coding/whowhen_184_coding.csv` and other files under `coding/`,
- `data/work/` extraction snapshots,
- `README.md`, `DATA_SOURCES.md`, and this `LICENSE.md`.

MIT License

Copyright (c) 2026 Abhinav Tharamel Baiju and Tejaswini Viswanath

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.

## 3. Redistributed upstream dataset files

Files under `data/raw/` are snapshots of third-party public datasets,
included for reproducibility. They are **not** covered by the licenses
above and remain under their original terms:

- `data/raw/agenterrorbench/Label/*.json` (AgentErrorBench annotation
  files) and `data/raw/agentdebug/detector/error_definitions.py`
  (AgentErrorTaxonomy definitions): from the public repository
  https://github.com/ulab-uiuc/AgentDebug, which is licensed under the
  MIT License (verified 2026-10-01); the annotation files were obtained
  via the Google Drive folder linked from that repository.
- `data/work/whowhen_reasons.csv`: derived extraction from the public,
  ungated Hugging Face dataset `Kevin355/Who_and_When`
  (https://huggingface.co/datasets/Kevin355/Who_and_When,
  paper arXiv:2505.00212). No explicit dataset license is stated on the
  dataset page; consult the original source for applicable terms.

If you reuse the upstream data, cite the original datasets and papers,
not just this archive.
