#!/usr/bin/env python3
"""Save a web page as a PDF snapshot with Google Chrome headless.

Every page of the snapshot carries a print header and footer:
  header: "Accessed: <day month year, time, UTC offset>" and the page title
  footer: the full URL and "page N of M"
so the PDF itself proves where and when the page was read. The script also
prints the accessed date in ISO form (for references.json) and in Cite Them
Right form (for the reference list).

Chrome is driven through the DevTools protocol over a pipe
(--remote-debugging-pipe), which lets the script wait for the page to load,
allow a render delay, hide cookie-consent overlays (they otherwise print over
the text), print A4 with the header/footer above, and close Chrome cleanly.

Usage (from the workspace root):
    python3 -B 06_workflow/scripts/save_web_pdf.py URL FILE_NAME.pdf [options]

Example form (replace URL and filename with the verified source details):
    python3 -B 06_workflow/scripts/save_web_pdf.py URL organisation-nd-page-title.pdf

Open-access PDF behind a publisher's browser check (saves the publisher's own
file, not a print; no header/footer is added):
    python3 -B 06_workflow/scripts/save_web_pdf.py LANDING_PAGE_URL KEY-SHORT-TITLE.pdf \
        --fetch-pdf PUBLISHER_PDF_URL

Standard library only. The Chrome profile lives in a temporary directory
outside the workspace and is deleted afterwards.
"""
from __future__ import annotations

import argparse
import base64
import datetime as dt
import fcntl
import html
import json
import os
import re
import select
import shutil
import signal
import subprocess
import sys
import tempfile
import time
from pathlib import Path

WS = Path(__file__).resolve().parents[2]
DEFAULT_OUT_DIR = WS / "04_references"
CHROME = Path("/Applications/Google Chrome.app/Contents/MacOS/Google Chrome")
NAME_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*\.pdf$")

# Common cookie-consent platforms. Hidden (not accepted) before printing.
CONSENT_SELECTORS = [
    "#onetrust-consent-sdk", "#onetrust-banner-sdk", ".onetrust-pc-dark-filter",
    "#CybotCookiebotDialog", "#CybotCookiebotDialogBodyUnderlay",
    "#usercentrics-root", "#didomi-host", ".qc-cmp2-container", "#qc-cmp2-ui",
    "#truste-consent-track", "#consent_blackbar", ".truste_box_overlay", ".truste_overlay",
    ".osano-cm-window", ".cky-consent-container", ".cky-overlay", ".cky-modal",
    "#cmplz-cookiebanner-container", ".cmplz-cookiebanner", "#ccc", "#ccc-overlay",
    ".cc-window", ".cc-banner", ".cc-grower", "#iubenda-cs-banner", ".klaro",
    "#cookie-law-info-bar", "#cookie-notice", "#cookieConsent", "#cookie-consent",
    ".cookie-consent", ".cookie-banner", "#cookie-banner", ".cookies-banner",
    "#gdpr-cookie-notice", ".gdpr-cookie-notice", "#termly-code-snippet-support",
    "[aria-label='cookieconsent']", "[id^='sp_message_container']",
]


def ctr_date(day: dt.date) -> str:
    """Cite Them Right accessed-date form, e.g. 27 September 2026."""
    return f"{day.day} {day.strftime('%B %Y')}"


def chrome_major(chrome: Path) -> str:
    out = subprocess.run([str(chrome), "--version"], capture_output=True, text=True, check=True).stdout
    match = re.search(r"(\d+)\.\d+", out)
    return match.group(1) if match else "130"


