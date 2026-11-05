(function () {
  const input = document.getElementById("search-input");
  const results = document.getElementById("search-results");
  if (!input || !results) return;

  let index = null;
  let loading = null;

  // The index holds every page in full, so it is only fetched once the
  // reader actually goes near the search box.
  function loadIndex() {
    if (loading) return loading;
    loading = fetch("/static/search-index.json")
      .then(function (r) { return r.json(); })
      .then(function (data) { index = data; })
      .catch(function () {});
    return loading;
  }

  input.addEventListener("focus", loadIndex);

  input.addEventListener("input", function () {
    if (!index) { loadIndex().then(render); return; }
    render();
  });

  function render() {
    const q = input.value.trim().toLowerCase();
    results.innerHTML = "";
    if (!index || q.length < 2) return;

    const hits = index.filter(function (p) {
      return p.title.toLowerCase().includes(q) || p.text.toLowerCase().includes(q);
    }).slice(0, 10);

    if (hits.length === 0) {
      results.innerHTML = '<li class="search-empty">No results</li>';
      return;
    }

    hits.forEach(function (p) {
      const li = document.createElement("li");
      const a = document.createElement("a");
      a.href = p.href;
      a.textContent = p.title;
      li.appendChild(a);
      results.appendChild(li);
    });
  }

  document.addEventListener("click", function (e) {
    if (!input.contains(e.target) && !results.contains(e.target)) {
      results.innerHTML = "";
    }
  });
})();
