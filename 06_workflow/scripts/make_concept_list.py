#!/usr/bin/env python3
"""Generate the permitted-concept list for draftcheck's scope check.

Reads the `### ` headings of 03_course_materials/concept-register.md and writes
03_course_materials/concept-list.txt: one permitted concept per line, the format
`draftcheck.py --concepts` expects. Backticked ids (hyphens → spaces) and the
title after an em dash are included. No concepts or aliases are invented here.
Module-first: outside concepts require an outside flag and verified PDF in the
register; the human scope review remains the control, not substring matching.

Usage (from the workspace root):
  python3 -B 06_workflow/scripts/make_concept_list.py
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
REGISTER = ROOT / "03_course_materials" / "concept-register.md"
OUTPUT = ROOT / "03_course_materials" / "concept-list.txt"



def heading_terms(line: str) -> tuple[list[str], list[str]]:
    ids = re.findall(r"`([^`]+)`", line)
    title = line.split("—", 1)[1] if "—" in line else ""
    title = re.sub(r"\([^)]*\)", "", title).strip()
    return ids, ([title] if title else [])


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.parse_args()
    if not REGISTER.exists():
        print(f"PENDING: {REGISTER.relative_to(ROOT)} does not exist; build it from verified sources in P1.")
        return 1
    terms: list[str] = []
    for line in REGISTER.read_text(encoding="utf-8").splitlines():
        if not line.startswith("### `"):
            continue
        ids, titles = heading_terms(line)
        terms += [i.replace("-", " ") for i in ids] + titles
    seen: set[str] = set()
    unique = []
    for term in terms:
        key = term.lower().strip()
        if key and key not in seen:
            seen.add(key)
            unique.append(term.strip())
    if not unique:
        print("PENDING: no concept headings found; use ### `concept-id` — Concept title in the verified register.")
        return 1
    header = [
        "# Permitted concepts for `draftcheck.py --concepts` (one per line).",
        "# GENERATED from concept-register.md by 06_workflow/scripts/make_concept_list.py; do not edit by hand.",
        "# Module-first; outside-flagged entries require verified PDFs and manual scope review.",
    ]
    OUTPUT.write_text("\n".join(header + unique) + "\n", encoding="utf-8")
    print(f"wrote {OUTPUT.relative_to(ROOT)}: {len(unique)} concepts")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
