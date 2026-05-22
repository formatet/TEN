import { QuartzComponent, QuartzComponentConstructor } from "./types"

const WiktionaryLookup: QuartzComponent = () => null

WiktionaryLookup.css = `
#wikt-tip {
  position: fixed;
  z-index: 1000;
  background: var(--dark);
  color: var(--light);
  padding: 0.3rem 0.8rem;
  border-radius: 4px;
  font-size: 0.82rem;
  font-family: var(--bodyFont);
  display: none;
  pointer-events: all;
  transform: translateX(-50%);
  white-space: nowrap;
  box-shadow: 0 2px 10px rgba(0,0,0,0.25);
}
#wikt-tip a {
  color: var(--light) !important;
  text-decoration: none !important;
  font-weight: 500;
}
#wikt-tip::after {
  content: '';
  position: absolute;
  top: 100%;
  left: 50%;
  transform: translateX(-50%);
  border: 5px solid transparent;
  border-top-color: var(--dark);
}
`

WiktionaryLookup.afterDOMLoaded = `
(function () {
  if (window._wiktOK) return;
  window._wiktOK = true;

  let justShown = false;

  function hide() {
    const t = document.getElementById("wikt-tip");
    if (t) t.style.display = "none";
  }

  function showTip(word, x, y) {
    const clean = word.toLowerCase().replace(/[^a-z'-]/g, "");
    if (clean.length < 3) return;

    let t = document.getElementById("wikt-tip");
    if (!t) {
      t = document.createElement("div");
      t.id = "wikt-tip";
      document.body.appendChild(t);
    }

    const url = "https://en.wiktionary.org/wiki/" + encodeURIComponent(clean);
    t.innerHTML = '<a href="' + url + '" target="_blank" rel="noopener">' + clean + " — Wiktionary ↗</a>";
    t.style.left = x + "px";
    t.style.top = (y - 38) + "px";
    t.style.display = "block";
    justShown = true;

    t.querySelector("a").onclick = function () {
      try { window.umami && window.umami.track("wiktionary", { word: clean }); } catch(e) {}
    };
  }

  function tryShow() {
    try {
      const sel = window.getSelection();
      if (!sel || sel.rangeCount === 0) return;
      const word = sel.toString().trim();
      if (!word || /\s/.test(word) || word.length < 2 || word.length > 30) return;

      const range = sel.getRangeAt(0);

      // getClientRects() fungerar även på radbrytningar där getBoundingClientRect() ger width=0
      const rects = range.getClientRects();
      let rect = null;
      for (let i = 0; i < rects.length; i++) {
        if (rects[i].width > 0) { rect = rects[i]; break; }
      }
      if (!rect) rect = range.getBoundingClientRect();
      if (!rect || rect.width === 0) return;

      showTip(word, rect.left + rect.width / 2, rect.top);
    } catch(e) {}
  }

  document.addEventListener("mouseup", function() { setTimeout(tryShow, 15); });
  document.addEventListener("touchend", function() { setTimeout(tryShow, 60); });

  document.addEventListener("click", function(e) {
    if (justShown) { justShown = false; return; }
    if (!e.target.closest("#wikt-tip")) hide();
  });

  document.addEventListener("keydown", function(e) {
    if (e.key === "Escape") hide();
  });
})();
`

export default (() => WiktionaryLookup) satisfies QuartzComponentConstructor
