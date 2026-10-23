/* Prezi-style zooming mind map: centre → modules → key ideas, with a camera path. Data: window.MINDMAP */
(function () {
  "use strict";
  const D = window.MINDMAP, NS = "http://www.w3.org/2000/svg";
  const svg = document.getElementById("mm-svg"), stage = document.getElementById("mm-stage"), notes = document.getElementById("mm-notes"), stepEl = document.getElementById("mm-step");
  const reduce = window.matchMedia && matchMedia("(prefers-reduced-motion: reduce)").matches;
  const el = (t, a, p) => { const e = document.createElementNS(NS, t); for (const k in a) e.setAttribute(k, a[k]); if (p) p.append(e); return e; };
  const wrap = (t, n) => { const w = String(t).split(/\s+/), o = []; let c = ""; w.forEach((x) => { if (c && (c + " " + x).length > n) { o.push(c); c = x; } else c = (c + " " + x).trim(); }); if (c) o.push(c); return o; };
  function box(g, x, y, w, h, lines, size, cls, sub) {
    el("rect", { x: x - w / 2, y: y - h / 2, width: w, height: h, rx: Math.min(18, h / 2.6), class: "node-box", "stroke-width": cls === "center" ? 0 : 2.5 }, g);
    const lh = size * 1.18, subl = sub ? wrap(sub, 30) : [], tot = lines.length * lh + subl.length * size * 0.85;
    let ty = y - tot / 2 + size * 0.9;
    lines.forEach((l) => { const t = el("text", { x, y: ty, "text-anchor": "middle", class: "node-label", style: `font-size:${size}px` }, g); t.textContent = l; ty += lh; });
    subl.forEach((l) => { const t = el("text", { x, y: ty, "text-anchor": "middle", class: "node-sub", style: `font-size:${size * 0.7}px` }, g); t.textContent = l; ty += size * 0.85; });
  }
  const n = D.branches.length, R1 = 560, OUT = 330, LW = 270, LH = 58, GAP = 12;
  const frames = [], bboxes = [];
  const gl = el("g", {}, svg), gn = el("g", {}, svg);
  // centre
  const gc = el("g", { class: "node sys-neutral center" }, gn);
  box(gc, 0, 0, 320, 120, wrap(D.center, 16), 40, "center", D.subtitle);
  gc.querySelector("rect").setAttribute("style", "fill:var(--ink)"); gc.querySelectorAll("text").forEach((t) => t.setAttribute("style", t.getAttribute("style") + ";fill:var(--paper)"));
  let all = { x0: -160, y0: -60, x1: 160, y1: 60 };
  const grow = (b, x0, y0, x1, y1) => { b.x0 = Math.min(b.x0, x0); b.y0 = Math.min(b.y0, y0); b.x1 = Math.max(b.x1, x1); b.y1 = Math.max(b.y1, y1); };
  const groups = [];
  D.branches.forEach((b, i) => {
    const a = -Math.PI / 2 + (2 * Math.PI * i) / n, ux = Math.cos(a), uy = Math.sin(a);
    const bx = R1 * ux, by = R1 * uy, BW = 320, BH = 96;
    const g = el("g", { class: `node br sys-${b.sys}`, tabindex: 0, role: "button", "aria-label": `Module ${b.id}: ${b.title}` }, gn);
    el("path", { d: `M0,0 C${R1 * 0.45 * ux},${R1 * 0.45 * uy} ${bx - 140 * ux},${by - 140 * uy} ${bx},${by}`, class: `sysstroke-${b.sys}`, fill: "none", "stroke-width": 7, opacity: 0.55 }, gl);
    box(g, bx, by, BW, BH, [b.id].concat(wrap(b.title, 24)).slice(0, 3), 24, "branch");
    const bb = { x0: bx - BW / 2, y0: by - BH / 2, x1: bx + BW / 2, y1: by + BH / 2 };
    // leaves: a stack placed outward from the branch
    const k = b.leaves.length, H = k * LH + (k - 1) * GAP;
    const ax = bx + (BW / 2 + OUT * 0.55) * Math.sign(ux) * (Math.abs(ux) > 0.35 ? 1 : 0) + (Math.abs(ux) <= 0.35 ? 0 : (ux > 0 ? LW / 2 : -LW / 2));
    const ay = Math.abs(ux) > 0.35 ? by : by + Math.sign(uy) * (BH / 2 + 50 + H / 2);
    b.leaves.forEach((t, j) => {
      const ly = ay - H / 2 + LH / 2 + j * (LH + GAP), lx = ax;
      el("path", { d: `M${bx + (Math.abs(ux) > 0.35 ? Math.sign(ux) * BW / 2 : 0)},${by + (Math.abs(ux) > 0.35 ? 0 : Math.sign(uy) * BH / 2)} L${lx - (Math.abs(ux) > 0.35 ? Math.sign(ux) * LW / 2 : 0)},${ly}`, class: `sysstroke-${b.sys}`, fill: "none", "stroke-width": 2.5, opacity: 0.6 }, gl);
      const lg = el("g", { class: `node leaf sys-${b.sys}` }, gn);
      box(lg, lx, ly, LW, LH, wrap(t, 28).slice(0, 2), 18, "leaf");
      lg.querySelector(".node-label").setAttribute("style", "font-size:18px;font-weight:600"); lg.querySelectorAll(".node-label").forEach((x) => x.setAttribute("style", "font-size:18px;font-weight:600;fill:var(--ink)"));
      lg.querySelector("rect").setAttribute("style", "fill:var(--card)");
      grow(bb, lx - LW / 2, ly - LH / 2, lx + LW / 2, ly + LH / 2);
    });
    grow(all, bb.x0, bb.y0, bb.x1, bb.y1);
    bboxes.push(bb); groups.push(g);
    g.addEventListener("click", () => go(i + 1)); g.addEventListener("keydown", (e) => { if (e.key === "Enter" || e.key === " ") { e.preventDefault(); go(i + 1); } });
  });
  const pad = (b, p) => ({ x: b.x0 - p, y: b.y0 - p, w: b.x1 - b.x0 + 2 * p, h: b.y1 - b.y0 + 2 * p });
  frames.push({ view: pad(all, 60), title: D.title, kind: "all" });
  D.branches.forEach((b, i) => frames.push({ view: pad(bboxes[i], 80), branch: i }));
  frames.push({ view: pad(all, 60), title: D.title, kind: "end" });
  let cur = 0, anim = null, view = Object.assign({}, frames[0].view);
  const setVB = (v) => svg.setAttribute("viewBox", `${v.x} ${v.y} ${v.w} ${v.h}`);
  setVB(view);
  function fly(to) {
    cancelAnimationFrame(anim);
    if (reduce) { view = Object.assign({}, to); setVB(view); return; }
    const from = Object.assign({}, view), t0 = performance.now(), dur = 950;
    const ease = (t) => (t < 0.5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2);
    const tick = (now) => { const t = Math.min(1, (now - t0) / dur), e = ease(t); ["x", "y", "w", "h"].forEach((k) => (view[k] = from[k] + (to[k] - from[k]) * e)); setVB(view); if (t < 1) anim = requestAnimationFrame(tick); };
    anim = requestAnimationFrame(tick);
  }
  function go(i) {
    cur = Math.max(0, Math.min(frames.length - 1, i)); const f = frames[cur];
    fly(f.view);
    groups.forEach((g, j) => g.style.opacity = f.branch == null || f.branch === j ? 1 : 0.35);
    stepEl.textContent = `${cur + 1} / ${frames.length}`;
    notes.innerHTML = "";
    if (f.branch != null) {
      const b = D.branches[f.branch];
      notes.innerHTML = `<h3>${b.id} ${esc(b.title)}</h3><p>${esc(b.summary)}</p><b>Remember</b><ul>${b.notes.map((x) => `<li>${esc(x)}</li>`).join("")}</ul><a href="${b.href}">Open module ${b.id}</a>`;
    } else if (f.kind === "all") notes.innerHTML = `<h3>${esc(D.title)}</h3><p>${esc(D.promise)}</p><p class="small muted">${n} modules. Press Next to zoom into each one.</p>`;
    else notes.innerHTML = `<h3>${esc(D.title)}</h3><p>That is the whole go. Pick any module on the map to revisit it.</p>`;
  }
  const esc = (s) => String(s).replace(/[&<>"]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]));
  document.getElementById("mm-start").addEventListener("click", () => { go(0); stage.focus(); });
  document.getElementById("mm-next").addEventListener("click", () => go(cur + 1));
  document.getElementById("mm-prev").addEventListener("click", () => go(cur - 1));
  document.getElementById("mm-all").addEventListener("click", () => go(0));
  const full = () => { if (document.fullscreenElement) document.exitFullscreen(); else if (stage.requestFullscreen) stage.requestFullscreen(); };
  document.getElementById("mm-full").addEventListener("click", full);
  stage.addEventListener("keydown", (e) => {
    if (["ArrowRight", "PageDown", " "].includes(e.key)) { e.preventDefault(); go(cur + 1); }
    else if (["ArrowLeft", "PageUp"].includes(e.key)) { e.preventDefault(); go(cur - 1); }
    else if (e.key === "Escape" || e.key === "Home") go(0);
    else if (e.key === "f" || e.key === "F") full();
  });
  window.MINDMAP_GO = go; window.MINDMAP_FRAMES = frames.length;
  go(0);
})();
