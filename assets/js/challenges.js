/* Simulation challenges: predict, then steer a small model to a goal, with animated feedback.
   Also adds progress bars, animations and a celebration to every multiple-choice quiz on the page.
   Challenge data: window.CHALLENGES[module] = [{title, level, icon, model, fixed, controls[], metric, op, target, tol, view, gmin, gmax, unit,
   goal, predict:{q, options[], answer}, hint, explain, solution}]. All numbers are teaching toys. */
(function () {
  "use strict";
  const NS = "http://www.w3.org/2000/svg";
  const $ = (s, r = document) => r.querySelector(s), $$ = (s, r = document) => Array.from(r.querySelectorAll(s));
  const css = (v) => getComputedStyle(document.documentElement).getPropertyValue(v).trim();
  const fmt = (x, d = 0) => (isFinite(x) ? Number(x).toLocaleString("en-US", { minimumFractionDigits: d, maximumFractionDigits: d }) : "–");
  const reduce = window.matchMedia && matchMedia("(prefers-reduced-motion: reduce)").matches;
  const h = (tag, attrs = {}, ...kids) => { const e = document.createElement(tag); for (const [k, v] of Object.entries(attrs)) { if (k === "class") e.className = v; else if (k === "html") e.innerHTML = v; else if (k.startsWith("on")) e.addEventListener(k.slice(2), v); else e.setAttribute(k, v); } kids.flat().forEach((c) => c != null && e.append(c.nodeType ? c : document.createTextNode(c))); return e; };
  const sv = (t, a, p) => { const e = document.createElementNS(NS, t); for (const k in a) e.setAttribute(k, a[k]); if (p) p.append(e); return e; };
  const icon = (name) => `<svg viewBox="0 0 24 24" aria-hidden="true"><path d="${(window.GCAM_ICONS || {})[name] || ""}"/></svg>`;
  const range = (a, b, s = 1) => { const r = []; for (let x = a; x <= b + 1e-9; x += s) r.push(+x.toFixed(6)); return r; };
  const logit = (costs, lam) => { const w = costs.map((c) => Math.pow(Math.max(c, 1e-6), lam)); const s = w.reduce((a, b) => a + b, 0); return w.map((x) => x / s); };

  // ------------------------------------------------------------------ toy models: (params) -> {value, line?, bars?}
  const M = {
    warming(p) { // cumulative CO2 -> warming, 0.45 °C per 1000 Gt (TCRE best estimate)
      const yrs = range(2020, 2100), peak = p.peak ?? 2025, z = Math.max(p.nz, peak + 5), g = (p.grow ?? 0) / 100, e0 = 40;
      const ep = e0 * Math.pow(1 + g, peak - 2020); let cum = 0;
      const em = yrs.map((y) => (y <= peak ? e0 * Math.pow(1 + g, y - 2020) : y >= z ? 0 : ep * (1 - (y - peak) / (z - peak))));
      const t = em.map((e) => { cum += e; return 1.1 + (0.45 * cum) / 1000; });
      return { value: { t2100: t[t.length - 1], cum }, line: { xs: yrs, series: [{ name: "Warming (°C)", values: t }], yMin: 1, yMax: 3, hline: { y: p.line ?? 1.5, label: (p.line ?? 1.5) + " °C" }, yTitle: "°C" } };
    },
    kaya(p) { // CO2 (Gt) = people (bn) × GDP per person (k$) × energy per $ (MJ) × CO2 per MJ (g)
      const co2 = p.pop * p.gdp * p.ei * p.ci / 1000;
      return { value: { co2 }, bars: { labels: ["2020 (about 33 Gt)", "Your 2050"], values: [33, co2], suffix: " Gt" } };
    },
    carbonprice(p) { // straight-line cost curve from module 1.4: price = 2 × cut %
      const yrs = range(2025, 2100, 5), price = yrs.map((y) => p.p0 * Math.pow(1 + p.g / 100, y - 2025)), cut = price.map((x) => Math.min(100, x / 2));
      const c50 = cut[yrs.indexOf(2050)];
      return { value: { cut2050: c50, p2050: price[yrs.indexOf(2050)] }, line: { xs: yrs, series: [{ name: "Cut below Reference (%)", values: cut }], yMax: 100, yTitle: "% cut", hline: { y: p.line ?? 60, label: (p.line ?? 60) + "% cut" } } };
    },
    market(p) { // demand Q = 100 − P, supply Q = P − t (tax t per unit)
      const q = Math.max(0, (100 - p.tax) / 2), pc = 100 - q;
      return { value: { q, price: pc, revenue: q * p.tax }, bars: { labels: ["Quantity sold", "Price buyers pay", "Tax revenue ÷ 10"], values: [q, pc, (q * p.tax) / 10] } };
    },
    logit(p) { // relative-cost logit: share_i ∝ cost_i^λ  (λ negative)
      const names = p.names || ["Option A", "Option B", "Option C"], costs = names.map((_, i) => p["c" + i]);
      const s = logit(costs, p.lam).map((x) => x * 100);
      return { value: { s0: s[0], s1: s[1], s2: s[2] }, bars: { labels: names, values: s, suffix: "%" } };
    },
    discount(p) { // present value of a damage D in T years at rate r
      const pv = p.dmg / Math.pow(1 + p.r / 100, p.T);
      const yrs = range(0, 100, 5);
      return { value: { pv }, line: { xs: yrs, series: [{ name: "Value today of $100 of damage", values: yrs.map((t) => 100 / Math.pow(1 + p.r / 100, t)) }], yMax: 100, yTitle: "$ today", vline: { x: p.T, label: "your year" } } };
    },
    feedback(p) { // CO2 stock: dC/dt = E − k·(C − 280)·(1 − f·ΔT); ΔT from ppm
      const yrs = range(2020, 2150), out = []; let C = 415, E = 40 / 7.8; // ppm per year at 40 Gt
      yrs.forEach((y) => {
        const e = y < p.nz ? E * (1 - (y - 2020) / (p.nz - 2020)) : 0;
        const dT = 3 * Math.log2(C / 280) * 0.55, sink = (p.k / 100) * (C - 280) * Math.max(0, 1 - (p.f / 100) * dT);
        C += e - sink; out.push(C);
      });
      return { value: { peak: Math.max(...out), end: out[out.length - 1] }, line: { xs: yrs, series: [{ name: "CO2 concentration (ppm)", values: out }], yMin: 300, yMax: 600, yTitle: "ppm", hline: { y: p.line ?? 450, label: (p.line ?? 450) + " ppm" } } };
    },
    macc(p) { // marginal abatement cost curve: options adopted if cost ≤ price
      const opts = [["Efficiency", -20, 4], ["Methane fixes", 10, 2.5], ["Wind and solar", 25, 7], ["Electric cars", 60, 3.5], ["Industry fuel switch", 90, 4], ["CCS", 120, 3], ["Direct air capture", 300, 4]];
      const ab = opts.reduce((a, o) => a + (o[1] <= p.price ? o[2] : 0), 0);
      return { value: { ab }, bars: { labels: opts.map((o) => o[0]), values: opts.map((o) => (o[1] <= p.price ? o[2] : 0)), suffix: "" } };
    },
    nexus(p) { // basin water: demand from irrigation, power cooling, cities vs renewable supply 100
      const irr = 60 * (p.food / 100) * (1 - p.eff / 100), cool = 15 * (p.power / 100) * (p.dry ? 0.1 : 1), city = 12 * (p.pop / 100), bio = 0.12 * p.bio;
      const d = irr + cool + city + bio;
      return { value: { stress: d }, bars: { labels: ["Irrigation", "Power cooling", "Cities", "Bioenergy crops"], values: [irr, cool, city, bio], suffix: "" } };
    },
    uncertainty(p) { // P(warming > threshold) when TCRE ~ normal(0.45, 0.11) per 1000 Gt; base 1.1 °C
      const cum = p.cum, mu = 1.1 + 0.45 * cum / 1000, sd = 0.11 * cum / 1000 + 0.05, z = (p.thr - mu) / sd;
      const P = 100 * (1 - 0.5 * (1 + erf(z / Math.SQRT2)));
      const xs = range(1, 4, 0.05);
      return { value: { prob: P, mid: mu }, line: { xs, series: [{ name: "Chance of each warming level", values: xs.map((x) => Math.exp(-0.5 * Math.pow((x - mu) / sd, 2))) }], yMax: 1.05, yTitle: "relative likelihood", vline: { x: p.thr, label: p.thr + " °C" }, area: true } };
    },
    trncost(p) { // generalised cost = money + value of time × hours; absolute-cost logit
      const vot = p.wage * (p.votf ?? 0.5), gc = [p.carMoney + vot * p.carT, p.busMoney + vot * p.busT, p.railMoney + vot * p.railT];
      const w = gc.map((g) => Math.exp(-p.beta * g)), s = w.reduce((a, b) => a + b, 0), sh = w.map((x) => (100 * x) / s);
      return { value: { car: sh[0], bus: sh[1], rail: sh[2] }, bars: { labels: ["Car", "Bus", "Rail"], values: sh, suffix: "%" } };
    },
    loadfactor(p) { // cost per passenger-km = vehicle cost per km ÷ load factor
      const car = p.carVkm / p.lf, bus = p.busVkm / p.blf;
      return { value: { car, bus, ratio: car / bus }, bars: { labels: ["Car $/pkm", "Bus $/pkm"], values: [car, bus], digits: 2 } };
    },
    lmdi(p) { // CO2 = activity × structure × intensity × carbon factor (index form)
      const r = (1 + p.a / 100) * (1 + p.s / 100) * (1 + p.i / 100) * (1 + p.c / 100);
      return { value: { change: (r - 1) * 100 }, bars: { labels: ["Activity", "Mode structure", "Energy intensity", "Carbon of fuel", "Total"], values: [p.a, p.s, p.i, p.c, (r - 1) * 100].map((x) => x + 100), suffix: "" } };
    },
    hotelling(p) { // perfect-foresight least cost: carbon price rises at the discount rate
      const yrs = range(2025, 2100, 5), pr = yrs.map((y) => p.p0 * Math.pow(1 + p.r / 100, y - 2025));
      return { value: { p2050: pr[5], p2100: pr[pr.length - 1] }, line: { xs: yrs, series: [{ name: "Carbon price ($/t)", values: pr.map((x) => Math.min(x, 2000)) }], yTitle: "$ per t CO2", yMax: 2000 } };
    },
    dice(p) { // one-shot cost–benefit: abatement cost = a·μ^2.6, avoided damage = d·μ, discounted over 50 years
      const disc = 1 / Math.pow(1 + p.r / 100, 50), a = 2.0, d = p.dmg * disc * 4;
      const mus = range(0, 1.2, 0.01), net = mus.map((m) => d * m - a * Math.pow(m, 2.6));
      let best = 0; net.forEach((v, i) => { if (v > net[best]) best = i; });
      return { value: { mu: mus[best] * 100 }, line: { xs: mus.map((m) => m * 100), series: [{ name: "Benefit − cost of cutting (toy units)", values: net }], yMin: -2, yMax: 4, yTitle: "net benefit", vline: { x: mus[best] * 100, label: "optimum" } } };
    },
    game(p) { // two regions: benefit b·(a1 + a2), cost a_i²/2. Nash a = b; full cooperation a = 2b
      const b = p.b, nash = b, coop = 2 * b, a = nash + (coop - nash) * (p.coop / 100), tot = 2 * a;
      return { value: { total: tot }, bars: { labels: ["Each region if acting alone", "Each region now", "Each region if fully cooperative"], values: [nash, a, coop], digits: 1 } };
    },
    ramsey(p) { // Ramsey rule: interest rate r = ρ + η·g
      const r = p.rho + p.eta * p.g;
      return { value: { r }, bars: { labels: ["Pure time preference ρ", "η × growth", "Discount rate r"], values: [p.rho, p.eta * p.g, r], digits: 1, suffix: "%" } };
    },
    landgrid(p) { // cropland needed = food demand ÷ yield; share of a 100-cell region
      const need = (p.food * 30) / p.yield + p.bio * 0.6;
      return { value: { cells: need }, bars: { labels: ["Cropland for food", "Energy crops", "Left for forest"], values: [(p.food * 30) / p.yield, p.bio * 0.6, Math.max(0, 100 - need)], digits: 0 } };
    },
    cge(p) { // two-sector economy: carbon tax shifts output from dirty to clean; GDP loss ≈ ½·tax·cut, cut grows with elasticity
      const cut = Math.min(95, 100 * (1 - Math.pow(1 + p.tax / 100, -p.sigma))), loss = 0.5 * (p.tax / 100) * (cut / 100) * 8;
      return { value: { cut, loss }, bars: { labels: ["Emissions cut (%)", "GDP loss (% × 10)"], values: [cut, loss * 10], digits: 1 } };
    },
    downscale(p) { // convergence: country share moves from base share to target share by year T
      const yrs = range(2020, 2100, 5), s = yrs.map((y) => p.s0 + (p.s1 - p.s0) * Math.min(1, (y - 2020) / (p.T - 2020)));
      return { value: { s2050: s[6] }, line: { xs: yrs, series: [{ name: "Country share of regional demand (%)", values: s }], yMax: 100, yTitle: "%" } };
    },
    ensemble(p) { // fraction of runs above a threshold when two uncertain inputs vary uniformly
      let n = 0, hit = 0; for (let i = 0; i < 400; i++) { const u = ((i * 0.618) % 1), v = ((i * 0.414) % 1); const cost = 0.5 + u, gdp = 0.5 + v; const em = 50 * gdp / cost; n++; if (em > p.thr && cost < p.box / 100 + 0.5) hit++; }
      const tot = Array.from({ length: 400 }, (_, i) => 50 * (0.5 + ((i * 0.414) % 1)) / (0.5 + ((i * 0.618) % 1))).filter((e) => e > p.thr).length;
      return { value: { coverage: tot ? (100 * hit) / tot : 0 }, bars: { labels: ["High-emission runs caught by your box (%)"], values: [tot ? (100 * hit) / tot : 0], suffix: "%" } };
    },
  };
  function erf(x) { const t = 1 / (1 + 0.3275911 * Math.abs(x)); const y = 1 - (((((1.061405429 * t - 1.453152027) * t) + 1.421413741) * t - 0.284496736) * t + 0.254829592) * t * Math.exp(-x * x); return x >= 0 ? y : -y; }
  window.IAMToyModels = M;

  // ------------------------------------------------------------------ gauge view
  function gauge(box, v, c) {
    const lo = c.gmin, hi = c.gmax, ang = (x) => Math.PI * (1 - (Math.max(lo, Math.min(hi, x)) - lo) / (hi - lo));
    let s = box.querySelector("svg.ch-gauge");
    if (!s) {
      box.innerHTML = ""; s = sv("svg", { viewBox: "0 0 320 190", class: "ch-gauge", role: "img" }, box);
      const arc = (a0, a1, r) => { const p = (a) => [160 + r * Math.cos(a), 150 - r * Math.sin(a)]; const [x0, y0] = p(a0), [x1, y1] = p(a1); return `M${x0},${y0} A${r},${r} 0 0 1 ${x1},${y1}`; };
      sv("path", { d: arc(Math.PI, 0, 110), stroke: css("--line"), "stroke-width": 22, fill: "none" }, s);
      let t0 = c.op === "<=" ? lo : c.op === ">=" ? c.target : c.target - c.tol, t1 = c.op === "<=" ? c.target : c.op === ">=" ? hi : c.target + c.tol;
      sv("path", { d: arc(ang(t0), ang(t1), 110), stroke: css("--land"), "stroke-width": 22, fill: "none", opacity: 0.55 }, s);
      [lo, (lo + hi) / 2, hi].forEach((x) => { const a = ang(x), t = sv("text", { x: 160 + 140 * Math.cos(a), y: 154 - 140 * Math.sin(a) + 4, "text-anchor": "middle", style: `font:12px var(--body);fill:${css("--muted")}` }, s); t.textContent = fmt(x, hi - lo < 10 ? 1 : 0); });
      const n = sv("g", { class: "needle" }, s);
      sv("line", { x1: 160, y1: 150, x2: 260, y2: 150, stroke: css("--ink"), "stroke-width": 5, "stroke-linecap": "round" }, n);
      sv("circle", { cx: 160, cy: 150, r: 10, fill: css("--ink") }, s);
      const lab = sv("text", { x: 160, y: 182, "text-anchor": "middle", style: `font:600 13px var(--body);fill:${css("--ink-soft")}` }, s); lab.textContent = "green band = goal";
    }
    $(".needle", s).style.transform = `rotate(${-(ang(v) * 180) / Math.PI}deg)`;
  }

  function hit(c, v) { return c.op === "<=" ? v <= c.target + 1e-9 : c.op === ">=" ? v >= c.target - 1e-9 : Math.abs(v - c.target) <= c.tol; }
  function burst(card) {
    if (reduce) return; const fx = h("div", { class: "ch-fx" }); card.append(fx);
    const cols = [css("--water"), css("--energy"), css("--land"), css("--economy"), css("--climate")];
    for (let i = 0; i < 36; i++) { const a = (Math.PI * 2 * i) / 36, r = 120 + Math.random() * 160; const p = h("i"); p.style.background = cols[i % cols.length]; p.style.setProperty("--x", Math.cos(a) * r + "px"); p.style.setProperty("--y", Math.sin(a) * r + "px"); p.style.animationDelay = Math.random() * 0.15 + "s"; fx.append(p); }
    setTimeout(() => fx.remove(), 1500);
  }
  const KEY = "gcam-challenges";
  const store = { load() { try { return JSON.parse(localStorage.getItem(KEY) || "{}"); } catch (e) { return {}; } }, save(d) { try { localStorage.setItem(KEY, JSON.stringify(d)); } catch (e) { } } };

  function countUp(el, to, d, unit) {
    const from = parseFloat(el.dataset.v || to); el.dataset.v = to;
    if (reduce || !isFinite(from)) { el.firstChild.textContent = fmt(to, d) + unit; return; }
    const t0 = performance.now(); const tick = (n) => { const t = Math.min(1, (n - t0) / 350); el.firstChild.textContent = fmt(from + (to - from) * t, d) + unit; if (t < 1) requestAnimationFrame(tick); }; requestAnimationFrame(tick);
  }

  function card(c, idx, mid, onScore) {
    const st = store.load(), key = `${mid}:${idx}`;
    const live = h("div", { class: "ch-live" }, h("span", {}, "–"), h("small", {}, c.metricLabel || ""));
    const view = h("div", { class: "ch-view" }), fb = h("div", { class: "ch-fb", "aria-live": "polite" });
    const params = Object.assign({}, c.fixed || {});
    let tries = 0, solved = !!st[key], predicted = !c.predict;
    const ctrls = c.controls.map((k) => {
      params[k.id] = k.value;
      if (k.type === "toggle") { const cb = h("input", { type: "checkbox" }); cb.checked = !!k.value; params[k.id] = cb.checked; cb.addEventListener("change", () => { params[k.id] = cb.checked; draw(); }); return h("div", { class: "ctrl" }, h("label", {}, cb, " " + k.label)); }
      const out = h("output"), inp = h("input", { type: "range", min: k.min, max: k.max, step: k.step || 1, value: k.value, "aria-label": k.label });
      const show = () => (out.textContent = fmt(+inp.value, k.digits || 0) + (k.unit || ""));
      inp.addEventListener("input", () => { params[k.id] = +inp.value; show(); draw(); }); show();
      const w = h("div", { class: "ctrl" }, h("label", {}, h("span", {}, k.label), out), inp, k.hint ? h("div", { class: "hint" }, k.hint) : null);
      w.inp = inp; w.k = k; return w;
    });
    const lockable = h("div", {}, ctrls);
    function draw() {
      const r = M[c.model](params), v = r.value[c.metric];
      countUp(live, v, c.digits || 0, c.unit || ""); live.classList.toggle("hit", hit(c, v));
      if (c.view === "gauge") gauge(view, v, c);
      else if (r.line && window.IAMChart) window.IAMChart.lineChart(view, Object.assign({ xTitle: c.xTitle || "", label: c.title }, r.line));
      else if (r.bars && window.IAMChart) window.IAMChart.barChart(view, Object.assign({ label: c.title }, r.bars));
      return v;
    }
    const stars = h("span", { class: "ch-stars", "aria-label": "stars" }, solved ? "★".repeat(st[key]) + "☆".repeat(3 - st[key]) : "");
    const check = h("button", { class: "btn", type: "button" }, "Check my answer");
    const hintB = h("button", { class: "btn quiet", type: "button", hidden: "" }, "Hint");
    const solB = h("button", { class: "btn quiet", type: "button", hidden: "" }, "Show a solution");
    const el = h("article", { class: "ch-card" + (solved ? " won" : "") },
      h("header", { class: "ch-head" }, h("span", { class: "ch-badge", html: icon(c.icon || "target") }), h("h4", {}, `Challenge ${idx + 1}: ${c.title}`), h("span", { class: "ch-level" }, c.level || "Core"), stars),
      h("div", { class: "ch-body" },
        h("div", {}, h("p", { class: "ch-goal", html: "<b>Goal:</b> " + c.goal }), lockable, h("div", { class: "ch-actions" }, check, hintB, solB), fb),
        h("div", {}, live, view)));
    // predict-first step
    if (c.predict) {
      lockable.style.opacity = 0.35; lockable.style.pointerEvents = "none"; check.disabled = true;
      const pq = h("div", { class: "q ch-predict" }, h("p", {}, h("b", {}, "Predict first: "), c.predict.q));
      const opts = h("div", { class: "opts" });
      c.predict.options.forEach((o, i) => opts.append(h("button", { class: "opt", type: "button", onclick: (e) => {
        if (predicted) return; predicted = true; $$(".opt", opts).forEach((b, j) => { b.disabled = true; if (j === c.predict.answer) b.classList.add("right"); });
        if (i !== c.predict.answer) e.currentTarget.classList.add("wrong");
        pq.append(h("p", { class: "small muted" }, (i === c.predict.answer ? "Good instinct. " : "Not quite, but now test it. ") + "Now use the sliders to check it with the model."));
        lockable.style.opacity = 1; lockable.style.pointerEvents = "auto"; check.disabled = false;
      } }, o)));
      pq.append(opts); lockable.before(pq);
    }
    check.addEventListener("click", () => {
      const v = draw(); tries++;
      if (hit(c, v)) {
        const s = Math.max(1, 4 - tries); if (!solved || s > (store.load()[key] || 0)) { const d = store.load(); d[key] = Math.max(s, d[key] || 0); store.save(d); }
        solved = true; el.classList.add("won"); stars.textContent = "★".repeat(store.load()[key]) + "☆".repeat(3 - store.load()[key]);
        fb.className = "ch-fb ok"; fb.innerHTML = `<b>Goal reached${tries === 1 ? " on the first try" : ""}.</b> ${c.explain}`; burst(el); onScore();
      } else {
        el.classList.remove("shake"); void el.offsetWidth; el.classList.add("shake");
        const dir = c.op === "<=" ? "too high" : c.op === ">=" ? "too low" : v > c.target ? "too high" : "too low";
        fb.className = "ch-fb no"; fb.innerHTML = `<b>Not yet:</b> ${c.metricLabel || "the result"} is ${fmt(v, c.digits || 0)}${c.unit || ""}, ${dir}. ${tries >= 1 && c.hint ? "Try the hint." : ""}`;
        if (c.hint) hintB.hidden = false; if (tries >= 3 && c.solution) solB.hidden = false;
      }
    });
    hintB.addEventListener("click", () => { fb.className = "ch-fb no"; fb.innerHTML = `<b>Hint:</b> ${c.hint}`; });
    solB.addEventListener("click", () => {
      Object.entries(c.solution).forEach(([k, val]) => { const w = ctrls.find((x) => x.k && x.k.id === k); if (w) { w.inp.value = val; w.inp.dispatchEvent(new Event("input")); } });
      fb.className = "ch-fb no"; fb.innerHTML = "<b>One solution is set on the sliders.</b> Press Check to confirm it, then try to find another.";
    });
    draw();
    return el;
  }

  function mountChallenges() {
    $$(".challenges[data-module]").forEach((root) => {
      const mid = root.dataset.module, list = (window.CHALLENGES || {})[mid]; if (!list) return;
      const ring = h("div", { class: "ch-score" }), cards = [];
      const upd = () => {
        const d = store.load(), got = list.reduce((a, _, i) => a + (d[`${mid}:${i}`] || 0), 0), max = list.length * 3, frac = got / max, C = 2 * Math.PI * 26;
        ring.innerHTML = `<svg class="ch-ring" viewBox="0 0 64 64"><circle class="bg" cx="32" cy="32" r="26"/><circle class="fg" cx="32" cy="32" r="26" stroke-dasharray="${C}" stroke-dashoffset="${C * (1 - frac)}"/><text x="32" y="37" text-anchor="middle">${got}/${max}</text></svg><div><b>Your simulation score</b><br><span class="small muted">${list.length} challenges · three stars for a first-try solve, fewer after misses. Saved in this browser.</span></div>`;
      };
      upd(); root.append(ring); list.forEach((c, i) => { const el = card(c, i, mid, upd); cards.push(el); root.append(el); });
    });
  }

  // ------------------------------------------------------------------ every quiz: progress bar, animations, celebration
  function quizFx() {
    $$(".quiz").forEach((qz) => {
      const items = $$(".q", qz); if (!items.length || qz.querySelector(".quiz-progress")) return;
      const bar = h("div", { class: "quiz-progress", "aria-hidden": "true" }, h("span")); qz.prepend(bar);
      const upd = () => { const n = items.filter((q) => q.dataset.done).length; bar.firstChild.style.width = (100 * n) / items.length + "%"; };
      qz.addEventListener("click", (e) => {
        const b = e.target.closest(".opt"); if (!b) return;
        setTimeout(() => {
          b.classList.add(b.classList.contains("wrong") ? "fx-wrong" : "fx-right"); upd();
          const res = $(".quiz-result", qz); if (res && !res.hidden && items.every((q) => q.dataset.done === "right")) { qz.style.position = "relative"; burst(qz); }
        }, 0);
      });
      const again = $(".quiz-again", qz); again && again.addEventListener("click", () => { setTimeout(upd, 0); $$(".opt", qz).forEach((o) => o.classList.remove("fx-right", "fx-wrong")); });
    });
  }

  // ------------------------------------------------------------------ concept-thread recall buttons and figure pause
  function misc() {
    $$(".thread-recall button").forEach((b) => b.addEventListener("click", () => { const r = b.closest(".thread-recall"); r.classList.toggle("open"); b.textContent = r.classList.contains("open") ? "Hide" : "Show answer"; }));
    $$(".figure-card .fig-play").forEach((b) => b.addEventListener("click", () => { const f = b.closest(".figure-card"); const p = f.classList.toggle("paused"); b.textContent = p ? "Play animation" : "Pause animation"; const s = f.querySelector("svg"); if (s && s.pauseAnimations) p ? s.pauseAnimations() : s.unpauseAnimations(); }));
  }
  function init() { mountChallenges(); quizFx(); misc(); }
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", init); else init();
})();
