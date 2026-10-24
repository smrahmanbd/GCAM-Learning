/* Question bank: filter, reveal, self-mark (saved in localStorage), flashcards. Data: window.QBANK, window.QBMETA */
(function () {
  "use strict";
  const Q = window.QBANK || [], META = window.QBMETA || {};
  const root = document.querySelector(".qb"); if (!root) return;
  const $ = (s) => root.querySelector(s), $$ = (s) => [...root.querySelectorAll(s)];
  const esc = (s) => String(s).replace(/[&<>"]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]));
  const KEY = "gcam-qbank-v1";
  const hash = (s) => { let h = 5381; for (let i = 0; i < s.length; i++) h = ((h << 5) + h + s.charCodeAt(i)) | 0; return (h >>> 0).toString(36); };
  Q.forEach((d) => (d.id = d.m + "|" + hash(d.q)));
  let marks = {};
  try { marks = JSON.parse(localStorage.getItem(KEY) || "{}") || {}; } catch (e) { marks = {}; }
  const save = () => { try { localStorage.setItem(KEY, JSON.stringify(marks)); } catch (e) { /* storage unavailable */ } };

  const params = new URLSearchParams(location.search);
  const st = { go: 0, module: "", search: "", status: "all", kinds: new Set(["Recall", "Explain", "Calculate", "Apply"]), view: "list", order: null, card: 0, revealAll: false };
  if (params.get("m")) { st.module = params.get("m"); st.go = +st.module.split(".")[0]; }
  else if (params.get("go")) st.go = +params.get("go") || 0;

  const modSel = $(".qb-module"), search = $(".qb-search"), status = $(".qb-status");
  modSel.value = st.module;

  function filtered() {
    const s = st.search.trim().toLowerCase();
    let list = Q.filter((d) => (!st.go || d.g === st.go) && (!st.module || d.m === st.module) && st.kinds.has(d.k)
      && (!s || (d.q + " " + d.a + " " + (META.titles[d.m] || "")).toLowerCase().includes(s))
      && (st.status === "all" || (st.status === "new" ? !marks[d.id] : marks[d.id] === st.status)));
    if (st.order) { const pos = new Map(st.order.map((i, j) => [i, j])); list = list.slice().sort((a, b) => pos.get(a.i) - pos.get(b.i)); }
    return list;
  }

  function markBtns(d) {
    const m = marks[d.id];
    return `<div class="qb-mark" role="group" aria-label="How did you do?"><button class="btn quiet qb-known" type="button" aria-pressed="${m === "known"}" data-id="${d.id}">I knew it</button><button class="btn quiet qb-review" type="button" aria-pressed="${m === "review"}" data-id="${d.id}">Review again</button></div>`;
  }
  function tag(d) {
    const slug = META.slugs[d.m];
    return `<p class="qb-meta"><span class="golevel">Go ${d.g}</span> <a href="modules/${slug}.html">Module ${d.m} · ${esc(META.titles[d.m])}</a> <span class="qb-k qb-k-${d.k.toLowerCase()}">${d.k}</span></p>`;
  }
  function itemHtml(d, n) {
    const open = st.revealAll ? "" : " hidden";
    return `<article class="qb-item ${marks[d.id] ? "is-" + marks[d.id] : ""}" data-id="${d.id}">${tag(d)}
<h3><span class="qb-n">${n}.</span> ${esc(d.q)}</h3>
<div class="qb-actions"><button class="btn qb-show" type="button" aria-expanded="${st.revealAll}">${st.revealAll ? "Hide answer" : "Show answer"}</button><button class="btn quiet qb-write" type="button">Write my answer first</button></div>
<textarea class="qb-draft" rows="3" hidden aria-label="Your answer (not saved)" placeholder="Your answer, in your own words (not saved)"></textarea>
<div class="qb-answer"${open}><p><b>Model answer.</b> ${esc(d.a)}</p>${markBtns(d)}</div></article>`;
  }

  function renderList(list) {
    const box = $(".qb-list"); let html = "", last = "";
    list.forEach((d, j) => {
      if (!st.order && d.m !== last) { html += `<h2 class="qb-mod">Module ${d.m}: ${esc(META.titles[d.m])}</h2>`; last = d.m; }
      html += itemHtml(d, j + 1);
    });
    box.innerHTML = html || `<p class="muted">No questions match these filters.</p>`;
  }

  function renderCards(list) {
    const box = $(".qb-cards");
    if (!list.length) { box.innerHTML = `<p class="muted">No questions match these filters.</p>`; return; }
    st.card = Math.max(0, Math.min(list.length - 1, st.card));
    const d = list[st.card];
    box.innerHTML = `<div class="qb-card" tabindex="0" data-id="${d.id}">${tag(d)}<p class="qb-count muted small">Card ${st.card + 1} of ${list.length}</p>
<h3 class="qb-front">${esc(d.q)}</h3>
<div class="qb-answer" hidden><p><b>Model answer.</b> ${esc(d.a)}</p>${markBtns(d)}</div>
<div class="btnrow"><button class="btn quiet qb-prev" type="button">Previous</button><button class="btn qb-flip" type="button">Show answer</button><button class="btn quiet qb-next" type="button">Next</button></div>
<p class="muted small">Keys: Space to flip, arrows to move, 1 = I knew it, 2 = Review again.</p></div>`;
  }

  function summary(list) {
    const known = list.filter((d) => marks[d.id] === "known").length, rev = list.filter((d) => marks[d.id] === "review").length;
    $(".qb-summary").textContent = `${list.length} question${list.length === 1 ? "" : "s"} shown · ${known} marked 'I knew it' · ${rev} to review · ${list.length - known - rev} not yet marked`;
    const pc = (x) => (list.length ? (100 * x) / list.length : 0) + "%";
    $(".qb-bar-known").style.width = pc(known); $(".qb-bar-review").style.width = pc(rev);
  }

  function render() {
    $$(".qb-go").forEach((b) => b.setAttribute("aria-pressed", +b.dataset.go === st.go));
    [...modSel.options].forEach((o) => (o.hidden = !!o.value && !!st.go && +o.dataset.go !== st.go));
    $$(".qb-view").forEach((b) => b.setAttribute("aria-pressed", b.dataset.view === st.view));
    $(".qb-list").hidden = st.view !== "list"; $(".qb-cards").hidden = st.view !== "cards";
    $(".qb-expand").hidden = st.view !== "list";
    $(".qb-expand").textContent = st.revealAll ? "Hide all answers" : "Reveal all answers";
    const list = filtered();
    if (st.view === "list") renderList(list); else renderCards(list);
    summary(list);
    const u = new URL(location.href); u.search = st.module ? "?m=" + st.module : st.go ? "?go=" + st.go : "";
    history.replaceState(null, "", u);
  }

  function setMark(id, val) {
    marks[id] = marks[id] === val ? undefined : val; if (!marks[id]) delete marks[id];
    save();
    root.querySelectorAll(`[data-id="${CSS.escape(id)}"]`).forEach((el) => {
      if (el.classList.contains("qb-item")) { el.classList.remove("is-known", "is-review"); if (marks[id]) el.classList.add("is-" + marks[id]); }
    });
    root.querySelectorAll(`.qb-known[data-id="${CSS.escape(id)}"]`).forEach((b) => b.setAttribute("aria-pressed", marks[id] === "known"));
    root.querySelectorAll(`.qb-review[data-id="${CSS.escape(id)}"]`).forEach((b) => b.setAttribute("aria-pressed", marks[id] === "review"));
    summary(filtered());
  }

  root.addEventListener("click", (e) => {
    const t = e.target.closest("button"); if (!t) return;
    if (t.classList.contains("qb-go")) { st.go = +t.dataset.go; if (st.module && st.go && +st.module.split(".")[0] !== st.go) { st.module = ""; modSel.value = ""; } st.card = 0; render(); }
    else if (t.classList.contains("qb-view")) { st.view = t.dataset.view; st.card = 0; render(); }
    else if (t.classList.contains("qb-show")) { const a = t.closest(".qb-item").querySelector(".qb-answer"); a.hidden = !a.hidden; t.textContent = a.hidden ? "Show answer" : "Hide answer"; t.setAttribute("aria-expanded", !a.hidden); }
    else if (t.classList.contains("qb-write")) { const ta = t.closest(".qb-item").querySelector(".qb-draft"); ta.hidden = !ta.hidden; if (!ta.hidden) ta.focus(); }
    else if (t.classList.contains("qb-known")) setMark(t.dataset.id, "known");
    else if (t.classList.contains("qb-review")) setMark(t.dataset.id, "review");
    else if (t.classList.contains("qb-shuffle")) { const ids = Q.map((d) => d.i); for (let i = ids.length - 1; i > 0; i--) { const j = Math.floor(Math.random() * (i + 1)); [ids[i], ids[j]] = [ids[j], ids[i]]; } st.order = ids; st.card = 0; t.textContent = "Shuffle again"; render(); }
    else if (t.classList.contains("qb-expand")) { st.revealAll = !st.revealAll; render(); }
    else if (t.classList.contains("qb-reset")) { if (Object.keys(marks).length && window.confirm && !confirm("Clear all your marks on this device?")) return; marks = {}; save(); render(); }
    else if (t.classList.contains("qb-flip")) flip();
    else if (t.classList.contains("qb-next")) { st.card++; render(); focusCard(); }
    else if (t.classList.contains("qb-prev")) { st.card--; render(); focusCard(); }
    else if (t.classList.contains("qb-print")) { const was = [st.view, st.revealAll]; st.view = "list"; st.revealAll = true; render(); setTimeout(() => { window.print(); st.view = was[0]; st.revealAll = was[1]; render(); }, 50); }
  });
  function flip() { const c = $(".qb-card"); if (!c) return; const a = c.querySelector(".qb-answer"), b = c.querySelector(".qb-flip"); a.hidden = !a.hidden; b.textContent = a.hidden ? "Show answer" : "Hide answer"; }
  function focusCard() { const c = $(".qb-card"); if (c) c.focus(); }
  root.addEventListener("keydown", (e) => {
    if (st.view !== "cards" || !e.target.closest(".qb-cards")) return;
    if (e.key === " ") { e.preventDefault(); flip(); }
    else if (e.key === "ArrowRight") { st.card++; render(); focusCard(); }
    else if (e.key === "ArrowLeft") { st.card--; render(); focusCard(); }
    else if (e.key === "1" || e.key === "2") { const c = $(".qb-card"); if (c) { setMark(c.dataset.id, e.key === "1" ? "known" : "review"); } }
  });
  modSel.addEventListener("change", () => { st.module = modSel.value; if (st.module) st.go = +st.module.split(".")[0]; st.card = 0; render(); });
  let tmr; search.addEventListener("input", () => { clearTimeout(tmr); tmr = setTimeout(() => { st.search = search.value; st.card = 0; render(); }, 150); });
  status.addEventListener("change", () => { st.status = status.value; st.card = 0; render(); });
  $$(".qb-kind input").forEach((c) => c.addEventListener("change", () => { c.checked ? st.kinds.add(c.value) : st.kinds.delete(c.value); st.card = 0; render(); }));
  render();
})();
