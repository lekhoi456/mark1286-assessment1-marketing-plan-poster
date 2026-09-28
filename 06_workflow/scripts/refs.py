#!/usr/bin/env python3
"""Reference registry tool for the MARK1286 Marketing Plan Poster.

The single source of truth is 04_references/references.json. This script
never changes bibliographic fields; it renders, verifies and audits them.

Subcommands (run from anywhere; paths are resolved from this file):
    python3 -B 06_workflow/scripts/refs.py build
        Render 04_references/references.html (self-contained, offline) and
        04_references/reference-list.md (Harvard list of `cited` entries).
    python3 -B 06_workflow/scripts/refs.py verify [--key KEY ...] [--offline]
        Crossref check for DOI entries and pdftotext check for entries with a
        PDF. Results are stored in each entry's `verification` block.
    python3 -B 06_workflow/scripts/refs.py check-draft DRAFT.md
        Map in-text citations to registry keys and audit the draft.

Style: Cite Them Right Harvard, as recommended by the University of Greenwich
Library. The exact patterns and their sources are documented in
06_workflow/references-workflow.md.

Standard library only; pdftotext/pdfinfo (poppler) are called via subprocess.
"""
from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import html
import json
import os
import re
import subprocess
import sys
import time
import unicodedata
import urllib.error
import urllib.parse
import urllib.request
from collections import defaultdict
from pathlib import Path

WS = Path(__file__).resolve().parents[2]
REF_DIR = WS / "04_references"
ARCHIVE_DIR = REF_DIR / "_archived"
INBOX_DIR = REF_DIR / "_inbox"
REGISTRY = REF_DIR / "references.json"
HTML_OUT = REF_DIR / "references.html"
MD_OUT = REF_DIR / "reference-list.md"
DRAFT_DIRS = [WS / "07_drafts", WS / "08_final"]

STATUSES = ("cited", "candidate", "archived")
RETRIEVAL_METHODS = ("open-access", "comet-sso", "user-download", "course-material", "web-snapshot")
ACADEMIC_TYPES = {"journal-article", "book", "ebook", "chapter"}
# Crossref fields whose documented differences may be accepted via `verification_accept`.
# DOI, year and author family names can never be accepted: a difference there means a wrong work or record.
ACCEPTABLE_FIELDS = {"title", "container", "volume", "issue", "pages"}
PDF_VERIFIED = {"match", "accepted-manual"}
PDF_IDENTITY_FIELDS = ("title", "authors", "editors", "organisation", "year", "type", "accessed", "url", "doi")
CROSSREF_IDENTITY_FIELDS = ("title", "authors", "editors", "organisation", "year", "type",
                           "doi", "container", "volume", "issue", "pages", "article_number")
NEVER_ACCEPT = {"doi", "year", "authors"}
MONTHS = ["January", "February", "March", "April", "May", "June", "July", "August",
          "September", "October", "November", "December"]

# Required fields per type. "a|b" means at least one of them.
TYPES: dict[str, dict] = {
    "journal-article": {"label": "Journal article",
                        "required": ["authors|organisation", "year", "title", "container", "volume",
                                     "pages|article_number"]},
    "book": {"label": "Book (print, or e-book that looks like print)",
             "required": ["authors|organisation|editors", "year", "title", "publisher"]},
    "ebook": {"label": "E-book (online only)",
              "required": ["authors|organisation|editors", "year", "title", "publisher", "doi|url"]},
    "chapter": {"label": "Chapter in edited book",
                "required": ["authors", "year", "title", "editors", "container", "publisher"]},
    "webpage": {"label": "Web page", "required": ["year", "title", "url", "accessed"]},
    "report": {"label": "Report (organisation or author)",
               "required": ["authors|organisation", "year", "title", "publisher|url|doi"]},
    "vle-slides": {"label": "Lecture slides / notes on the VLE (Moodle)",
                   "required": ["authors|organisation", "year", "title", "module", "institution", "url",
                                "accessed"]},
    "social-media": {"label": "Social media post",
                     "required": ["authors|organisation", "year", "title", "platform", "day_month", "url",
                                  "accessed"]},
    "dataset": {"label": "Online dataset / statistics",
                "required": ["authors|organisation", "year", "title", "url", "accessed"]},
    "video": {"label": "Online video (e.g. YouTube)",
              "required": ["authors|organisation", "year", "title", "day_month", "url", "accessed"]},
    "news-article": {"label": "Online newspaper or news agency article",
                     "required": ["authors|organisation", "year", "title", "container", "day_month", "url",
                                  "accessed"]},
}

STOPWORDS = set("""a an and are as at be by for from in into is it its of on or the to with via
within without toward towards over under between about new""".split())
YEAR_TOKEN = r"(?:\d{4}[a-z]?|no\s+date(?:\s?[a-z](?![a-z]))?|n\.\s?d\.(?:\s?[a-z](?![a-z]))?)"
YEARS_RE = re.compile(rf"^\s*({YEAR_TOKEN}(?:\s*,\s*{YEAR_TOKEN})*)(.*)$", re.S)
ISO_DATE = re.compile(r"^\d{4}-\d{2}-\d{2}$")


# --------------------------------------------------------------------------- utilities

def today() -> str:
    return dt.date.today().isoformat()


def fold(text: str) -> str:
    """Lower-case ASCII fold for comparisons."""
    text = unicodedata.normalize("NFKD", html.unescape(text or ""))
    return "".join(c for c in text if not unicodedata.combining(c)).lower()


def norm_words(text: str) -> str:
    text = fold(text).replace("&", " and ")
    text = re.sub(r"[^a-z0-9]+", " ", text)
    return " ".join(text.split())


