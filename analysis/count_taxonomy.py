#!/usr/bin/env python3
"""Taxonomy-size audit for AgentErrorBench's released definition file.

Reproduces the paper's label-noise finding: the repository README claims
"17 error types across 5 modules", while
data/raw/agentdebug/detector/error_definitions.py actually contains
18 distinct label strings across 19 module-qualified pairs
(`hallucination` is defined under both `memory` and `reflection`).

Run from the archive root:  python3 analysis/count_taxonomy.py
"""
import re
from collections import Counter
from pathlib import Path

SRC = Path("data/raw/agentdebug/detector/error_definitions.py")

def main():
    src = SRC.read_text()
    pairs = []
    for m in re.finditer(r"definitions\['(\w+)'\] = \{(.*?)\n        \}", src, re.S):
        module, body = m.group(1), m.group(2)
        for label in re.findall(r"^\s{12}'(\w+)': \{", body, re.M):
            pairs.append((module, label))

    n_pairs = len(pairs)
    labels = [lab for _, lab in pairs]
    n_distinct = len(set(labels))
    dupes = {l: n for l, n in Counter(labels).items() if n > 1}
    modules = sorted({mod for mod, _ in pairs})

    print(f"source file: {SRC}")
    print(f"module-qualified pairs: {n_pairs}")
    print(f"distinct label strings: {n_distinct}")
    print(f"modules ({len(modules)}): {', '.join(modules)}")
    print(f"labels defined under >1 module: {dupes or 'none'}")
    print()
    for mod, lab in pairs:
        print(f"  {mod}.{lab}")
    print()
    print('README claim: "17 error types across 5 modules" '
          "(data/raw/agentdebug/README.md)")
    print(f"counted in error_definitions.py: {n_distinct} distinct label "
          f"strings across {n_pairs} module-qualified pairs")

    assert n_pairs == 19, f"expected 19 module-qualified pairs, got {n_pairs}"
    assert n_distinct == 18, f"expected 18 distinct strings, got {n_distinct}"
    print("\nassertions passed: 19 pairs, 18 distinct strings (README says 17)")

if __name__ == "__main__":
    main()