class DevTools:
    """Minimal Chrome DevTools protocol client over --remote-debugging-pipe."""

    def __init__(self, cmd: list[str]):
        to_chrome_r, to_chrome_w = os.pipe()
        from_chrome_r, from_chrome_w = os.pipe()
        # Chrome reads commands on fd 3 and writes replies on fd 4. Park the
        # child's ends at fd >= 10 (close-on-exec) so the dup2 calls in the
        # child cannot clobber each other; dup2 makes 3 and 4 inheritable.
        child_r = fcntl.fcntl(to_chrome_r, fcntl.F_DUPFD_CLOEXEC, 10)
        child_w = fcntl.fcntl(from_chrome_w, fcntl.F_DUPFD_CLOEXEC, 10)
        os.close(to_chrome_r)
        os.close(from_chrome_w)

        def wire_fds() -> None:
            os.dup2(child_r, 3)
            os.dup2(child_w, 4)

        self.log = tempfile.TemporaryFile(mode="w+")
        self.proc = subprocess.Popen(
            cmd, stdin=subprocess.DEVNULL, stdout=self.log, stderr=subprocess.STDOUT,
            preexec_fn=wire_fds, close_fds=False, start_new_session=True,
        )
        os.close(child_r)
        os.close(child_w)
        self.wfd, self.rfd = to_chrome_w, from_chrome_r
        self.buffer = b""
        self.next_id = 0
        self.events: list[dict] = []

    def _read_message(self, deadline: float) -> dict | None:
        while b"\0" not in self.buffer:
            remaining = deadline - time.monotonic()
            if remaining <= 0:
                return None
            ready, _, _ = select.select([self.rfd], [], [], min(remaining, 0.5))
            if ready:
                chunk = os.read(self.rfd, 1 << 20)
                if not chunk:
                    raise RuntimeError("Chrome closed the DevTools pipe")
                self.buffer += chunk
        raw, self.buffer = self.buffer.split(b"\0", 1)
        return json.loads(raw)

    def call(self, method: str, params: dict | None = None, session: str | None = None,
             timeout: float = 60) -> dict:
        self.next_id += 1
        msg: dict = {"id": self.next_id, "method": method, "params": params or {}}
        if session:
            msg["sessionId"] = session
        os.write(self.wfd, json.dumps(msg).encode() + b"\0")
        deadline = time.monotonic() + timeout
        while True:
            reply = self._read_message(deadline)
            if reply is None:
                raise TimeoutError(f"{method} timed out after {timeout:.0f}s")
            if reply.get("id") == self.next_id:
                if "error" in reply:
                    raise RuntimeError(f"{method}: {reply['error'].get('message')}")
                return reply.get("result", {})
            if "method" in reply:
                self.events.append(reply)

    def wait_event(self, name: str, timeout: float) -> bool:
        if any(e.get("method") == name for e in self.events):
            return True
        deadline = time.monotonic() + timeout
        while True:
            msg = self._read_message(deadline)
            if msg is None:
                return False
            if msg.get("method") == name:
                return True

    def close(self) -> str:
        try:
            if self.proc.poll() is None:
                try:
                    self.call("Browser.close", timeout=5)
                except Exception:
                    pass
                try:
                    self.proc.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    os.killpg(self.proc.pid, signal.SIGKILL)
        except ProcessLookupError:
            pass
        for fd in (self.wfd, self.rfd):
            try:
                os.close(fd)
            except OSError:
                pass
        self.log.seek(0)
        text = self.log.read()
        self.log.close()
        return text


def header_footer(accessed: dt.datetime) -> tuple[str, str]:
    stamp = html.escape(
        f"Accessed: {accessed.day} {accessed.strftime('%B %Y, %H:%M')} (UTC{accessed.strftime('%z')[:3]}:"
        f"{accessed.strftime('%z')[3:]})"
    )
    style = "font-size:8px;font-family:Helvetica,Arial,sans-serif;color:#333;width:100%;margin:0 10mm;"
    header = (
        f'<div style="{style}display:flex;justify-content:space-between;">'
        f'<span>{stamp}</span><span class="title" style="max-width:60%;overflow:hidden;'
        'white-space:nowrap;text-overflow:ellipsis;"></span></div>'
    )
    footer = (
        f'<div style="{style}display:flex;justify-content:space-between;">'
        '<span class="url" style="max-width:85%;word-break:break-all;"></span>'
        '<span>page <span class="pageNumber"></span> of <span class="totalPages"></span></span></div>'
    )
    return header, footer


