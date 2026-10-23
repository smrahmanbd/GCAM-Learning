/* Interactive explorers, one per week. All numbers are toy/illustrative unless stated. */
(function () {
  "use strict";
  const NS = "http://www.w3.org/2000/svg";
  const css = (v) => getComputedStyle(document.documentElement).getPropertyValue(v).trim();
  const fmt = (x, d = 0) => (isFinite(x) ? Number(x).toLocaleString("en-US", { minimumFractionDigits: d, maximumFractionDigits: d }) : "–");
  const h = (tag, attrs = {}, ...kids) => {
    const e = document.createElement(tag);
    for (const [k, v] of Object.entries(attrs)) {
      if (k === "class") e.className = v; else if (k === "html") e.innerHTML = v;
      else if (k.startsWith("on")) e.addEventListener(k.slice(2), v); else e.setAttribute(k, v);
    }
    kids.flat().forEach((c) => c != null && e.append(c.nodeType ? c : document.createTextNode(c)));
    return e;
  };
  function slider(label, { min, max, step = 1, value, unit = "", digits = 0, hint }, onChange) {
    const out = h("output");
    const inp = h("input", { type: "range", min, max, step, value, "aria-label": label });
    const show = () => (out.textContent = fmt(+inp.value, digits) + unit);
    inp.addEventListener("input", () => { show(); onChange(); });
    show();
    const wrap = h("div", { class: "ctrl" }, h("label", {}, h("span", {}, label), out), inp, hint ? h("div", { class: "hint" }, hint) : null);
    wrap.get = () => +inp.value; wrap.set = (v) => { inp.value = v; show(); };
    return wrap;
  }
  function select(label, options, value, onChange) {
    const s = h("select", { "aria-label": label }, options.map(([v, t]) => h("option", { value: v }, t)));
    s.value = value; s.addEventListener("change", onChange);
    const wrap = h("div", { class: "ctrl" }, h("label", {}, h("span", {}, label)), s);
    wrap.get = () => s.value; return wrap;
  }
  function readout(items) {
    const box = h("div", { class: "readout" });
    const cells = items.map(([k, label]) => { const b = h("b"); const d = h("div", {}, b, h("span", {}, label)); box.append(d); return [k, b, d]; });
    box.set = (k, v, hot) => { const c = cells.find((x) => x[0] === k); if (c) { c[1].textContent = v; c[2].classList.toggle("hot", !!hot); } };
    return box;
  }
  function layout(el, controls, view, intro) {
    el.innerHTML = "";
    const w = h("div", { class: "widget" });
    if (intro) w.append(h("p", { class: "muted" }, intro));
    w.append(h("div", { class: "wgrid" }, h("div", {}, controls), h("div", {}, view)));
    el.append(w);
    return w;
  }
  // ---- SVG charts ----
  function svg(w, hgt) { const s = document.createElementNS(NS, "svg"); s.setAttribute("viewBox", `0 0 ${w} ${hgt}`); s.setAttribute("class", "chart"); s.setAttribute("role", "img"); return s; }
  function el(tag, attrs, parent) { const e = document.createElementNS(NS, tag); for (const k in attrs) e.setAttribute(k, attrs[k]); if (parent) parent.append(e); return e; }
  function niceMax(v) { if (v <= 0) return 1; const p = Math.pow(10, Math.floor(Math.log10(v))); const m = v / p; return (m <= 1 ? 1 : m <= 2 ? 2 : m <= 2.5 ? 2.5 : m <= 5 ? 5 : 10) * p; }
  function colors() { return [css("--c1"), css("--c2"), css("--c3"), css("--c4")]; }
  /** line chart: xs numeric, series [{name, values, color, dash}] */
  function lineChart(target, { xs, series, xTitle, yTitle, yMax, yMin = 0, label, vline, hline, area }) {
    const W = 640, H = 340, L = 58, R = 16, T = 16, B = 46;
    const s = svg(W, H); if (label) s.setAttribute("aria-label", label);
    const all = series.flatMap((x) => x.values).filter(isFinite);
    const top = yMax != null ? yMax : niceMax(Math.max(...all, hline ? hline.y : 0) * 1.05);
    const x0 = xs[0], x1 = xs[xs.length - 1];
    const X = (x) => L + ((x - x0) / (x1 - x0 || 1)) * (W - L - R), Y = (y) => T + (1 - (y - yMin) / (top - yMin)) * (H - T - B);
    const g = el("g", { class: "grid" }, s);
    for (let i = 0; i <= 4; i++) { const v = yMin + ((top - yMin) * i) / 4; el("line", { x1: L, x2: W - R, y1: Y(v), y2: Y(v) }, g); const t = el("text", { x: L - 8, y: Y(v) + 4, "text-anchor": "end" }, s); t.textContent = fmt(v, top - yMin < 5 ? 1 : 0); }
    const ticks = 6; for (let i = 0; i <= ticks; i++) { const v = x0 + ((x1 - x0) * i) / ticks; const t = el("text", { x: X(v), y: H - B + 18, "text-anchor": "middle" }, s); t.textContent = fmt(v, Math.abs(x1 - x0) < 10 ? 1 : 0); }
    el("line", { x1: L, x2: W - R, y1: Y(yMin), y2: Y(yMin), class: "axis" }, s);
    if (xTitle) { const t = el("text", { x: (L + W - R) / 2, y: H - 6, "text-anchor": "middle", class: "ttl" }, s); t.textContent = xTitle; }
    if (yTitle) { const t = el("text", { x: 14, y: (T + H - B) / 2, "text-anchor": "middle", transform: `rotate(-90 14 ${(T + H - B) / 2})`, class: "ttl" }, s); t.textContent = yTitle; }
    const cs = colors();
    if (hline) { el("line", { x1: L, x2: W - R, y1: Y(hline.y), y2: Y(hline.y), stroke: css("--orange"), "stroke-dasharray": "6 5", "stroke-width": 2 }, s); const t = el("text", { x: W - R - 4, y: Y(hline.y) - 6, "text-anchor": "end" }, s); t.textContent = hline.label; t.style.fill = css("--orange"); }
    if (vline) { el("line", { x1: X(vline.x), x2: X(vline.x), y1: T, y2: H - B, stroke: css("--muted"), "stroke-dasharray": "4 4" }, s); const t = el("text", { x: X(vline.x) + 4, y: T + 12 }, s); t.textContent = vline.label; }
    series.forEach((se, i) => {
      const c = se.color || cs[i % 4];
      const pts = xs.map((x, j) => [X(x), Y(Math.max(yMin, Math.min(top, se.values[j])))]).filter((p, j) => isFinite(se.values[j]));
      if (area && i === 0) el("path", { d: `M${pts[0][0]},${Y(yMin)} ` + pts.map((p) => `L${p[0]},${p[1]}`).join(" ") + ` L${pts[pts.length - 1][0]},${Y(yMin)} Z`, fill: c, opacity: 0.15 }, s);
      el("path", { d: pts.map((p, k) => (k ? "L" : "M") + p[0] + "," + p[1]).join(" "), fill: "none", stroke: c, "stroke-width": 3, "stroke-dasharray": se.dash || "", "stroke-linejoin": "round" }, s);
    });
    target.innerHTML = "";
    if (series.length > 1) target.append(legend(series));
    target.append(s);
  }
  function barChart(target, { labels, values, colorsFor, yTitle, yMax, digits = 0, label, suffix = "" }) {
    const W = 640, H = 300, L = 58, R = 16, T = 24, B = 40;
    const s = svg(W, H); if (label) s.setAttribute("aria-label", label);
    const top = yMax != null ? yMax : niceMax(Math.max(...values, 0) * 1.1);
    const Y = (y) => T + (1 - y / top) * (H - T - B);
    const g = el("g", { class: "grid" }, s);
    for (let i = 0; i <= 4; i++) { const v = (top * i) / 4; el("line", { x1: L, x2: W - R, y1: Y(v), y2: Y(v) }, g); const t = el("text", { x: L - 8, y: Y(v) + 4, "text-anchor": "end" }, s); t.textContent = fmt(v, top < 5 ? 1 : 0); }
    const n = values.length, bw = ((W - L - R) / n) * 0.62, cs = colors();
    values.forEach((v, i) => {
      const cx = L + ((i + 0.5) * (W - L - R)) / n, vv = Math.max(0, Math.min(top, v));
      el("rect", { x: cx - bw / 2, y: Y(vv), width: bw, height: Y(0) - Y(vv), rx: 4, fill: colorsFor ? colorsFor(i, v) : cs[0] }, s);
      const t = el("text", { x: cx, y: Y(vv) - 6, "text-anchor": "middle" }, s); t.textContent = fmt(v, digits) + suffix; t.style.fill = css("--ink"); t.style.fontWeight = 600;
      const l = el("text", { x: cx, y: H - B + 18, "text-anchor": "middle" }, s); l.textContent = labels[i];
    });
    el("line", { x1: L, x2: W - R, y1: Y(0), y2: Y(0), class: "axis" }, s);
    if (yTitle) { const t = el("text", { x: 14, y: (T + H - B) / 2, "text-anchor": "middle", transform: `rotate(-90 14 ${(T + H - B) / 2})`, class: "ttl" }, s); t.textContent = yTitle; }
    target.innerHTML = ""; target.append(s);
  }
  function legend(series) {
    const cs = colors();
    return h("div", { class: "legend" }, series.map((se, i) => h("span", {}, h("i", { style: `background:${se.color || cs[i % 4]}` }), se.name)));
  }
  const range = (a, b, step = 1) => { const r = []; for (let x = a; x <= b + 1e-9; x += step) r.push(+x.toFixed(6)); return r; };

  // ======================= WIDGETS =======================
  const W = {};

  // Week 1: cumulative emissions -> warming
  W.warming = (root) => {
    const chart = h("div"), out = readout([["cum", "CO2 emitted 2020–2100 (Gt)"], ["t", "Warming by 2100 (°C)"], ["b", "Carbon budget it fits"]]);
    const peak = slider("Year emissions peak", { min: 2020, max: 2050, value: 2025 }, draw);
    const grow = slider("Growth until the peak", { min: 0, max: 3, step: 0.1, value: 1, unit: "% / yr", digits: 1 }, draw);
    const nz = slider("Year CO2 reaches zero", { min: 2035, max: 2100, value: 2070, hint: "After the peak, emissions fall in a straight line to zero." }, draw);
    function draw() {
      const p = peak.get(), z = Math.max(nz.get(), p + 5), g = grow.get() / 100, yrs = range(2020, 2100);
      let ep = 40 * Math.pow(1 + g, p - 2020);
      const em = yrs.map((y) => (y <= p ? 40 * Math.pow(1 + g, y - 2020) : y >= z ? 0 : ep * (1 - (y - p) / (z - p))));
      let cum = 0; const temp = em.map((e) => { cum += e; return 1.1 + (0.45 * cum) / 1000; });
      out.set("cum", fmt(cum)); out.set("t", fmt(temp[temp.length - 1], 2), temp[temp.length - 1] > 2);
      out.set("b", cum <= 500 ? "1.5 °C (500 Gt)" : cum <= 1150 ? "2 °C (1,150 Gt)" : "Neither", cum > 1150);
      const c = h("div"); const c2 = h("div");
      lineChart(c, { xs: yrs, series: [{ name: "CO2 emissions (Gt/yr)", values: em }], yTitle: "Gt CO2 per year", xTitle: "Year", area: true, label: "Emissions path" });
      lineChart(c2, { xs: yrs, series: [{ name: "Warming (°C)", values: temp, color: css("--c2") }], yTitle: "°C above pre-industrial", xTitle: "Year", yMin: 1, yMax: 3, hline: { y: 1.5, label: "1.5 °C" }, label: "Warming path" });
      chart.innerHTML = ""; chart.append(c, c2);
    }
    layout(root, [peak, grow, nz], [out, chart, h("p", { class: "note" }, "Toy model: today ≈ 40 Gt CO2 a year and ≈ 1.1 °C of warming in 2020; each 1,000 Gt adds ≈ 0.45 °C. CO2 only; other gases ignored. Budget sizes from IPCC AR6 WGI, counted from 2020.")]);
    draw();
  };

  // Week 2: carbon budget bathtub
  W.budget = (root) => {
    const tub = h("div"), out = readout([["flat", "Years left if flat"], ["line", "Years if falling in a straight line"], ["year", "Budget used up in"]]);
    const target = select("Temperature goal", [["500", "1.5 °C (50% chance): 500 Gt"], ["850", "1.7 °C (50% chance): 850 Gt"], ["1150", "2 °C (67% chance): 1,150 Gt"]], "500", draw);
    const rate = slider("Emissions per year", { min: 10, max: 60, value: 40, unit: " Gt" }, draw);
    const yrs = slider("Years that pass (flat emissions)", { min: 0, max: 40, value: 5, unit: " yr" }, draw);
    function draw() {
      const B = +target.get(), E = rate.get(), n = yrs.get(), used = E * n, frac = Math.min(1, used / B);
      out.set("flat", fmt(B / E, 1)); out.set("line", fmt((2 * B) / E, 1)); out.set("year", fmt(2020 + B / E), false);
      const s = svg(640, 300), wall = css("--ink-soft");
      el("path", { d: "M120 40 L140 260 L500 260 L520 40", fill: "none", stroke: wall, "stroke-width": 6, "stroke-linejoin": "round" }, s);
      const top = 40 + (1 - frac) * 220, inset = (y) => 120 + ((y - 40) / 220) * 20;
      el("path", { d: `M${inset(top)} ${top} L140 257 L500 257 L${640 - inset(top)} ${top} Z`, fill: frac >= 1 ? css("--orange") : css("--teal"), opacity: 0.75 }, s);
      el("rect", { x: 300, y: 4, width: 40, height: 30, rx: 4, fill: wall }, s);
      if (n > 0) el("rect", { x: 312, y: 34, width: 16, height: Math.max(6, top - 34), fill: css("--teal"), opacity: 0.5 }, s);
      const t = el("text", { x: 320, y: 290, "text-anchor": "middle", class: "ttl" }, s);
      t.textContent = frac >= 1 ? `Overflowing: ${fmt(used - B)} Gt over the budget` : `${fmt(used)} of ${fmt(B)} Gt used (${fmt(frac * 100)}%)`;
      tub.innerHTML = ""; tub.append(s);
    }
    layout(root, [target, rate, yrs], [out, tub, h("p", { class: "note" }, "The bathtub is the budget: the tap is yearly emissions, and the water level is the running total. Budgets from IPCC AR6 WGI (2021), counted from the start of 2020. Check them against the report before teaching.")]);
    draw();
  };

  // Week 3: Kaya identity
  W.kaya = (root) => {
    const chart = h("div"), out = readout([["co2", "CO2 ratio (end ÷ start)"], ["pct", "Change in CO2"], ["wrong", "Wrong: adding the %"]]);
    const mk = (l, v, min, max) => slider(l, { min, max, value: v, unit: "%" }, draw);
    const pop = mk("Population change", 20, -30, 80), inc = mk("Income per person change", 50, -30, 200), ei = mk("Energy per $ change", -30, -70, 30), ci = mk("CO2 per unit of energy change", -20, -95, 30);
    function draw() {
      const f = [pop, inc, ei, ci].map((s) => 1 + s.get() / 100), r = f.reduce((a, b) => a * b, 1), wrong = [pop, inc, ei, ci].reduce((a, s) => a + s.get(), 0);
      out.set("co2", fmt(r, 3)); out.set("pct", (r >= 1 ? "+" : "") + fmt((r - 1) * 100, 1) + "%", r > 1); out.set("wrong", (wrong >= 0 ? "+" : "") + fmt(wrong) + "%");
      barChart(chart, { labels: ["Population", "Income", "Energy/GDP", "CO2/energy", "CO2"], values: [...f, r], digits: 2, yTitle: "Ratio (1 = no change)", colorsFor: (i, v) => (i === 4 ? css("--c2") : v >= 1 ? css("--c3") : css("--c1")), label: "Kaya factor ratios" });
    }
    layout(root, [pop, inc, ei, ci], [out, chart, h("p", { class: "note" }, "CO2 = population × income per person × energy per $ × CO2 per unit of energy. The factor changes multiply, so adding percentages gives the wrong answer. Defaults are the invented country Avalon from the lecture.")]);
    draw();
  };

  // Week 4: toy energy market
  W.market = (root) => {
    const c1 = h("div"), c2 = h("div"), out = readout([["win", "Cheapest technology"], ["p", "Market price ($/MWh)"], ["q", "Quantity sold (MWh)"], ["buy", "Buyers pay of the tax"]]);
    const tax = slider("Carbon price", { min: 0, max: 100, value: 0, unit: " $/t" }, draw);
    function draw() {
      const t = tax.get(), techs = [["Coal", 60, 0.9], ["Gas", 70, 0.4], ["Solar", 80, 0]], costs = techs.map(([, b, e]) => b + e * t);
      const iMin = costs.indexOf(Math.min(...costs));
      out.set("win", techs[iMin][0]);
      const p = (1000 + 5.4 * t) / 10, q = 1000 - 4 * p;
      out.set("p", fmt(p, 1)); out.set("q", fmt(q)); out.set("buy", t ? fmt(p - 100, 1) + " of " + fmt(0.9 * t, 1) : "–");
      barChart(c1, { labels: techs.map((x) => x[0]), values: costs, digits: 1, yTitle: "$ per MWh", yMax: 200, colorsFor: (i) => (i === iMin ? css("--c1") : css("--line")), label: "Technology costs" });
      const ps = range(0, 200, 5);
      lineChart(c2, { xs: ps, series: [{ name: "Demand", values: ps.map((x) => 1000 - 4 * x) }, { name: "Supply (coal, with tax)", values: ps.map((x) => Math.max(0, 6 * (x - 0.9 * t))) }], xTitle: "Price ($/MWh)", yTitle: "MWh", yMax: 1200, vline: { x: p, label: "price " + fmt(p) }, label: "Supply and demand" });
    }
    layout(root, [tax, h("div", { class: "explain" }, "Break-even prices: gas beats coal above $20/t; solar beats gas above $25/t.")], [out, c1, c2, h("p", { class: "note" }, "Illustrative numbers from lab 4: coal 60 $/MWh and 0.9 t/MWh, gas 70 and 0.4, solar 80 and 0. Demand 1000 − 4p, supply 6 × (p − 0.9 × tax).")]);
    draw();
  };

  // Week 5: discounting and DICE trade-off
  W.discount = (root) => {
    const chart = h("div"), out = readout([["ann", "$1 a year for 100 years, today"], ["one", "$100 in 100 years, today"], ["dmg", "Output lost at 3 °C"]]);
    const r = slider("Discount rate", { min: 0, max: 7, step: 0.1, value: 3, unit: "%", digits: 1 }, draw);
    const dm = slider("Damage setting (× DICE default)", { min: 0.5, max: 3, step: 0.1, value: 1, unit: "×", digits: 1 }, draw);
    function draw() {
      const rr = r.get() / 100, ann = rr ? (1 - Math.pow(1 + rr, -100)) / rr : 100;
      out.set("ann", "$" + fmt(ann, 2)); out.set("one", "$" + fmt(100 / Math.pow(1 + rr, 100), 2)); out.set("dmg", fmt(0.00236 * 9 * dm.get() * 100, 1) + "%");
      const ys = range(0, 100, 2);
      lineChart(chart, { xs: ys, series: [{ name: `Your rate (${fmt(r.get(), 1)}%)`, values: ys.map((y) => 100 / Math.pow(1 + rr, y)) }, { name: "1.5%", values: ys.map((y) => 100 / Math.pow(1.015, y)), dash: "6 5" }, { name: "5%", values: ys.map((y) => 100 / Math.pow(1.05, y)), dash: "2 4" }], xTitle: "Years from now", yTitle: "Value today of $100", yMax: 100, label: "Discount curves" });
    }
    layout(root, [r, dm, h("div", { class: "explain" }, "DICE weighs cutting emissions now (costs today) against damages later. A higher discount rate shrinks those later damages, so the model chooses less cutting. Bigger damages push the other way.")], [out, chart, h("p", { class: "note" }, "Present value = amount ÷ (1 + r)^years. Damage share D = 0.00236 × T² × your setting (DICE default coefficient; check against the DICE documentation).")]);
    draw();
  };

  // Week 6: SSP x RCP matrix
  W.matrix = (root) => {
    const SSP = [
      ["SSP1", "Sustainability", "A greener, cooperative world: fast technology change, low population growth, strong education and health.", 5.5],
      ["SSP2", "Middle of the road", "Trends continue roughly as in the past: uneven progress, moderate challenges for cutting and adapting.", 6.5],
      ["SSP3", "Regional rivalry", "Countries focus on security and go their own way: slow growth, high population, weak cooperation.", 7.0],
      ["SSP4", "Inequality", "A divided world: a rich, high-tech elite and many poorer groups left behind.", 6.5],
      ["SSP5", "Fossil-fuelled development", "Fast growth powered by abundant fossil fuels and energy-hungry lifestyles.", 8.5]];
    const RCP = [[1.9, "≈ 1.4 °C"], [2.6, "≈ 1.8 °C"], [4.5, "≈ 2.7 °C"], [7.0, "≈ 3.6 °C"], [8.5, "≈ 4.4 °C"]];
    const CORE = { "SSP1-1.9": 1, "SSP1-2.6": 1, "SSP2-4.5": 1, "SSP3-7.0": 1, "SSP5-8.5": 1 };
    const info = h("div", { class: "box teal" }, h("p", {}, "Click a cell to read its story."));
    const grid = h("div", { class: "matrix", role: "grid" }, h("div"), RCP.map(([f]) => h("div", { class: "h" }, f.toFixed(1) + " W/m²")));
    SSP.forEach(([id, name, story, base]) => {
      grid.append(h("div", { class: "rh" }, id, h("br"), h("span", { class: "muted small" }, name)));
      RCP.forEach(([f, warm]) => {
        const key = `${id}-${f.toFixed(1)}`, above = f > base + 0.1, infeasible = id === "SSP3" && f < 3;
        const b = h("button", { class: (CORE[key] ? "core " : "") + (above || infeasible ? "no" : ""), "aria-label": key }, key);
        b.addEventListener("click", () => {
          grid.querySelectorAll("button").forEach((x) => x.classList.remove("sel")); b.classList.add("sel");
          const status = above ? `Not a policy case: ${id}'s world without new climate policy already ends near ${base} W/m², so reaching ${f} W/m² would mean emitting more than its baseline.`
            : infeasible ? "Models could not reach this level in SSP3: with weak cooperation and slow technology change, the required cuts were judged out of reach." : f >= base - 0.1 ? `Close to ${id}'s no-new-policy baseline.` : `Needs climate policy beyond ${id}'s baseline; models generally found it reachable.`;
          info.innerHTML = "";
          info.append(h("h4", {}, key + (CORE[key] ? " · one of the five headline AR6 scenarios" : "")), h("p", {}, h("b", {}, `${id}, ${name}: `), story),
            h("p", {}, h("b", {}, `Forcing ${f} W/m² in 2100: `), `warming late this century ${warm} (rough value for the headline scenario at this forcing level).`), h("p", { style: "margin:0" }, status));
        });
        grid.append(b);
      });
    });
    root.innerHTML = "";
    root.append(h("div", { class: "widget" }, h("p", { class: "muted" }, "Rows are stories about society (SSPs). Columns are how much extra heat-trapping (radiative forcing) the atmosphere holds in 2100. Highlighted cells are the five headline scenarios used in IPCC AR6 climate runs; striped cells are not policy cases or were out of reach for models."),
      h("div", { class: "tscroll" }, grid), info,
      h("p", { class: "note" }, "Baseline forcing levels and warming values are approximate, from Riahi et al. (2017) and IPCC AR6 WGI. Check them against the sources before teaching.")));
  };

  // Week 7: logit sharing
  W.logit = (root) => {
    const chart = h("div"), out = readout([["c", "Coal share"], ["g", "Gas share"], ["s", "Solar share"], ["n", "Exponent for 90% to the cheapest"]]);
    const cc = slider("Coal cost", { min: 30, max: 150, value: 60, unit: " $/MWh" }, draw), gc = slider("Gas cost", { min: 30, max: 150, value: 70, unit: " $/MWh" }, draw), sc = slider("Solar cost", { min: 30, max: 150, value: 80, unit: " $/MWh" }, draw);
    const ex = slider("Logit exponent", { min: -15, max: -0.5, step: 0.5, value: -4, digits: 1, hint: "More negative = buyers react more strongly to cost differences." }, draw);
    const shares = (cs, l) => { const w = cs.map((c) => Math.pow(c, l)); const s = w.reduce((a, b) => a + b, 0); return w.map((x) => x / s); };
    function draw() {
      const cs = [cc.get(), gc.get(), sc.get()], sh = shares(cs, ex.get());
      out.set("c", fmt(sh[0] * 100) + "%"); out.set("g", fmt(sh[1] * 100) + "%"); out.set("s", fmt(sh[2] * 100) + "%");
      let need = null; for (let l = -0.5; l >= -100; l -= 0.5) { if (Math.max(...shares(cs, l)) >= 0.9) { need = l; break; } }
      out.set("n", need == null ? "ties: never" : fmt(need, 1));
      barChart(chart, { labels: ["Coal", "Gas", "Solar"], values: sh.map((x) => x * 100), suffix: "%", yMax: 100, yTitle: "Share of new investment (%)", colorsFor: (i) => colors()[[2, 1, 0][i]], label: "Logit shares" });
    }
    layout(root, [cc, gc, sc, ex], [out, chart, h("div", { class: "explain" }, "Share = cost^exponent ÷ sum of all cost^exponent (equal share weights). The cheapest option wins the biggest share, but not all of it, just as in GCAM.")]);
    draw();
  };

  // Week 8: learning curve
  W.learning = (root) => {
    const chart = h("div"), out = readout([["cost", "Solar cost ($/MWh)"], ["share", "Solar share of new investment"]]);
    const lr = slider("Learning rate", { min: 0, max: 40, value: 20, unit: "%", hint: "Cost falls by this % each time capacity doubles." }, draw);
    const dbl = slider("Number of doublings", { min: 0, max: 6, step: 0.5, value: 2, digits: 1 }, draw);
    function share(sol) { const w = [60, 70, sol].map((c) => Math.pow(c, -4)); return w[2] / w.reduce((a, b) => a + b, 0); }
    function draw() {
      const l = lr.get() / 100, d = dbl.get(), c = 80 * Math.pow(1 - l, d);
      out.set("cost", fmt(c, 1)); out.set("share", fmt(share(c) * 100) + "%");
      const xs = range(0, 6, 0.25);
      lineChart(chart, { xs, series: [{ name: "Solar cost ($/MWh)", values: xs.map((x) => 80 * Math.pow(1 - l, x)) }, { name: "Solar share (%)", values: xs.map((x) => share(80 * Math.pow(1 - l, x)) * 100) }], xTitle: "Doublings of solar capacity", yMax: 100, vline: { x: d, label: "you are here" }, label: "Learning curve" });
    }
    layout(root, [lr, dbl], [out, chart, h("p", { class: "note" }, "Coal 60 and gas 70 $/MWh stay fixed; logit exponent −4 as in week 7. In the GCAM release used here, technology costs are inputs you choose; a learning curve is one way to decide what to write in those inputs, not something GCAM computes during a run.")]);
    draw();
  };

  // Week 9: land for bioenergy
  W.land = (root) => {
    const chart = h("div"), out = readout([["land", "Land needed (million ha)"], ["crop", "Share of today's cropland"], ["grass", "Contested land to energy grass"]]);
    const ej = slider("Bioenergy wanted", { min: 0, max: 200, step: 5, value: 100, unit: " EJ/yr" }, draw);
    const y = slider("Energy-crop yield", { min: 2, max: 20, step: 0.5, value: 10, unit: " t/ha", digits: 1 }, draw);
    const gp = slider("Energy grass price", { min: 30, max: 120, value: 60, unit: " $/t" }, draw);
    function draw() {
      const land = (ej.get() * 1e9) / (y.get() * 18) / 1e6, crop = 1500;
      out.set("land", fmt(land)); out.set("crop", fmt((land / crop) * 100) + "%", land > 0.3 * crop);
      const wheat = (200 - 120) * 3, grass = Math.max(0, (gp.get() - 30) * 10);
      out.set("grass", fmt((grass / (wheat + grass || 1)) * 100) + "%");
      barChart(chart, { labels: ["Land for bioenergy", "Cropland today (approx.)"], values: [land, crop], yTitle: "million hectares", colorsFor: (i) => (i ? css("--line") : css("--c1")), label: "Land comparison" });
    }
    layout(root, [ej, y, gp], [out, chart, h("p", { class: "note" }, "Land = energy ÷ (yield × 18 GJ per tonne). Profit per hectare: wheat (200 − 120) × 3 t = $240; grass (price − 30) × 10 t; land is shared in proportion to profit (exponent 1), as in the lecture's simplified rule. World cropland ≈ 1,500 million ha (approximate). All numbers illustrative.")]);
    draw();
  };

  // Week 10: carbon price path and cuts
  W.carbonprice = (root) => {
    const chart = h("div"), out = readout([["p50", "Price in 2050 ($/t)"], ["cut", "Cut below Reference in 2050"], ["need", "Growth needed for a 60% cut"]]);
    const p0 = slider("Starting price in 2025", { min: 0, max: 100, value: 25, unit: " $/t" }, draw);
    const g = slider("Yearly growth of the price", { min: 0, max: 10, step: 0.5, value: 5, unit: "%", digits: 1, hint: "GCAM's own carbon price examples often rise around 5% a year." }, draw);
    function draw() {
      const yrs = range(2025, 2100, 5), price = yrs.map((y) => p0.get() * Math.pow(1 + g.get() / 100, y - 2025)), cut = price.map((p) => Math.min(100, p / 2));
      const p50 = p0.get() * Math.pow(1 + g.get() / 100, 25);
      out.set("p50", fmt(p50)); out.set("cut", fmt(Math.min(100, p50 / 2)) + "%");
      out.set("need", p0.get() > 0 ? fmt((Math.pow(120 / p0.get(), 1 / 25) - 1) * 100, 1) + "% / yr" : "–");
      lineChart(chart, { xs: yrs, series: [{ name: "Cut below Reference (%)", values: cut }, { name: "Carbon price ($/t, capped at 300 on the chart)", values: price.map((p) => Math.min(300, p)) }], xTitle: "Year", yMax: 300, hline: { y: 60, label: "60% cut" }, label: "Carbon price path" });
    }
    layout(root, [p0, g], [out, chart, h("p", { class: "note" }, "Toy straight-line cost curve from the lecture: price = 2 × cut%, so $50 buys a 25% cut and a 60% cut needs $120. Real GCAM cost curves are not straight lines.")]);
    draw();
  };

  // Week 11: linear program (exact vertex enumeration)
  function solveLP(cap) {
    // vars c,g,s; c+g+s=100; bounds; .9c+.4g<=cap; min 60c+70g+80s
    const cons = [[[1, 0, 0], 60], [[0, 1, 0], 50], [[0, 0, 1], 30], [[-1, 0, 0], 0], [[0, -1, 0], 0], [[0, 0, -1], 0], [[0.9, 0.4, 0], cap]];
    const eq = [[1, 1, 1], 100]; let best = null;
    const solve3 = (A, b) => { const det = (m) => m[0][0] * (m[1][1] * m[2][2] - m[1][2] * m[2][1]) - m[0][1] * (m[1][0] * m[2][2] - m[1][2] * m[2][0]) + m[0][2] * (m[1][0] * m[2][1] - m[1][1] * m[2][0]); const D = det(A); if (Math.abs(D) < 1e-9) return null; return [0, 1, 2].map((k) => det(A.map((r, i) => r.map((v, j) => (j === k ? b[i] : v)))) / D); };
    for (let i = 0; i < cons.length; i++) for (let j = i + 1; j < cons.length; j++) {
      const x = solve3([eq[0], cons[i][0], cons[j][0]], [eq[1], cons[i][1], cons[j][1]]); if (!x) continue;
      if (cons.every(([a, r]) => a[0] * x[0] + a[1] * x[1] + a[2] * x[2] <= r + 1e-7)) { const cost = 60 * x[0] + 70 * x[1] + 80 * x[2]; if (!best || cost < best.cost - 1e-9) best = { x, cost }; }
    }
    return best;
  }
  W.lp = (root) => {
    const chart = h("div"), out = readout([["mix", "Coal / gas / solar (TWh)"], ["cost", "Total cost (million $)"], ["em", "Emissions (Mt CO2)"], ["sp", "Shadow price of the cap ($/t)"]]);
    const cap = slider("CO2 cap", { min: 30, max: 75, step: 0.5, value: 40, unit: " Mt", digits: 1, hint: "Above 70 Mt the cap does not bind." }, draw);
    function draw() {
      const c = cap.get(), r = solveLP(c);
      if (!r) { out.set("mix", "no solution", true); out.set("cost", "–"); out.set("em", "–"); out.set("sp", "–"); }
      else {
        const [a, b, s] = r.x, up = solveLP(c + 0.01);
        out.set("mix", `${fmt(a, 1)} / ${fmt(b, 1)} / ${fmt(s, 1)}`); out.set("cost", fmt(r.cost, 1)); out.set("em", fmt(0.9 * a + 0.4 * b, 1));
        out.set("sp", fmt(up ? (r.cost - up.cost) / 0.01 : 0, 2), true);
      }
      const caps = range(38, 75, 0.5), costs = caps.map((k) => { const x = solveLP(k); return x ? x.cost : NaN; });
      lineChart(chart, { xs: caps, series: [{ name: "Cheapest total cost", values: costs }], xTitle: "CO2 cap (Mt)", yTitle: "million $", yMin: 6000, yMax: 7500, vline: { x: Math.max(38, Math.min(75, c)), label: "your cap" }, label: "Cost against cap" });
    }
    layout(root, [cap, h("div", { class: "explain" }, "The shadow price is how much the total cost rises when the cap is tightened by one tonne. It is the carbon price that would give the same result.")], [out, chart, h("p", { class: "note" }, "Lab 11 numbers (illustrative): coal 60 $/MWh, 0.9 t/MWh, max 60 TWh; gas 70, 0.4, max 50; solar 80, 0, max 30; demand 100 TWh. Below 38 Mt no mix can meet demand.")]);
    draw();
  };

  // Week 12: why models disagree
  W.disagree = (root) => {
    const chart = h("div"), out = readout([["a", "Model A: 2050 CO2 (Gt)"], ["b", "Model B: 2050 CO2 (Gt)"], ["gap", "Gap between models"]]);
    const price = slider("Carbon price (same for both)", { min: 0, max: 200, step: 5, value: 50, unit: " $/t" }, draw);
    const solA = slider("Model A: solar cost", { min: 40, max: 120, value: 60, unit: " $/MWh" }, draw);
    const drA = slider("Model A: demand response", { min: 0, max: 2, step: 0.1, value: 1, digits: 1, unit: "×", hint: "How much people cut energy use when prices rise." }, draw);
    const cut = (p, sol, dr) => 1 - Math.exp(-p * (0.01 * Math.pow(80 / sol, 2) + 0.006 * dr));
    function draw() {
      const p = price.get(), a = 40 * (1 - cut(p, solA.get(), drA.get())), b = 40 * (1 - cut(p, 80, 1));
      out.set("a", fmt(a, 1)); out.set("b", fmt(b, 1)); out.set("gap", fmt(Math.abs(a - b), 1) + " Gt", Math.abs(a - b) > 8);
      const ps = range(0, 200, 5);
      lineChart(chart, { xs: ps, series: [{ name: "Model A", values: ps.map((x) => 40 * (1 - cut(x, solA.get(), drA.get()))) }, { name: "Model B (solar 80, response 1×)", values: ps.map((x) => 40 * (1 - cut(x, 80, 1))) }], xTitle: "Carbon price ($/t)", yTitle: "2050 CO2 (Gt)", yMax: 40, vline: { x: p, label: "your price" }, label: "Two model responses" });
    }
    layout(root, [price, solA, drA], [out, chart, h("p", { class: "note" }, "Two invented toy models, not real ones. Same policy, different assumptions about technology cost and behaviour, different answers: that is most of why real IAMs disagree.")]);
    draw();
  };

  // Week 13: ensemble + scenario discovery
  W.ensemble = (root) => {
    const IN = [["g", "GDP growth", 1, 3, "%/yr"], ["d", "Clean-tech cost decline", 0, 4, "%/yr"], ["e", "Efficiency gain", 0.5, 2, "%/yr"]];
    let seed = 7, runs = [];
    const rnd = () => { seed = (seed * 16807) % 2147483647; return (seed - 1) / 2147483646; };
    function make() { runs = Array.from({ length: 300 }, () => { const r = {}; IN.forEach(([k, , lo, hi]) => (r[k] = lo + rnd() * (hi - lo))); r.E = 40 * Math.pow((1 + r.g / 100) / (1 + r.e / 100), 30) * (1 - Math.min(0.9, 0.15 * r.d)); return r; }); }
    make();
    const plot = h("div"), out = readout([["hi", "High-emission runs"], ["cov", "Coverage of the rule"], ["den", "Density of the rule"]]);
    const thr = slider("'High' means 2050 CO2 above", { min: 20, max: 70, value: 45, unit: " Gt" }, draw);
    const xs = select("x-axis input", IN.map(([k, l]) => [k, l]), "g", draw), ys = select("y-axis input", IN.map(([k, l]) => [k, l]), "d", draw);
    const rx = slider("Rule: x-axis input above", { min: 0, max: 4, step: 0.1, value: 2, digits: 1 }, draw), ry = slider("… and y-axis input below", { min: 0, max: 4, step: 0.1, value: 1.5, digits: 1 }, draw);
    const again = h("button", { class: "btn", onclick: () => { seed = Math.floor(Math.random() * 1e6) + 1; make(); draw(); } }, "New random ensemble");
    function draw() {
      const kx = xs.get(), ky = ys.get(), T = thr.get(), hi = runs.filter((r) => r.E > T), inRule = runs.filter((r) => r[kx] > rx.get() && r[ky] < ry.get());
      const both = inRule.filter((r) => r.E > T).length;
      out.set("hi", `${hi.length} of ${runs.length}`); out.set("cov", hi.length ? fmt((both / hi.length) * 100) + "%" : "–"); out.set("den", inRule.length ? fmt((both / inRule.length) * 100) + "%" : "–");
      const [, lx, x0, x1, ux] = IN.find((i) => i[0] === kx), [, ly, y0, y1, uy] = IN.find((i) => i[0] === ky);
      const W2 = 640, H2 = 360, L = 58, R = 16, T2 = 16, B = 46, s = svg(W2, H2), X = (v) => L + ((v - x0) / (x1 - x0)) * (W2 - L - R), Y = (v) => T2 + (1 - (v - y0) / (y1 - y0)) * (H2 - T2 - B);
      const g = el("g", { class: "grid" }, s);
      for (let i = 0; i <= 4; i++) { const v = y0 + ((y1 - y0) * i) / 4, u = x0 + ((x1 - x0) * i) / 4; el("line", { x1: L, x2: W2 - R, y1: Y(v), y2: Y(v) }, g); el("text", { x: L - 8, y: Y(v) + 4, "text-anchor": "end" }, s).textContent = fmt(v, 1); el("text", { x: X(u), y: H2 - B + 18, "text-anchor": "middle" }, s).textContent = fmt(u, 1); }
      const bx = Math.max(x0, Math.min(x1, rx.get())), by = Math.max(y0, Math.min(y1, ry.get()));
      el("rect", { x: X(bx), y: Y(by), width: X(x1) - X(bx), height: Y(y0) - Y(by), fill: css("--orange"), opacity: 0.12, stroke: css("--orange"), "stroke-dasharray": "5 4" }, s);
      runs.forEach((r) => el("circle", { cx: X(r[kx]), cy: Y(r[ky]), r: 4, fill: r.E > T ? css("--c2") : css("--c1"), opacity: r.E > T ? 0.9 : 0.45 }, s));
      el("text", { x: (L + W2 - R) / 2, y: H2 - 6, "text-anchor": "middle", class: "ttl" }, s).textContent = `${lx} (${ux})`;
      el("text", { x: 14, y: (T2 + H2 - B) / 2, "text-anchor": "middle", transform: `rotate(-90 14 ${(T2 + H2 - B) / 2})`, class: "ttl" }, s).textContent = `${ly} (${uy})`;
      plot.innerHTML = ""; plot.append(legend([{ name: "High-emission run", color: css("--c2") }, { name: "Other run", color: css("--c1") }, { name: "Your rule (box)", color: css("--orange") }]), s);
    }
    layout(root, [thr, xs, ys, rx, ry, again], [out, plot, h("p", { class: "note" }, "Toy model: 2050 CO2 = 40 × ((1 + growth) ÷ (1 + efficiency))^30 × (1 − 0.15 × clean-tech decline, at most 0.9). Coverage = share of high runs your box catches; density = share of runs in your box that are high. Good rules score high on both.")]);
    draw();
  };

  // Week 14: carbon dioxide removal
  W.cdr = (root) => {
    const chart = h("div"), out = readout([["gross", "Gross CO2, 2020–2100 (Gt)"], ["need", "Removal needed (Gt)"], ["miss", "Extra warming if removal falls short"]]);
    const budget = select("Carbon budget", [["500", "1.5 °C: 500 Gt"], ["850", "1.7 °C: 850 Gt"], ["1150", "2 °C: 1,150 Gt"]], "500", draw);
    const nz = slider("Year gross emissions bottom out", { min: 2035, max: 2090, value: 2050 }, draw);
    const res = slider("Hard-to-cut emissions left after that", { min: 0, max: 10, step: 0.5, value: 4, unit: " Gt/yr", digits: 1 }, draw);
    const del = slider("Share of the removal actually delivered", { min: 0, max: 100, value: 60, unit: "%" }, draw);
    function draw() {
      const yrs = range(2020, 2100), z = nz.get(), R = res.get();
      const em = yrs.map((y) => (y >= z ? R : 40 - ((40 - R) * (y - 2020)) / (z - 2020)));
      const gross = em.reduce((a, b) => a + b, 0), need = Math.max(0, gross - +budget.get()), miss = need * (1 - del.get() / 100);
      out.set("gross", fmt(gross)); out.set("need", fmt(need), need > 0); out.set("miss", "+" + fmt((0.45 * miss) / 1000, 2) + " °C", miss > 0);
      lineChart(chart, { xs: yrs, series: [{ name: "Gross CO2 (Gt/yr)", values: em }], xTitle: "Year", yTitle: "Gt CO2 per year", yMax: 45, area: true, label: "Gross emissions" });
    }
    layout(root, [budget, nz, res, del], [out, chart, h("p", { class: "note" }, "Toy accounting: removal needed = gross emissions 2020–2100 − budget. Shortfall warms the world by ≈ 0.45 °C per 1,000 Gt. Emissions fall in a straight line from 40 Gt in 2020. Budgets from IPCC AR6 WGI; check before teaching.")]);
    draw();
  };

  // Week 15: project planner (saved in this browser)
  W.project = (root, ctx) => {
    const KEY = "iam-course-project-plan";
    let st = {}; try { st = JSON.parse(localStorage.getItem(KEY) || "{}"); } catch (e) { st = {}; }
    const save = () => { try { localStorage.setItem(KEY, JSON.stringify(st)); } catch (e) { /* storage off */ } };
    const fields = [["q", "Policy question (one sentence)", "e.g. How does a net-zero pathway change if CCS is unavailable?"], ["ref", "Reference scenario", "e.g. GCAM Reference, no new policy"], ["v1", "Variation 1", "e.g. NetZero 2060"], ["v2", "Variation 2", "e.g. NetZero 2060 without CCS"], ["sens", "Sensitivity test", "e.g. solar cost low / central / high"]];
    const runsOut = h("b");
    const count = () => { const v = ["ref", "v1", "v2"].filter((k) => (st[k] || "").trim()).length; const s = (st.sens || "").split("/").filter((x) => x.trim()).length || 1; runsOut.textContent = `${v} scenarios × ${s} sensitivity values = ${v * s} GCAM runs`; };
    const inputs = fields.map(([k, l, ph]) => { const t = h("textarea", { rows: 2, placeholder: ph, style: "width:100%;padding:8px;border-radius:8px;border:1px solid var(--line);background:var(--bg-card);color:var(--ink);font:inherit" }); t.value = st[k] || ""; t.addEventListener("input", () => { st[k] = t.value; save(); count(); }); return h("div", { class: "ctrl" }, h("label", {}, h("span", {}, l)), t); });
    const checks = (ctx && ctx.checklist) || [];
    const list = h("div", { class: "checklist" }, checks.map((c, i) => { const cb = h("input", { type: "checkbox" }); cb.checked = !!(st.chk || {})[i]; cb.addEventListener("change", () => { st.chk = st.chk || {}; st.chk[i] = cb.checked; save(); }); return h("label", {}, cb, h("span", {}, c)); }));
    const dl = h("button", { class: "btn", onclick: () => { const txt = fields.map(([k, l]) => `${l}:\n${st[k] || ""}\n`).join("\n") + "\n" + runsOut.textContent + "\n"; const a = h("a", { href: URL.createObjectURL(new Blob([txt], { type: "text/plain" })), download: "project-plan.txt" }); document.body.append(a); a.click(); a.remove(); } }, "Download my plan (.txt)");
    count();
    layout(root, inputs, [h("div", { class: "box teal" }, h("h4", {}, "Run count"), runsOut), h("h4", {}, "Presentation-day checklist"), list, dl, h("p", { class: "note" }, "Your plan is kept only in this browser on this device.")]);
  };


  // ======================= NEW WIDGETS (GCAM site) =======================
  // Transport: generalised cost with value of time, mode shares (relative logit) and car technology (absolute logit)
  W.trncost = (root) => {
    const c1 = h("div"), c2 = h("div"), out = readout([["wage", "Wage ($ per hour)"], ["car", "Car share of passenger-km"], ["bev", "BEV share of new car km"], ["gc", "Car generalised cost ($/pkm)"]]);
    const gdp = slider("Income: GDP per person", { min: 5, max: 80, value: 18, unit: " k$", hint: "Wage = GDP per person ÷ 2,000 hours (as in GCAM)." }, draw);
    const fuel = slider("Liquid fuel price", { min: 5, max: 40, value: 15, unit: " $/GJ" }, draw);
    const bevc = slider("BEV non-fuel cost (vs today)", { min: 50, max: 130, value: 100, unit: "%" }, draw);
    const lf = slider("Car load factor (people per car)", { min: 1.0, max: 3.0, step: 0.05, value: 2.33, digits: 2 }, draw);
    const cp = slider("Carbon price", { min: 0, max: 300, step: 10, value: 0, unit: " $/tCO2" }, draw);
    function draw() {
      const wage = gdp.get() * 1000 / 2000, ef = 19.6 * 44 / 12 / 1000, pf = fuel.get() + ef * cp.get();
      const ice = (0.6345 + pf * 3.322 / 1000) / lf.get(), bev = (0.7407 * bevc.get() / 100 + 30 * 1.026 / 1000) / lf.get();
      const c0 = Math.max(ice, bev), x = [Math.exp(-8 * ice / c0), Math.exp(-8 * bev / c0)], bs = x[1] / (x[0] + x[1]);
      const carMoney = ice * (1 - bs) + bev * bs;
      const modes = [["Walk", 0, 1.066, 4.8, 0.25], ["Bus", (1.6319 + pf * 7.908 / 1000) / 25, 0.808, 22, 1], ["Rail", (16.005 + 30 * 53.197 / 1000) / 1152, 0.8, 42, 0.6], ["Car", carMoney, 0.82, 35, 1]];
      const gc = modes.map(([, m, v, sp]) => m + wage * v / sp);
      const w = modes.map((m, i) => m[4] * Math.pow(gc[i], -2)), S = w.reduce((a, b) => a + b, 0), sh = w.map((v) => v / S);
      out.set("wage", fmt(wage, 1)); out.set("car", fmt(sh[3] * 100) + "%"); out.set("bev", fmt(bs * 100) + "%", bs > 0.5); out.set("gc", fmt(gc[3], 3));
      barChart(c1, { labels: modes.map((m) => m[0]), values: modes.map((m) => m[1]), digits: 3, yTitle: "Money cost ($ per pkm)", label: "money cost" });
      barChart(c2, { labels: modes.map((m) => m[0]), values: sh.map((v) => v * 100), suffix: "%", yMax: 100, yTitle: "Share of passenger-km", colorsFor: (i) => colors()[i % 4], label: "mode shares" });
    }
    layout(root, [gdp, fuel, bevc, lf, cp, h("div", { class: "explain" }, "Generalised cost = money cost per passenger-km + wage × time-value multiplier ÷ speed. As people get richer, time costs more, so fast modes win.")],
      [out, h("div", { class: "two-charts" }, c1, c2), h("p", { class: "note" }, "Toy numbers rounded from the Go 3 transport kit (Middle East car, bus and rail costs, 2005$). Mode shares use a relative-cost logit (exponent −2) with illustrative share-weights; cars split ICE vs BEV with GCAM's absolute-cost logit (exponent −8). Not GCAM output.")]);
    draw();
  };

  // LMDI decomposition of a CO2 change into activity, structure, intensity and carbon effects (two modes)
  W.lmdi = (root) => {
    const chart = h("div"), out = readout([["d", "Change in CO2 (Mt)"], ["res", "Residual"]]);
    const s = (l, v, min, max, unit = "%") => slider(l, { min, max, value: v, unit }, draw);
    const act = s("Travel (passenger-km) change", 40, -30, 120), car = s("Car share in 2050 (2020: 60%)", 65, 20, 95), ei = s("Energy per pkm change", -30, -70, 20), cf = s("CO2 per unit energy change", -40, -100, 10);
    const L = (a, b) => (Math.abs(a - b) < 1e-12 ? a : (a - b) / Math.log(a / b));
    function draw() {
      const A0 = 1000, A1 = A0 * (1 + act.get() / 100), s0 = [0.6, 0.4], s1 = [car.get() / 100, 1 - car.get() / 100];
      const I0 = [2.0, 0.6], I1 = I0.map((x) => x * (1 + ei.get() / 100)), F0 = [0.07, 0.07], F1 = F0.map((x) => Math.max(1e-6, x * (1 + cf.get() / 100)));
      const C0 = [0, 1].map((i) => A0 * s0[i] * I0[i] * F0[i]), C1 = [0, 1].map((i) => A1 * s1[i] * I1[i] * F1[i]);
      const eff = { Activity: 0, Structure: 0, Intensity: 0, Carbon: 0 };
      for (const i of [0, 1]) { const w = L(C1[i], C0[i]); eff.Activity += w * Math.log(A1 / A0); eff.Structure += w * Math.log(s1[i] / s0[i]); eff.Intensity += w * Math.log(I1[i] / I0[i]); eff.Carbon += w * Math.log(F1[i] / F0[i]); }
      const dC = C1[0] + C1[1] - C0[0] - C0[1], sum = Object.values(eff).reduce((a, b) => a + b, 0);
      out.set("d", (dC >= 0 ? "+" : "") + fmt(dC, 1)); out.set("res", fmt(Math.abs(dC - sum), 6));
      const labels = Object.keys(eff).concat(["Total"]), vals = Object.values(eff).concat([dC]);
      const base = Math.max(...vals.map(Math.abs)) * 1.15 || 1;
      const W2 = 640, H2 = 300, L0 = 60, T = 20, B = 40, Y = (v) => T + (H2 - T - B) / 2 - (v / base) * (H2 - T - B) / 2;
      const sv = svg(W2, H2); el("line", { x1: L0, x2: W2 - 10, y1: Y(0), y2: Y(0), class: "axis" }, sv);
      let run = 0; const bw = (W2 - L0 - 20) / labels.length;
      labels.forEach((lab, i) => {
        const v = vals[i], last = i === labels.length - 1, y0 = last ? 0 : run, y1 = last ? v : run + v, x = L0 + i * bw + bw * 0.2;
        el("rect", { x, y: Math.min(Y(y0), Y(y1)), width: bw * 0.6, height: Math.max(1, Math.abs(Y(y0) - Y(y1))), rx: 3, fill: last ? css("--c3") : v >= 0 ? css("--c2") : css("--c1") }, sv);
        const t = el("text", { x: x + bw * 0.3, y: Math.min(Y(y0), Y(y1)) - 5, "text-anchor": "middle" }, sv); t.textContent = (v >= 0 ? "+" : "") + fmt(v, 1); t.style.fill = css("--ink"); t.style.fontWeight = 600;
        const l2 = el("text", { x: x + bw * 0.3, y: H2 - 14, "text-anchor": "middle" }, sv); l2.textContent = lab;
        if (!last) run += v;
      });
      chart.innerHTML = ""; chart.append(sv);
    }
    layout(root, [act, car, ei, cf], [out, chart, h("p", { class: "note" }, "LMDI-I: each effect = Σ over modes of L(C₁, C₀) × ln(factor₁ ÷ factor₀), with L the logarithmic mean. The effects add up exactly to the total change; the residual is zero. Two modes (car, bus), invented numbers.")]);
    draw();
  };

  // Downscaling a region to countries: proportional vs convergence
  W.downscale = (root) => {
    const chart = h("div"), out = readout([["a", "Country A 2050 (proportional)"], ["b", "Country A 2050 (convergence)"]]);
    const conv = slider("Convergence year", { min: 2050, max: 2150, step: 10, value: 2100 }, draw);
    const regGrowth = slider("Regional energy growth", { min: -2, max: 4, step: 0.5, value: 1.5, unit: "%/yr", digits: 1 }, draw);
    const C = [["A (rich, intensive)", 40, 8.0], ["B (middle)", 20, 5.0], ["C (poor, light)", 8, 3.0]];   // GDP pc k$, energy intensity MJ/$
    const pop = [30, 60, 110];
    function draw() {
      const yrs = range(2020, 2100, 5), g = regGrowth.get() / 100, cy = conv.get();
      const reg = yrs.map((y) => 1.0 * Math.pow(1 + g, y - 2020));                      // index of regional total
      const gdpg = [0.012, 0.025, 0.04];
      const prop = [], cvg = [];
      yrs.forEach((y, k) => {
        const gdp = C.map((c, i) => c[1] * Math.pow(1 + gdpg[i], y - 2020) * pop[i]);
        const regInt = C.reduce((a, c, i) => a + c[2] * C[i][1] * pop[i], 0) / C.reduce((a, c, i) => a + C[i][1] * pop[i], 0);
        const wgt = Math.min(1, (y - 2020) / (cy - 2020));
        const raw = gdp.map((G, i) => G * (C[i][2] * (1 - wgt) + regInt * wgt));
        const base = C.map((c, i) => c[2] * c[1] * pop[i]); const bs = base.reduce((a, b) => a + b, 0);
        const total = reg[k] * bs;
        const rs = raw.reduce((a, b) => a + b, 0);
        prop.push(base.map((b) => total * b / bs)); cvg.push(raw.map((r) => total * r / rs));
      });
      const i50 = yrs.indexOf(2050);
      out.set("a", fmt(prop[i50][0] / prop[0][0], 2) + "× 2020"); out.set("b", fmt(cvg[i50][0] / cvg[0][0], 2) + "× 2020");
      lineChart(chart, { xs: yrs, series: [0, 1, 2].map((i) => ({ name: "Country " + C[i][0] + " (convergence)", values: cvg.map((r) => r[i] / cvg[0][i]) })).concat([{ name: "Any country (proportional)", values: prop.map((r) => r[0] / prop[0][0]), dash: "6 5" }]), xTitle: "Year", yTitle: "Energy use (2020 = 1)", label: "downscaled paths" });
    }
    layout(root, [conv, regGrowth, h("div", { class: "explain" }, "Proportional downscaling keeps every country's 2020 share. Convergence lets countries' energy intensities move toward the regional average by the convergence year, then rescales so the countries still add up to the regional total.")], [out, chart, h("p", { class: "note" }, "Three invented countries in one region. A simplified convergence rule inspired by DSCALE (Sferra et al., 2026, GMD); the real method also uses projections, an econometric step and harmonisation.")]);
    draw();
  };

  // Solver: watch prices converge for two linked markets (Newton steps; GCAM uses Broyden's quasi-Newton method)
  W.solver = (root) => {
    const chart = h("div"), log = h("div", { class: "solverlog" }), out = readout([["it", "Iterations"], ["p", "Prices (oil, electricity)"], ["x", "Largest excess demand"]]);
    const cp = slider("Carbon price", { min: 0, max: 100, step: 5, value: 0, unit: " $/t" }, reset);
    const g0 = slider("Starting guess (× equilibrium-ish)", { min: 0.3, max: 3, step: 0.1, value: 2, digits: 1, unit: "×" }, reset);
    const exd = (p, c) => { const [o, e] = p, oc = o + 0.07 * c; return [100 * Math.pow(oc / 10, -0.6) * Math.pow(e / 30, 0.3) - 100 * Math.pow(o / 10, 1.2), 80 * Math.pow(e / 30, -0.5) * Math.pow(oc / 10, 0.3) - 80 * (e / 30)]; };
    let hist = [];
    function reset() { hist = [[10 * g0.get(), 30 * g0.get()]]; render(); }
    function step() {
      const p = hist[hist.length - 1], c = cp.get(), f = exd(p, c), J = [[0, 0], [0, 0]];
      for (let j = 0; j < 2; j++) { const q = p.slice(); q[j] *= 1.0001; const fq = exd(q, c); for (let i = 0; i < 2; i++) J[i][j] = (fq[i] - f[i]) / (q[j] - p[j]); }
      const det = J[0][0] * J[1][1] - J[0][1] * J[1][0]; let dx = [(J[1][1] * f[0] - J[0][1] * f[1]) / det, (-J[1][0] * f[0] + J[0][0] * f[1]) / det];
      let np = [p[0] - dx[0], p[1] - dx[1]];
      let k = 0; while ((np[0] <= 0 || np[1] <= 0) && k < 20) { dx = dx.map((v) => v / 2); np = [p[0] - dx[0], p[1] - dx[1]]; k++; }
      hist.push(np); render();
    }
    function render() {
      const c = cp.get(), last = hist[hist.length - 1], f = exd(last, c), mx = Math.max(...f.map(Math.abs));
      out.set("it", String(hist.length - 1)); out.set("p", fmt(last[0], 2) + " / " + fmt(last[1], 2)); out.set("x", mx < 1e-6 ? "solved (< 0.000001)" : fmt(mx, 3), mx >= 1e-3);
      lineChart(chart, { xs: hist.map((_, i) => i).concat(hist.length < 2 ? [1] : []), series: [{ name: "Oil price", values: hist.map((x) => x[0]).concat(hist.length < 2 ? [hist[0][0]] : []) }, { name: "Electricity price", values: hist.map((x) => x[1]).concat(hist.length < 2 ? [hist[0][1]] : []) }], xTitle: "Iteration", yTitle: "Price", label: "solver iterations" });
      log.innerHTML = ""; hist.forEach((x, i) => { const e = exd(x, c); log.append(h("div", {}, `#${i}: prices ${fmt(x[0], 3)}, ${fmt(x[1], 3)} → excess demand ${fmt(e[0], 3)}, ${fmt(e[1], 3)}`)); });
    }
    const bStep = h("button", { class: "btn", type: "button", onclick: step }, "Take one solver step");
    const bReset = h("button", { class: "btn ghost-btn", type: "button", onclick: reset }, "Start again");
    layout(root, [cp, g0, h("div", { class: "btnrow" }, bStep, bReset), h("div", { class: "explain" }, "Each step measures how excess demand responds to each price (the Jacobian) and jumps toward the prices where both markets clear. GCAM does this for hundreds of markets every 5-year period.")], [out, chart, log]);
    reset();
  };

  // Value factor: intermittent solar is worth less the more of it there is (GCAM v7.3+ method, CMP 394)
  W.valuefactor = (root) => {
    const chart = h("div"), out = readout([["s0", "Solar share without value factor"], ["s1", "Solar share with value factor"], ["vf", "Value factor at that share"]]);
    const lc = slider("Solar LCOE", { min: 15, max: 90, value: 40, unit: " $/MWh" }, draw), gas = slider("Gas generation cost", { min: 30, max: 120, value: 70, unit: " $/MWh" }, draw);
    const vf = (s) => Math.max(0.05, (0.972 - 1.443 * s) / 0.903);
    const share = (cs, cg) => { const a = Math.pow(cs, -6), b = Math.pow(cg, -6); return a / (a + b); };
    function draw() {
      const s0 = share(lc.get(), gas.get());
      let s = s0; for (let k = 0; k < 200; k++) s = 0.5 * s + 0.5 * share(lc.get() / vf(s), gas.get());
      out.set("s0", fmt(s0 * 100) + "%"); out.set("s1", fmt(s * 100) + "%", true); out.set("vf", fmt(vf(s), 2));
      const xs = range(0, 0.7, 0.02);
      lineChart(chart, { xs: xs.map((x) => x * 100), series: [{ name: "Effective solar cost = LCOE ÷ value factor", values: xs.map((x) => lc.get() / vf(x)) }, { name: "Gas cost", values: xs.map(() => gas.get()), dash: "6 5" }], xTitle: "Solar share of the market (%)", yTitle: "$ per MWh", yMax: 250, vline: { x: s * 100, label: "equilibrium share" }, label: "value factor" });
    }
    layout(root, [lc, gas, h("div", { class: "explain" }, "In GCAM since v7.3, wind and solar compete on LCOE ÷ value factor, and the value factor falls as their share rises. Solar PV: VF = (0.972 − 1.443 × share) ÷ 0.903.")], [out, chart, h("p", { class: "note" }, "Coefficients from GCAM change proposal 394 (via the GCAM v8.2 documentation). Two-option logit with exponent −6 is illustrative. The fitted relationship comes from US data and may not hold above about 75% renewables.")]);
    draw();
  };

  window.IAMWidgets = W;
  window.IAMChart = { lineChart, barChart };
})();
