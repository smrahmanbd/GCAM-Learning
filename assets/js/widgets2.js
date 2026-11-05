/* More explorers (Nov 2026): Foundations 1.7–1.10, model comparison (3.9), and one toy simulator per model in the model atlas.
   All numbers are illustrative teaching toys, not model output. Each explorer has a Play button that animates the simulation. */
(function () {
  "use strict";
  const W = window.IAMWidgets = window.IAMWidgets || {};
  const C = () => window.IAMChart;
  const NS = "http://www.w3.org/2000/svg";
  const css = (v) => getComputedStyle(document.documentElement).getPropertyValue(v).trim();
  const fmt = (x, d = 0) => (isFinite(x) ? Number(x).toLocaleString("en-US", { minimumFractionDigits: d, maximumFractionDigits: d }) : "–");
  const reduce = window.matchMedia && matchMedia("(prefers-reduced-motion: reduce)").matches;
  const h = (tag, attrs = {}, ...kids) => { const e = document.createElement(tag); for (const [k, v] of Object.entries(attrs)) { if (k === "class") e.className = v; else if (k === "html") e.innerHTML = v; else if (k.startsWith("on")) e.addEventListener(k.slice(2), v); else e.setAttribute(k, v); } kids.flat().forEach((c) => c != null && e.append(c.nodeType ? c : document.createTextNode(c))); return e; };
  const sv = (t, a, p) => { const e = document.createElementNS(NS, t); for (const k in a) e.setAttribute(k, a[k]); if (p) p.append(e); return e; };
  const range = (a, b, s = 1) => { const r = []; for (let x = a; x <= b + 1e-9; x += s) r.push(+x.toFixed(6)); return r; };
  function slider(label, { min, max, step = 1, value, unit = "", digits = 0, hint }, onChange) {
    const out = h("output"), inp = h("input", { type: "range", min, max, step, value, "aria-label": label });
    const show = () => (out.textContent = fmt(+inp.value, digits) + unit);
    inp.addEventListener("input", () => { show(); onChange(); }); show();
    const w = h("div", { class: "ctrl" }, h("label", {}, h("span", {}, label), out), inp, hint ? h("div", { class: "hint" }, hint) : null);
    w.get = () => +inp.value; w.set = (v) => { inp.value = v; show(); }; return w;
  }
  function readout(items) {
    const box = h("div", { class: "readout" });
    const cells = items.map(([k, label]) => { const b = h("b"); const d = h("div", {}, b, h("span", {}, label)); box.append(d); return [k, b, d]; });
    box.set = (k, v, hot) => { const c = cells.find((x) => x[0] === k); if (c) { c[1].textContent = v; c[2].classList.toggle("hot", !!hot); } };
    return box;
  }
  function layout(el, controls, view, intro) { el.innerHTML = ""; const w = h("div", { class: "widget" }); if (intro) w.append(h("p", { class: "muted" }, intro)); w.append(h("div", { class: "wgrid" }, h("div", {}, controls), h("div", {}, view))); el.append(w); return w; }
  // animate: calls step(k) for k = 0..n over dur ms
  function player(label, n, dur, step) {
    let raf = null;
    const b = h("button", { class: "btn", type: "button" }, "▶ " + label);
    b.addEventListener("click", () => {
      cancelAnimationFrame(raf); if (reduce) { step(n); return; }
      const t0 = performance.now(); const tick = (now) => { const k = Math.min(n, Math.floor(((now - t0) / dur) * n)); step(k); if (k < n) raf = requestAnimationFrame(tick); }; raf = requestAnimationFrame(tick);
    });
    return b;
  }

  // ------------------------------------------------------------------ 1.7 stocks, flows and feedbacks
  W.feedback = (root) => {
    const chart = h("div"), out = readout([["peak", "Peak CO2 (ppm)"], ["yr", "Year of the peak"], ["end", "CO2 in 2150 (ppm)"]]);
    const nz = slider("Year emissions reach zero", { min: 2040, max: 2120, value: 2070, hint: "Emissions fall in a straight line from 40 Gt CO2 a year in 2020." }, () => draw());
    const k = slider("Strength of natural sinks", { min: 0.5, max: 3, step: 0.1, value: 1.5, unit: "% of excess / yr", digits: 1, hint: "Oceans and forests absorb a share of the CO2 above pre-industrial (280 ppm)." }, () => draw());
    const f = slider("Feedback: sinks weaken per °C", { min: 0, max: 30, value: 10, unit: "%", hint: "A reinforcing loop: warming makes sinks less effective, so more CO2 stays." }, () => draw());
    function sim() {
      const yrs = range(2020, 2150), c = []; let C0 = 415; const E = 40 / 7.8;
      yrs.forEach((y) => { const e = y < nz.get() ? E * (1 - (y - 2020) / (nz.get() - 2020)) : 0; const dT = 3 * Math.log2(C0 / 280) * 0.55; C0 += e - (k.get() / 100) * (C0 - 280) * Math.max(0, 1 - (f.get() / 100) * dT); c.push(C0); });
      return { yrs, c };
    }
    function draw(upto) {
      const { yrs, c } = sim(), n = upto == null ? yrs.length : upto + 1, pk = Math.max(...c), iy = c.indexOf(pk);
      out.set("peak", fmt(pk)); out.set("yr", fmt(yrs[iy])); out.set("end", fmt(c[c.length - 1]), c[c.length - 1] > 450);
      C().lineChart(chart, { xs: yrs, series: [{ name: "CO2 in the air (ppm)", values: c.map((v, i) => (i < n ? v : NaN)) }, { name: "Without the feedback", values: (() => { const s = f.get(); f.set(0); const r = sim().c; f.set(s); return r; })(), dash: "6 5" }], xTitle: "Year", yTitle: "ppm", yMin: 300, yMax: 600, hline: { y: 450, label: "450 ppm" }, label: "CO2 stock" });
    }
    layout(root, [nz, k, f, h("div", { class: "btnrow" }, player("Play the century", 130, 5000, (i) => draw(i))), h("div", { class: "explain" }, "The stock only falls once the outflow (sinks) beats the inflow (emissions). That is why CO2 keeps rising for years after emissions start to fall.")], [out, chart, h("p", { class: "note" }, "Toy one-box carbon model: 1 ppm ≈ 7.8 Gt CO2; warming ≈ 0.55 × 3 °C per doubling as a rough transient response. Real carbon-cycle models such as Hector have several boxes.")]);
    draw();
  };

  // ------------------------------------------------------------------ 1.8 marginal abatement cost curve
  W.macc = (root) => {
    const OPTS = [["Efficiency", -20, 4, "--land"], ["Methane fixes", 10, 2.5, "--land"], ["Wind and solar", 25, 7, "--energy"], ["Electric cars", 60, 3.5, "--water"], ["Industry fuel switch", 90, 4, "--economy"], ["CCS", 120, 3, "--policy"], ["Direct air capture", 300, 4, "--climate"]];
    const view = h("div"), out = readout([["ab", "Cut bought (Gt CO2 / yr)"], ["cost", "Total yearly cost ($ bn)"], ["avg", "Average cost ($ / t)"]]);
    const price = slider("Carbon price", { min: -20, max: 320, value: 50, unit: " $/t" }, () => draw());
    const solar = slider("Solar and wind cost falls by", { min: 0, max: 80, value: 0, unit: "%", hint: "Cheaper technology moves a bar down the curve." }, () => draw());
    function draw() {
      const p = price.get(), o = OPTS.map((x) => (x[0] === "Wind and solar" ? [x[0], x[1] * (1 - solar.get() / 100), x[2], x[3]] : x)).sort((a, b) => a[1] - b[1]);
      const W0 = 640, H0 = 320, L = 56, B = 40, T = 16, tot = o.reduce((a, x) => a + x[2], 0), X = (q) => L + (q / tot) * (W0 - L - 16), Y = (c) => T + (1 - (c + 50) / 370) * (H0 - T - B);
      const s = sv("svg", { viewBox: `0 0 ${W0} ${H0}`, class: "chart", role: "img", "aria-label": "Marginal abatement cost curve" });
      let q = 0, ab = 0, cost = 0;
      o.forEach((x, i) => {
        const on = x[1] <= p, r = sv("rect", { x: X(q), y: Math.min(Y(x[1]), Y(0)), width: X(q + x[2]) - X(q) - 2, height: Math.abs(Y(x[1]) - Y(0)), fill: css(x[3]), opacity: on ? 0.9 : 0.25, rx: 3 }, s);
        r.style.transition = "opacity .4s"; const t = sv("text", { x: (X(q) + X(q + x[2])) / 2, y: x[1] >= 0 ? Y(x[1]) - 6 : Y(x[1]) + 14, "text-anchor": "middle", style: `font-size:11px;fill:${css("--ink")}` }, s); t.textContent = x[0];
        if (on) { ab += x[2]; cost += x[2] * x[1]; } q += x[2];
      });
      sv("line", { x1: L, x2: W0 - 16, y1: Y(0), y2: Y(0), stroke: css("--ink") }, s);
      sv("line", { x1: L, x2: W0 - 16, y1: Y(p), y2: Y(p), stroke: css("--climate"), "stroke-width": 3, "stroke-dasharray": "8 6" }, s);
      const lt = sv("text", { x: W0 - 20, y: Y(p) - 6, "text-anchor": "end", style: `fill:${css("--climate")};font-weight:600` }, s); lt.textContent = `carbon price $${fmt(p)}/t`;
      [-50, 0, 100, 200, 300].forEach((v) => { const t = sv("text", { x: L - 6, y: Y(v) + 4, "text-anchor": "end", style: "font-size:11px" }, s); t.textContent = v; });
      const xt = sv("text", { x: (L + W0) / 2, y: H0 - 8, "text-anchor": "middle", class: "ttl" }, s); xt.textContent = "Tonnes cut per year (bar width) →";
      view.innerHTML = ""; view.append(s);
      out.set("ab", fmt(ab, 1)); out.set("cost", fmt(cost)); out.set("avg", ab ? fmt(cost / ab) : "–");
    }
    layout(root, [price, solar, h("div", { class: "btnrow" }, player("Raise the price from $0 to $300", 60, 4000, (i) => { price.set(i * 5); draw(); })), h("div", { class: "explain" }, "A carbon price buys every option whose cost per tonne is below it. Notice that the average cost is far below the price: the last tonne is the most expensive.")], [out, view, h("p", { class: "note" }, "Illustrative options, costs and potentials for teaching. GCAM does not use a fixed curve like this: costs emerge from technology competition, but the logic of 'cheapest first, up to the price' is the same.")]);
    draw();
  };

  // ------------------------------------------------------------------ 1.9 water–energy–food nexus
  W.nexus = (root) => {
    const chart = h("div"), out = readout([["d", "Water demand (% of basin supply)"], ["p", "Water price signal"], ["src", "Where extra water comes from"]]);
    const food = slider("Food demand", { min: 60, max: 180, value: 100, unit: "%", hint: "100% = today." }, () => draw());
    const eff = slider("Irrigation efficiency gain", { min: 0, max: 50, value: 0, unit: "%" }, () => draw());
    const power = slider("Thermal power output", { min: 0, max: 200, value: 100, unit: "%" }, () => draw());
    const bio = slider("Irrigated bioenergy crops", { min: 0, max: 200, value: 0, unit: " units" }, () => draw());
    const dry = h("input", { type: "checkbox" }); dry.addEventListener("change", () => draw());
    function draw() {
      const irr = 60 * (food.get() / 100) * (1 - eff.get() / 100), cool = 15 * (power.get() / 100) * (dry.checked ? 0.1 : 1), city = 12, b = 0.12 * bio.get(), d = irr + cool + city + b;
      out.set("d", fmt(d) + "%", d > 100); out.set("p", d < 80 ? "Low" : d < 100 ? "Rising" : "High", d >= 100); out.set("src", d <= 100 ? "Rivers and lakes" : d <= 120 ? "Groundwater (costlier)" : "Desalination (costliest)", d > 100);
      C().barChart(chart, { labels: ["Irrigation", "Power cooling", "Cities", "Bioenergy", "Total"], values: [irr, cool, city, b, d], yMax: 160, suffix: "%", colorsFor: (i, v) => (i === 4 ? (v > 100 ? css("--climate") : css("--land")) : [css("--land"), css("--energy"), css("--economy"), css("--land"), css("--ink")][i]), label: "water demand" });
    }
    layout(root, [food, eff, power, bio, h("div", { class: "ctrl" }, h("label", {}, dry, " Switch power plants to dry cooling")), h("div", { class: "explain" }, "GCAM tracks water in 235 basins. When demand nears the renewable supply, the water price rises and costlier sources come in: groundwater, then desalination.")], [out, chart, h("p", { class: "note" }, "Toy basin with renewable supply = 100%. The three supply tiers follow GCAM's logic; the numbers are illustrative.")]);
    draw();
  };

  // ------------------------------------------------------------------ 1.10 uncertainty: ensemble of runs
  W.uncertainty = (root) => {
    const chart = h("div"), out = readout([["med", "Median warming 2100 (°C)"], ["lo", "Likely range (17–83%)"], ["p2", "Chance of exceeding 2 °C"]]);
    const cum = slider("CO2 emitted 2020–2100", { min: 300, max: 4000, step: 50, value: 1500, unit: " Gt" }, () => draw());
    const spread = slider("Uncertainty in climate response", { min: 0.5, max: 2, step: 0.1, value: 1, unit: "×", digits: 1, hint: "1× ≈ the IPCC likely range for warming per tonne (about 0.27–0.63 °C per 1,000 Gt)." }, () => draw());
    const nRuns = slider("Number of runs", { min: 10, max: 400, step: 10, value: 100 }, () => draw());
    let seed = 1; const rnd = () => { seed = (seed * 16807) % 2147483647; return (seed - 1) / 2147483646; };
    const gauss = () => { let u = 0, v = 0; while (!u) u = rnd(); v = rnd(); return Math.sqrt(-2 * Math.log(u)) * Math.cos(2 * Math.PI * v); };
    function draw(show) {
      seed = 7; const n = nRuns.get(), T = [];
      for (let i = 0; i < n; i++) T.push(1.1 + Math.max(0.1, 0.45 + 0.11 * spread.get() * gauss()) * cum.get() / 1000);
      T.sort((a, b) => a - b); const q = (p) => T[Math.min(n - 1, Math.floor(p * n))];
      out.set("med", fmt(q(0.5), 2)); out.set("lo", fmt(q(0.17), 1) + "–" + fmt(q(0.83), 1)); out.set("p2", fmt((100 * T.filter((t) => t > 2).length) / n) + "%", q(0.5) > 2);
      const bins = range(1, 5, 0.25), cnt = bins.map((b) => T.filter((t) => t >= b && t < b + 0.25).length), lim = show == null ? bins.length : show;
      C().barChart(chart, { labels: bins.map((b) => fmt(b, 2)), values: cnt.map((c, i) => (i < lim ? c : 0)), colorsFor: (i) => (bins[i] >= 2 ? css("--climate") : css("--water")), label: "histogram of warming", yTitle: "number of runs" });
    }
    layout(root, [cum, spread, nRuns, h("div", { class: "btnrow" }, player("Run the ensemble", 17, 2500, (i) => draw(i))), h("div", { class: "explain" }, "Each run draws a different climate response. Report the median and the range, and say how likely a threshold is. Red bars are runs above 2 °C.")], [out, chart, h("p", { class: "note" }, "Warming in 2100 ≈ 1.1 °C + TCRE × cumulative CO2, with TCRE drawn from a normal distribution (mean 0.45 °C per 1,000 Gt). Illustrative only.")]);
    draw();
  };

  // ------------------------------------------------------------------ 3.9 compare two models
  const PROFILE = {
    GCAM: { foresight: 0, economy: 1, land: 3, detail: 3, open: 3 }, "MESSAGEix-GLOBIOM": { foresight: 3, economy: 2, land: 3, detail: 3, open: 3 },
    "REMIND-MAgPIE": { foresight: 3, economy: 3, land: 3, detail: 2, open: 3 }, IMAGE: { foresight: 0, economy: 1, land: 3, detail: 3, open: 1 },
    "AIM-Hub": { foresight: 0, economy: 3, land: 2, detail: 2, open: 1 }, WITCH: { foresight: 3, economy: 3, land: 1, detail: 1, open: 3 }, DICE: { foresight: 3, economy: 2, land: 0, detail: 0, open: 3 } };
  const AX = [["foresight", "Foresight"], ["economy", "Economy covered"], ["land", "Land detail"], ["detail", "Technology detail"], ["open", "Openness of code"]];
  W.modelcompare = (root) => {
    const names = Object.keys(PROFILE), view = h("div");
    const mk = (v) => { const s = h("select", { "aria-label": "Model" }, names.map((n) => h("option", { value: n }, n))); s.value = v; s.addEventListener("change", draw); return s; };
    const a = mk("GCAM"), b = mk("REMIND-MAgPIE");
    function draw() {
      const W0 = 420, cx = 210, cy = 200, R = 140, s = sv("svg", { viewBox: `0 0 ${W0} 400`, class: "chart", role: "img", "aria-label": "Radar comparison" });
      const pt = (i, v) => { const ang = -Math.PI / 2 + (2 * Math.PI * i) / AX.length; return [cx + R * (v / 3) * Math.cos(ang), cy + R * (v / 3) * Math.sin(ang)]; };
      [1, 2, 3].forEach((l) => sv("polygon", { points: AX.map((_, i) => pt(i, l).join(",")).join(" "), fill: "none", stroke: css("--line") }, s));
      AX.forEach(([k, lab], i) => { const [x, y] = pt(i, 3.55); const t = sv("text", { x, y, "text-anchor": "middle", style: "font-size:12px" }, s); t.textContent = lab; });
      [[a.value, css("--c1")], [b.value, css("--c2")]].forEach(([n, col], j) => {
        const pts = AX.map(([k], i) => pt(i, PROFILE[n][k]).join(",")).join(" ");
        const pg = sv("polygon", { points: AX.map(() => `${cx},${cy}`).join(" "), fill: col, "fill-opacity": 0.22, stroke: col, "stroke-width": 3 }, s);
        if (reduce) pg.setAttribute("points", pts); else { const an = sv("animate", { attributeName: "points", from: AX.map(() => `${cx},${cy}`).join(" "), to: pts, dur: "0.7s", begin: "indefinite", fill: "freeze" }, pg); requestAnimationFrame(() => an.beginElement()); }
      });
      view.innerHTML = ""; view.append(h("div", { class: "legend" }, h("span", {}, h("i", { style: `background:${css("--c1")}` }), a.value), h("span", {}, h("i", { style: `background:${css("--c2")}` }), b.value)), s);
    }
    layout(root, [h("div", { class: "ctrl" }, h("label", {}, h("span", {}, "First model")), a), h("div", { class: "ctrl" }, h("label", {}, h("span", {}, "Second model")), b), h("div", { class: "explain" }, "Scores are the course's rough 0–3 teaching ratings, from the IAMC model documentation, not an official ranking. 'Economy covered': 1 = partial equilibrium (energy and land markets), 3 = whole economy.")], [view]);
    draw();
  };

  // ------------------------------------------------------------------ model atlas simulators
  // GCAM: period-by-period logit with a rising carbon price; no foresight
  W.model_gcam = (root) => {
    const chart = h("div"), out = readout([["s50", "Low-carbon share 2050"], ["s100", "Low-carbon share 2100"]]);
    const p0 = slider("Carbon price in 2025", { min: 0, max: 100, value: 25, unit: " $/t" }, () => draw());
    const g = slider("Price growth", { min: 0, max: 8, step: 0.5, value: 5, unit: "% / yr", digits: 1 }, () => draw());
    const lam = slider("Logit exponent", { min: -12, max: -1, step: 0.5, value: -6, digits: 1, hint: "More negative = buyers react more sharply to cost differences." }, () => draw());
    function draw(upto) {
      const yrs = range(2025, 2100, 5), s = yrs.map((y, i) => { const p = p0.get() * Math.pow(1 + g.get() / 100, y - 2025), fossil = 60 + 0.25 * p, clean = 90 * Math.pow(0.985, y - 2025); const a = Math.pow(clean, lam.get()), b = Math.pow(fossil, lam.get()); return (100 * a) / (a + b); });
      const n = upto == null ? yrs.length : upto + 1;
      out.set("s50", fmt(s[5]) + "%"); out.set("s100", fmt(s[s.length - 1]) + "%");
      C().lineChart(chart, { xs: yrs, series: [{ name: "Low-carbon share (%)", values: s.map((v, i) => (i < n ? v : NaN)) }], yMax: 100, xTitle: "Model period", yTitle: "%", label: "GCAM-style shares" });
    }
    layout(root, [p0, g, lam, h("div", { class: "btnrow" }, player("Solve period by period", 15, 3000, (i) => draw(i))), h("div", { class: "explain" }, "Each five-year period is solved on its own, using only that period's prices. Shares change smoothly because the logit never gives everything to the cheapest option.")], [out, chart]);
    draw();
  };
  // MESSAGE: perfect foresight least cost under a cumulative budget -> Hotelling price path, early action
  W.model_message = (root) => {
    const chart = h("div"), out = readout([["p0", "Carbon price 2025 ($/t)"], ["p50", "Carbon price 2050 ($/t)"], ["cum", "Budget used (Gt)"]]);
    const bud = slider("Cumulative CO2 budget 2025–2100", { min: 400, max: 2500, step: 50, value: 1000, unit: " Gt" }, () => draw());
    const r = slider("Discount rate", { min: 1, max: 8, step: 0.5, value: 5, unit: "%", digits: 1 }, () => draw());
    function draw() {
      const yrs = range(2025, 2100, 5), base = 40;
      const run = (p0) => { let cum = 0; const em = yrs.map((y) => { const p = p0 * Math.pow(1 + r.get() / 100, y - 2025), cut = Math.min(1, p / 400); const e = base * (1 - cut); cum += e * 5; return e; }); return { em, cum }; };
      let lo = 0, hi = 400; for (let k = 0; k < 40; k++) { const m = (lo + hi) / 2; if (run(m).cum > bud.get()) lo = m; else hi = m; }
      const { em, cum } = run(hi), price = yrs.map((y) => hi * Math.pow(1 + r.get() / 100, y - 2025));
      out.set("p0", fmt(hi)); out.set("p50", fmt(price[5])); out.set("cum", fmt(cum));
      C().lineChart(chart, { xs: yrs, series: [{ name: "Emissions (Gt CO2 / yr)", values: em }, { name: "Carbon price ÷ 10 ($/t)", values: price.map((p) => Math.min(80, p / 10)) }], xTitle: "Year", yMax: 80, label: "least cost path" });
    }
    layout(root, [bud, r, h("div", { class: "explain" }, "With perfect foresight and a budget, the least-cost carbon price rises at the discount rate (the Hotelling rule). The model finds the starting price that just uses the budget.")], [out, chart, h("p", { class: "note" }, "Toy: straight-line cost curve (cut = price ÷ 400) and a solver that searches for the starting price. MESSAGEix itself solves a large linear programme.")]);
    draw();
  };
  // REMIND: Ramsey rule and the consumption–investment trade-off
  W.model_remind = (root) => {
    const chart = h("div"), out = readout([["r", "Interest (discount) rate"], ["inv", "Energy investment now vs later"]]);
    const rho = slider("Pure rate of time preference ρ", { min: 0.1, max: 3, step: 0.1, value: 1, unit: "%", digits: 1 }, () => draw());
    const eta = slider("Elasticity of marginal utility η", { min: 0.5, max: 3, step: 0.1, value: 1.5, digits: 1 }, () => draw());
    const g = slider("Growth of consumption per person", { min: 0, max: 4, step: 0.1, value: 2, unit: "%", digits: 1 }, () => draw());
    function draw() {
      const rr = rho.get() + eta.get() * g.get(), yrs = range(2025, 2100, 5), w = yrs.map((y) => 100 / Math.pow(1 + rr / 100, y - 2025));
      out.set("r", fmt(rr, 1) + "%"); out.set("inv", rr < 3 ? "Invest early" : rr < 5 ? "Balanced" : "Delay", rr >= 5);
      C().lineChart(chart, { xs: yrs, series: [{ name: "Weight of $100 of consumption in each year (today = 100)", values: w }], yMax: 100, xTitle: "Year", yTitle: "weight", label: "Ramsey discounting" });
    }
    layout(root, [rho, eta, g, h("div", { class: "explain" }, "REMIND's planner maximises discounted welfare over the century. The Ramsey rule r = ρ + η·g sets how much the future counts, and so how early it pays to invest in clean energy.")], [out, chart]);
    draw();
  };
  // IMAGE: grid-cell land allocation by suitability
  W.model_image = (root) => {
    const view = h("div"), out = readout([["crop", "Cells under cropland"], ["for", "Forest cells left"]]);
    const food = slider("Food demand (index)", { min: 50, max: 200, value: 100 }, () => draw());
    const yld = slider("Crop yield growth", { min: 0, max: 100, value: 20, unit: "%" }, () => draw());
    const bio = slider("Bioenergy cells demanded", { min: 0, max: 40, value: 5 }, () => draw());
    const suit = Array.from({ length: 144 }, (_, i) => { const x = i % 12, y = Math.floor(i / 12); return Math.sin(x * 0.7) + Math.cos(y * 0.5) + ((i * 37) % 11) / 10; });
    const order = suit.map((v, i) => [v, i]).sort((a, b) => b[0] - a[0]).map((x) => x[1]);
    function draw(limit) {
      const need = Math.min(144, Math.round((food.get() * 0.45) / (1 + yld.get() / 100) + bio.get())), n = limit == null ? need : Math.min(need, limit);
      const s = sv("svg", { viewBox: "0 0 360 360", class: "chart", role: "img", "aria-label": "Land grid" }), set = new Set(order.slice(0, n)), bset = new Set(order.slice(Math.max(0, n - bio.get()), n));
      for (let i = 0; i < 144; i++) sv("rect", { x: (i % 12) * 30, y: Math.floor(i / 12) * 30, width: 28, height: 28, rx: 4, fill: set.has(i) ? (bset.has(i) ? css("--water") : css("--energy")) : css("--land"), opacity: set.has(i) ? 0.85 : 0.55 }, s);
      view.innerHTML = ""; view.append(h("div", { class: "legend" }, h("span", {}, h("i", { style: `background:${css("--energy")}` }), "food crops"), h("span", {}, h("i", { style: `background:${css("--water")}` }), "bioenergy"), h("span", {}, h("i", { style: `background:${css("--land")}` }), "forest")), s);
      out.set("crop", fmt(need)); out.set("for", fmt(144 - need), 144 - need < 40);
    }
    layout(root, [food, yld, bio, h("div", { class: "btnrow" }, player("Grow the cropland", 60, 3000, (i) => draw(i * 3))), h("div", { class: "explain" }, "IMAGE allocates land on a grid: the most suitable cells are converted first. Higher yields spare land; bioenergy demand takes more.")], [out, view]);
    draw();
  };
  // AIM-Hub: CGE with carbon tax, substitution elasticity
  W.model_aim = (root) => {
    const chart = h("div"), out = readout([["cut", "Emissions cut"], ["gdp", "GDP loss"], ["rev", "Tax revenue (% GDP)"]]);
    const tax = slider("Carbon tax", { min: 0, max: 300, step: 10, value: 100, unit: " $/t" }, () => draw());
    const sig = slider("Ease of substitution (elasticity)", { min: 0.2, max: 2, step: 0.1, value: 0.8, digits: 1, hint: "How easily firms and households switch away from carbon-intensive inputs." }, () => draw());
    function draw() {
      const t = tax.get(), cut = 100 * (1 - Math.pow(1 + t / 100, -sig.get() * 0.6)), loss = 0.5 * (t / 100) * (cut / 100) * 6 / Math.max(0.4, sig.get()), rev = (t / 100) * (1 - cut / 100) * 3;
      out.set("cut", fmt(cut) + "%"); out.set("gdp", fmt(loss, 1) + "%", loss > 2); out.set("rev", fmt(rev, 1) + "%");
      const ts = range(0, 300, 20), c = ts.map((x) => 100 * (1 - Math.pow(1 + x / 100, -sig.get() * 0.6))), l = ts.map((x, i) => 0.5 * (x / 100) * (c[i] / 100) * 6 / Math.max(0.4, sig.get()) * 10);
      C().lineChart(chart, { xs: ts, series: [{ name: "Emissions cut (%)", values: c }, { name: "GDP loss (% × 10)", values: l }], xTitle: "Carbon tax ($/t)", yMax: 100, vline: { x: t, label: "your tax" }, label: "CGE toy" });
    }
    layout(root, [tax, sig, h("div", { class: "explain" }, "In a general equilibrium model every market adjusts at once, so the cost of a policy appears as lost GDP or consumption. The easier the substitution, the larger the cut and the smaller the loss.")], [out, chart, h("p", { class: "note" }, "Toy with a constant-elasticity response; AIM-Hub solves a full multi-sector equilibrium (a mixed complementarity problem).")]);
    draw();
  };
  // WITCH: two-region abatement game
  W.model_witch = (root) => {
    const chart = h("div"), out = readout([["n", "Global cut, acting alone"], ["c", "Global cut, cooperating"], ["gap", "Gap closed by your coalition"]]);
    const b = slider("Benefit of one unit of global cut", { min: 1, max: 10, value: 4 }, () => draw());
    const k = slider("Number of regions", { min: 2, max: 17, value: 2 }, () => draw());
    const co = slider("Regions in the coalition", { min: 1, max: 17, value: 1 }, () => draw());
    function draw() {
      const n = k.get(), m = Math.min(co.get(), n), bb = b.get();
      const nash = n * bb, coop = n * n * bb, mine = m * m * bb + (n - m) * bb; // coalition members internalise m regions' benefit
      out.set("n", fmt(nash)); out.set("c", fmt(coop)); out.set("gap", fmt((100 * (mine - nash)) / Math.max(1, coop - nash)) + "%");
      C().barChart(chart, { labels: ["Acting alone (Nash)", "Your coalition", "Full cooperation"], values: [nash, mine, coop], label: "abatement game", yTitle: "global abatement (toy units)" });
    }
    layout(root, [b, k, co, h("div", { class: "explain" }, "Each region pays its own cost of cutting but shares the benefit with everyone. Acting alone, each ignores the benefit to others; a coalition counts its members' benefits. With 17 regions the free-rider gap is large.")], [out, chart, h("p", { class: "note" }, "Toy: cost a²/2, benefit b × total cut. WITCH solves this kind of game with full growth and energy models for each region.")]);
    draw();
  };
  // DICE: optimal abatement rate and the social cost of carbon
  W.model_dice = (root) => {
    const chart = h("div"), out = readout([["mu", "Optimal share cut now"], ["scc", "Social cost of carbon (toy $/t)"]]);
    const r = slider("Discount rate", { min: 1, max: 6, step: 0.1, value: 3, unit: "%", digits: 1 }, () => draw());
    const d = slider("Damage coefficient", { min: 0.5, max: 3, step: 0.1, value: 1, unit: "×", digits: 1, hint: "1× ≈ a damage function of the DICE type; higher = more harm per °C." }, () => draw());
    function draw() {
      const scc = (60 * d.get()) / Math.pow(r.get() / 1.5, 1.6), mus = range(0, 100, 2), mc = mus.map((m) => 550 * Math.pow(m / 100, 1.6));
      let mu = 0; for (const m of mus) if (550 * Math.pow(m / 100, 1.6) <= scc) mu = m;
      out.set("mu", fmt(mu) + "%"); out.set("scc", fmt(scc));
      C().lineChart(chart, { xs: mus, series: [{ name: "Marginal cost of cutting ($/t)", values: mc }, { name: "Social cost of carbon ($/t)", values: mus.map(() => scc), dash: "6 5" }], xTitle: "Share of emissions cut (%)", yMax: 600, vline: { x: mu, label: "optimum" }, label: "DICE toy" });
    }
    layout(root, [r, d, h("div", { class: "explain" }, "Cost–benefit models cut until the cost of the last tonne equals the damage it avoids (the social cost of carbon). The discount rate and the damage function drive the answer.")], [out, chart, h("p", { class: "note" }, "Toy relationship for teaching. DICE-2023 (Barrage and Nordhaus, 2024) solves a full optimal growth problem with a carbon cycle and climate module.")]);
    draw();
  };
})();
