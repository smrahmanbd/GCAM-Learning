/* GCAM family decks: slide controller, SVG step animations, toy explorers and three.js scenes.
   Teaching pictures with illustrative numbers; nothing here is model output. Needs three.js r128 (global THREE). */
(function () {
  "use strict";
  const $ = (s, r = document) => r.querySelector(s), $$ = (s, r = document) => Array.from(r.querySelectorAll(s));
  const NS = "http://www.w3.org/2000/svg";
  const reduce = window.matchMedia && matchMedia("(prefers-reduced-motion: reduce)").matches;
  const css = (v) => getComputedStyle(document.documentElement).getPropertyValue(v).trim();
  const SYS = () => ({ economy: css("--economy"), energy: css("--energy"), land: css("--land"), water: css("--water"), climate: css("--climate"), policy: css("--policy"), ink: css("--ink"), muted: css("--muted"), line: css("--line"), paper: css("--paper-2"), card: css("--card") });
  const el = (tag, attrs, parent) => { const e = document.createElementNS(NS, tag); for (const k in attrs || {}) e.setAttribute(k, attrs[k]); if (parent) parent.append(e); return e; };
  const txt = (p, x, y, t, o = {}) => { const e = el("text", Object.assign({ x, y, fill: SYS().ink, "font-size": 13, "text-anchor": "middle" }, o), p); e.textContent = t; return e; };

  // ---------------- deck controller ----------------
  function deck(sec) {
    const slides = $$(".fslide", sec), dots = $$(".f-dots i", sec), cur = $(".f-cur", sec); let i = 0;
    const show = (n) => { i = Math.max(0, Math.min(slides.length - 1, n)); slides.forEach((s, j) => s.classList.toggle("on", j === i)); dots.forEach((d, j) => d.classList.toggle("on", j === i)); cur.textContent = i + 1;
      const s = slides[i]; $$(".f3d", s).forEach(mount3d); $$(".f-anim", s).forEach(mountAnim); $$(".f-toy", s).forEach(mountToy); sec.dispatchEvent(new CustomEvent("slide", { detail: i })); };
    $(".f-prev", sec).addEventListener("click", () => show(i - 1)); $(".f-next", sec).addEventListener("click", () => show(i + 1));
    dots.forEach((d, j) => d.addEventListener("click", () => show(j)));
    $(".f-full", sec).addEventListener("click", () => { if (document.fullscreenElement) document.exitFullscreen(); else sec.requestFullscreen && sec.requestFullscreen(); });
    sec.tabIndex = 0;
    sec.addEventListener("keydown", (e) => { if (e.target.matches("input,textarea,button,select")) return; if (e.key === "ArrowRight" || e.key === "PageDown") { show(i + 1); e.preventDefault(); } if (e.key === "ArrowLeft" || e.key === "PageUp") { show(i - 1); e.preventDefault(); } });
    show(0); sec.showSlide = show;
  }
  function tabs() {
    const decks = $$(".fdeck"), ts = $$(".f-tab");
    const open = (k) => { ts.forEach((b) => b.setAttribute("aria-pressed", b.dataset.k === k)); decks.forEach((d) => { d.hidden = d.dataset.k !== k; if (!d.hidden) { d.showSlide(0); d.scrollIntoView({ behavior: reduce ? "auto" : "smooth", block: "start" }); } }); };
    ts.forEach((b) => b.addEventListener("click", () => open(b.dataset.k)));
    window.openFamilyDeck = open;
  }

  // ---------------- SVG step animations ----------------
  const ANIMS = {};
  function base(w = 640, h = 400) { return el("svg", { viewBox: `0 0 ${w} ${h}` }); }
  function box(svg, x, y, w, h, label, color, o = {}) { const g = el("g", { class: "ab" }, svg); el("rect", { x, y, width: w, height: h, rx: 8, fill: color, "fill-opacity": o.fo || .18, stroke: color, "stroke-width": 1.6 }, g); const lines = String(label).split("\n"); lines.forEach((l, i) => txt(g, x + w / 2, y + h / 2 + (i - (lines.length - 1) / 2) * 15 + 5, l, { "font-size": o.fs || 12.5, "font-weight": i === 0 ? 700 : 400 })); return g; }
  function arrow(svg, x1, y1, x2, y2, color) { const p = el("path", { d: `M${x1},${y1} L${x2},${y2}`, stroke: color, "stroke-width": 2.2, fill: "none", "stroke-dasharray": "6 5", class: "aa" }, svg); if (!reduce) el("animate", { attributeName: "stroke-dashoffset", from: 22, to: 0, dur: "0.8s", repeatCount: "indefinite" }, p); el("circle", { cx: x2, cy: y2, r: 4, fill: color }, svg); return p; }
  const fade = (g, on) => { g.style.transition = "opacity .4s"; g.style.opacity = on ? 1 : .18; };

  ANIMS.hector = () => {
    const C = SYS(), svg = base();
    const em = box(svg, 20, 30, 120, 50, "Emissions\nfrom GCAM", C.policy), atm = box(svg, 250, 20, 150, 60, "Atmosphere\nCO₂ ppm", C.climate, { fo: .25 });
    const veg = box(svg, 60, 150, 100, 46, "Vegetation", C.land), det = box(svg, 60, 206, 100, 46, "Detritus", C.land), soil = box(svg, 60, 262, 100, 46, "Soil", C.land);
    const os = box(svg, 440, 150, 150, 46, "Ocean surface", C.water), oi = box(svg, 440, 206, 150, 46, "Intermediate", C.water), od = box(svg, 440, 262, 150, 46, "Deep ocean", C.water);
    const forc = box(svg, 250, 150, 150, 50, "Forcing\nW/m²", C.energy), temp = box(svg, 250, 240, 150, 50, "Temperature\n°C", C.climate, { fo: .35 });
    const a1 = el("g", {}, svg); arrow(a1, 140, 55, 250, 50, C.policy);
    const a2 = el("g", {}, svg); arrow(a2, 300, 80, 110, 150, C.land); arrow(a2, 350, 80, 515, 150, C.water); arrow(a2, 110, 196, 110, 206, C.land); arrow(a2, 110, 252, 110, 262, C.land); arrow(a2, 515, 196, 515, 206, C.water); arrow(a2, 515, 252, 515, 262, C.water);
    const a4 = el("g", {}, svg); arrow(a4, 325, 80, 325, 150, C.energy);
    const a5 = el("g", {}, svg); arrow(a5, 325, 200, 325, 240, C.climate);
    const a6 = el("g", {}, svg); arrow(a6, 250, 270, 160, 285, C.climate); arrow(a6, 400, 270, 440, 180, C.climate);
    const lvl = el("rect", { x: 252, y: 78, width: 146, height: 0, fill: C.climate, "fill-opacity": .35 }, svg);
    const ppm = txt(svg, 325, 100, "", { "font-size": 12, fill: C.muted });
    const groups = [[em, a1], [veg, det, soil, os, oi, od, a2], [atm], [forc, a4], [temp, a5], [a6]];
    const all = groups.flat();
    return { svg, set(k) { all.forEach((g) => fade(g, false)); groups.slice(0, k + 1).forEach((gs) => gs.forEach((g) => fade(g, true))); lvl.setAttribute("height", Math.min(58, 10 + k * 9)); lvl.setAttribute("y", 78 - Math.min(58, 10 + k * 9)); ppm.textContent = k >= 2 ? `${280 + k * 60} ppm (illustrative)` : ""; } };
  };

  ANIMS.xanthos = () => {
    const C = SYS(), svg = base(); const groups = [];
    const cl = box(svg, 20, 20, 150, 50, "Climate\nrain, temperature", C.policy); groups.push([cl]);
    const g2 = el("g", {}, svg); box(g2, 20, 100, 150, 50, "Potential ET", C.energy); arrow(g2, 95, 70, 95, 100, C.policy); groups.push([g2]);
    const g3 = el("g", {}, svg);
    for (let r = 0; r < 4; r++) for (let c = 0; c < 6; c++) { const x = 220 + c * 60, y = 30 + r * 60; el("rect", { x, y, width: 54, height: 54, fill: C.land, "fill-opacity": .12 + ((r + c) % 3) * .08, stroke: C.line }, g3); const b = el("rect", { x: x + 12, y: y + 30, width: 30, height: 0, fill: C.water, "fill-opacity": .7 }, g3); if (!reduce) { el("animate", { attributeName: "height", values: "0;22;0", dur: `${2 + ((r * c) % 3)}s`, repeatCount: "indefinite" }, b); el("animate", { attributeName: "y", values: `${y + 48};${y + 26};${y + 48}`, dur: `${2 + ((r * c) % 3)}s`, repeatCount: "indefinite" }, b); } }
    txt(g3, 400, 285, "0.5° cells: each has a soil bucket", { "font-size": 12, fill: C.muted }); groups.push([g3]);
    const g4 = el("g", {}, svg); const river = el("path", { d: "M235,60 C300,120 340,120 400,180 S520,220 560,250", stroke: C.water, "stroke-width": 5, fill: "none", "stroke-linecap": "round", "stroke-dasharray": "10 8" }, g4); if (!reduce) el("animate", { attributeName: "stroke-dashoffset", from: 36, to: 0, dur: "1.2s", repeatCount: "indefinite" }, river); groups.push([g4]);
    const g5 = el("g", {}, svg); box(g5, 460, 300, 150, 50, "Basin total\n(235 basins)", C.water, { fo: .3 }); arrow(g5, 560, 250, 535, 300, C.water); groups.push([g5]);
    const g6 = el("g", {}, svg); box(g6, 230, 310, 180, 50, "GCAM water supply", C.policy); arrow(g6, 460, 325, 410, 335, C.water); groups.push([g6]);
    const all = groups.flat();
    return { svg, set(k) { all.forEach((g) => fade(g, false)); groups.slice(0, k + 1).forEach((gs) => gs.forEach((g) => fade(g, true))); } };
  };

  ANIMS.tethys = () => {
    const C = SYS(), svg = base(); const groups = [];
    const g1 = el("g", {}, svg); box(g1, 20, 30, 150, 60, "GCAM\nwithdrawals", C.policy); groups.push([g1]);
    const g2 = el("g", {}, svg); ["Population", "Irrigated area", "Livestock", "Power plants"].forEach((t, i) => box(g2, 20, 120 + i * 48, 150, 38, t, C.economy, { fs: 11.5 })); txt(g2, 95, 320, "proxies", { fill: C.muted, "font-size": 12 }); groups.push([g2]);
    const g3 = el("g", {}, svg); const cells = []; for (let r = 0; r < 5; r++) for (let c = 0; c < 7; c++) { const v = Math.abs(Math.sin(r * 3 + c * 7)); const x = 230 + c * 50, y = 40 + r * 50; const rc = el("rect", { x, y, width: 46, height: 46, fill: C.water, "fill-opacity": .05 + v * .6, stroke: C.line }, g3); cells.push([rc, v, r, c]); } arrow(g3, 170, 60, 230, 60, C.policy); groups.push([g3]);
    const g4 = el("g", {}, svg); const mon = txt(g4, 400, 320, "Month: January", { "font-weight": 700 }); groups.push([g4]);
    const g5 = el("g", {}, svg); txt(g5, 400, 345, "2020 → 2025: yearly values interpolated", { fill: C.muted, "font-size": 12 }); groups.push([g5]);
    const g6 = el("g", {}, svg); box(g6, 230, 360, 340, 34, "Gridded monthly withdrawals by sector", C.water, { fo: .3, fs: 12 }); groups.push([g6]);
    const all = groups.flat(); let timer;
    const M = ["January", "March", "May", "July", "September", "November"];
    return { svg, set(k) { all.forEach((g) => fade(g, false)); groups.slice(0, k + 1).forEach((gs) => gs.forEach((g) => fade(g, true))); clearInterval(timer); if (k >= 3 && !reduce) { let m = 0; timer = setInterval(() => { m = (m + 1) % 6; mon.textContent = "Month: " + M[m]; const s = .5 + .5 * Math.sin(m / 6 * Math.PI * 2); cells.forEach(([rc, v, r, c]) => rc.setAttribute("fill-opacity", .05 + v * (c % 3 === 0 ? .2 + .5 * s : .6))); }, 700); } } };
  };

  ANIMS.demeter = () => {
    const C = SYS(), svg = base(); const groups = []; const N = 8, S = 34, X0 = 300, Y0 = 40; const cells = [];
    const g1 = el("g", {}, svg); for (let r = 0; r < N; r++) for (let c = 0; c < N; c++) { const d = Math.hypot(r - 3.5, c - 2.5); const crop = d < 1.6 ? .7 : 0; const rc = el("rect", { x: X0 + c * S, y: Y0 + r * S, width: S - 2, height: S - 2, fill: crop ? C.energy : C.land, "fill-opacity": crop ? .3 + crop * .5 : .35 + ((r * 7 + c * 3) % 5) * .08 }, g1); cells.push({ rc, r, c, crop, d }); } txt(g1, X0 + N * S / 2, Y0 + N * S + 18, "base-year map (yellow = cropland)", { fill: C.muted, "font-size": 12 }); groups.push([g1]);
    const g2 = el("g", {}, svg); box(g2, 20, 30, 220, 50, "GCAM: +40% cropland\nin this basin", C.policy); groups.push([g2]);
    const g3 = el("g", {}, svg); box(g3, 20, 100, 220, 50, "Suitability score\nsoil, slope, neighbours", C.economy); groups.push([g3]);
    const g4 = el("g", {}, svg); box(g4, 20, 170, 220, 46, "1. Intensify", C.energy); groups.push([g4]);
    const g5 = el("g", {}, svg); box(g5, 20, 236, 220, 46, "2. Expand outward", C.energy); groups.push([g5]);
    const g6 = el("g", {}, svg); box(g6, 20, 302, 220, 46, "Map for 2050", C.land, { fo: .3 }); groups.push([g6]);
    const all = groups.flat();
    return { svg, set(k) { all.forEach((g) => fade(g, false)); groups.slice(0, k + 1).forEach((gs) => gs.forEach((g) => fade(g, true))); cells.forEach((cl) => { let crop = cl.crop; if (k >= 3 && cl.crop) crop = 1; if (k >= 4 && !cl.crop && cl.d < 2.7) crop = .75; cl.rc.style.transition = "fill .5s, fill-opacity .5s"; cl.rc.setAttribute("fill", crop ? C.energy : C.land); cl.rc.setAttribute("fill-opacity", crop ? .3 + crop * .5 : .35 + ((cl.r * 7 + cl.c * 3) % 5) * .08); if (k === 2 && !cl.crop) cl.rc.setAttribute("fill-opacity", .15 + Math.max(0, .5 - cl.d * .08)); }); } };
  };

  ANIMS.moirai = () => {
    const C = SYS(), svg = base(); const groups = [];
    const layers = [["HYDE land use", C.land], ["SAGE crops", C.energy], ["FAO statistics", C.policy], ["Carbon maps", C.climate], ["Basins × countries", C.water]];
    const g1 = el("g", {}, svg); layers.slice(0, 4).forEach(([t, c], i) => { const g = el("g", { transform: `translate(${40 + i * 18}, ${40 + i * 44})` }, g1); el("path", { d: "M0,40 L120,0 L240,40 L120,80 Z", fill: c, "fill-opacity": .25, stroke: c }, g); txt(g, 120, 44, t, { "font-size": 12 }); }); groups.push([g1]);
    const g2 = el("g", { transform: "translate(112, 216)" }, svg); el("path", { d: "M0,40 L120,0 L240,40 L120,80 Z", fill: C.water, "fill-opacity": .15, stroke: C.water, "stroke-width": 2 }, g2); el("path", { d: "M40,27 L150,65 M80,13 L190,52 M60,60 L170,22", stroke: C.water, "stroke-width": 1.5, fill: "none" }, g2); txt(g2, 120, 95, "land units = country × basin", { "font-size": 12, fill: C.muted }); groups.push([g2]);
    const g3 = el("g", {}, svg); for (let i = 0; i < 6; i++) { const p = el("path", { d: "M0,10 L30,0 L60,10 L30,20 Z", fill: layers[i % 4][1], "fill-opacity": .5, transform: `translate(${330 + (i % 3) * 70}, ${60 + Math.floor(i / 3) * 40})` }, g3); if (!reduce) el("animateTransform", { attributeName: "transform", type: "translate", from: `${330 + (i % 3) * 70} ${60 + Math.floor(i / 3) * 40}`, to: `${330 + (i % 3) * 70} ${200 + Math.floor(i / 3) * 40}`, dur: "1.6s", begin: `${i * .2}s`, repeatCount: "indefinite" }, p); } txt(g3, 400, 40, "cut every layer by unit", { "font-size": 12, fill: C.muted }); groups.push([g3]);
    const g4 = el("g", {}, svg); box(g4, 330, 300, 120, 40, "scale to FAO", C.policy, { fs: 11.5 }); groups.push([g4]);
    const g5 = el("g", {}, svg); box(g5, 460, 300, 120, 40, "attach carbon", C.climate, { fs: 11.5 }); groups.push([g5]);
    const g6 = el("g", {}, svg); const t = el("g", { transform: "translate(330, 350)" }, g6); el("rect", { width: 250, height: 40, fill: C.card, stroke: C.ink }, t); el("path", { d: "M0,13 H250 M0,26 H250 M60,0 V40 M130,0 V40 M190,0 V40", stroke: C.line }, t); txt(t, 30, 10, "unit", { "font-size": 9 }); txt(t, 95, 10, "land type", { "font-size": 9 }); txt(t, 160, 10, "area", { "font-size": 9 }); txt(t, 220, 10, "carbon", { "font-size": 9 }); groups.push([g6]);
    const all = groups.flat();
    return { svg, set(k) { all.forEach((g) => fade(g, false)); groups.slice(0, k + 1).forEach((gs) => gs.forEach((g) => fade(g, true))); } };
  };

  ANIMS.land = () => {
    const C = SYS(), svg = base(); const groups = [];
    const g1 = el("g", {}, svg); box(g1, 20, 20, 150, 50, "Prices\nfrom markets", C.economy); groups.push([g1]);
    const g2 = el("g", {}, svg); const bars = [["Crops", C.energy, 60], ["Pasture", C.land, 40], ["Forest", C.land, 30]]; const bEls = bars.map(([t, c, h], i) => { const x = 220 + i * 70; const r = el("rect", { x, y: 120 - h, width: 50, height: h, fill: c, "fill-opacity": .6 }, g2); txt(g2, x + 25, 136, t, { "font-size": 11.5 }); return r; }); txt(g2, 290, 30, "profit per hectare", { "font-size": 12, fill: C.muted }); groups.push([g2]);
    const g3 = el("g", {}, svg); const sl = el("g", { transform: "translate(440, 60)" }, g3); const segs = bars.map(([t, c], i) => el("rect", { x: 0, y: 0, width: 0, height: 60, fill: c, "fill-opacity": .5 + i * .15, stroke: C.paper }, sl)); txt(g3, 530, 140, "share of the land unit", { "font-size": 12, fill: C.muted }); groups.push([g3]);
    const g4 = el("g", {}, svg); txt(g4, 320, 200, "share ∝ weight × profit^λ   (nested: crop nest × crop within nest)", { "font-size": 12.5 }); groups.push([g4]);
    const g5 = el("g", {}, svg); box(g5, 20, 240, 150, 50, "Supply = area × yield", C.land); arrow(g5, 170, 265, 220, 265, C.land); box(g5, 220, 240, 150, 50, "Market clears", C.economy); arrow(g5, 295, 240, 95, 70, C.economy); groups.push([g5]);
    const g6 = el("g", {}, svg); box(g6, 420, 240, 180, 50, "Land-use change\ncarbon → Hector", C.climate); groups.push([g6]);
    const all = groups.flat(); let t0;
    const draw = (p) => { const prof = [60, 40, 30].map((h, i) => h * (i === 0 ? 1 + p : 1)); const lam = 2; const w = prof.map((x) => Math.pow(x, lam)); const S = w.reduce((a, b) => a + b, 0); let x = 0; segs.forEach((sg, i) => { const ww = 180 * w[i] / S; sg.setAttribute("x", x); sg.setAttribute("width", ww); x += ww; }); bEls.forEach((b, i) => { b.setAttribute("height", prof[i]); b.setAttribute("y", 120 - prof[i]); }); };
    return { svg, set(k) { all.forEach((g) => fade(g, false)); groups.slice(0, k + 1).forEach((gs) => gs.forEach((g) => fade(g, true))); cancelAnimationFrame(t0); if (k >= 2) { let p = 0; const run = () => { p = Math.min(.8, p + .01); draw(p); if (p < .8 && !reduce) t0 = requestAnimationFrame(run); }; draw(0); run(); } } };
  };

  ANIMS.economy = () => {
    const C = SYS(), svg = base(); const groups = [];
    const g1 = el("g", {}, svg); box(g1, 20, 20, 140, 50, "Population\nIncome (SSP)", C.economy); groups.push([g1]);
    const g2 = el("g", {}, svg); box(g2, 200, 20, 140, 50, "Service demand", C.energy); arrow(g2, 160, 45, 200, 45, C.economy); groups.push([g2]);
    const g3 = el("g", {}, svg); const pie = el("g", { transform: "translate(450, 45)" }, g3); const shares = [.5, .3, .2], cols = [C.energy, C.water, C.economy]; let a = 0; shares.forEach((s, i) => { const b = a + s * Math.PI * 2; el("path", { d: `M0,0 L${Math.cos(a) * 28},${Math.sin(a) * 28} A28,28 0 ${s > .5 ? 1 : 0} 1 ${Math.cos(b) * 28},${Math.sin(b) * 28} Z`, fill: cols[i], "fill-opacity": .7 }, pie); a = b; }); txt(g3, 450, 95, "logit shares", { "font-size": 12, fill: C.muted }); arrow(g3, 340, 45, 420, 45, C.energy); groups.push([g3]);
    const g4 = el("g", {}, svg); el("path", { d: "M40,330 C120,320 200,300 300,200", stroke: C.energy, "stroke-width": 2.5, fill: "none" }, g4); txt(g4, 170, 350, "supply curve: dearer as you take more", { "font-size": 12, fill: C.muted }); groups.push([g4]);
    const g5 = el("g", {}, svg); const beam = el("g", { transform: "translate(450, 240)" }, g5); const bm = el("line", { x1: -70, y1: 0, x2: 70, y2: 0, stroke: C.ink, "stroke-width": 3 }, beam); el("path", { d: "M-6,0 L6,0 L0,20 Z", fill: C.ink }, beam); txt(beam, -70, -10, "supply", { "font-size": 11 }); txt(beam, 70, -10, "demand", { "font-size": 11 }); txt(g5, 450, 290, "Broyden: tilt prices until level", { "font-size": 12, fill: C.muted }); groups.push([g5]);
    const g6 = el("g", {}, svg); box(g6, 20, 110, 140, 50, "Macro module\nGDP ← energy cost", C.economy, { fs: 11.5 }); arrow(g6, 90, 110, 90, 70, C.economy); groups.push([g6]);
    const all = groups.flat(); let raf;
    return { svg, set(k) { all.forEach((g) => fade(g, false)); groups.slice(0, k + 1).forEach((gs) => gs.forEach((g) => fade(g, true))); cancelAnimationFrame(raf); if (k >= 4 && !reduce) { let t = 0; const run = () => { t += .05; const ang = 14 * Math.exp(-t / 2) * Math.cos(t * 3); bm.setAttribute("transform", `rotate(${ang})`); if (t < 8) raf = requestAnimationFrame(run); }; run(); } } };
  };

  ANIMS.gcamdata = () => {
    const C = SYS(), svg = base(); const groups = [];
    const st = ["Raw files", "L0, L1\nclean, aggregate", "L2\nstructures", "Calibrate", "XML", "GCAM run"]; const cols = [C.policy, C.economy, C.economy, C.energy, C.water, C.climate];
    el("rect", { x: 20, y: 200, width: 600, height: 14, rx: 7, fill: C.line }, svg);
    st.forEach((t, i) => { const g = el("g", {}, svg); box(g, 30 + i * 98, 120, 86, 60, t, cols[i], { fs: 11 }); groups.push([g]); });
    const cube = el("rect", { x: 40, y: 186, width: 20, height: 20, rx: 3, fill: C.policy }, svg);
    const all = groups.flat(); let raf;
    return { svg, set(k) { all.forEach((g) => fade(g, false)); groups.slice(0, k + 1).forEach((gs) => gs.forEach((g) => fade(g, true))); cancelAnimationFrame(raf); const tx = 40 + k * 98; cube.setAttribute("fill", cols[k]); if (reduce) { cube.setAttribute("x", tx); return; } let x = +cube.getAttribute("x"); const run = () => { x += (tx - x) * .12; cube.setAttribute("x", x); if (Math.abs(tx - x) > .5) raf = requestAnimationFrame(run); }; run(); } };
  };

  function mountAnim(host) {
    if (host.dataset.ready) return; host.dataset.ready = "1";
    const mk = ANIMS[host.dataset.anim]; if (!mk) return; const a = mk(); host.append(a.svg);
    const slide = host.closest(".fslide"), items = $$(".f-steplist li", slide), n = items.length; let k = 0, timer;
    const set = (j) => { k = Math.max(0, Math.min(n - 1, j)); a.set(k); items.forEach((li, i) => { li.classList.toggle("on", i === k); li.classList.toggle("done", i < k); }); };
    $(".f-prev-step", slide).addEventListener("click", () => { clearInterval(timer); set(k - 1); }); $(".f-next-step", slide).addEventListener("click", () => { clearInterval(timer); set(k + 1); });
    $(".f-play-steps", slide).addEventListener("click", () => { clearInterval(timer); set(0); timer = setInterval(() => { if (k >= n - 1) clearInterval(timer); else set(k + 1); }, 2200); });
    items.forEach((li, i) => li.addEventListener("click", () => { clearInterval(timer); set(i); }));
    set(0);
  }

  // ---------------- toy explorers ----------------
  const TOYS = {};
  function slider(row, label, min, max, step, val, unit = "") { const l = document.createElement("label"); const inp = document.createElement("input"); Object.assign(inp, { type: "range", min, max, step, value: val }); const o = document.createElement("span"); o.className = "out"; l.append(label, inp, o); row.append(l); const upd = () => (o.textContent = inp.value + unit); inp.addEventListener("input", upd); upd(); return inp; }
  function ui(host) { host.innerHTML = ""; const row = document.createElement("div"); row.className = "row"; const svg = el("svg", { viewBox: "0 0 600 220" }); host.append(row, svg); return { row, svg }; }
  function axes(svg, C) { el("line", { x1: 50, y1: 190, x2: 580, y2: 190, stroke: C.line }, svg); el("line", { x1: 50, y1: 20, x2: 50, y2: 190, stroke: C.line }, svg); }
  function poly(svg, pts, color, w = 2.5) { return el("polyline", { points: pts.map((p) => p.join(",")).join(" "), fill: "none", stroke: color, "stroke-width": w }, svg); }

  TOYS.hector = (host) => { const C = SYS(), { row, svg } = ui(host); const e = slider(row, "Emissions (Gt C/yr)", 0, 20, .5, 10), s = slider(row, "Climate sensitivity (°C per doubling)", 1.5, 5, .1, 3), stop = slider(row, "Stop emissions after year", 10, 100, 5, 60); const draw = () => { svg.innerHTML = ""; axes(svg, C); let Ca = 600, Co = 0, T = 0; const pc = [], pt = []; for (let y = 0; y <= 100; y++) { const E = y < +stop.value ? +e.value : 0; const ex = (Ca - 600) * .02 - (Co) * .002; Ca += E - ex; Co += ex; const F = 5.35 * Math.log(Ca / 600); const Teq = F * (+s.value / 3.7); T += (Teq - T) * .06; pc.push([50 + y * 5.3, 190 - Math.min(170, (Ca - 600) * .12)]); pt.push([50 + y * 5.3, 190 - Math.min(170, T * 30)]); } poly(svg, pc, C.climate); poly(svg, pt, C.energy); txt(svg, 120, 30, "CO₂ above pre-industrial", { fill: C.climate, "text-anchor": "start", "font-size": 12 }); txt(svg, 120, 48, "temperature", { fill: C.energy, "text-anchor": "start", "font-size": 12 }); txt(svg, 315, 210, "years", { "font-size": 11, fill: C.muted }); }; [e, s, stop].forEach((i) => i.addEventListener("input", draw)); draw(); };
  TOYS.xanthos = (host) => { const C = SYS(), { row, svg } = ui(host); const r = slider(row, "Rain (mm/month)", 0, 200, 5, 80), pet = slider(row, "Potential ET (mm/month)", 0, 200, 5, 60), cap = slider(row, "Bucket size (mm)", 50, 400, 10, 200); const draw = () => { svg.innerHTML = ""; axes(svg, C); let S = 50; const ps = [], pr = []; for (let m = 0; m <= 48; m++) { const rain = +r.value * (1 + .6 * Math.sin(m / 12 * Math.PI * 2)); const et = Math.min(S, +pet.value * (1 + .3 * Math.cos(m / 12 * Math.PI * 2))); S = S + rain - et; let run = 0; if (S > +cap.value) { run = S - +cap.value; S = +cap.value; } ps.push([50 + m * 11, 190 - S * .4]); pr.push([50 + m * 11, 190 - run * .8]); } poly(svg, ps, C.land); poly(svg, pr, C.water); txt(svg, 120, 30, "soil water", { fill: C.land, "text-anchor": "start", "font-size": 12 }); txt(svg, 120, 48, "runoff (what Xanthos reports)", { fill: C.water, "text-anchor": "start", "font-size": 12 }); txt(svg, 315, 210, "months", { "font-size": 11, fill: C.muted }); }; [r, pet, cap].forEach((i) => i.addEventListener("input", draw)); draw(); };
  TOYS.tethys = (host) => { const C = SYS(), { row, svg } = ui(host); const sl = [slider(row, "Cell A people", 0, 100, 1, 60), slider(row, "Cell B people", 0, 100, 1, 25), slider(row, "Cell C people", 0, 100, 1, 15)]; const draw = () => { svg.innerHTML = ""; const tot = 120; const p = sl.map((s) => +s.value), S = p.reduce((a, b) => a + b, 0) || 1; el("rect", { x: 40, y: 190 - tot, width: 70, height: tot, fill: C.water, "fill-opacity": .6 }, svg); txt(svg, 75, 208, "region total: 120", { "font-size": 11 }); p.forEach((v, i) => { const h = tot * v / S; el("rect", { x: 200 + i * 110, y: 190 - h, width: 70, height: h, fill: C.water, "fill-opacity": .4 + i * .2 }, svg); txt(svg, 235 + i * 110, 208, `cell ${"ABC"[i]}: ${h.toFixed(0)}`, { "font-size": 11 }); }); txt(svg, 320, 30, "household water follows population; the three columns always add to 120", { "font-size": 12, fill: C.muted }); }; sl.forEach((i) => i.addEventListener("input", draw)); draw(); };
  TOYS.demeter = (host) => { const C = SYS(), { row, svg } = ui(host); const need = slider(row, "Cropland to add (cells)", 0, 30, 1, 8), N = 10, S = 18; const base = []; for (let r = 0; r < N; r++) for (let c = 0; c < N; c++) base.push({ r, c, crop: Math.hypot(r - 5, c - 3) < 1.8 ? .6 : 0, d: Math.hypot(r - 5, c - 3) }); const draw = () => { svg.innerHTML = ""; let left = +need.value; const cells = base.map((x) => ({ ...x })); cells.filter((x) => x.crop).forEach((x) => { const add = Math.min(left, 1 - x.crop); x.crop += add; left -= add; }); cells.filter((x) => !x.crop).sort((a, b) => a.d - b.d).forEach((x) => { if (left > 0) { const add = Math.min(left, 1); x.crop = add; left -= add; } }); cells.forEach((x) => el("rect", { x: 200 + x.c * S, y: 15 + x.r * S, width: S - 1, height: S - 1, fill: x.crop ? C.energy : C.land, "fill-opacity": x.crop ? .25 + .6 * x.crop : .3 }, svg)); const inten = cells.reduce((a, x, i) => a + (base[i].crop ? x.crop - base[i].crop : 0), 0); txt(svg, 100, 60, "intensified:", { "text-anchor": "start", "font-size": 12 }); txt(svg, 100, 78, inten.toFixed(1) + " cells", { "text-anchor": "start", "font-size": 12, fill: C.energy }); txt(svg, 100, 110, "expanded:", { "text-anchor": "start", "font-size": 12 }); txt(svg, 100, 128, (+need.value - inten).toFixed(1) + " cells", { "text-anchor": "start", "font-size": 12, fill: C.energy }); txt(svg, 460, 60, "darker = fuller cell", { "text-anchor": "start", "font-size": 11, fill: C.muted }); }; need.addEventListener("input", draw); draw(); };
  TOYS.moirai = (host) => { const C = SYS(), { row, svg } = ui(host); const b = slider(row, "Basin boundary (x position)", 100, 500, 5, 300); const draw = () => { svg.innerHTML = ""; const x = +b.value; el("path", { d: "M60,40 L540,30 L560,180 L80,190 Z", fill: C.land, "fill-opacity": .2, stroke: C.land, "stroke-width": 2 }, svg); el("line", { x1: x, y1: 20, x2: x + 20, y2: 200, stroke: C.water, "stroke-width": 3, "stroke-dasharray": "8 5" }, svg); const aL = ((x - 60) / 480 * 100).toFixed(0), aR = (100 - aL); txt(svg, (60 + x) / 2, 115, `unit 1: ${aL}%`, { "font-size": 13, "font-weight": 700 }); txt(svg, (x + 550) / 2, 115, `unit 2: ${aR}%`, { "font-size": 13, "font-weight": 700 }); txt(svg, 300, 212, "one country, two basins → two land units; the country total is always 100%", { "font-size": 12, fill: C.muted }); }; b.addEventListener("input", draw); draw(); };
  TOYS.land = (host) => { const C = SYS(), { row, svg } = ui(host); const p = slider(row, "Crop price (index)", 50, 200, 5, 100), lam = slider(row, "λ (logit exponent)", .5, 6, .5, 2); const draw = () => { svg.innerHTML = ""; const prof = [+p.value * .6 - 20, 40, 30].map((v) => Math.max(1, v)); const w = prof.map((v) => Math.pow(v, +lam.value)), S = w.reduce((a, c) => a + c, 0); const names = ["crops", "pasture", "forest"], cols = [C.energy, C.land, C.policy]; let x = 60; w.forEach((v, i) => { const ww = 480 * v / S; el("rect", { x, y: 60, width: ww, height: 70, fill: cols[i], "fill-opacity": .55, stroke: C.paper }, svg); if (ww > 50) txt(svg, x + ww / 2, 100, `${names[i]} ${(100 * v / S).toFixed(0)}%`, { "font-size": 12, fill: "#fff", "font-weight": 700 }); x += ww; }); txt(svg, 300, 170, `profits: crops ${prof[0].toFixed(0)}, pasture 40, forest 30 per hectare (illustrative)`, { "font-size": 12, fill: C.muted }); }; [p, lam].forEach((i) => i.addEventListener("input", draw)); draw(); };
  TOYS.economy = (host) => { const C = SYS(), { row, svg } = ui(host); const pr = slider(row, "Price", 1, 20, .1, 4); const btn = document.createElement("button"); btn.className = "btn quiet"; btn.type = "button"; btn.textContent = "Solve"; row.append(btn); const D = (P) => 200 / Math.pow(P, .8), Sf = (P) => 20 * Math.pow(P, 1.2); const draw = () => { svg.innerHTML = ""; axes(svg, C); const pd = [], ps = []; for (let P = 1; P <= 20; P += .5) { pd.push([50 + P * 26, 190 - Math.min(170, D(P) * .8)]); ps.push([50 + P * 26, 190 - Math.min(170, Sf(P) * .8)]); } poly(svg, pd, C.economy); poly(svg, ps, C.energy); const P = +pr.value, gap = Sf(P) - D(P); el("line", { x1: 50 + P * 26, y1: 20, x2: 50 + P * 26, y2: 190, stroke: C.ink, "stroke-dasharray": "4 4" }, svg); txt(svg, 300, 30, `price ${P.toFixed(1)}: supply − demand = ${gap.toFixed(1)}`, { "font-size": 13, "font-weight": 700 }); txt(svg, 120, 55, "demand", { fill: C.economy, "text-anchor": "start", "font-size": 12 }); txt(svg, 120, 72, "supply", { fill: C.energy, "text-anchor": "start", "font-size": 12 }); }; pr.addEventListener("input", draw); btn.addEventListener("click", () => { let P = +pr.value, n = 0; const step = () => { const g = Sf(P) - D(P); const dg = (Sf(P + .01) - D(P + .01) - g) / .01; P = Math.max(1, Math.min(20, P - g / dg)); pr.value = P.toFixed(2); pr.dispatchEvent(new Event("input")); if (Math.abs(g) > .05 && ++n < 12) setTimeout(step, 350); }; step(); }); draw(); };
  TOYS.gcamdata = (host) => { const C = SYS(), { row, svg } = ui(host); const sel = document.createElement("select"); ["IEA energy balances", "FAO crop production", "SSP population", "Vehicle costs (UC Davis)"].forEach((t) => { const o = document.createElement("option"); o.textContent = t; sel.append(o); }); const l = document.createElement("label"); l.append("Change this input: ", sel); row.append(l); const chains = [["L1 energy balances", "L2 energy supply", "L2 transport", "energy XML", "transport XML"], ["L1 ag production", "L2 land allocation", "L2 ag supply", "land XML"], ["L1 socioeconomics", "L2 demand drivers", "socio XML", "transport XML", "building XML"], ["L2 transport", "transport XML"]]; const draw = () => { svg.innerHTML = ""; const ch = chains[sel.selectedIndex]; const all = ["L1 energy balances", "L1 ag production", "L1 socioeconomics", "L2 energy supply", "L2 land allocation", "L2 demand drivers", "L2 transport", "L2 ag supply", "energy XML", "land XML", "socio XML", "transport XML", "building XML"]; all.forEach((t, i) => { const x = 40 + (i % 5) * 112, y = 30 + Math.floor(i / 5) * 60; const on = ch.includes(t); el("rect", { x, y, width: 100, height: 36, rx: 6, fill: on ? C.energy : C.line, "fill-opacity": on ? .5 : .4 }, svg); txt(svg, x + 50, y + 22, t, { "font-size": 10.5 }); }); txt(svg, 300, 212, `${ch.length} chunks and files must be rebuilt (illustrative dependency graph)`, { "font-size": 12, fill: C.muted }); }; sel.addEventListener("change", draw); draw(); };
  function mountToy(host) { if (host.dataset.ready) return; host.dataset.ready = "1"; const f = TOYS[host.dataset.toy]; f && f(host); }

  // ---------------- three.js scenes ----------------
  const T = window.THREE;
  function hex(c) { return new T.Color(c); }
  function mat(color, o = {}) { return new T.MeshStandardMaterial(Object.assign({ color: hex(color), roughness: .6, metalness: .05 }, o)); }
  function label(text, color, size = 128) { color = color || css("--ink"); const c = document.createElement("canvas"); c.width = 1024; c.height = size; const g = c.getContext("2d"); g.font = `600 ${size * .36}px Archivo, Arial, sans-serif`; g.textAlign = "center"; g.fillStyle = color; g.fillText(text, 512, size * .62, 1000); const tx = new T.CanvasTexture(c); const sp = new T.Sprite(new T.SpriteMaterial({ map: tx, transparent: true, depthWrite: false })); sp.scale.set(4.8, 4.8 * size / 1024, 1); return sp; }
  function orbit(cam, dom, opts = {}) {
    let th = opts.theta || .7, ph = opts.phi || 1.05, r = opts.r || 12, drag = null, auto = !reduce; const target = new T.Vector3(0, opts.y || 0, 0);
    const upd = () => { cam.position.set(target.x + r * Math.sin(ph) * Math.sin(th), target.y + r * Math.cos(ph), target.z + r * Math.sin(ph) * Math.cos(th)); cam.lookAt(target); };
    dom.addEventListener("pointerdown", (e) => { drag = [e.clientX, e.clientY]; auto = false; dom.setPointerCapture(e.pointerId); });
    dom.addEventListener("pointermove", (e) => { if (!drag) return; th -= (e.clientX - drag[0]) * .008; ph = Math.max(.2, Math.min(1.5, ph - (e.clientY - drag[1]) * .008)); drag = [e.clientX, e.clientY]; upd(); });
    dom.addEventListener("pointerup", () => (drag = null)); dom.addEventListener("pointercancel", () => (drag = null));
    dom.addEventListener("wheel", (e) => { e.preventDefault(); r = Math.max(4, Math.min(40, r * (1 + e.deltaY * .001))); upd(); }, { passive: false });
    upd(); return { tick(dt) { if (auto) { th += dt * .12; upd(); } }, stop() { auto = false; } };
  }
  const SCENES = {};
  function lights(scene) { scene.add(new T.HemisphereLight(0xffffff, 0x8899aa, .9)); const d = new T.DirectionalLight(0xffffff, .7); d.position.set(5, 10, 6); scene.add(d); }
  function cube(scene, x, y, z, w, h, d, color, text) { const m = new T.Mesh(new T.BoxGeometry(w, h, d), mat(color, { transparent: true, opacity: .85 })); m.position.set(x, y, z); scene.add(m); if (text) { const l = label(text); l.position.set(x, y + h / 2 + .5, z); scene.add(l); } return m; }
  function particles(scene, n, color, size = .13) { const g = new T.BufferGeometry(); g.setAttribute("position", new T.BufferAttribute(new Float32Array(n * 3), 3)); const p = new T.Points(g, new T.PointsMaterial({ color: hex(color), size })); scene.add(p); return p; }
  function ground(scene, w, d, color) { const m = new T.Mesh(new T.PlaneGeometry(w, d), mat(color, { transparent: true, opacity: .35 })); m.rotation.x = -Math.PI / 2; m.position.y = -.01; scene.add(m); return m; }

  SCENES.hector = (scene, C) => {
    const atm = cube(scene, 0, 4, 0, 3, 1.2, 3, C.climate, "atmosphere"); [["vegetation", -3.2, 1.8, 1.5], ["detritus", -3.2, 1.0, .5], ["soil", -3.2, .25, 1.1]].forEach(([t, x, y, h]) => cube(scene, x, y, 0, 2.2, h * .9, 2.2, C.land, t));
    const oc = [["surface", 3.2, 1.9, .6], ["intermediate", 3.2, 1.1, .9], ["deep", 3.2, -.2, 2.2]].map(([t, x, y, h]) => cube(scene, x, y, 0, 2.6, h * .9, 2.6, C.water, t));
    ground(scene, 14, 8, C.line);
    const therm = new T.Mesh(new T.CylinderGeometry(.18, .18, 1, 16), mat(C.climate)); therm.position.set(0, 1.2, 2.6); scene.add(therm); const tl = label("temperature"); tl.position.set(0, .2, 2.6); scene.add(tl);
    const P = particles(scene, 240, C.ink, .11), pos = P.geometry.attributes.position.array, st = [];
    for (let i = 0; i < 240; i++) st.push({ t: Math.random(), path: i % 3, sp: .15 + Math.random() * .2 });
    const paths = [[[0, 4, 0], [-3.2, 1.8, 0], [-3.2, 1.0, 0], [-3.2, .25, 0]], [[0, 4, 0], [3.2, 1.9, 0], [3.2, 1.1, 0], [3.2, -.2, 0]], [[0, 6.5, 0], [0, 4, 0]]];
    let time = 0;
    return (dt) => { time += dt; const fill = Math.min(1, time / 25); atm.scale.y = .6 + fill * .9; atm.position.y = 4 + (atm.scale.y - 1) * .6; therm.scale.y = .6 + fill * 1.4; therm.position.y = .7 + therm.scale.y * .5; oc[2].material.opacity = .5 + fill * .35;
      for (let i = 0; i < 240; i++) { const s = st[i]; s.t += dt * s.sp * (s.path === 1 ? .6 : 1); if (s.t > 1) s.t = 0; const pth = paths[s.path], k = s.t * (pth.length - 1), j = Math.min(pth.length - 2, Math.floor(k)), f = k - j; const a = pth[j], b = pth[j + 1]; pos[i * 3] = a[0] + (b[0] - a[0]) * f + (Math.random() - .5) * .5; pos[i * 3 + 1] = a[1] + (b[1] - a[1]) * f + (Math.random() - .5) * .3; pos[i * 3 + 2] = a[2] + (b[2] - a[2]) * f + (Math.random() - .5) * .5; } P.geometry.attributes.position.needsUpdate = true; };
  };

  SCENES.xanthos = (scene, C) => {
    const N = 14, S = .7, hts = []; const geo = new T.BoxGeometry(S * .96, 1, S * .96);
    for (let r = 0; r < N; r++) for (let c = 0; c < N; c++) { const h = .3 + 2.2 * Math.max(0, 1 - Math.hypot(r - N + 1, c) / N) + .15 * Math.sin(r * 1.3) * Math.cos(c * 1.1); hts.push(h); const m = new T.Mesh(geo, mat(C.land, { opacity: .9, transparent: true })); m.scale.y = h; m.position.set((c - N / 2) * S, h / 2, (r - N / 2) * S); m.material.color.lerp(hex(C.paper), (h - .3) / 2.6 * .5); scene.add(m); }
    const outlet = new T.Mesh(new T.CylinderGeometry(.6, .6, .3, 24), mat(C.water)); outlet.position.set((-N / 2) * S - .6, .15, (N / 2) * S); scene.add(outlet); const ol = label("basin outlet"); ol.position.set(outlet.position.x, 1.2, outlet.position.z); scene.add(ol);
    const rain = particles(scene, 300, C.water, .1), rp = rain.geometry.attributes.position.array, rs = []; for (let i = 0; i < 300; i++) rs.push({ x: (Math.random() - .5) * N * S, z: (Math.random() - .5) * N * S, y: Math.random() * 6, flow: false, t: 0 });
    const counter = label("0 km³", C.water); counter.position.set(outlet.position.x, 2, outlet.position.z); scene.add(counter); let tot = 0, acc = 0;
    const hAt = (x, z) => { const c = Math.round(x / S + N / 2), r = Math.round(z / S + N / 2); return (r >= 0 && r < N && c >= 0 && c < N) ? hts[r * N + c] : 0; };
    return (dt) => { for (let i = 0; i < 300; i++) { const s = rs[i]; if (!s.flow) { s.y -= dt * 3; if (s.y <= hAt(s.x, s.z)) { s.flow = true; s.t = 0; } } else { s.t += dt; const gx = hAt(s.x - .3, s.z) - hAt(s.x + .3, s.z), gz = hAt(s.x, s.z - .3) - hAt(s.x, s.z + .3); s.x += (gx * 2 - .4) * dt; s.z += (gz * 2 + .4) * dt; s.y = hAt(s.x, s.z) + .08; if (s.x < outlet.position.x || s.z > outlet.position.z || s.t > 6) { if (s.t <= 6) acc += 1; s.flow = false; s.x = (Math.random() - .5) * N * S; s.z = (Math.random() - .5) * N * S; s.y = 5 + Math.random() * 2; } } rp[i * 3] = s.x; rp[i * 3 + 1] = s.y; rp[i * 3 + 2] = s.z; } rain.geometry.attributes.position.needsUpdate = true; if (acc >= 10) { tot += 1; acc = 0; counter.material = label(`${tot} km³ (illustrative)`, C.water).material; } };
  };

  SCENES.tethys = (scene, C) => {
    const N = 8, S = .55; ground(scene, 12, 8, C.line);
    const big = cube(scene, -4, 1.6, 0, 1.6, 3.2, 1.6, C.water, "region total"); const cells = [], base = [];
    for (let r = 0; r < N; r++) for (let c = 0; c < N; c++) { const v = .15 + .85 * Math.abs(Math.sin(r * 2.1 + c * 1.3)) * (1 - Math.hypot(r - 3.5, c - 3.5) / 7); base.push(v); const m = new T.Mesh(new T.BoxGeometry(S * .9, 1, S * .9), mat(c % 3 === 0 ? C.land : C.water, { transparent: true, opacity: .9 })); m.position.set(1 + (c - N / 2) * S, 0, (r - N / 2) * S); m.scale.y = .01; scene.add(m); cells.push(m); }
    const gl = label("grid cells (proxy heights)"); gl.position.set(1, 2.6, 0); scene.add(gl); const ml = label("month 1"); ml.position.set(1, 3.3, 0); scene.add(ml); let time = 0, month = 0;
    const M = ["Jan", "Mar", "May", "Jul", "Sep", "Nov"];
    return (dt) => { time += dt; const f = Math.min(1, time / 4); big.scale.y = 1 - f * .85; big.position.y = 1.6 * big.scale.y; const sum = base.reduce((a, b) => a + b, 0); const season = .5 + .5 * Math.sin(time * .8); cells.forEach((m, i) => { const c = i % N; const h = f * (base[i] / sum) * 40 * (c % 3 === 0 ? .4 + .9 * season : 1); m.scale.y = Math.max(.01, h); m.position.y = h / 2; }); const mo = Math.floor((time * .8 / (Math.PI * 2)) * 6) % 6; if (mo !== month) { month = mo; ml.material = label(`month: ${M[mo]} (irrigation cells pulse)`).material; } };
  };

  SCENES.demeter = (scene, C) => {
    const N = 12, S = .6; const cells = []; for (let r = 0; r < N; r++) for (let c = 0; c < N; c++) { const d = Math.hypot(r - 5, c - 4); const m = new T.Mesh(new T.BoxGeometry(S * .92, 1, S * .92), mat(C.land, { transparent: true, opacity: .9 })); m.position.set((c - N / 2) * S, .2, (r - N / 2) * S); m.scale.y = .4; m.userData = { crop: d < 1.8 ? .5 : 0, forest: d > 4 ? 1 : 0, d }; scene.add(m); cells.push(m); }
    const lg = label("cropland rises, forest shrinks"); lg.position.set(0, 3.2, 0); scene.add(lg); const ph = label("phase: intensify"); ph.position.set(0, 2.6, 0); scene.add(ph); let time = 0, phase = 0;
    return (dt) => { time += dt; const t = time % 14; const inten = Math.min(1, t / 5), exp = Math.max(0, Math.min(1, (t - 5) / 6)); const np = t < 5 ? 0 : t < 11 ? 1 : 2; if (np !== phase) { phase = np; ph.material = label(["phase: intensify", "phase: expand", "phase: done"][np]).material; }
      cells.forEach((m) => { const u = m.userData; let crop = u.crop; if (u.crop) crop = u.crop + (1 - u.crop) * inten; else if (u.d < 3.2) crop = exp * Math.max(0, 1 - (u.d - 1.8) / 1.6); const forest = u.forest * (1 - exp * .5); const h = .4 + crop * 1.4 + forest * .9; m.scale.y = h; m.position.y = h / 2; m.material.color.copy(hex(C.land)).lerp(hex(C.energy), crop).lerp(hex(C.policy), forest * .5 * (1 - crop)); }); };
  };

  SCENES.moirai = (scene, C) => {
    const layers = [["HYDE land use", C.land], ["SAGE crops", C.energy], ["carbon", C.climate], ["basins × countries", C.water]]; const planes = layers.map(([t, c], i) => { const m = new T.Mesh(new T.PlaneGeometry(6, 4), mat(c, { transparent: true, opacity: .45, side: T.DoubleSide })); m.rotation.x = -Math.PI / 2; m.position.y = 4 - i * 1.1; scene.add(m); const l = label(t); l.position.set(-3.6, m.position.y + .3, -2); scene.add(l); return m; });
    const lines = new T.LineSegments(new T.EdgesGeometry(new T.PlaneGeometry(6, 4, 3, 2)), new T.LineBasicMaterial({ color: hex(C.ink) })); lines.rotation.x = -Math.PI / 2; lines.position.y = 4 - 3 * 1.1 + .02; scene.add(lines);
    const pieces = []; for (let r = 0; r < 2; r++) for (let c = 0; c < 3; c++) { const m = new T.Mesh(new T.BoxGeometry(1.9, .3, 1.9), mat(layers[(r * 3 + c) % 3][1])); m.position.set((c - 1) * 2, -2, (r - .5) * 2); scene.add(m); pieces.push(m); }
    const tl = label("one row per land unit"); tl.position.set(0, -1.2, 0); scene.add(tl); let time = 0;
    return (dt) => { time += dt; const t = time % 8; const f = Math.min(1, t / 4); planes.forEach((m, i) => { m.position.y = 4 - i * 1.1 * (1 - f * .9); }); lines.position.y = planes[3].position.y + .02; pieces.forEach((m, i) => { const g = Math.max(0, Math.min(1, (t - 4 - i * .3) / 2)); m.position.y = planes[3].position.y - .3 - g * 2.2; m.scale.setScalar(.2 + g * .8); }); };
  };

  SCENES.land = (scene, C) => {
    const slab = new T.Mesh(new T.BoxGeometry(8, .3, 5), mat(C.line)); slab.position.y = -.15; scene.add(slab);
    const uses = [["crops", C.energy], ["pasture", C.land], ["forest", C.policy]]; const segs = uses.map(([t, c]) => { const m = new T.Mesh(new T.BoxGeometry(1, .3, 5), mat(c, { transparent: true, opacity: .85 })); m.position.y = .05; scene.add(m); const l = label(t); l.position.set(0, .8, 3.2); scene.add(l); m.userData.l = l; return m; });
    const bars = uses.map(([t, c], i) => { const m = new T.Mesh(new T.BoxGeometry(.6, 1, .6), mat(c)); m.position.set(-2 + i * 2, .5, -4); scene.add(m); return m; }); const bl = label("profit per hectare"); bl.position.set(0, 3.2, -4); scene.add(bl); const pl = label("crop price rising"); pl.position.set(0, 2.4, 0); scene.add(pl); let time = 0;
    return (dt) => { time += dt; const p = .5 + .5 * Math.sin(time * .5); const prof = [1.2 + 2 * p, 1.4, 1.1]; const w = prof.map((x) => Math.pow(x, 2)), S = w.reduce((a, b) => a + b, 0); let x = -4; segs.forEach((m, i) => { const ww = 8 * w[i] / S; m.scale.x = ww; m.position.x = x + ww / 2; m.userData.l.position.x = x + ww / 2; x += ww; }); bars.forEach((m, i) => { m.scale.y = prof[i]; m.position.y = prof[i] / 2; }); };
  };

  SCENES.economy = (scene, C) => {
    ground(scene, 14, 10, C.line); const mk = [["oil", C.energy], ["electricity", C.energy], ["crops", C.land], ["water", C.water], ["carbon", C.climate]]; const scales = mk.map(([t, c], i) => { const g = new T.Group(); const post = new T.Mesh(new T.CylinderGeometry(.06, .06, 2, 8), mat(C.ink)); post.position.y = 1; g.add(post); const beam = new T.Mesh(new T.BoxGeometry(2.4, .08, .2), mat(C.ink)); beam.position.y = 2; g.add(beam); const l = new T.Mesh(new T.BoxGeometry(.7, .1, .7), mat(c)); l.position.set(-1.1, 1.6, 0); g.add(l); const r = new T.Mesh(new T.BoxGeometry(.7, .1, .7), mat(c)); r.position.set(1.1, 1.6, 0); g.add(r); g.position.set((i - 2) * 2.8, 0, 0); scene.add(g); const lb = label(t); lb.position.set(g.position.x, 2.9, 0); scene.add(lb); return { g, beam, l, r, ang: (Math.random() - .5) * .6, vel: 0 }; });
    const gdp = new T.Mesh(new T.BoxGeometry(1.2, 1, 1.2), mat(C.economy)); gdp.position.set(5.5, .5, -3.5); scene.add(gdp); const gl = label("GDP (macro loop)"); gl.position.set(5.5, 2.2, -3.5); scene.add(gl); let time = 0;
    return (dt) => { time += dt; scales.forEach((s, i) => { const nb = scales[(i + 1) % 5]; s.vel += (-s.ang * 2 - s.vel * .8 + nb.ang * .4) * dt * 3; s.ang += s.vel * dt * 3; if (time % 9 < dt) { s.ang += (Math.random() - .5) * .7; } s.beam.rotation.z = s.ang; s.l.position.y = 1.6 - Math.sin(s.ang) * 1.1; s.r.position.y = 1.6 + Math.sin(s.ang) * 1.1; }); const e = Math.abs(scales[0].ang) + Math.abs(scales[1].ang); gdp.scale.y = 1.6 - Math.min(1, e); gdp.position.y = gdp.scale.y / 2; };
  };

  SCENES.gcamdata = (scene, C) => {
    const belt = new T.Mesh(new T.BoxGeometry(14, .2, 1.6), mat(C.ink, { opacity: .6, transparent: true })); scene.add(belt);
    const st = ["raw", "L0/L1", "L2", "calibrate", "XML"]; const cols = [C.policy, C.economy, C.economy, C.energy, C.water]; st.forEach((t, i) => { const m = new T.Mesh(new T.BoxGeometry(1.2, 2, 2.2), mat(C.line, { transparent: true, opacity: .35 })); m.position.set(-5.5 + i * 2.75, 1, 0); scene.add(m); const l = label(t); l.position.set(m.position.x, 2.6, 0); scene.add(l); });
    const core = new T.Mesh(new T.CylinderGeometry(1, 1, 1.2, 6), mat(C.climate)); core.position.set(7.5, .7, 0); scene.add(core); const cl = label("GCAM core"); cl.position.set(7.5, 2.2, 0); scene.add(cl);
    const side = new T.Mesh(new T.BoxGeometry(4, .15, 1), mat(C.energy, { opacity: .6, transparent: true })); side.position.set(4, .1, 2.2); side.rotation.y = -.5; scene.add(side); const sl = label("add-on XML"); sl.position.set(3.4, 1, 3); scene.add(sl);
    const cubes = []; for (let i = 0; i < 6; i++) { const m = new T.Mesh(new T.BoxGeometry(.6, .6, .6), mat(cols[0])); m.userData.t = i / 6; scene.add(m); cubes.push(m); }
    return (dt) => { cubes.forEach((m) => { m.userData.t = (m.userData.t + dt * .06) % 1; const x = -6.5 + m.userData.t * 14; m.position.set(x, .5 + Math.abs(Math.sin(m.userData.t * 20)) * .1, 0); const stage = Math.min(4, Math.max(0, Math.floor((x + 6) / 2.75))); m.material.color.copy(hex(cols[stage])); m.rotation.y = m.userData.t * 8; m.scale.setScalar(stage === 4 ? .6 : 1); }); core.rotation.y += dt * .5; };
  };

  SCENES.family = (scene, C, host) => {
    const core = new T.Mesh(new T.IcosahedronGeometry(1.4, 1), mat(C.climate, { flatShading: true })); scene.add(core); const cl = label("GCAM core"); cl.position.y = 2.3; scene.add(cl);
    const members = [["hector", "Hector", C.climate, "in"], ["land", "Land module", C.land, "in"], ["economy", "Economy", C.economy, "in"], ["xanthos", "Xanthos", C.water, "before"], ["moirai", "moirai", C.land, "before"], ["gcamdata", "gcamdata", C.policy, "before"], ["tethys", "Tethys", C.water, "after"], ["demeter", "Demeter", C.land, "after"]];
    const objs = members.map(([k, n, c, w], i) => { const m = new T.Mesh(w === "in" ? new T.SphereGeometry(.55, 24, 16) : new T.BoxGeometry(1, 1, 1), mat(c)); const l = label(n); m.userData = { k, w, i, l }; scene.add(m); scene.add(l); return m; });
    const lineMat = new T.LineBasicMaterial({ color: hex(C.muted) }); const links = objs.map((m) => { const g = new T.BufferGeometry().setFromPoints([new T.Vector3(), m.position]); const ln = new T.Line(g, lineMat); scene.add(ln); return ln; });
    const l1 = label("runs before", C.muted), l2 = label("runs after", C.muted); l1.position.set(-7, 3.2, 0); l2.position.set(7, 3.2, 0); scene.add(l1, l2); let time = 0;
    const ray = new T.Raycaster(), mouse = new T.Vector2(); host.style.cursor = "pointer";
    host.addEventListener("click", (e) => { const r = host.getBoundingClientRect(); mouse.set(((e.clientX - r.left) / r.width) * 2 - 1, -((e.clientY - r.top) / r.height) * 2 + 1); ray.setFromCamera(mouse, host._cam); const hit = ray.intersectObjects(objs)[0]; if (hit && window.openFamilyDeck) window.openFamilyDeck(hit.object.userData.k); });
    return (dt) => { time += dt; core.rotation.y += dt * .3; objs.forEach((m, i) => { const u = m.userData; if (u.w === "in") { const a = time * .4 + i * 2.1; m.position.set(Math.cos(a) * 3, Math.sin(a * 2) * .4, Math.sin(a) * 3); } else { const side = u.w === "before" ? -1 : 1; const j = u.w === "before" ? i - 3 : i - 6; m.position.set(side * 7, 1.2 - j * 1.6, (j - 1) * 1.5); m.rotation.y += dt * .5; } u.l.position.set(m.position.x, m.position.y + .9, m.position.z); links[i].geometry.setFromPoints([new T.Vector3(), m.position]); }); };
  };

  const live = new Set();
  function mount3d(host) {
    if (host.dataset.ready || !T) return; const mk = SCENES[host.dataset.scene]; if (!mk) return; host.dataset.ready = "1";
    let renderer; try { renderer = new T.WebGLRenderer({ antialias: true, alpha: true }); } catch (e) { return; }
    const C = SYS(); const scene = new T.Scene(); lights(scene); const cam = new T.PerspectiveCamera(42, 16 / 9, .1, 200); host._cam = cam;
    const wide = host.classList.contains("f3d-wide"), mini = host.dataset.mini; const R = { gcamdata: 19, economy: 19, xanthos: 15, moirai: 14 }; const ctl = orbit(cam, renderer.domElement, { r: wide ? 17 : (R[host.dataset.scene] || 13), phi: mini ? 1.2 : 1.05, y: 1 });
    if (mini) ctl.stop();
    const tick = mk(scene, C, host); host.append(renderer.domElement); host.classList.add("ready");
    if (!mini) { const hint = document.createElement("span"); hint.className = "f3d-hint"; hint.textContent = "drag to orbit · scroll to zoom"; host.append(hint); }
    const size = () => { const w = host.clientWidth, h = host.clientHeight; renderer.setSize(w, h, false); renderer.setPixelRatio(Math.min(2, devicePixelRatio)); cam.aspect = w / h; cam.updateProjectionMatrix(); }; size(); new ResizeObserver(size).observe(host);
    let last = performance.now(); const o = { host, frame() { const now = performance.now(), dt = Math.min(.05, (now - last) / 1000); last = now; tick(reduce ? 0 : dt); ctl.tick(dt); renderer.render(scene, cam); } };
    live.add(o); if (reduce) o.frame();
  }
  function loop() { live.forEach((o) => { const r = o.host.getBoundingClientRect(); if (r.bottom > 0 && r.top < innerHeight && o.host.offsetParent !== null) o.frame(); }); requestAnimationFrame(loop); }

  document.addEventListener("DOMContentLoaded", () => { $$(".fdeck").forEach(deck); tabs(); $$(".f3d-wide").forEach(mount3d); if (!reduce) loop(); else document.addEventListener("scroll", () => live.forEach((o) => o.frame())); });
})();
