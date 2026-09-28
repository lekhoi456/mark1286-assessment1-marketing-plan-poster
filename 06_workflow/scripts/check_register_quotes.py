"""Check concept-register quotations against numbered module extracts or registered PDFs.

Run from the workspace root (assessment1-marketing-plan-poster):

    python3 -B 06_workflow/scripts/check_register_quotes.py [extra.md ...]
    python3 -B 06_workflow/scripts/check_register_quotes.py --self-test

Format checked: one or more consecutive lines starting with "> " (the quote),
followed immediately by a locator line starting with "— ", for example

    > Exact wording copied from the source
    — `w01-lecture` s12

Every "> " line must occur verbatim (exact characters) in EVERY location on the
locator line. A location is a backticked slug from 03_course_materials/extracted/
plus slide or page numbers ("s12", "s12, s15", "s24–25", "p. 86"); the whole
"## Slide N" / "## Page N" section is searched (body, tables, alt text, speaker
notes). Text in parentheses after the numbers, e.g. "(speaker notes)", is ignored.
`module-handbook` has no slide sections, so the whole handbook file is searched.

Default file: 03_course_materials/concept-register.md; further Markdown files
may be passed as arguments. For outside concepts, a registry key plus p. N
reads the saved PDF (pdftotext); the outside flag and claim meaning require
manual review. Exit 1 on missing register or failed quotes, 0 otherwise.
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path

WS = Path(__file__).resolve().parents[2]
EXTRACTED = WS / "03_course_materials" / "extracted"
DEFAULT_FILES = [WS / "03_course_materials" / "concept-register.md"]
WHOLE_FILE_SLUGS = {"module-handbook"}

SECTION_RE = re.compile(r"^## (?:Slide|Page) (\d+)\b")
LOCATION_RE = re.compile(r"`([a-z0-9-]+)`([^;]*)")
NUMBER_RE = re.compile(r"(\d+)(?:\s*[–-]\s*(\d+))?")


class Source:
    """Text of one extracted file, split into numbered slide/page sections."""

    def __init__(self, slug: str, extracted_dir: Path):
        path = extracted_dir / f"{slug}.md"
        self.exists = path.exists()
        self.text = path.read_text(encoding="utf-8") if self.exists else ""
        self.sections: dict[int, str] = {}
        if not self.exists:
            registry = WS / "04_references" / "references.json"
            entries = json.loads(registry.read_text(encoding="utf-8")).get("entries", []) if registry.exists() else []
            entry = next((e for e in entries if e.get("key") == slug and e.get("status") != "archived"), None)
            name = entry.get("file") if entry else None
            pdf = WS / "04_references" / name if name and Path(name).name == name else None
            if pdf and pdf.is_file():
                result = subprocess.run(["pdftotext", "-layout", str(pdf), "-"],
                                        capture_output=True, text=True, check=True)
                self.exists = True
                self.text = result.stdout
                self.sections = {n: text for n, text in enumerate(self.text.split("\f"), 1)}
            return
        current: int | None = None
        lines: list[str] = []
        for line in self.text.split("\n"):
            if line.startswith("## "):
                if current is not None:
                    self.sections[current] = "\n".join(lines)
                match = SECTION_RE.match(line)
                current = int(match.group(1)) if match else None
                lines = []
            if current is not None:
                lines.append(line)
        if current is not None:
            self.sections[current] = "\n".join(lines)


def parse_locator(locator: str) -> list[tuple[str, list[int]]]:
    """Return [(slug, [numbers])] for a locator line (without the leading "— ")."""
    locations = []
    for slug, rest in LOCATION_RE.findall(locator):
        numbers: list[int] = []
        for first, last in NUMBER_RE.findall(rest.split("(")[0]):
            numbers.extend(range(int(first), int(last) + 1) if last else [int(first)])
        locations.append((slug, numbers))
    return locations


def check_file(path: Path, extracted_dir: Path, cache: dict[str, Source]) -> tuple[int, list[str]]:
    """Check one Markdown file. Returns (number of quote lines passed, failure messages)."""
    lines = path.read_text(encoding="utf-8").split("\n")
    passed = 0
    failures: list[str] = []
    i = 0
    while i < len(lines):
        if not lines[i].startswith("> "):
            i += 1
            continue
        block = []
        while i < len(lines) and lines[i].startswith("> "):
            block.append((i + 1, lines[i][2:]))
            i += 1
        locator = lines[i][2:].strip() if i < len(lines) and lines[i].startswith("— ") else None
        locations = parse_locator(locator) if locator else []
        for line_no, quote in block:
            problems = []
            if not locator:
                problems.append("no locator line after the quote")
            elif not locations:
                problems.append("locator names no `slug`")
            for slug, numbers in locations:
                source = cache.setdefault(slug, Source(slug, extracted_dir))
                if not source.exists:
                    problems.append(f"{slug}: no extracted file")
                    continue
                if slug in WHOLE_FILE_SLUGS:
                    if quote not in source.text:
                        problems.append(f"{slug}: not found")
                    continue
                if not numbers:
                    problems.append(f"{slug}: no slide/page number")
                    continue
                for number in numbers:
                    section = source.sections.get(number)
                    if section is None:
                        problems.append(f"{slug} {number}: no such slide/page")
                    elif quote not in section:
                        problems.append(f"{slug} {number}: not found")
            if problems:
                failures.append(
                    f"{path}:{line_no}\n    quote:   {quote}\n    locator: {locator}\n    problem: {'; '.join(problems)}"
                )
            else:
                passed += 1
    return passed, failures


def run(files: list[Path], extracted_dir: Path = EXTRACTED, verbose: bool = True) -> int:
    cache: dict[str, Source] = {}
    total_passed = total_failed = 0
    for path in files:
        passed, failures = check_file(path, extracted_dir, cache)
        total_passed += passed
        total_failed += len(failures)
        if verbose:
            try:
                shown = path.relative_to(WS)
            except ValueError:
                shown = path
            print(f"{shown}: {passed} passed, {len(failures)} failed")
            for failure in failures:
                print(f"  FAIL {failure}")
    if verbose:
        print(f"TOTAL: {total_passed} passed, {total_failed} failed")
    return total_failed


def self_test() -> int:
    """Exercise exact wording and locator rejection in a temporary synthetic fixture."""
    with tempfile.TemporaryDirectory(prefix="mark1286-quote-check-") as tmp:
        folder = Path(tmp)
        (folder / "fixture.md").write_text("## Slide 1\nExact fixture wording.\n## Slide 2\nOther words.\n", encoding="utf-8")
        register = folder / "fixture-register.md"
        register.write_text("> Exact fixture wording.\n— `fixture` s1\n", encoding="utf-8")
        baseline = run([register], folder, verbose=False)
        with register.open("a", encoding="utf-8") as handle:
            handle.write("\n> Fabricated fixture quote.\n— `fixture` s1\n"
                         "\n> Exact fixture wording.\n— `fixture` s2\n")
        failures = run([register], folder, verbose=False)
    ok = baseline == 0 and failures == 2
    print(f"self-test: {'PASS' if ok else 'FAIL'} (baseline {baseline}; rejected {failures}/2 planted errors)")
    print("Synthetic fixture only; the actual concept register remains pending until P1.")
    return 0 if ok else 1


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("files", nargs="*", type=Path, help="extra Markdown files to check")
    parser.add_argument("--self-test", action="store_true", help="isolated synthetic quotation/locator check")
    args = parser.parse_args(argv)
    if args.self_test:
        return self_test()
    files = DEFAULT_FILES + [path.resolve() for path in args.files]
    missing = [f for f in files if not f.exists()]
    if missing:
        for f in missing:
            print(f"PENDING: missing {f}; create the evidence-backed concept register in P1, not a dummy file.")
        return 1
    return 1 if run(files) else 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
