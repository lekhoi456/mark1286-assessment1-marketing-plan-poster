#!/usr/bin/env python3
"""Count MARK1286 poster panels or estimate pitch timing (not an official word limit).

Poster: ## panels, with <!-- budget: N -->. Heading words and citations count.
Pitch: ## sections, <!-- speaker: Name --> and <!-- time: m:ss --> (duration).
Headings, Owner lines and [stage directions] are not spoken. Link labels count.
Both modes exclude front matter, title block, comments, images, code fences,
Markdown markers, table separator rows, and the References section onwards.
A word is a whitespace-separated token containing a letter or digit.

Usage: wordcount.py DRAFT.md [--mode auto|poster|pitch] [--wpm 130] [--json]
Exit 1: missing sections/metadata, exceeded panel budget or pitch duration.
Pitch time is an estimate: rehearse the actual delivery and allow for pauses.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from collections import defaultdict
from pathlib import Path

REFERENCE_HEADINGS = {"references", "reference list", "bibliography"}
BUDGET_RE = re.compile(r"<!--\s*budget:\s*(\d+)\s*-->", re.I)
SPEAKER_RE = re.compile(r"<!--\s*speaker:\s*([^<>]+?)\s*-->", re.I)
TIME_RE = re.compile(r"<!--\s*time:\s*(\d+):([0-5]\d)\s*-->", re.I)
COMMENT_RE = re.compile(r"<!--.*?-->", re.S)
LINK_RE = re.compile(r"\[([^\]]*)\]\([^)]*\)")
HEADING_RE = re.compile(r"^(#{1,6})\s+(.*?)\s*#*\s*$")
CITATION_RE = re.compile(r"\((?=[^()]*(?:\b(?:1[89]|20)\d{2}[a-z]?\b|n\.d\.|\bno date\b))[^()]*\)")


def strip_front_matter(text: str) -> str:
    return re.sub(r"\A---\n.*?\n---(?:\n|$)", "", text, count=1, flags=re.S)


def clean_text(text: str, spoken: bool, exclude_citations: bool = False) -> str:
    text = COMMENT_RE.sub("", text)
    text = re.sub(r"!\[[^\]]*\]\([^)]*\)", "", text)
    text = LINK_RE.sub(r"\1", text)
    if spoken:
        text = re.sub(r"\[[^\]]*\]", "", text, flags=re.S)
    if exclude_citations:
        text = CITATION_RE.sub("", text)
    return text


def count_words(line: str, exclude_citations: bool = False, heading: bool = False) -> int:
    if re.fullmatch(r"\s*\|?\s*:?-{3,}:?\s*(?:\|\s*:?-{3,}:?\s*)+\|?\s*", line):
        return 0
    line = clean_text(line, spoken=False, exclude_citations=exclude_citations)
    if not heading:
        line = re.sub(r"^\s*(?:[-*+]|\d+[.)])\s+", "", line)
        line = re.sub(r"^\s*>\s?", "", line)
    line = line.replace("|", " ")
    return sum(any(char.isalnum() for char in token) for token in line.split())


def analyse(raw: str, mode: str = "auto", wpm: float = 130,
            exclude_headings: bool = False, exclude_citations: bool = False) -> dict:
    raw = strip_front_matter(raw)
    if mode == "auto":
        mode = "pitch" if SPEAKER_RE.search(raw) or TIME_RE.search(raw) else "poster"
    sections = []
    current = None
    fence = None
    # Mask comments but keep metadata available at its original line index.
    raw_lines = raw.splitlines()
    masked = COMMENT_RE.sub(lambda m: "\n" * m.group(0).count("\n"), raw)
    for index, line in enumerate(masked.splitlines()):
        marker = re.match(r"^\s*(`{3,}|~{3,})", line)
        if marker:
            if fence is None:
                fence = marker.group(1)[0]
            elif marker.group(1)[0] == fence:
                fence = None
            continue
        if fence:
            continue
        heading = HEADING_RE.match(line)
        if heading:
            title = heading.group(2).strip()
            if re.sub(r"^\d+[.)]?\s*", "", title).lower() in REFERENCE_HEADINGS:
                break
            if len(heading.group(1)) == 2:
                current = {"heading": title, "words": 0, "budget": None, "speaker": None,
                           "time_seconds": None, "estimated_seconds": None, "body": []}
                sections.append(current)
            if current is not None and mode == "poster" and not exclude_headings:
                current["words"] += count_words(title, exclude_citations, heading=True)
            continue
        if current is None:
            continue
        original = raw_lines[index]
        budget = BUDGET_RE.search(original)
        speaker = SPEAKER_RE.search(original)
        duration = TIME_RE.search(original)
        if budget:
            current["budget"] = int(budget.group(1))
        if speaker:
            current["speaker"] = speaker.group(1).strip()
        if duration:
            current["time_seconds"] = 60 * int(duration.group(1)) + int(duration.group(2))
        if mode == "pitch" and re.match(r"^\s*Owner:\s*", line, re.I):
            continue
        current["body"].append(line)
    errors = []
    speakers = defaultdict(lambda: {"words": 0, "time_seconds": 0, "estimated_seconds": 0})
    if not sections:
        errors.append("No '## ' sections found; nothing counted.")
    for section in sections:
        body = clean_text("\n".join(section.pop("body")), spoken=mode == "pitch",
                          exclude_citations=exclude_citations)
        section["words"] += sum(count_words(line) for line in body.splitlines())
        if mode == "poster":
            budget = section["budget"]
            if budget is None:
                errors.append(f"{section['heading']}: missing <!-- budget: N -->")
            elif section["words"] > budget:
                errors.append(f"{section['heading']}: {section['words'] - budget} words over budget")
        else:
            section["estimated_seconds"] = section["words"] * 60 / wpm
            if not section["speaker"]:
                errors.append(f"{section['heading']}: missing <!-- speaker: Name -->")
            if section["time_seconds"] is None:
                errors.append(f"{section['heading']}: missing/invalid <!-- time: m:ss -->")
            elif section["estimated_seconds"] > section["time_seconds"]:
                errors.append(f"{section['heading']}: estimated speech exceeds allocated duration")
            speaker = speakers[section["speaker"] or "UNASSIGNED"]
            speaker["words"] += section["words"]
            speaker["time_seconds"] += section["time_seconds"] or 0
            speaker["estimated_seconds"] += section["estimated_seconds"]
    return {"mode": mode, "wpm": wpm, "total_words": sum(s["words"] for s in sections),
            "sections": sections, "speakers": dict(speakers),
            "total_estimated_seconds": sum(s["estimated_seconds"] or 0 for s in sections),
            "total_time_seconds": sum(s["time_seconds"] or 0 for s in sections), "errors": errors}


def clock(seconds: float) -> str:
    seconds = round(seconds)
    return f"{seconds // 60}:{seconds % 60:02d}"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("draft", type=Path)
    parser.add_argument("--mode", choices=("auto", "poster", "pitch"), default="auto")
    parser.add_argument("--wpm", type=float, default=130, help="spoken words per minute (default: 130)")
    parser.add_argument("--json", action="store_true", help="emit machine-readable report")
    parser.add_argument("--exclude-headings", action="store_true", help="exclude poster headings (pitch already does)")
    parser.add_argument("--exclude-citations", action="store_true", help="exclude parenthetical Harvard citations")
    args = parser.parse_args()
    if not 0 < args.wpm < float("inf"):
        parser.error("--wpm must be a finite positive number")
    try:
        report = analyse(args.draft.read_text(encoding="utf-8"), args.mode, args.wpm,
                         args.exclude_headings, args.exclude_citations)
    except OSError as exc:
        parser.error(str(exc))
    if args.json:
        print(json.dumps(report, indent=2, ensure_ascii=False))
    else:
        print(f"Mode: {report['mode']}; total words: {report['total_words']}")
        for section in report["sections"]:
            detail = f"budget {section['budget']}" if report["mode"] == "poster" else (
                f"{section['speaker'] or 'UNASSIGNED'}; estimated {clock(section['estimated_seconds'])}; "
                f"allocated {clock(section['time_seconds'] or 0)}")
            print(f"{section['heading']}: {section['words']} words; {detail}")
        if report["mode"] == "pitch":
            for name, values in report["speakers"].items():
                print(f"Speaker {name}: {values['words']} words; estimated {clock(values['estimated_seconds'])}; "
                      f"allocated {clock(values['time_seconds'])}")
            print(f"Pitch total: estimated {clock(report['total_estimated_seconds'])}; "
                  f"allocated {clock(report['total_time_seconds'])} at {args.wpm:g} wpm. Rehearse with pauses.")
        for error in report["errors"]:
            print(f"ERROR: {error}")
    return 1 if report["errors"] else 0


if __name__ == "__main__":
    sys.exit(main())
