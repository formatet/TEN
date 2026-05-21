import { QuartzComponent, QuartzComponentConstructor } from "./types"

const TENTracking: QuartzComponent = () => null

TENTracking.afterDOMLoaded = `
(function () {
  function track(event, data) {
    try { window.umami && window.umami.track(event, data || {}); } catch(e) {}
  }

  // ── 1. Scrolldjup — spåra 25/50/75/100% per sida ─────────────────────────
  const reached = new Set();
  function onScroll() {
    const el = document.documentElement;
    const pct = Math.round(el.scrollTop / (el.scrollHeight - el.clientHeight) * 100);
    [25, 50, 75, 100].forEach(function(mark) {
      if (pct >= mark && !reached.has(mark)) {
        reached.add(mark);
        track("scroll-depth", { pct: mark, page: location.pathname });
      }
    });
  }
  window.addEventListener("scroll", onScroll, { passive: true });

  // ── 2. Sök — spåra när sökning görs ────────────────────────────────────
  document.addEventListener("nav", function() {
    reached.clear(); // nollställ scroll per sida
    const searchBar = document.querySelector(".search-bar");
    if (searchBar && !searchBar._tenTracked) {
      searchBar._tenTracked = true;
      searchBar.addEventListener("input", function() {
        const q = searchBar.value.trim();
        if (q.length > 2) track("search", { q: q });
      });
    }
  });

  // ── 3. Explorer-klick — vilka sidor navigeras till via sidomenyn ─────────
  document.addEventListener("click", function(e) {
    const link = e.target.closest(".explorer-content a");
    if (link) {
      track("nav-explorer", { to: link.dataset.for || link.href });
    }
    // ToC-klick
    const toc = e.target.closest(".toc-content a");
    if (toc) {
      track("nav-toc", { section: toc.textContent.trim().slice(0, 40) });
    }
  });

  // ── 4. Externt länkklick ────────────────────────────────────────────────
  document.addEventListener("click", function(e) {
    const a = e.target.closest("article a[href^='http']");
    if (a && !a.href.includes("wiktionary")) {
      track("external-link", { url: a.href.slice(0, 80) });
    }
  });

  // ── 5. Tid på sida — fire event när sidan lämnas ────────────────────────
  let startTime = Date.now();
  document.addEventListener("prenav", function() {
    const secs = Math.round((Date.now() - startTime) / 1000);
    if (secs > 5) track("time-on-page", { secs: secs, page: location.pathname });
    startTime = Date.now();
  });
  window.addEventListener("beforeunload", function() {
    const secs = Math.round((Date.now() - startTime) / 1000);
    if (secs > 5) track("time-on-page", { secs: secs, page: location.pathname });
  });
})();
`

export default (() => TENTracking) satisfies QuartzComponentConstructor