def snapshot(args: argparse.Namespace, target: Path, accessed: dt.datetime) -> tuple[dict, str]:
    profile = Path(tempfile.mkdtemp(prefix="save-web-pdf-"))
    user_agent = (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) "
        f"Chrome/{chrome_major(args.chrome)}.0.0.0 Safari/537.36"
    )
    cmd = [
        str(args.chrome), "--headless=new", "--remote-debugging-pipe", "--disable-gpu",
        "--no-first-run", "--no-default-browser-check", "--disable-extensions",
        "--disable-background-networking", "--disable-component-update", "--disable-sync",
        "--hide-scrollbars", "--lang=en-GB", "--window-size=1280,1800",
        f"--user-data-dir={profile}", f"--user-agent={user_agent}", "about:blank",
    ]
    devtools = DevTools(cmd)
    info: dict = {}
    try:
        target_id = devtools.call("Target.createTarget", {"url": "about:blank"})["targetId"]
        session = devtools.call("Target.attachToTarget", {"targetId": target_id, "flatten": True})["sessionId"]
        devtools.call("Page.enable", session=session)
        devtools.call("Emulation.setEmulatedMedia", {"media": "print"}, session=session)
        nav = devtools.call("Page.navigate", {"url": args.url}, session=session, timeout=args.timeout)
        if nav.get("errorText"):
            raise RuntimeError(f"navigation failed: {nav['errorText']}")
        info["load_event"] = devtools.wait_event("Page.loadEventFired", timeout=args.timeout)
        time.sleep(args.delay / 1000)
        page = devtools.call("Runtime.evaluate", {
            "expression": "JSON.stringify({title: document.title, url: location.href})", "returnByValue": True,
        }, session=session)
        info.update(json.loads(page.get("result", {}).get("value") or "{}"))
        if args.fetch_pdf:
            # Download the original PDF inside the page, so cookies and any
            # JavaScript challenge the publisher set on the landing page apply.
            script = (
                "(async () => { const r = await fetch(%s, {credentials: 'include'});"
                " const b = new Uint8Array(await r.arrayBuffer()); let s = '';"
                " for (let i = 0; i < b.length; i += 0x8000) s += String.fromCharCode.apply(null, b.subarray(i, i + 0x8000));"
                " return JSON.stringify({status: r.status, type: r.headers.get('content-type'), url: r.url,"
                " data: btoa(s)}); })()" % json.dumps(args.fetch_pdf)
            )
            reply = devtools.call("Runtime.evaluate", {"expression": script, "awaitPromise": True,
                                                       "returnByValue": True}, session=session, timeout=args.timeout)
            if "exceptionDetails" in reply:
                raise RuntimeError(f"fetch failed: {reply['exceptionDetails'].get('text')}")
            got = json.loads(reply["result"]["value"])
            data = base64.b64decode(got["data"])
            if got["status"] != 200 or not data.startswith(b"%PDF"):
                raise RuntimeError(f"not a PDF (HTTP {got['status']}, {got['type']}); "
                                   "the file may need institutional access")
            info["fetched_from"] = got["url"]
            target.write_bytes(data)
            return info, ""
        if not args.keep_banners:
            # Known consent platforms first, then any fixed/sticky overlay or
            # dialog whose text is about cookies or consent.
            script = (
                "(() => { const sel = %s; let n = 0;"
                " for (const s of sel) { for (const el of document.querySelectorAll(s)) { el.remove(); n++; } }"
                " const re = /cookie|consent/i;"
                " for (const el of Array.from(document.querySelectorAll('body *'))) {"
                "   if (!el.isConnected) continue;"
                "   const st = getComputedStyle(el);"
                "   const overlay = st.position === 'fixed' || st.position === 'sticky'"
                "     || el.getAttribute('role') === 'dialog' || el.getAttribute('aria-modal') === 'true';"
                "   const text = el.innerText || '';"
                "   if (overlay && re.test(text) && text.length < 4000) { el.remove(); n++; } }"
                " for (const el of [document.documentElement, document.body]) { if (el) {"
                " el.style.setProperty('overflow', 'visible', 'important');"
                " el.style.setProperty('position', 'static', 'important'); } }"
                " return n; })()" % json.dumps(CONSENT_SELECTORS)
            )
            removed = devtools.call("Runtime.evaluate", {"expression": script, "returnByValue": True},
                                    session=session)
            info["banners_removed"] = removed.get("result", {}).get("value", 0)
            page = devtools.call("Runtime.evaluate", {
                "expression": "document.title", "returnByValue": True}, session=session)
            info["title"] = page.get("result", {}).get("value") or info.get("title", "")
        # Print-layout repair. (1) Fixed elements repeat on every printed page: off-screen or invisible ones
        # (e.g. closed navigation drawers parked below the viewport) are hidden, visible ones (headers) are
        # pinned once to the top of the document. (2) Some sites (e.g. Next.js layouts) put the whole page in a
        # fixed-height scroll container, which prints as one truncated page: every non-fixed scroll container
        # grows to its full content.
        repair = (
            "(() => { const vw = innerWidth, vh = innerHeight; let hidden = 0, pinned = 0, grown = 0;"
            " for (const el of Array.from(document.querySelectorAll('body *'))) {"
            "   const st = getComputedStyle(el); if (st.position !== 'fixed') continue;"
            "   const r = el.getBoundingClientRect();"
            "   if (r.bottom <= 0 || r.top >= vh || r.right <= 0 || r.left >= vw || st.visibility === 'hidden'"
            "       || parseFloat(st.opacity) === 0) { el.style.setProperty('display', 'none', 'important'); hidden++; }"
            "   else { el.style.setProperty('position', 'absolute', 'important'); pinned++; } }"
            " for (const el of Array.from(document.querySelectorAll('body *'))) {"
            "   const st = getComputedStyle(el);"
            "   if (st.position === 'fixed' || st.position === 'sticky' || st.display === 'none') continue;"
            "   if (/(auto|scroll)/.test(st.overflowY) && el.scrollHeight > el.clientHeight + 20) {"
            "     el.style.setProperty('height', 'auto', 'important');"
            "     el.style.setProperty('max-height', 'none', 'important');"
            "     el.style.setProperty('overflow', 'visible', 'important'); grown++; } }"
            " return JSON.stringify({hidden, pinned, grown}); })()"
        )
        fixed = devtools.call("Runtime.evaluate", {"expression": repair, "returnByValue": True}, session=session)
        counts = json.loads(fixed.get("result", {}).get("value") or "{}")
        info["fixed_hidden"] = counts.get("hidden", 0)
        info["fixed_pinned"] = counts.get("pinned", 0)
        info["scroll_containers_expanded"] = counts.get("grown", 0)
        time.sleep(0.5)
        header, footer = header_footer(accessed)
        pdf = devtools.call("Page.printToPDF", {
            "displayHeaderFooter": not args.no_header_footer,
            "headerTemplate": header, "footerTemplate": footer,
            "printBackground": True, "paperWidth": 8.27, "paperHeight": 11.69,
            "marginTop": 0.6, "marginBottom": 0.6, "marginLeft": 0.4, "marginRight": 0.4,
        }, session=session, timeout=args.timeout)
        target.write_bytes(base64.b64decode(pdf["data"]))
    finally:
        log = devtools.close()
        shutil.rmtree(profile, ignore_errors=True)
    return info, log


