(function () {
  if (window._wiktOK) return;
  window._wiktOK = true;

  let justShown = false;

  function hide() {
    const t = document.getElementById("wikt-tip");
    if (t) t.style.display = "none";
  }

  function showTip(word, x, y) {
    // Keep every letter, not just a-z — stripping diacritics turned
    // "Glück" into "glck" and sent the reader to a 404.
    const clean = word.toLowerCase().replace(/[^\p{L}'-]/gu, "");
    if (clean.length < 3) return;

    let t = document.getElementById("wikt-tip");
    if (!t) {
      t = document.createElement("div");
      t.id = "wikt-tip";
      document.body.appendChild(t);
    }

    const url = "https://en.wiktionary.org/wiki/" + encodeURIComponent(clean);
    t.innerHTML = '<a href="' + url + '" target="_blank" rel="noopener">' + clean + " — Wiktionary ↗</a>";
    t.style.display = "block";

    // Clamp horizontally so the tooltip never clips off the screen edge
    // (the tip is centred on x via translateX(-50%)).
    const halfW = t.offsetWidth / 2;
    const margin = 8;
    const clampedX = Math.max(halfW + margin, Math.min(x, window.innerWidth - halfW - margin));
    t.style.left = clampedX + "px";
    t.style.top = (y - 38) + "px";
    justShown = true;

    t.querySelector("a").onclick = function () {
      try { window.umami && window.umami.track("wiktionary", { word: clean }); } catch (e) {}
    };
  }

  function tryShow() {
    try {
      const sel = window.getSelection();
      if (!sel || sel.rangeCount === 0) return;
      const word = sel.toString().trim();
      if (!word || /\s/.test(word) || word.length < 2 || word.length > 30) return;

      const range = sel.getRangeAt(0);
      const rects = range.getClientRects();
      let rect = null;
      for (let i = 0; i < rects.length; i++) {
        if (rects[i].width > 0) { rect = rects[i]; break; }
      }
      if (!rect) rect = range.getBoundingClientRect();
      if (!rect || rect.width === 0) return;

      showTip(word, rect.left + rect.width / 2, rect.top);
    } catch (e) {}
  }

  document.addEventListener("mouseup", function () { setTimeout(tryShow, 15); });
  document.addEventListener("touchend", function () { setTimeout(tryShow, 60); });

  document.addEventListener("click", function (e) {
    if (justShown) { justShown = false; return; }
    if (!e.target.closest("#wikt-tip")) hide();
  });

  document.addEventListener("keydown", function (e) {
    if (e.key === "Escape") hide();
  });
})();
