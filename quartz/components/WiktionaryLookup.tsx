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
  let tip = null;
  let hideTimer = null;
  let justShown = false;

  function getTip() {
    if (!tip) {
      tip = document.createElement("div");
      tip.id = "wikt-tip";
      document.body.appendChild(tip);
    }
    return tip;
  }

  function show(word, x, y) {
    const clean = word.toLowerCase().replace(/[^a-z'-]/g, "");
    if (clean.length < 3) return;
    clearTimeout(hideTimer);
    const url = "https://en.wiktionary.org/wiki/" + encodeURIComponent(clean);
    const t = getTip();
    t.innerHTML =
      '<a href="' + url + '" target="_blank" rel="noopener">' +
      word + " — Wiktionary ↗</a>";
    t.style.left = x + "px";
    t.style.top = (y - 48) + "px";
    t.style.display = "block";
    justShown = true;
    setTimeout(function() { justShown = false; }, 400);
    const link = t.querySelector("a");
    link.onclick = function () {
      try { window.umami && window.umami.track("wiktionary", { word: clean }); }
      catch (e) {}
    };
  }

  function hide() {
    if (tip) tip.style.display = "none";
    justShown = false;
  }

  function onUp(e) {
    clearTimeout(hideTimer);
    const sel = window.getSelection();
    const word = sel && sel.toString().trim();
    if (!word || /\\s/.test(word) || word.length < 3 || word.length > 35) {
      hideTimer = setTimeout(hide, 300);
      return;
    }
    const anchor = sel.anchorNode;
    const el = anchor && (anchor.nodeType === 3 ? anchor.parentElement : anchor);
    if (!el || !el.closest("article")) { hideTimer = setTimeout(hide, 300); return; }
    try {
      const r = sel.getRangeAt(0).getBoundingClientRect();
      show(word, r.left + r.width / 2 + window.scrollX, r.top + window.scrollY);
    } catch (_) {}
  }

  document.addEventListener("mouseup", onUp);
  document.addEventListener("touchend", onUp);

  document.addEventListener("mousedown", function (e) {
    if (justShown) return;
    if (!e.target.closest("#wikt-tip")) {
      hideTimer = setTimeout(hide, 100);
    }
  });

  document.addEventListener("keydown", function (e) {
    if (e.key === "Escape") hide();
  });
  document.addEventListener("nav", hide);
})();
`

export default (() => WiktionaryLookup) satisfies QuartzComponentConstructor