def pdf_summary(pdf: Path) -> dict:
    info = subprocess.run(["pdfinfo", str(pdf)], capture_output=True, text=True).stdout
    pages = re.search(r"^Pages:\s+(\d+)", info, re.M)
    text = subprocess.run(
        ["pdftotext", "-f", "1", "-l", "1", "-layout", str(pdf), "-"], capture_output=True, text=True
    ).stdout
    lines = [" ".join(line.split()) for line in text.splitlines() if line.strip()]
    return {"pages": int(pages.group(1)) if pages else 0, "first_lines": lines[:10]}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("url", help="page to save (http or https)")
    parser.add_argument("file_name", help="kebab-case PDF name, e.g. organisation-nd-page-title.pdf")
    parser.add_argument("--out-dir", type=Path, default=DEFAULT_OUT_DIR, help="default: 04_references/")
    parser.add_argument("--delay", type=int, default=5000,
                        help="extra render time in milliseconds after the page load event (default 5000)")
    parser.add_argument("--timeout", type=int, default=90, help="timeout in seconds for load and print")
    parser.add_argument("--keep-banners", action="store_true", help="do not hide cookie-consent overlays")
    parser.add_argument("--no-header-footer", action="store_true",
                        help="omit the header/footer (NOT recommended: it records URL and accessed date)")
    parser.add_argument("--fetch-pdf", metavar="PDF_URL",
                        help="instead of printing URL, open URL (the article landing page) and save the "
                             "publisher's own PDF from PDF_URL (for open-access PDFs behind a browser check)")
    parser.add_argument("--force", action="store_true", help="overwrite an existing file")
    parser.add_argument("--chrome", type=Path, default=CHROME)
    args = parser.parse_args()

    if not re.match(r"^https?://", args.url) or (args.fetch_pdf and not re.match(r"^https?://", args.fetch_pdf)):
        parser.error("URLs must start with http:// or https://")
    if not NAME_RE.match(args.file_name):
        parser.error("file name must be kebab-case and end in .pdf, e.g. organisation-nd-page-title.pdf")
    if not args.chrome.exists():
        parser.error(f"Chrome not found at {args.chrome}")
    out_dir = args.out_dir.resolve()
    if not out_dir.is_dir():
        parser.error(f"output folder does not exist: {out_dir}")
    target = out_dir / args.file_name
    if target.exists() and not args.force:
        parser.error(f"{target.name} already exists (use --force to overwrite)")

    accessed = dt.datetime.now().astimezone()
    try:
        info, _log = snapshot(args, target, accessed)
    except Exception as exc:  # report and fail cleanly; nothing half-written is kept
        target.unlink(missing_ok=True)
        print(f"ERROR: could not save {args.url}: {exc}", file=sys.stderr)
        return 1

    summary = pdf_summary(target)
    try:
        shown = target.relative_to(WS)
    except ValueError:
        shown = target
    day = accessed.date()
    print(f"Saved: {shown} ({summary['pages']} pages, {target.stat().st_size:,} bytes)")
    print(f"Page title: {info.get('title', '')}")
    if info.get("url") and info["url"] != args.url:
        print(f"NOTE: final URL after redirects: {info['url']}")
    if not info.get("load_event"):
        print("WARNING: page load event not seen before timeout; check the PDF is complete.", file=sys.stderr)
    if args.fetch_pdf:
        print(f"Publisher PDF fetched from: {info.get('fetched_from', args.fetch_pdf)}")
        print(f"Retrieved on (ISO): {day.isoformat()}")
    else:
        print(f"Cookie overlays hidden: {info.get('banners_removed', 0)}")
        print(f"Print repairs: {info.get('fixed_hidden', 0)} off-screen fixed elements hidden, "
              f"{info.get('fixed_pinned', 0)} visible fixed elements pinned, "
              f"{info.get('scroll_containers_expanded', 0)} scroll containers expanded")
        print(f"Accessed (ISO, for references.json): {day.isoformat()}")
        print(f"Accessed (Cite Them Right):          (Accessed: {ctr_date(day)})")
    print("First lines of page 1 (check it rendered the content, not a block or error page):")
    for line in summary["first_lines"]:
        print(f"  | {line[:110]}")
    print("Registry fragment:")
    if args.fetch_pdf:
        fragment = {"file": target.name, "retrieval": {
            "method": "open-access", "from": info.get("fetched_from", args.fetch_pdf), "date": day.isoformat()}}
    else:
        fragment = {"url": args.url, "accessed": day.isoformat(), "file": target.name, "retrieval": {
            "method": "web-snapshot", "from": info.get("url") or args.url, "date": day.isoformat()}}
    print(json.dumps(fragment, indent=2))
    if summary["pages"] == 0:
        print("WARNING: PDF has no pages; inspect it before registering.", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
