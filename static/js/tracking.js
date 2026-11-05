(function () {
  function track(event, data) {
    try { window.umami && window.umami.track(event, data || {}); } catch (e) {}
  }

  // ── 1. Reading depth ─────────────────────────────────────────────────
  //  Long pages (chapters): which sections the reader reached. A section
  //  counts as reached when its heading passes into the top half of the
  //  screen. Page-percent says nothing on a chapter where one part fills
  //  a third of the page.
  //  Short pages (fewer than 3 headings): 25/50/75/100% as before.
  const headings = document.querySelectorAll("article h2, article h3");
  if (headings.length >= 3 && "IntersectionObserver" in window) {
    //  The heading id is sent, not its text: Kipling, Buck and Steinbeck
    //  each have an "A — Context", and only the ids tell them apart.
    const io = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (!entry.isIntersecting) return;
        io.unobserve(entry.target);
        const name = entry.target.id || entry.target.textContent.trim().slice(0, 40);
        track("section-view", { section: name, page: location.pathname });
      });
    }, { rootMargin: "0px 0px -50% 0px" });
    headings.forEach(function (h) { io.observe(h); });
  } else {
    const reached = new Set();
    const onScroll = function () {
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
    };
    window.addEventListener("scroll", onScroll, { passive: true });
  }

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

  // ── 3b. Internal link clicks — chapter → archive, chapter → gallery ──
  document.addEventListener("click", function (e) {
    const a = e.target.closest("article a[href^='/']");
    if (a) {
      track("internal-link", { from: location.pathname, to: a.getAttribute("href") });
    }
  });

  // ── 4. Time on page — fire when the page is hidden/closed ────────────
  //  visibilitychange + pagehide are reliable on Chrome/Chromebook where
  //  beforeunload is not (bfcache, backgrounded tabs).
  //  Each hidden/close reports the time since the last report, so a reader
  //  who switches tabs and comes back is still measured for the rest of
  //  the visit instead of being counted once and then dropped.
  //  A closed Chromebook lid does not always fire "hidden", so a tab left
  //  open could report days. Timers stop while the device sleeps: a gap of
  //  more than two minutes between ticks means sleep, and the time up to
  //  the last tick is reported then. No single report exceeds two hours.
  const MAX_SECS = 2 * 3600;
  let lastMark = Date.now();
  let lastTick = lastMark;
  function sendTime(end) {
    const secs = Math.min(Math.round(((end || Date.now()) - lastMark) / 1000), MAX_SECS);
    lastMark = Date.now();
    if (secs > 5) track("time-on-page", { secs: secs, page: location.pathname });
  }
  setInterval(function () {
    const now = Date.now();
    if (document.visibilityState === "visible" && now - lastTick > 120000) sendTime(lastTick);
    lastTick = now;
  }, 30000);
  document.addEventListener("visibilitychange", function () {
    if (document.visibilityState === "hidden") sendTime();
    else lastMark = lastTick = Date.now();
  });
  window.addEventListener("pagehide", function () { sendTime(); });

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