def squash(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", "", fold(text))


def slug(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", fold(text)).strip("-")


def ctr_date(iso: str) -> str:
    """2026-09-27 -> 27 September 2026 (Cite Them Right accessed-date form)."""
    try:
        d = dt.date.fromisoformat(iso)
    except (TypeError, ValueError):
        return f"[INVALID DATE {iso}]"
    return f"{d.day} {MONTHS[d.month - 1]} {d.year}"


def ordinal(edition: str) -> str:
    edition = str(edition).strip()
    if edition.isdigit():
        n = int(edition)
        suffix = "th" if 10 <= n % 100 <= 20 else {1: "st", 2: "nd", 3: "rd"}.get(n % 10, "th")
        return f"{n}{suffix}"
    return edition


def bare_doi(doi: str) -> str:
    return re.sub(r"^(?:https?://(?:dx\.)?doi\.org/|doi:\s*)", "", (doi or "").strip(), flags=re.I)


def pages_text(pages: str) -> str:
    pages = str(pages).strip().replace("--", "–").replace("-", "–").replace("—", "–")
    return f"pp. {pages}" if "–" in pages else f"p. {pages}"


def load_registry() -> dict:
    if not REGISTRY.exists():
        sys.exit(f"Registry not found: {REGISTRY}")
    with REGISTRY.open(encoding="utf-8") as fh:
        data = json.load(fh)
    data.setdefault("meta", {})
    data.setdefault("entries", [])
    return data


def save_registry(data: dict) -> None:
    tmp = REGISTRY.with_suffix(".json.tmp")
    tmp.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    os.replace(tmp, REGISTRY)


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(WS))
    except ValueError:
        return str(path)


# --------------------------------------------------------------------------- names and citations

def persons(entry: dict) -> list[dict]:
    return [a for a in entry.get("authors") or [] if a.get("family")]


def initials(given: str) -> str:
    out = []
    for part in (given or "").replace(".", " ").split():
        pieces = [p for p in part.split("-") if p]
        out.append("-".join(p[0].upper() + "." for p in pieces))
    return "".join(out)


def name_family_first(person: dict) -> str:
    ini = initials(person.get("given", ""))
    return f"{person['family']}, {ini}" if ini else person["family"]


def name_initials_first(person: dict) -> str:
    ini = initials(person.get("given", ""))
    return f"{ini} {person['family']}" if ini else person["family"]


def join_names(names: list[str]) -> str:
    if len(names) <= 1:
        return "".join(names)
    return ", ".join(names[:-1]) + " and " + names[-1]


def year_text(entry: dict) -> str:
    year = str(entry.get("year") or "").strip()
    suffix = (entry.get("suffix") or "").strip()
    if year.lower() in ("n.d.", "nd", "no date"):
        return f"no date {suffix}" if suffix else "no date"
    return f"{year}{suffix}"


def is_nd(entry: dict) -> bool:
    return str(entry.get("year") or "").strip().lower() in ("n.d.", "nd", "no date")


def intext_author_segs(entry: dict) -> list[tuple[str, str]]:
    ps = persons(entry)
    if not ps and not entry.get("organisation"):
        ps = [e for e in entry.get("editors") or [] if e.get("family")]
    if ps:
        fam = [p["family"] for p in ps]
        if len(fam) >= 4:
            return [("t", f"{fam[0]} "), ("i", "et al.")]
        return [("t", join_names(fam))]
    if entry.get("organisation"):
        return [("t", entry["organisation"])]
    return [("i", entry.get("title") or "[MISSING title]")]


def intext(entry: dict) -> tuple[list, list]:
    """(parenthetical, narrative) citation segments."""
    author = intext_author_segs(entry)
    year = year_text(entry)
    return [("t", "(")] + author + [("t", f", {year})")], author + [("t", f" ({year})")]


def author_variants(entry: dict) -> list[tuple[str, str | None]]:
    """Normalised author strings that map to this entry, with an optional style warning."""
    variants: list[tuple[str, str | None]] = []
    ps = persons(entry)
    if not ps and not entry.get("organisation"):
        ps = [e for e in entry.get("editors") or [] if e.get("family")]
    if ps:
        fam = [p["family"] for p in ps]
        if len(fam) >= 4:
            variants.append((norm_words(f"{fam[0]} et al"), None))
            variants.append((norm_words(join_names(fam)), None))
        else:
            variants.append((norm_words(join_names(fam)), None))
            if len(fam) == 3:
                variants.append((norm_words(f"{fam[0]} et al"),
                                 "three authors: Cite Them Right names all three in-text; et al. is for four or more"))
    elif entry.get("organisation"):
        variants.append((norm_words(entry["organisation"]), None))
        for alias in entry.get("citation_aliases") or []:
            variants.append((norm_words(alias), None))
    elif entry.get("title"):
        variants.append((norm_words(entry["title"]), None))
    return variants


def norm_year_token(token: str) -> str:
    token = " ".join(token.lower().split())
    match = re.match(r"^(?:no\s*date|n\.\s?d\.)\s?([a-z]?)$", token)
    if match:
        return f"no date {match.group(1)}".strip()
    return token


def entry_year_key(entry: dict) -> str:
    return norm_year_token(year_text(entry))


def expected_key(entry: dict) -> str | None:
    year = "nd" if is_nd(entry) else str(entry.get("year") or "").strip()
    if not year:
        return None
    ps = persons(entry)
    if not ps and not entry.get("organisation"):
        ps = [e for e in entry.get("editors") or [] if e.get("family")]
    if ps:
        fam = [slug(p["family"]) for p in ps]
        base = fam[0] if len(fam) == 1 else f"{fam[0]}-{fam[1]}" if len(fam) == 2 else f"{fam[0]}-et-al"
    elif entry.get("organisation"):
        base = slug(entry["organisation"])
    else:
        return None
    return f"{base}-{year}{(entry.get('suffix') or '').strip()}"


def sort_key(entry: dict) -> tuple:
    ps = persons(entry) or [e for e in entry.get("editors") or [] if e.get("family")]
    if ps:
        head = [fold(p["family"]) + " " + fold(initials(p.get("given", ""))) for p in ps]
        lead = head[0]
    elif entry.get("organisation"):
        head, lead = [fold(entry["organisation"])], fold(entry["organisation"])
    else:
        head, lead = [fold(entry.get("title", ""))], fold(entry.get("title", ""))
    year = 9999 if is_nd(entry) else int(re.sub(r"\D", "", str(entry.get("year") or "0")) or 0)
    return (lead, len(head), head, year, entry.get("suffix") or "", fold(entry.get("title", "")))


# --------------------------------------------------------------------------- reference rendering

class Ref:
    """Reference built from segments: ("t", text), ("i", italic text), ("u", url)."""

    def __init__(self) -> None:
        self.segs: list[tuple[str, str]] = []

    def t(self, s: str) -> "Ref":
        if s:
            self.segs.append(("t", s))
        return self

    def i(self, s: str) -> "Ref":
        if s:
            self.segs.append(("i", s))
        return self

    def u(self, s: str) -> "Ref":
        if s:
            self.segs.append(("u", s))
        return self

    def plain(self) -> str:
        return "".join(s for _, s in self.segs)

    def stop(self) -> "Ref":
        """Close a unit with a full stop unless it already ends in . ? or !"""
        text = self.plain().rstrip()
        if text and text[-1] not in ".?!":
            self.t(".")
        return self


def need(entry: dict, field: str) -> str:
    value = entry.get(field)
    if value in (None, "", []):
        return f"[MISSING {field}]"
    return str(value)


def author_part(entry: dict) -> str | None:
    ps = persons(entry)
    if ps:
        return join_names([name_family_first(p) for p in ps])
    if entry.get("organisation"):
        return entry["organisation"]
    eds = [e for e in entry.get("editors") or [] if e.get("family")]
    if eds and entry.get("type") in ("book", "ebook"):
        return join_names([name_family_first(e) for e in eds]) + (" (ed.)" if len(eds) == 1 else " (eds.)")
    return None


def lead(r: Ref, entry: dict, title_style: str) -> bool:
    """Author (Year) Title  -- or, with no author, Title (Year). Returns True if an author led."""
    title = need(entry, "title")
    author = author_part(entry)
    styled = (lambda: r.i(title)) if title_style == "italic" else (lambda: r.t(f"‘{title}’"))
    if author:
        r.t(f"{author} ({year_text(entry)}) ")
        styled()
        return True
    styled()
    r.t(f" ({year_text(entry)})")
    return False


def online_part(r: Ref, entry: dict, accessed_for_doi: bool = False) -> None:
    doi = bare_doi(entry.get("doi", ""))
    if doi:
        r.t(" Available at: ").u(f"https://doi.org/{doi}")
        if accessed_for_doi and entry.get("accessed"):
            r.t(f" (Accessed: {ctr_date(entry['accessed'])})")
        r.t(".")
    elif entry.get("url"):
        r.t(" Available at: ").u(entry["url"]).t(f" (Accessed: {ctr_date(entry.get('accessed')) if entry.get('accessed') else '[MISSING accessed]'}).")


def render(entry: dict) -> Ref:
    kind = entry.get("type")
    r = Ref()
    if kind == "journal-article":
        lead(r, entry, "quoted")
        r.t(", ").i(need(entry, "container"))
        if entry.get("volume"):
            r.t(f", {entry['volume']}")
            if entry.get("issue"):
                r.t(f"({entry['issue']})")
        if entry.get("article_number"):
            r.t(f", article {entry['article_number']}")
        elif entry.get("pages"):
            r.t(f", {pages_text(entry['pages'])}")
        r.t(".")
        online_part(r, entry)
    elif kind in ("book", "ebook"):
        lead(r, entry, "italic")
        r.stop()
        if entry.get("edition"):
            r.t(f" {ordinal(entry['edition'])} edn.")
        r.t(f" {need(entry, 'publisher')}.")
        if kind == "ebook" or entry.get("doi") or entry.get("url"):
            online_part(r, entry)
    elif kind == "chapter":
        lead(r, entry, "quoted")
        eds = [e for e in entry.get("editors") or [] if e.get("family")]
        ed_names = join_names([name_initials_first(e) for e in eds]) or "[MISSING editors]"
        r.t(f", in {ed_names} ({'ed.' if len(eds) <= 1 else 'eds.'}) ").i(need(entry, "container"))
        r.stop()
        if entry.get("edition"):
            r.t(f" {ordinal(entry['edition'])} edn.")
        r.t(f" {need(entry, 'publisher')}")
        if entry.get("pages"):
            r.t(f", {pages_text(entry['pages'])}")
        r.t(".")
        online_part(r, entry)
    elif kind in ("webpage", "dataset"):
        if lead(r, entry, "italic"):
            r.stop()
        if not entry.get("url"):
            r.t(" Available at: [MISSING url] (Accessed: [MISSING accessed]).")
        else:
            online_part(r, entry)
    elif kind == "report":
        lead(r, entry, "italic")
        r.stop()
        if entry.get("report_number"):
            r.t(f" {entry['report_number']}.")
        if entry.get("doi") or entry.get("url"):
            online_part(r, entry)
        else:
            r.t(f" {need(entry, 'publisher')}.")
    elif kind == "vle-slides":
        lead(r, entry, "quoted")
        r.t(", ").i(need(entry, "module"))
        r.t(f". {need(entry, 'institution')}.")
        r.t(" Available at: ").u(need(entry, "url"))
        r.t(f" (Accessed: {ctr_date(entry['accessed']) if entry.get('accessed') else '[MISSING accessed]'}).")
    elif kind == "social-media":
        lead(r, entry, "italic")
        r.t(f" [{need(entry, 'platform')}] {need(entry, 'day_month')}.")
        online_part(r, entry) if entry.get("url") else r.t(" Available at: [MISSING url].")
    elif kind == "video":
        lead(r, entry, "italic")
        r.stop()
        r.t(f" {need(entry, 'day_month')}.")
        online_part(r, entry) if entry.get("url") else r.t(" Available at: [MISSING url].")
    elif kind == "news-article":
        # Cite Them Right: Author (Year) 'Title', Newspaper, Day Month. Available at: URL (Accessed: date).
        # With no personal author the newspaper title takes the author position (organisation = container),
        # so it is not repeated after the article title.
        lead(r, entry, "quoted")
        if persons(entry) or fold(entry.get("organisation", "")) != fold(entry.get("container", "")):
            r.t(", ").i(need(entry, "container"))
        r.t(f", {need(entry, 'day_month')}.")
        online_part(r, entry)
    else:
        r.t(f"[UNKNOWN TYPE {kind}] {entry.get('title', '')}")
    return r


def segs_html(segs: list[tuple[str, str]]) -> str:
    out = []
    for kind, text in segs:
        if kind == "i":
            out.append(f"<i>{html.escape(text)}</i>")
        elif kind == "u" and re.match(r"^https?://", text):
            out.append(f'<a href="{html.escape(text, quote=True)}">{html.escape(text)}</a>')
        else:
            out.append(html.escape(text))
    return "".join(out)


def md_escape(text: str) -> str:
    return re.sub(r"([*_`\\])", r"\\\1", text)


def segs_md(segs: list[tuple[str, str]]) -> str:
    out = []
    for kind, text in segs:
        if kind == "i":
            core = text.strip()
            lead_ws, trail_ws = text[: len(text) - len(text.lstrip())], text[len(text.rstrip()):]
            out.append(f"{lead_ws}*{md_escape(core)}*{trail_ws}")
        elif kind == "u":
            out.append(text)
        else:
            out.append(md_escape(text))
    return "".join(out)


# --------------------------------------------------------------------------- problems

def problem(sev: str, key: str, code: str, msg: str) -> dict:
    return {"severity": sev, "key": key, "code": code, "message": msg}


def file_path(entry: dict) -> Path | None:
    name = entry.get("file")
    if not name:
        return None
    base = ARCHIVE_DIR if entry.get("status") == "archived" else REF_DIR
    return base / name


def diff_field(diff: str) -> str:
    """Field named by a stored Crossref difference ('title: registry ... vs Crossref ...')."""
    return diff.split(":", 1)[0].strip()


def valid_accepts(entry: dict) -> dict[str, dict]:
    """Well-formed `verification_accept` items on acceptable fields, keyed by field."""
    out: dict[str, dict] = {}
    items = entry.get("verification_accept")
    for item in items if isinstance(items, list) else []:
        if (isinstance(item, dict) and item.get("field") in ACCEPTABLE_FIELDS
                and str(item.get("reason") or "").strip() and ISO_DATE.match(str(item.get("accepted_on") or ""))):
            out[item["field"]] = item
    return out


def crossref_identity_sha256(entry: dict) -> str:
    """Bind the cached comparison to its requested DOI and compared bibliographic fields."""
    identity = {field: entry.get(field) for field in CROSSREF_IDENTITY_FIELDS}
    raw = json.dumps(identity, sort_keys=True, ensure_ascii=False, separators=(",", ":"))
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()


def crossref_state(entry: dict) -> dict:
    """Effective Crossref result: current identity binding, then documented field acceptances.

    status: None (not checked), "error", "match", "accepted" (every difference is on a documented,
    accepted field) or "mismatch". `accepted` pairs each accepted difference with its acceptance item.
    """
    cr = (entry.get("verification") or {}).get("crossref")
    if not cr:
        return {"status": None, "accepted": [], "unaccepted": []}
    if cr.get("status") == "error":
        return {"status": "error", "accepted": [], "unaccepted": [], "error": cr.get("error")}
    if cr.get("identity_sha256") != crossref_identity_sha256(entry):
        return {"status": "error", "accepted": [], "unaccepted": [],
                "error": "Crossref comparison is absent or stale; run verify without --offline"}
    diffs = cr.get("differences") or []
    accepts = valid_accepts(entry)
    accepted = [(accepts[diff_field(d)], d) for d in diffs if diff_field(d) in accepts]
    unaccepted = [d for d in diffs if diff_field(d) not in accepts]
    status = "match" if not diffs else "accepted" if not unaccepted else "mismatch"
    return {"status": status, "accepted": accepted, "unaccepted": unaccepted}


def accepted_text(state: dict) -> str:
    return "; ".join(f"{a['field']} (accepted {a['accepted_on']}): {a['reason']}" for a, _ in state["accepted"])


def valid_date(value) -> bool:
    if not isinstance(value, str) or not ISO_DATE.fullmatch(value):
        return False
    try:
        dt.date.fromisoformat(value)
    except ValueError:
        return False
    return True


def pdf_identity_sha256(entry: dict) -> str:
    """Exact bibliographic values, not fuzzy matching; retrieval mode binds the stamp requirement."""
    identity = {field: entry.get(field) for field in PDF_IDENTITY_FIELDS}
    identity["retrieval_method"] = (entry.get("retrieval") or {}).get("method")
    raw = json.dumps(identity, sort_keys=True, ensure_ascii=False, separators=(",", ":"))
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()


def pdf_sha256(path: Path) -> str:
    with path.open("rb") as fh:
        return hashlib.file_digest(fh, "sha256").hexdigest()


def pdf_state(entry: dict) -> dict:
    """Effective PDF identity result; retain the unmodified automatic result for the audit.

    A manual record never overrides extraction errors, stamps or Crossref. Both the
    automatic check and manual record must bind the same current bytes and identity.
    """
    automatic = (entry.get("verification") or {}).get("pdf_text") or {}
    state = {"status": automatic.get("status"), "automatic": automatic, "details": []}
    path = file_path(entry)
    if not path or not path.is_file():
        state.update(status="error", details=["PDF file not found"])
        return state
    manual = entry.get("pdf_identity_accept")
    if "pdf_identity_accept" not in entry:
        # A stored effective status is not an automatic match or a manual audit.
        if state["status"] not in (None, "match", "mismatch", "error"):
            state.update(status="error", details=["invalid automatic PDF status; run verify"])
        elif state["status"] == "match":
            try:
                if (automatic.get("sha256") != pdf_sha256(path) or
                        automatic.get("identity_sha256") != pdf_identity_sha256(entry)):
                    state.update(status="error", details=["automatic PDF check is absent or stale; run verify"])
            except OSError as exc:
                state.update(status="error", details=[str(exc)])
        return state

    errors = state["details"]
    required = {"sha256", "identity_sha256", "fields", "checked_on", "verified_by",
                "locator", "evidence", "reason"}
    if not isinstance(manual, dict) or set(manual) != required:
        state.update(status="error", details=["pdf_identity_accept must contain exactly: "
                                             + ", ".join(sorted(required))])
        return state
    for field in required - {"fields"}:
        if not isinstance(manual[field], str) or not manual[field].strip():
            errors.append(f"pdf_identity_accept.{field} must be a non-empty string")
    fields = manual["fields"]
    if (not isinstance(fields, list) or not fields or
            any(not isinstance(f, str) or f not in {"title", "author"} for f in fields) or
            len(fields) != len(set(fields))):
        errors.append("pdf_identity_accept.fields must list title and/or author once each")
    if not valid_date(manual["checked_on"]) or manual["checked_on"] > today():
        errors.append("pdf_identity_accept.checked_on must be a real, non-future YYYY-MM-DD date")
    for field in ("sha256", "identity_sha256"):
        if not isinstance(manual[field], str) or not re.fullmatch(r"[0-9a-f]{64}", manual[field]):
            errors.append(f"pdf_identity_accept.{field} must be a lower-case SHA-256 digest")
    kind = entry.get("type")
    if not isinstance(kind, str) or kind not in TYPES:
        errors.append("manual PDF identity requires a supported bibliographic type")
    elif any(not any(entry.get(f) not in (None, "", []) for f in req.split("|"))
             for req in TYPES[kind]["required"]):
        errors.append("manual PDF identity requires all bibliographic fields for its type")
    identity = pdf_identity_sha256(entry)
    if manual["identity_sha256"] != identity:
        errors.append("manual PDF identity binding is stale (bibliographic metadata changed)")
    try:
        with path.open("rb") as fh:
            if fh.read(5) != b"%PDF-":
                errors.append("file is not a PDF")
        digest = pdf_sha256(path)
        if manual["sha256"] != digest:
            errors.append("manual PDF identity binding is stale (PDF bytes changed)")
        if automatic.get("sha256") != digest or automatic.get("identity_sha256") != identity:
            errors.append("automatic PDF check is absent or stale; run verify")
    except OSError as exc:
        errors.append(str(exc))
    mismatches = automatic.get("mismatch_fields")
    if (automatic.get("status") != "mismatch" or not isinstance(mismatches, list) or
            not mismatches or any(f not in ("title", "author") for f in mismatches)):
        errors.append("manual acceptance is only for automatic title/author extraction mismatches")
    elif isinstance(fields, list) and fields != sorted(mismatches):
        errors.append("manual fields must match the sorted automatic mismatch_fields exactly")
    if errors:
        state["status"] = "error"
    else:
        state.update(status="accepted-manual", acceptance=manual)
    return state


def manual_pdf_text(state: dict) -> str:
    item = state["acceptance"]
    return (f"{', '.join(item['fields'])}; checked {item['checked_on']} by {item['verified_by']}; "
            f"locator: {item['locator']}; evidence: {item['evidence']}; reason: {item['reason']}; "
            f"PDF SHA-256: {item['sha256']}; identity SHA-256: {item['identity_sha256']}")



def title_case_suspect(title: str) -> bool:
    body = re.split(r"[:?!]\s+", title)
    words = []
    for part in body:
        tokens = re.findall(r"[A-Za-z][A-Za-z'’\-]*", part)
        words += tokens[1:]
    candidates = [w for w in words if w.lower() not in STOPWORDS and not w.isupper()]
    if len(candidates) < 3:
        return False
    caps = sum(1 for w in candidates if w[0].isupper())
    return caps / len(candidates) > 0.6


def find_problems(data: dict) -> list[dict]:
    entries = data["entries"]
    probs: list[dict] = []
    seen: dict[str, int] = defaultdict(int)
    for e in entries:
        seen[e.get("key", "")] += 1
    for key, n in seen.items():
        if n > 1:
            probs.append(problem("error", key, "duplicate-key", f"key used by {n} entries"))

    registered_files = set()
    for e in entries:
        key = e.get("key") or "(no key)"
        kind = e.get("type")
        status = e.get("status")
        if not e.get("key"):
            probs.append(problem("error", key, "missing-field", "entry has no key"))
        if kind not in TYPES:
            probs.append(problem("error", key, "unknown-type", f"type '{kind}' is not one of: {', '.join(TYPES)}"))
        if status not in STATUSES:
            probs.append(problem("error", key, "bad-status", f"status '{status}' is not one of: {', '.join(STATUSES)}"))
        method = (e.get("retrieval") or {}).get("method")
        if method and method not in RETRIEVAL_METHODS:
            probs.append(problem("error", key, "bad-retrieval", f"retrieval.method '{method}' is not one of: "
                                 f"{', '.join(RETRIEVAL_METHODS)}"))
        if not method:
            probs.append(problem("warning", key, "missing-field", "retrieval.method not recorded"))

        # required fields
        for req in TYPES.get(kind, {}).get("required", []):
            options = req.split("|")
            if not any(e.get(o) not in (None, "", []) for o in options):
                probs.append(problem("error", key, "missing-field",
                                     f"{TYPES[kind]['label']}: missing {' or '.join(options)}"))
        if kind in ("journal-article", "ebook", "chapter", "report") and e.get("url") and not e.get("doi") \
                and not e.get("accessed"):
            probs.append(problem("error", key, "missing-field", "online source with URL needs an accessed date"))
        if e.get("doi") and not re.match(r"^10\.\d{4,9}/\S+$", bare_doi(e["doi"])):
            probs.append(problem("error", key, "bad-doi", f"DOI looks malformed: {e['doi']}"))
        for field in ("accessed",):
            if e.get(field) and not ISO_DATE.match(str(e[field])):
                probs.append(problem("error", key, "bad-date", f"{field} must be YYYY-MM-DD, got {e[field]}"))
        year = str(e.get("year") or "")
        if year and not (re.match(r"^\d{4}$", year) or is_nd(e)):
            probs.append(problem("error", key, "bad-year", f"year must be YYYY or n.d., got {year}"))
        if e.get("suffix") and not re.match(r"^[a-z]$", e["suffix"]):
            probs.append(problem("error", key, "bad-suffix", f"suffix must be a single lower-case letter"))

        # key and file naming
        exp = expected_key(e)
        if exp and e.get("key") and e["key"] != exp:
            probs.append(problem("warning", key, "key-rule", f"key does not follow the naming rule; expected '{exp}'"))
        name = e.get("file")
        if name:
            registered_files.add(name)
            if not re.match(rf"^{re.escape(e.get('key', ''))}(?:-[a-z0-9]+)*\.pdf$", name):
                probs.append(problem("error", key, "file-name",
                                     f"file '{name}' must be '{e.get('key')}-short-title.pdf' (kebab-case)"))
            path = file_path(e)
            if not path.exists():
                where = "04_references/_archived/" if status == "archived" else "04_references/"
                probs.append(problem("error", key, "missing-pdf", f"PDF not found: {where}{name}"))
        elif status != "archived":
            probs.append(problem("error", key, "missing-pdf", "no PDF registered (no PDF, no citation)"))

        # verification
        ver = e.get("verification") or {}
        state = crossref_state(e)
        if e.get("doi"):
            if state["status"] is None:
                probs.append(problem("warning", key, "not-verified", "DOI not yet checked against Crossref (run verify)"))
            elif state["status"] == "mismatch":
                probs.append(problem("error", key, "crossref-mismatch",
                                     "Crossref differs: " + "; ".join(state["unaccepted"])
                                     + (f" (accepted separately: {', '.join(a['field'] for a, _ in state['accepted'])})"
                                        if state["accepted"] else "")))
            elif state["status"] == "accepted":
                probs.append(problem("note", key, "crossref-accepted",
                                     "Crossref difference accepted: " + accepted_text(state)))
            elif state["status"] == "error":
                probs.append(problem("warning", key, "crossref-error", f"Crossref check failed: {state.get('error')}"))
        accepts = e.get("verification_accept")
        if accepts not in (None, []):
            if not isinstance(accepts, list):
                probs.append(problem("error", key, "bad-accept", "verification_accept must be a list"))
                accepts = []
            if not e.get("doi"):
                probs.append(problem("warning", key, "bad-accept", "verification_accept is set but the entry has no DOI"))
            stored = {diff_field(d) for d in ((ver.get("crossref") or {}).get("differences") or [])}
            for item in accepts:
                field = item.get("field") if isinstance(item, dict) else None
                if field in NEVER_ACCEPT:
                    probs.append(problem("error", key, "bad-accept", f"a Crossref difference in '{field}' can never be "
                                         "accepted (doi, year and author family names must match)"))
                elif field not in ACCEPTABLE_FIELDS:
                    probs.append(problem("error", key, "bad-accept", f"verification_accept field '{field}' is not one "
                                         f"of: {', '.join(sorted(ACCEPTABLE_FIELDS))}"))
                elif not str(item.get("reason") or "").strip() or not ISO_DATE.match(str(item.get("accepted_on") or "")):
                    probs.append(problem("error", key, "bad-accept", f"verification_accept '{field}' needs a reason "
                                         "and accepted_on (YYYY-MM-DD)"))
                elif state["status"] in ("match", "accepted", "mismatch") and field not in stored:
                    probs.append(problem("warning", key, "stale-accept", f"accepted difference on '{field}' no longer "
                                         "occurs in the latest Crossref check; remove the acceptance"))
        pt = ver.get("pdf_text")
        pdf = pdf_state(e)
        if "pdf_identity_accept" in e and pdf["status"] != "accepted-manual":
            probs.append(problem("error", key, "bad-pdf-accept", "; ".join(pdf["details"])))
        if name and file_path(e) and file_path(e).exists():
            if pdf["status"] == "accepted-manual":
                probs.append(problem("note", key, "pdf-accepted-manual", manual_pdf_text(pdf)
                                     + " | Automatic PDF mismatch: " + "; ".join(pt.get("details") or [])))
            elif not pt:
                probs.append(problem("warning", key, "not-verified", "PDF text not yet checked (run verify)"))
            elif pdf["status"] == "mismatch":
                probs.append(problem("error", key, "pdf-mismatch",
                                     "PDF text check failed: " + "; ".join(pt.get("details") or [])))
            elif pdf["status"] == "error":
                probs.append(problem("warning", key, "pdf-error",
                                     "PDF identity check failed: " + ("; ".join(pdf["details"])
                                                                    or str(pt.get("error")))))
        if status == "cited":
            if pdf["status"] not in PDF_VERIFIED:
                probs.append(problem("error", key, "citation-gate",
                                     "cited PDF must pass verify or current audited manual identity verification"))
            if e.get("doi") and state["status"] not in ("match", "accepted"):
                probs.append(problem("error", key, "citation-gate", "cited DOI must pass Crossref verification"))

        # module scope and style
        if kind in ACADEMIC_TYPES and not e.get("module_source") and not e.get("outside"):
            probs.append(problem("warning", key, "module-scope",
                                 "record module_source or flag outside: true; outside concepts also need a "
                                 "PDF-backed, outside-flagged concept-register entry"))
        if kind in ("journal-article", "book", "ebook", "chapter", "report", "webpage", "news-article") \
                and e.get("title") and title_case_suspect(e["title"]):
            probs.append(problem("warning", key, "style", "title looks like Title Case; Cite Them Right uses "
                                 "sentence case (capitalise the first word and proper nouns only)"))

    # same author and year
    groups: dict[tuple, list[dict]] = defaultdict(list)
    for e in entries:
        if e.get("status") == "archived":
            continue
        author = norm_words("".join(t for _, t in intext_author_segs(e)))
        groups[(author, "nd" if is_nd(e) else str(e.get("year")))].append(e)
    for (author, year), group in groups.items():
        keys = ", ".join(g.get("key", "?") for g in group)
        if len(group) > 1:
            suffixes = [g.get("suffix") or "" for g in group]
            if "" in suffixes or len(set(suffixes)) != len(suffixes):
                probs.append(problem("error", group[0].get("key", "?"), "same-author-year",
                                     f"same author and year without distinct suffixes: {keys} "
                                     "(add a, b, c ... in title order)"))
            else:
                ordered = sorted(group, key=lambda g: fold(g.get("title", "")))
                if [g.get("suffix") for g in ordered] != sorted(suffixes):
                    probs.append(problem("warning", group[0].get("key", "?"), "suffix-order",
                                         f"suffixes should follow alphabetical title order: {keys}"))
        elif group[0].get("suffix"):
            probs.append(problem("warning", group[0].get("key", "?"), "lonely-suffix",
                                 "year suffix used but no other active entry has the same author and year"))

    # files on disk that nobody registered
    for pdf in sorted(REF_DIR.glob("*.pdf")):
        if pdf.name not in registered_files:
            probs.append(problem("warning", pdf.name, "orphan-file", "PDF in 04_references/ not registered"))
    for pdf in sorted(INBOX_DIR.glob("*")) if INBOX_DIR.exists() else []:
        if pdf.is_file() and not pdf.name.startswith("."):
            probs.append(problem("note", pdf.name, "inbox", "file waiting in _inbox/: rename, verify, register"))
    order = {"error": 0, "warning": 1, "note": 2}
    probs.sort(key=lambda p: (order[p["severity"]], p["key"], p["code"]))
    return probs


# --------------------------------------------------------------------------- citation extraction

def strip_markup(text: str) -> str:
    text = re.sub(r"(?s)^---\n.*?\n---\n", "", text)  # front matter
    text = re.sub(r"(?s)<!--.*?-->", "", text)
    text = re.sub(r"(?s)```.*?```", "", text)
    return text


def split_references(text: str) -> tuple[str, str | None]:
    """Return (body, references section or None)."""
    match = re.search(r"(?im)^(#{1,6})\s*(references|reference list)\s*$", text)
    if not match:
        return text, None
    level = len(match.group(1))
    rest = text[match.end():]
    nxt = re.search(rf"(?m)^#{{1,{level}}}\s+\S", rest)
    section = rest[: nxt.start()] if nxt else rest
    body = text[: match.start()] + (rest[nxt.start():] if nxt else "")
    return body, section


def lookback_author(before: str) -> str:
    before = re.sub(r"[*_]", "", before)
    before = re.sub(r"['’]s\s*$", "", before.rstrip())
    tail = before[-200:]
    match = re.search(r"((?:(?:[A-Z][\w’'\-.]*|&|and|et\s+al\.?|of|the|for|de|van|von|der|la|le|du|da|dos|y)\s+)*"
                      r"(?:[A-Z][\w’'\-.]*|et\s+al\.?))\s*$", tail)
    if not match:
        return ""
    words = match.group(1).split()
    while words and not words[0][0].isupper():
        words.pop(0)
    return " ".join(words)


def extract_citations(body: str) -> list[dict]:
    cites: list[dict] = []
    for m in re.finditer(r"\(([^()]*)\)", body):
        content = m.group(1)
        line = body.count("\n", 0, m.start()) + 1
        parts = content.split(";")
        head = parts[0]
        ym = YEARS_RE.match(head)
        if ym and re.match(rf"^\s*{YEAR_TOKEN}", head):
            # Narrative: Author (Year, p. x; see also Other, Year)
            years = [y.strip() for y in re.split(r"\s*,\s*", ym.group(1))]
            before = body[max(0, m.start() - 200): m.start()]
            cites.append({"form": "narrative", "author_raw": lookback_author(before), "years": years,
                          "locator": ym.group(2).strip(" ,"), "line": line, "before": before,
                          "raw": m.group(0)})
            parts = parts[1:]
        elif not re.search(YEAR_TOKEN, content):
            continue
        for part in parts:
            part = part.strip()
            secondary = None
            sec = re.split(r",?\s+(?:cited|quoted)\s+in\s+", part, maxsplit=1)
            if len(sec) == 2:
                secondary, part = sec[0].strip(), sec[1].strip()
            part = re.sub(r"^(?:e\.g\.,?|i\.e\.,?|see also|see|cf\.|for example,?)\s+", "", part, flags=re.I)
            pm = re.match(rf"^(?P<author>[*_]?[A-Z].*?)[*_]?,?\s+(?P<years>{YEAR_TOKEN}(?:\s*,\s*{YEAR_TOKEN})*)"
                          r"(?P<loc>.*)$", part, re.S)
            if not pm:
                continue
            years = [y.strip() for y in re.split(r"\s*,\s*", pm.group("years"))]
            cites.append({"form": "parenthetical", "author_raw": re.sub(r"[*_]", "", pm.group("author")).strip(),
                          "years": years, "locator": pm.group("loc").strip(" ,"), "line": line,
                          "secondary": secondary, "raw": m.group(0)})
    return cites


def citation_index(entries: list[dict]) -> dict[tuple[str, str], list[tuple[str, str | None]]]:
    index: dict[tuple[str, str], list[tuple[str, str | None]]] = defaultdict(list)
    for e in entries:
        for variant, warn in author_variants(e):
            index[(variant, entry_year_key(e))].append((e["key"], warn))
    return index


def resolve(cite: dict, index: dict, variants_by_len: list[str]) -> list[dict]:
    """Resolve one extracted citation into per-year results."""
    out = []
    for year in cite["years"]:
        ykey = norm_year_token(year)
        author_norm = norm_words(cite["author_raw"])
        hit = None
        if cite["form"] == "narrative":
            tail = norm_words(re.sub(r"[*_]", "", cite["before"]))
            for variant in variants_by_len:
                if (tail == variant or tail.endswith(" " + variant)) and (variant, ykey) in index:
                    hit, author_norm = index[(variant, ykey)], variant
                    break
        elif (author_norm, ykey) in index:
            hit = index[(author_norm, ykey)]
        warnings = []
        if hit:
            warnings += [w for _, w in hit if w]
        raw_author = cite["author_raw"]
        if "&" in raw_author:
            warnings.append("use 'and', not '&', between author names")
        if re.match(r"n\.\s?d\.", year):
            warnings.append("Cite Them Right uses 'no date', not 'n.d.'")
        if re.search(r"\bpp?\.\d", cite.get("locator") or ""):
            warnings.append("put a space after p./pp. (e.g. p. 5)")
        out.append({"author": raw_author or "(author not found)", "year": year, "keys": [k for k, _ in hit] if hit else [],
                    "line": cite["line"], "form": cite["form"], "locator": cite.get("locator", ""),
                    "secondary": cite.get("secondary"), "warnings": warnings, "raw": cite["raw"]})
    return out


def draft_citations(text: str, entries: list[dict]) -> tuple[list[dict], str | None]:
    body, refs = split_references(strip_markup(text))
    index = citation_index(entries)
    variants = sorted({v for v, _ in index}, key=len, reverse=True)
    results = []
    for cite in extract_citations(body):
        results += resolve(cite, index, variants)
    return results, refs


def where_cited(entries: list[dict]) -> dict[str, list[str]]:
    found: dict[str, dict[str, int]] = defaultdict(lambda: defaultdict(int))
    for folder in DRAFT_DIRS:
        if not folder.exists():
            continue
        for md in sorted(folder.glob("*.md")):  # drafts only; not reviews/ or figures/
            try:
                results, _ = draft_citations(md.read_text(encoding="utf-8"), entries)
            except (OSError, UnicodeDecodeError):
                continue
            for r in results:
                for k in r["keys"]:
                    found[k][rel(md)] += 1
    return {k: [f"{f} ({n})" for f, n in files.items()] for k, files in found.items()}


# --------------------------------------------------------------------------- build

def reference_list(entries: list[dict]) -> list[dict]:
    return sorted([e for e in entries if e.get("status") == "cited"], key=sort_key)


def build_markdown(entries: list[dict]) -> str:
    lines = [f"<!-- Generated by 06_workflow/scripts/refs.py build on {today()} from "
             "04_references/references.json (status: cited). Do not edit by hand. -->", "", "## References", ""]
    cited = reference_list(entries)
    if not cited:
        lines += ["_No entries have status `cited` yet._", ""]
    for e in cited:
        lines += [segs_md(render(e).segs), ""]
    return "\n".join(lines)


CSS = """
:root{--ink:#1f2328;--muted:#59636e;--line:#d1d9e0;--bg:#f6f8fa;--accent:#0b3d91;--ok:#1a7f37;--bad:#cf222e;
--warn:#9a6700;--na:#6e7781}
*{box-sizing:border-box}body{margin:0;font:15px/1.55 -apple-system,BlinkMacSystemFont,"Segoe UI",Helvetica,Arial,
sans-serif;color:var(--ink);background:#fff}
header{background:var(--accent);color:#fff;padding:28px 40px 22px}header h1{margin:0 0 4px;font-size:24px;
font-weight:600}header p{margin:2px 0;opacity:.92;font-size:14px}
main{max-width:1100px;margin:0 auto;padding:24px 40px 60px}
.cards{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:12px;margin:0 0 22px}
.card{border:1px solid var(--line);border-radius:8px;padding:12px 14px;background:var(--bg)}
.card b{display:block;font-size:22px;line-height:1.2}.card span{color:var(--muted);font-size:13px}
.controls{display:flex;flex-wrap:wrap;gap:10px;align-items:center;margin:0 0 18px;padding:12px 14px;
border:1px solid var(--line);border-radius:8px}
.controls input[type=search]{flex:1 1 260px;padding:7px 10px;border:1px solid var(--line);border-radius:6px;font:inherit}
.controls button{padding:6px 12px;border:1px solid var(--line);background:#fff;border-radius:16px;cursor:pointer;
font:inherit;font-size:13px}.controls button.on{background:var(--accent);color:#fff;border-color:var(--accent)}
.controls label{font-size:13px;color:var(--muted)}#count{margin-left:auto;font-size:13px;color:var(--muted)}
details.problems{border:1px solid var(--line);border-radius:8px;margin:0 0 22px}
details.problems summary{padding:10px 14px;cursor:pointer;font-weight:600;background:var(--bg);border-radius:8px}
table{border-collapse:collapse;width:100%;font-size:13.5px}th,td{text-align:left;padding:6px 10px;
border-top:1px solid var(--line);vertical-align:top}th{color:var(--muted);font-weight:600}
details.problems td:nth-child(3){white-space:nowrap}
.sev{font-weight:600;text-transform:uppercase;font-size:11.5px;letter-spacing:.03em}
.sev.error{color:var(--bad)}.sev.warning{color:var(--warn)}.sev.note{color:#0a5c63}
h2{font-size:18px;margin:26px 0 10px;border-bottom:1px solid var(--line);padding-bottom:6px}
article.ref{border:1px solid var(--line);border-radius:8px;padding:14px 16px;margin:0 0 12px}
article.ref.hidden{display:none}
.citation{padding-left:2em;text-indent:-2em;font-family:Georgia,"Times New Roman",serif;font-size:16px;margin:0 0 8px}
.citation a{color:var(--accent);overflow-wrap:anywhere}
.badges{display:flex;flex-wrap:wrap;gap:6px;margin:0 0 8px}
.badge{font-size:12px;padding:2px 9px;border-radius:12px;border:1px solid;white-space:nowrap}
.badge.ok{color:var(--ok);border-color:var(--ok);background:#dafbe1}.badge.bad{color:var(--bad);border-color:var(--bad);
background:#ffebe9}.badge.warn{color:var(--warn);border-color:#d4a72c;background:#fff8c5}
.badge.na{color:var(--na);border-color:var(--line);background:var(--bg)}
.badge.acc{color:#0a5c63;border-color:#1b7c83;background:#e0f4f5}
.badge.st-cited{color:#fff;background:var(--accent);border-color:var(--accent)}
.badge.st-candidate{color:var(--accent);border-color:var(--accent);background:#eef3fc}
.badge.st-archived{color:var(--na);border-color:var(--na);background:#fff}
dl{display:grid;grid-template-columns:150px 1fr;gap:3px 14px;margin:0;font-size:13.5px}
dt{color:var(--muted)}dd{margin:0;word-break:break-word}dd a{color:var(--accent)}
.note{color:var(--muted);font-size:13px}code{font-size:12.5px;background:var(--bg);padding:1px 4px;border-radius:4px}
footer{max-width:1100px;margin:0 auto;padding:0 40px 40px;color:var(--muted);font-size:13px}
footer li{margin:2px 0}footer a{color:var(--accent)}
@media print{.controls{display:none}details.problems{display:none}article.ref{break-inside:avoid}
header{background:#fff;color:#000;border-bottom:2px solid #000}}
"""

JS = """
(function(){
  var q=document.getElementById('q'),only=document.getElementById('only'),cnt=document.getElementById('count');
  var status='all',items=[].slice.call(document.querySelectorAll('article.ref'));
  function apply(){var t=(q.value||'').toLowerCase().trim(),n=0;
    items.forEach(function(a){var ok=(status==='all'||a.dataset.status===status)
      &&(!t||a.dataset.search.indexOf(t)>=0)&&(!only.checked||a.dataset.problems!=='0');
      a.classList.toggle('hidden',!ok);if(ok)n++;});
    cnt.textContent=n+' of '+items.length+' shown';}
  [].slice.call(document.querySelectorAll('button[data-status]')).forEach(function(b){
    b.addEventListener('click',function(){status=b.dataset.status;
      document.querySelectorAll('button[data-status]').forEach(function(x){x.classList.toggle('on',x===b);});apply();});});
  q.addEventListener('input',apply);only.addEventListener('change',apply);apply();
})();
"""


def badge(cls: str, text: str, title: str = "") -> str:
    t = f' title="{html.escape(title, quote=True)}"' if title else ""
    return f'<span class="badge {cls}"{t}>{html.escape(text)}</span>'


def entry_badges(e: dict) -> str:
    out = [badge(f"st-{e.get('status')}", str(e.get("status") or "no status"))]
    path = file_path(e)
    if path and path.exists():
        out.append(badge("ok", "PDF present"))
    else:
        out.append(badge("bad", "PDF missing"))
    ver = e.get("verification") or {}
    pt = ver.get("pdf_text")
    pdf = pdf_state(e)
    if not (path and path.exists()):
        out.append(badge("na", "PDF text: n/a"))
    elif not pt:
        out.append(badge("warn", "PDF text: not checked"))
    else:
        cls = {"match": "ok", "accepted-manual": "acc", "mismatch": "bad", "error": "bad"}.get(pdf["status"], "warn")
        out.append(badge(cls, f"PDF identity: {pdf['status']}",
                         manual_pdf_text(pdf) if pdf["status"] == "accepted-manual"
                         else "; ".join(pdf["details"] or pt.get("details") or [])))
        out.append(badge("na", f"Automatic PDF text: {pt.get('status')}"))
    state = crossref_state(e)
    if not e.get("doi"):
        out.append(badge("na", "Crossref: no DOI"))
    elif state["status"] is None:
        out.append(badge("warn", "Crossref: not checked"))
    elif state["status"] == "accepted":
        out.append(badge("acc", "Crossref: accepted difference", accepted_text(state)))
    else:
        cls = {"match": "ok", "mismatch": "bad"}.get(state["status"], "warn")
        out.append(badge(cls, f"Crossref: {state['status']}", "; ".join(state["unaccepted"])
                         or str(state.get("error") or "")))
    return "".join(out)


def module_source_text(ms) -> str:
    if not ms:
        return ""
    items = ms if isinstance(ms, list) else [ms]
    parts = []
    for m in items:
        if isinstance(m, dict):
            bits = [m.get("slug", "")]
            if m.get("slide"):
                bits.append(f"slide {m['slide']}")
            text = ", ".join(b for b in bits if b)
            if m.get("cited_as"):
                text += f" (cited as: {m['cited_as']})"
            if m.get("note"):
                text += f" ({m['note']})"
            parts.append(text)
        else:
            parts.append(str(m))
    return "; ".join(parts)


def build_html(data: dict, probs: list[dict], cited_in: dict[str, list[str]]) -> str:
    entries = data["entries"]
    meta = data.get("meta", {})
    by_key_probs: dict[str, int] = defaultdict(int)
    for p in probs:
        if p["severity"] != "note":  # notes (accepted differences, inbox files) are not problems
            by_key_probs[p["key"]] += 1
    active = [e for e in entries if e.get("status") != "archived"]
    with_pdf = sum(1 for e in active if file_path(e) and file_path(e).exists())
    doi_entries = [e for e in active if e.get("doi")]
    cr_ok = sum(1 for e in doi_entries if crossref_state(e)["status"] in ("match", "accepted"))
    file_entries = [e for e in active if file_path(e) and file_path(e).exists()]
    pdf_states = [pdf_state(e)["status"] for e in file_entries]
    pt_ok = sum(st in PDF_VERIFIED for st in pdf_states)
    pt_manual = pdf_states.count("accepted-manual")
    n_err = sum(1 for p in probs if p["severity"] == "error")
    n_warn = sum(1 for p in probs if p["severity"] == "warning")
    counts = {s: sum(1 for e in entries if e.get("status") == s) for s in STATUSES}
    generated = dt.datetime.now().astimezone()

    cards = [
        (len(entries), "entries in registry"), (counts["cited"], "cited"), (counts["candidate"], "candidate"),
        (counts["archived"], "archived"), (f"{with_pdf}/{len(active)}", "active entries with PDF"),
        (f"{pt_ok}/{len(file_entries)}", f"PDF identity verified ({pt_manual} accepted-manual)"),
        (f"{cr_ok}/{len(doi_entries)}", "Crossref verified (incl. accepted differences)"),
        (f"{n_err} / {n_warn}", "problems: errors / warnings"),
    ]
    h = []
    h.append("<!DOCTYPE html><html lang=\"en-GB\"><head><meta charset=\"utf-8\">"
             "<meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">"
             f"<title>References — {html.escape(meta.get('module', 'MARK1286'))}</title>"
             f"<style>{CSS}</style></head><body>")
    h.append("<header>")
    h.append(f"<h1>{html.escape(meta.get('title', 'Reference registry'))}</h1>")
    h.append(f"<p>{html.escape(meta.get('module', ''))} · {html.escape(meta.get('assessment', ''))}</p>")
    h.append(f"<p>Referencing style: {html.escape(meta.get('style', 'Cite Them Right Harvard'))}</p>")
    h.append(f"<p>Generated {generated.strftime('%d %B %Y, %H:%M')} from <code style=\"background:transparent;"
             f"color:inherit\">references.json</code>. Every entry links to its saved PDF in this folder.</p>")
    h.append("</header><main>")
    h.append('<section class="cards">' + "".join(f'<div class="card"><b>{html.escape(str(v))}</b>'
                                                  f'<span>{html.escape(t)}</span></div>' for v, t in cards)
             + "</section>")
    h.append('<div class="controls"><input id="q" type="search" placeholder="Search author, title, key, notes…" '
             'aria-label="Search references">')
    for s, label in (("all", "All"), ("cited", "Cited"), ("candidate", "Candidate"), ("archived", "Archived")):
        h.append(f'<button type="button" data-status="{s}"{" class=\"on\"" if s == "all" else ""}>{label}</button>')
    h.append('<label><input id="only" type="checkbox"> only entries with problems</label>'
             '<span id="count"></span></div>')

    h.append(f'<details class="problems"{" open" if probs else ""}><summary>Problems ({n_err} errors, '
             f'{n_warn} warnings, {len(probs) - n_err - n_warn} notes)</summary>')
    if probs:
        h.append("<table><thead><tr><th>Severity</th><th>Entry / file</th><th>Check</th><th>Detail</th></tr>"
                 "</thead><tbody>")
        for p in probs:
            h.append(f'<tr><td class="sev {p["severity"]}">{p["severity"]}</td><td><code>{html.escape(p["key"])}'
                     f'</code></td><td>{html.escape(p["code"])}</td><td>{html.escape(p["message"])}</td></tr>')
        h.append("</tbody></table>")
    else:
        h.append('<p class="note" style="padding:0 14px">No problems found.</p>')
    h.append("</details>")

    h.append("<h2>Reference list (Harvard, alphabetical)</h2>")
    for e in sorted(entries, key=sort_key):
        key = e.get("key", "")
        ref = render(e)
        paren, narr = intext(e)
        path = file_path(e)
        search = " ".join([key, ref.plain(), e.get("notes", "") or "", e.get("status", "") or "",
                           json.dumps(e.get("used_for", ""), ensure_ascii=False)]).lower()
        h.append(f'<article class="ref" id="{html.escape(key, quote=True)}" data-status="{html.escape(e.get("status") or "", quote=True)}" '
                 f'data-problems="{by_key_probs.get(key, 0)}" data-search="{html.escape(search, quote=True)}">')
        h.append(f'<p class="citation">{segs_html(ref.segs)}</p>')
        h.append(f'<div class="badges">{entry_badges(e)}'
                 + (badge("bad", f"{by_key_probs[key]} problem(s)") if by_key_probs.get(key) else "") + "</div>")
        rows = [("Key", f"<code>{html.escape(key)}</code>"),
                ("Type", html.escape(TYPES.get(e.get("type"), {}).get("label", str(e.get("type"))))),
                ("In-text", f"{segs_html(paren)} &nbsp;·&nbsp; {segs_html(narr)}")]
        if e.get("file"):
            href = ("_archived/" if e.get("status") == "archived" else "") + e["file"]
            state = "" if path and path.exists() else " <span class=\"sev error\">(missing)</span>"
            rows.append(("PDF", f'<a href="{html.escape(href, quote=True)}">{html.escape(e["file"])}</a>{state}'))
        else:
            rows.append(("PDF", '<span class="sev error">none registered</span>'))
        if e.get("doi"):
            d = bare_doi(e["doi"])
            rows.append(("DOI", f'<a href="https://doi.org/{html.escape(d, quote=True)}">{html.escape(d)}</a>'))
        if e.get("url"):
            rows.append(("URL", f'<a href="{html.escape(e["url"], quote=True)}">{html.escape(e["url"])}</a>'))
        if e.get("accessed"):
            rows.append(("Accessed", html.escape(ctr_date(e["accessed"]))))
        ret = e.get("retrieval") or {}
        if ret:
            rows.append(("Retrieved", html.escape(" · ".join(str(x) for x in (ret.get("method"), ret.get("from"),
                                                                             ret.get("date")) if x))))
        ver = e.get("verification") or {}
        vbits = []
        if ver.get("crossref"):
            cr, state = ver["crossref"], crossref_state(e)
            vbits.append(f"Crossref {state['status']} ({cr.get('checked_on', '')})"
                         + (": " + "; ".join(state["unaccepted"]) if state["unaccepted"] else "")
                         + (f" {state['error']}" if state.get("error") else ""))
            if state["accepted"]:
                vbits.append("Accepted Crossref difference: " + accepted_text(state)
                             + " | Crossref record: " + "; ".join(d for _, d in state["accepted"]))
        if ver.get("pdf_text"):
            pt = ver["pdf_text"]
            vbits.append(f"PDF text {pt.get('status')} ({pt.get('checked_on', '')}): title words "
                         f"{pt.get('title_words', '?')}, author/organisation "
                         f"{'found' if pt.get('author_found') else 'NOT found'}"
                         + (f"; {'; '.join(pt.get('details'))}" if pt.get("details") else ""))
            pdf = pdf_state(e)
            vbits.append(f"Effective PDF identity: {pdf['status']}"
                         + (": " + manual_pdf_text(pdf) if pdf["status"] == "accepted-manual"
                            else ": " + "; ".join(pdf["details"]) if pdf["details"] else ""))
        if ver.get("notes"):
            vbits.append(f"Notes: {ver['notes']}")
        if vbits:
            rows.append(("Verification", "<br>".join(html.escape(v) for v in vbits)))
        if e.get("module_source"):
            rows.append(("Module source", html.escape(module_source_text(e["module_source"]))))
        if e.get("used_for"):
            uf = e["used_for"]
            rows.append(("Used for", html.escape("; ".join(uf) if isinstance(uf, list) else str(uf))))
        rows.append(("Where cited", html.escape("; ".join(cited_in.get(key, []))) or
                     '<span class="note">not cited in 07_drafts/ or 08_final/</span>'))
        if e.get("notes"):
            rows.append(("Notes", html.escape(e["notes"])))
        h.append("<dl>" + "".join(f"<dt>{k}</dt><dd>{v}</dd>" for k, v in rows) + "</dl></article>")
    h.append("</main><footer><p><b>Style authority.</b> Harvard as set out in Cite Them Right, the referencing "
             "resource named by the University of Greenwich Library. Saved copies of the guidance used "
             "(project folder <code>00_brief_and_criteria/source/</code>):</p><ul>")
    for src in meta.get("style_sources", []):
        h.append(f"<li>{html.escape(Path(src).name)}</li>")
    h.append("</ul></footer>")
    h.append(f"<script>{JS}</script></body></html>")
    return "\n".join(h)


def cmd_build(_args) -> int:
    data = load_registry()
    probs = find_problems(data)
    cited_in = where_cited(data["entries"])
    HTML_OUT.write_text(build_html(data, probs, cited_in), encoding="utf-8")
    MD_OUT.write_text(build_markdown(data["entries"]), encoding="utf-8")
    n_err = sum(1 for p in probs if p["severity"] == "error")
    n_warn = sum(1 for p in probs if p["severity"] == "warning")
    print(f"Wrote {rel(HTML_OUT)} ({len(data['entries'])} entries) and {rel(MD_OUT)} "
          f"({len(reference_list(data['entries']))} cited).")
    print(f"Problems: {n_err} errors, {n_warn} warnings, {len(probs) - n_err - n_warn} notes.")
    for p in probs:
        print(f"  [{p['severity']}] {p['key']}: {p['code']}: {p['message']}")
    return 1 if n_err else 0


# --------------------------------------------------------------------------- verify

def crossref_record(doi: str, mailto: str) -> dict:
    url = "https://api.crossref.org/works/" + urllib.parse.quote(doi, safe="/:();.-_")
    agent = f"mark1286-marketing-plan-poster-refs/1.0 (mailto:{mailto})" if mailto else "mark1286-marketing-plan-poster-refs/1.0"
    req = urllib.request.Request(url, headers={"User-Agent": agent, "Accept": "application/json"})
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.load(resp)["message"]


def date_year(msg: dict, field: str) -> str | None:
    parts = (msg.get(field) or {}).get("date-parts") or [[None]]
    return str(parts[0][0]) if parts and parts[0] and parts[0][0] else None


def compare_crossref(e: dict, msg: dict) -> tuple[list[str], dict]:
    title = " ".join((msg.get("title") or [""])[0].split())
    subtitle = " ".join((msg.get("subtitle") or [""])[0].split()) if msg.get("subtitle") else ""
    full_title = f"{title}: {subtitle}" if subtitle else title
    cr_authors = [a.get("family") or a.get("name") or "" for a in msg.get("author") or []]
    record = {
        "type": msg.get("type"), "title": html.unescape(full_title), "authors": cr_authors,
        "year_issued": date_year(msg, "issued"), "year_print": date_year(msg, "published-print"),
        "year_online": date_year(msg, "published-online"),
        "container": html.unescape((msg.get("container-title") or [""])[0]),
        "volume": msg.get("volume"), "issue": msg.get("issue"), "pages": msg.get("page"),
        "article_number": msg.get("article-number"), "publisher": msg.get("publisher"),
    }
    diffs = []
    if squash(e.get("title", "")) not in (squash(full_title), squash(title)):
        diffs.append(f"title: registry '{e.get('title')}' vs Crossref '{record['title']}'")
    elif subtitle and squash(e.get("title", "")) == squash(title):
        diffs.append(f"title: Crossref has subtitle '{subtitle}' that the registry omits")
    reg_fam = [norm_words(p["family"]) for p in persons(e)]
    if e.get("type") == "chapter" or reg_fam or cr_authors:
        if reg_fam != [norm_words(a) for a in cr_authors]:
            diffs.append(f"authors: registry {[p['family'] for p in persons(e)]} vs Crossref {cr_authors}")
    years = {y for y in (record["year_issued"], record["year_print"]) if y}
    if str(e.get("year")) not in years:
        diffs.append(f"year: registry {e.get('year')} vs Crossref issued {record['year_issued']}, "
                     f"print {record['year_print']}, online {record['year_online']}")
    if record["container"] and e.get("container") and norm_words(e["container"]) != norm_words(record["container"]):
        diffs.append(f"container: registry '{e.get('container')}' vs Crossref '{record['container']}'")
    for field in ("volume", "issue"):
        mine, theirs = str(e.get(field) or "").strip(), str(record[field] or "").strip()
        if theirs and mine != theirs:
            diffs.append(f"{field}: registry '{mine}' vs Crossref '{theirs}'")
    if record["pages"] and e.get("pages"):
        if re.sub(r"[–—-]+", "-", str(e["pages"])).replace(" ", "") != re.sub(r"[–—-]+", "-", record["pages"]):
            diffs.append(f"pages: registry '{e['pages']}' vs Crossref '{record['pages']}'")
    elif record["pages"] and not e.get("pages") and not e.get("article_number"):
        diffs.append(f"pages: registry empty vs Crossref '{record['pages']}'")
    return diffs, record


def pdf_text(path: Path, first: int = 1, last: int = 2) -> str:
    proc = subprocess.run(["pdftotext", "-f", str(first), "-l", str(last), "-enc", "UTF-8", str(path), "-"],
                          capture_output=True, text=True)
    if proc.returncode != 0:
        raise RuntimeError(proc.stderr.strip() or f"pdftotext exit {proc.returncode}")
    return proc.stdout


def check_pdf(e: dict, path: Path) -> dict:
    with path.open("rb") as fh:
        if fh.read(5) != b"%PDF-":
            return {"status": "error", "checked_on": today(), "error": "file is not a PDF"}
    text = pdf_text(path)
    flat = squash(text)
    words = [w for w in norm_words(e.get("title", "")).split() if len(w) >= 4 and w not in STOPWORDS]
    if not words:
        words = [w for w in norm_words(e.get("title", "")).split() if len(w) >= 2]
    found = [w for w in words if w in flat]
    ps = persons(e) or [x for x in e.get("editors") or [] if x.get("family")]
    where = "1-2"

    def org_in(flat_text: str, name: str) -> bool:
        tokens = [t for t in norm_words(name).split() if t not in STOPWORDS]
        return bool(tokens) and all(t in flat_text for t in tokens)

    if ps:
        who = ps[0]["family"]
        author_found = squash(who) in flat
    elif e.get("organisation"):
        who = e["organisation"]
        author_found = org_in(flat, who)
        # Web pages usually name their publisher in the site footer, which prints on the last page of a
        # snapshot. Accept it there, and record where it was found.
        if not author_found and e.get("type") in ("webpage", "news-article"):
            full = squash(pdf_text(path, 1, 10_000))
            if org_in(full, who):
                author_found, where = True, "1-2 (title); publisher found later in the document"
    else:
        who, author_found = "", True
    details, mismatch_fields = [], []
    ratio = len(found) / len(words) if words else 0
    if ratio < 0.8:
        missing = [w for w in words if w not in found]
        details.append(f"title words missing from pages 1-2: {', '.join(missing)}")
        mismatch_fields.append("title")
    if not author_found:
        details.append(f"first author/organisation '{who}' not found on pages 1-2"
                       + (" or anywhere in the snapshot" if e.get("type") in ("webpage", "news-article") else ""))
        mismatch_fields.append("author")
    if (e.get("retrieval") or {}).get("method") == "web-snapshot":
        stamp = re.search(r"Accessed:\s*(\d{1,2} [A-Z][a-z]+ \d{4})", text)
        if not valid_date(e.get("accessed")):
            details.append("web snapshot requires a valid registry accessed date")
            mismatch_fields.append("accessed")
        elif not stamp:
            details.append("snapshot header with the accessed date not found")
            mismatch_fields.append("accessed")
        elif stamp.group(1) != ctr_date(e["accessed"]):
            details.append(f"snapshot printed on {stamp.group(1)} but registry accessed is {ctr_date(e['accessed'])}")
            mismatch_fields.append("accessed")
    return {"status": "match" if not details else "mismatch", "checked_on": today(),
            "title_words": f"{len(found)}/{len(words)}", "author_found": author_found, "pages_checked": where,
            "details": details, "mismatch_fields": sorted(mismatch_fields),
            "sha256": pdf_sha256(path), "identity_sha256": pdf_identity_sha256(e)}


def cmd_verify(args) -> int:
    data = load_registry()
    mailto = os.environ.get("REFS_MAILTO") or data["meta"].get("mailto", "")
    targets = [e for e in data["entries"] if not args.key or e.get("key") in args.key]
    if args.key:
        unknown = set(args.key) - {e.get("key") for e in targets}
        if unknown:
            print(f"Unknown key(s): {', '.join(sorted(unknown))}", file=sys.stderr)
            return 2
    failures = 0
    for e in targets:
        key = e.get("key")
        ver = e.setdefault("verification", {})
        ver.setdefault("notes", "")
        lines = []
        if e.get("doi") and not args.offline:
            doi = bare_doi(e["doi"])
            try:
                msg = crossref_record(doi, mailto)
                diffs, record = compare_crossref(e, msg)
                ver["crossref"] = {"status": "mismatch" if diffs else "match", "checked_on": today(),
                                   "doi": doi, "differences": diffs, "record": record,
                                   "identity_sha256": crossref_identity_sha256(e)}
                state = crossref_state(e)
                ver["crossref"]["status"] = state["status"]
                ver["crossref"]["accepted_differences"] = [a["field"] for a, _ in state["accepted"]]
            except (urllib.error.URLError, TimeoutError, ValueError, KeyError) as exc:
                ver["crossref"] = {"status": "error", "checked_on": today(), "doi": doi, "error": str(exc)}
            cr = ver["crossref"]
            if cr["status"] == "accepted":
                lines.append(f"Crossref match (accepted: {', '.join(cr['accepted_differences'])})")
            else:
                state = crossref_state(e)
                lines.append(f"Crossref {cr['status']}" + (": " + "; ".join(state["unaccepted"])
                                                            if state["unaccepted"] else "")
                             + (f" [accepted: {', '.join(a['field'] for a, _ in state['accepted'])}]"
                                if state["accepted"] else "")
                             + (f" ({cr['error']})" if cr.get("error") else ""))
            time.sleep(0.3)
        elif e.get("doi"):
            state = crossref_state(e)
            lines.append(f"Crossref cached {state['status'] or 'not checked'}"
                         + (": " + "; ".join(state["unaccepted"]) if state["unaccepted"] else "")
                         + (f" ({state['error']})" if state.get("error") else ""))
        path = file_path(e)
        if path and path.exists():
            try:
                ver["pdf_text"] = check_pdf(e, path)
            except (OSError, RuntimeError) as exc:
                ver["pdf_text"] = {"status": "error", "checked_on": today(), "error": str(exc)}
            pt = ver["pdf_text"]
            lines.append(f"PDF text {pt['status']} (title words {pt.get('title_words', '?')}, author "
                         f"{'found' if pt.get('author_found') else 'NOT found'})"
                         + (": " + "; ".join(pt.get("details") or []) if pt.get("details") else "")
                         + (f" ({pt['error']})" if pt.get("error") else ""))
        else:
            message = "PDF file not found" if e.get("file") else "no PDF registered"
            ver["pdf_text"] = {"status": "error", "checked_on": today(), "error": message}
            lines.append(message + "; no PDF, no citation")
        if not e.get("doi"):
            lines.append("no DOI; Crossref check not applicable")
        ver["checked_on"] = today()
        pdf = pdf_state(e)
        lines.append(f"PDF identity {pdf['status']}"
                     + (": " + manual_pdf_text(pdf) if pdf["status"] == "accepted-manual"
                        else ": " + "; ".join(pdf["details"]) if pdf["details"] else ""))
        bad = (pdf["status"] not in PDF_VERIFIED or
               bool(e.get("doi") and crossref_state(e)["status"] not in ("match", "accepted")))
        failures += bad
        print(f"{'FAIL' if bad else 'ok  '} {key}: " + " | ".join(lines))
    save_registry(data)
    print(f"Verified {len(targets)} entr{'y' if len(targets) == 1 else 'ies'}; {failures} effective verification failures. "
          f"Results stored in {rel(REGISTRY)} (bibliographic fields unchanged).")
    return 1 if failures else 0


# --------------------------------------------------------------------------- check-draft

def norm_ref_line(line: str) -> str:
    line = re.sub(r"^\s*(?:[-*+]|\d+[.)])\s+", "", line)
    line = line.replace("\\", "").replace("’", "'").replace("‘", "'").replace("“", '"').replace("”", '"')
    line = line.replace("–", "-").replace("—", "-")
    return " ".join(line.split())


def ref_paragraphs(section: str) -> list[str]:
    section = re.sub(r"(?s)<!--.*?-->", "", section)
    paras, cur = [], []
    for line in section.splitlines():
        if not line.strip():
            if cur:
                paras.append(" ".join(cur))
                cur = []
            continue
        if re.match(r"^\s*(?:[-*+]|\d+[.)])\s+", line) and cur:
            paras.append(" ".join(cur))
            cur = []
        cur.append(line.strip())
    if cur:
        paras.append(" ".join(cur))
    return [norm_ref_line(p) for p in paras if not p.strip().startswith("_No entries")]


def cmd_check_draft(args) -> int:
    draft = Path(args.draft)
    if not draft.is_absolute():
        draft = (Path.cwd() / draft).resolve()
    if not draft.exists():
        print(f"Draft not found: {draft}", file=sys.stderr)
        return 2
    data = load_registry()
    entries = data["entries"]
    by_key = {e.get("key"): e for e in entries}
    results, refs_section = draft_citations(draft.read_text(encoding="utf-8"), entries)
    errors = warnings = 0
    print(f"Draft: {rel(draft)}")
    print(f"In-text citations found: {len(results)}")
    for r in results:
        target = ", ".join(r["keys"]) if r["keys"] else "UNKNOWN"
        loc = f" [{r['locator']}]" if r["locator"] else ""
        sec = f" (secondary: {r['secondary']})" if r.get("secondary") else ""
        print(f"  line {r['line']:>4}  {r['form']:<13} {r['author']} {r['year']}{loc}{sec} -> {target}")

    unknown = [r for r in results if not r["keys"]]
    ambiguous = [r for r in results if len(r["keys"]) > 1]
    cited_keys = sorted({k for r in results for k in r["keys"]})
    print("\nUnknown citations (not in the registry):")
    for r in unknown:
        print(f"  ERROR line {r['line']}: {r['raw']} -> author '{r['author']}', year '{r['year']}'")
    errors += len(unknown)
    if not unknown:
        print("  none")
    for r in ambiguous:
        print(f"  ERROR line {r['line']}: {r['raw']} matches several entries: {', '.join(r['keys'])}")
        errors += 1

    print("\nCited in the draft but registry status is not 'cited':")
    rows = [k for k in cited_keys if by_key[k].get("status") != "cited"]
    for k in rows:
        print(f"  WARNING {k}: status is '{by_key[k].get('status')}' (set it to 'cited' when the citation is final)")
    warnings += len(rows)
    if not rows:
        print("  none")

    print("\nRegistry entries with status 'cited' that the draft does not cite:")
    rows = [e["key"] for e in entries if e.get("status") == "cited" and e.get("key") not in cited_keys]
    for k in rows:
        print(f"  WARNING {k}")
    warnings += len(rows)
    if not rows:
        print("  none")

    print("\nCited entries without a PDF in 04_references/ (no PDF, no citation):")
    rows = [k for k in cited_keys if not (file_path(by_key[k]) and file_path(by_key[k]).exists())]
    for k in rows:
        print(f"  ERROR {k}: {by_key[k].get('file') or 'no file registered'}")
    errors += len(rows)
    if not rows:
        print("  none")

    print("\nCited entries with failed or missing verification:")
    rows = []
    for k in cited_keys:
        ver = by_key[k].get("verification") or {}
        for part in ("crossref", "pdf_text"):
            st = (ver.get(part) or {}).get("status")
            applicable = (part == "crossref" and by_key[k].get("doi")) or (part == "pdf_text" and by_key[k].get("file"))
            if part == "crossref":
                st = crossref_state(by_key[k])["status"]
            else:
                st = pdf_state(by_key[k])["status"]
            verified = ("match", "accepted") if part == "crossref" else PDF_VERIFIED
            if applicable and st not in verified:
                rows.append(f"{k}: {part} {st or 'not checked'}")
    for row in rows:
        print(f"  ERROR {row}")
    errors += len(rows)
    if not rows:
        print("  none")

    print("\nRegistry errors on entries the draft cites (see the Problems panel in references.html):")
    rows = [p for p in find_problems(data) if p["severity"] == "error" and p["key"] in cited_keys
            and p["code"] != "missing-pdf"]
    for p in rows:
        print(f"  ERROR {p['key']}: {p['code']}: {p['message']}")
    errors += len(rows)
    if not rows:
        print("  none")

    print("\nCitation style notes:")
    style = [(r, w) for r in results for w in r["warnings"]]
    for r, w in style:
        print(f"  WARNING line {r['line']}: {r['raw']}: {w}")
    warnings += len(style)
    if not style:
        print("  none")

    print("\nReferences section vs generated list (04_references/reference-list.md, status 'cited'):")
    generated = [norm_ref_line(segs_md(render(e).segs)) for e in reference_list(entries)]
    if refs_section is None:
        print("  ERROR no '## References' heading found in the draft")
        errors += 1
    else:
        mine = ref_paragraphs(refs_section)
        if mine == generated:
            print(f"  identical ({len(mine)} entries, same order)")
        else:
            missing = [g for g in generated if g not in mine]
            extra = [m for m in mine if m not in generated]
            for g in missing:
                print(f"  ERROR missing from draft: {g}")
            for m in extra:
                print(f"  ERROR in draft but not generated (edited by hand, or entry not 'cited'): {m}")
            if not missing and not extra:
                print("  ERROR same entries but different order (list must be alphabetical as generated)")
            errors += len(missing) + len(extra) + (0 if missing or extra else 1)
    print(f"\nSummary: {errors} errors, {warnings} warnings.")
    return 1 if errors else 0


# --------------------------------------------------------------------------- main

def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = parser.add_subparsers(dest="cmd", required=True)
    sub.add_parser("build", help="render references.html and reference-list.md").set_defaults(func=cmd_build)
    p = sub.add_parser("verify", help="Crossref + PDF text verification")
    p.add_argument("--key", action="append", help="verify only this key (repeatable)")
    p.add_argument("--offline", action="store_true", help="skip Crossref; only check PDFs")
    p.set_defaults(func=cmd_verify)
    p = sub.add_parser("check-draft", help="audit citations in a Markdown draft")
    p.add_argument("draft", help="path to the draft .md")
    p.set_defaults(func=cmd_check_draft)
    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
