// Save a web page as a dated PDF snapshot from the student's Comet browser (headed), for sites that must be
// opened in Comet (D-025: every Green SM page). Parent agent only: it drives a dedicated tab in the student's
// real browser through the omp `browser` tool, attached via 06_workflow/scripts/comet_cdp_shim.py.
//
// Usage inside the parent agent's JavaScript eval (Bun), after starting the shim as a named service:
//   const { openCometTab, cometSave } = await import('<workspace>/06_workflow/scripts/comet_capture.mjs');
//   await openCometTab(browser);                       // attaches tab "gsm-comet" (student may need to click Allow)
//   const r = await cometSave(browser, URL, '/tmp/x.pdf', { delay: 6000 });
// Then check pages, words and one rendered middle page, move the file into 04_references/ with its final name,
// and register it with retrieval.browser = "Comet (headed, D-025)".
//
// The print repairs match save_web_pdf.py: consent overlays are hidden (never accepted), off-screen fixed elements
// are hidden, visible fixed elements are pinned once, fixed-height scroll containers are expanded. Every page carries
// "Accessed: <date, time, UTC offset> [Comet]", the page title, the URL and "page N of M".

export const CONSENT_SELECTORS = [
  '#onetrust-consent-sdk', '#onetrust-banner-sdk', '.onetrust-pc-dark-filter', '#CybotCookiebotDialog',
  '#CybotCookiebotDialogBodyUnderlay', '#usercentrics-root', '#didomi-host', '.qc-cmp2-container', '#qc-cmp2-ui',
  '#truste-consent-track', '#consent_blackbar', '.truste_box_overlay', '.truste_overlay', '.osano-cm-window',
  '.cky-consent-container', '.cky-overlay', '.cky-modal', '#cmplz-cookiebanner-container', '.cmplz-cookiebanner',
  '#ccc', '#ccc-overlay', '.cc-window', '.cc-banner', '.cc-grower', '#iubenda-cs-banner', '.klaro',
  '#cookie-law-info-bar', '#cookie-notice', '#cookieConsent', '#cookie-consent', '.cookie-consent', '.cookie-banner',
  '#cookie-banner', '.cookies-banner', '#gdpr-cookie-notice', '.gdpr-cookie-notice', '#termly-code-snippet-support',
  "[aria-label='cookieconsent']", "[id^='sp_message_container']",
];

export const TAB_NAME = 'gsm-comet';

export async function openCometTab(browser, { cdpUrl = 'http://127.0.0.1:9333', url = 'about:blank' } = {}) {
  return browser.open({ name: TAB_NAME, app: { cdp_url: cdpUrl }, url, persist: true, timeout: 120 });
}

export async function cometSave(browser, url, outPath, { delay = 6000, waitUntil = 'domcontentloaded' } = {}) {
  const tab = browser.tab(TAB_NAME);
  await tab.goto(url, { waitUntil, timeout: 120000 });
  return tab.run(async ({ page }, delayMs, out, selectors) => {
    await new Promise((r) => setTimeout(r, delayMs));
    await page.emulateMediaType('print');
    const counts = await page.evaluate((sel) => {
      let banners = 0, hidden = 0, pinned = 0, grown = 0;
      for (const s of sel) for (const el of document.querySelectorAll(s)) { el.style.setProperty('display', 'none', 'important'); banners++; }
      const re = /cookie|consent/i;
      for (const el of Array.from(document.querySelectorAll('body *'))) {
        const st = getComputedStyle(el);
        const overlay = st.position === 'fixed' || st.position === 'sticky' || el.getAttribute('role') === 'dialog'
          || el.getAttribute('aria-modal') === 'true';
        const text = el.innerText || '';
        if (overlay && re.test(text) && text.length < 4000 && st.display !== 'none') { el.style.setProperty('display', 'none', 'important'); banners++; }
      }
      for (const el of [document.documentElement, document.body]) {
        if (el) { el.style.setProperty('overflow', 'visible', 'important'); el.style.setProperty('position', 'static', 'important'); }
      }
      const vw = innerWidth, vh = innerHeight;
      for (const el of Array.from(document.querySelectorAll('body *'))) {
        const st = getComputedStyle(el);
        if (st.position !== 'fixed' || st.display === 'none') continue;
        const r = el.getBoundingClientRect();
        if (r.bottom <= 0 || r.top >= vh || r.right <= 0 || r.left >= vw || st.visibility === 'hidden' || parseFloat(st.opacity) === 0) {
          el.style.setProperty('display', 'none', 'important'); hidden++;
        } else { el.style.setProperty('position', 'absolute', 'important'); pinned++; }
      }
      for (const el of Array.from(document.querySelectorAll('body *'))) {
        const st = getComputedStyle(el);
        if (st.position === 'fixed' || st.position === 'sticky' || st.display === 'none') continue;
        if (/(auto|scroll)/.test(st.overflowY) && el.scrollHeight > el.clientHeight + 20) {
          el.style.setProperty('height', 'auto', 'important');
          el.style.setProperty('max-height', 'none', 'important');
          el.style.setProperty('overflow', 'visible', 'important'); grown++;
        }
      }
      return { banners, hidden, pinned, grown };
    }, selectors);
    await new Promise((r) => setTimeout(r, 500));
    const now = new Date();
    const months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'];
    const off = -now.getTimezoneOffset();
    const offset = `${off >= 0 ? '+' : '-'}${String(Math.floor(Math.abs(off) / 60)).padStart(2, '0')}:${String(Math.abs(off) % 60).padStart(2, '0')}`;
    const stamp = `Accessed: ${now.getDate()} ${months[now.getMonth()]} ${now.getFullYear()}, `
      + `${String(now.getHours()).padStart(2, '0')}:${String(now.getMinutes()).padStart(2, '0')} (UTC${offset}) [Comet]`;
    const style = 'font-size:8px;font-family:Helvetica,Arial,sans-serif;color:#333;width:100%;margin:0 10mm;';
    const headerTemplate = `<div style="${style}display:flex;justify-content:space-between;"><span>${stamp}</span>`
      + '<span class="title" style="max-width:60%;overflow:hidden;white-space:nowrap;text-overflow:ellipsis;"></span></div>';
    const footerTemplate = `<div style="${style}display:flex;justify-content:space-between;">`
      + '<span class="url" style="max-width:85%;word-break:break-all;"></span>'
      + '<span>page <span class="pageNumber"></span> of <span class="totalPages"></span></span></div>';
    const pdf = await page.pdf({
      displayHeaderFooter: true, headerTemplate, footerTemplate, printBackground: true,
      width: '8.27in', height: '11.69in', margin: { top: '0.6in', bottom: '0.6in', left: '0.4in', right: '0.4in' },
      timeout: 120000,
    });
    await Bun.write(out, pdf);
    await page.emulateMediaType(null);
    const iso = `${now.getFullYear()}-${String(now.getMonth() + 1).padStart(2, '0')}-${String(now.getDate()).padStart(2, '0')}`;
    return { counts, title: await page.title(), url: page.url(), bytes: pdf.length, accessed: iso, stamp };
  }, { args: [delay, outPath, CONSENT_SELECTORS], timeout: 200000 });
}
