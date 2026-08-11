(function () {
  function track(event, data) {
    try { window.umami && window.umami.track(event, data || {}); } catch (e) {}
  }

  // ── 1. Scroll depth — 25/50/75/100% per page ─────────────────────────
  const reached = new Set();
  function onScroll() {
    const el = document.documentElement;
    const scrolled = el.scrollTop || document.body.scrollTop;
    const total = el.scrollHeight - el.clientHeight;
    if (total <= 0) return;
    const pct = Math.round(scrolled / total * 100);
    [25, 50, 75, 100].forEach(function (mark) {
      if (pct >= mark && !reached.has(mark)) {
        reached.add(mark);
        track("scroll-depth", { pct: mark, page: location.pathname });
      }
    });
    if (reached.size === 4) window.removeEventListener("scroll", onScroll);
  }
  window.addEventListener("scroll", onScroll, { passive: true });

  // ── 2. Nav clicks — explorer and TOC ─────────────────────────────────
  document.addEventListener("click", function (e) {
    const navLink = e.target.closest(".site-nav a");
    if (navLink) {
      track("nav-explorer", { to: navLink.getAttribute("href") });
    }
    const tocLink = e.target.closest(".toc a");
    if (tocLink) {
      track("nav-toc", { section: tocLink.textContent.trim().slice(0, 40) });
    }
  });

  // ── 3. External link clicks ───────────────────────────────────────────
  document.addEventListener("click", function (e) {
    const a = e.target.closest("article a[href^='http']");
    if (a && !a.href.includes("wiktionary")) {
      track("external-link", { url: a.href.slice(0, 80) });
    }
  });

  // ── 4. Time on page — fire when the page is hidden/closed ────────────
  //  visibilitychange + pagehide are reliable on Chrome/Chromebook where
  //  beforeunload is not (bfcache, backgrounded tabs).
  //  Each hidden/close reports the time since the last report, so a reader
  //  who switches tabs and comes back is still measured for the rest of
  //  the visit instead of being counted once and then dropped.
  let lastMark = Date.now();
  function sendTime() {
    const secs = Math.round((Date.now() - lastMark) / 1000);
    lastMark = Date.now();
    if (secs > 5) track("time-on-page", { secs: secs, page: location.pathname });
  }
  document.addEventListener("visibilitychange", function () {
    if (document.visibilityState === "hidden") sendTime();
    else lastMark = Date.now();
  });
  window.addEventListener("pagehide", sendTime);

  // ── 5. Search ─────────────────────────────────────────────────────────
  const searchInput = document.getElementById("search-input");
  if (searchInput) {
    let searchTimer;
    searchInput.addEventListener("input", function () {
      clearTimeout(searchTimer);
      searchTimer = setTimeout(function () {
        const q = searchInput.value.trim();
        if (q.length > 2) track("search", { q: q });
      }, 600);
    });
  }
})();
