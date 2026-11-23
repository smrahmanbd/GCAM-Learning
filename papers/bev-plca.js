/* Paper-study page: animations, explorers, exercises. Needs bev-plca-model.js and plca-common.js. */
(function () {
  const M = window.PLCA, P = M.P, L = window.PL, $ = (s) => document.querySelector(s);
  const R = Object.keys(P.grid_2025), S = P.scenarios, SC4 = S.slice(1), PT = P.powertrains;
  const rname = (r) => `${P.region_names[r]} (${r})`;
  const n0 = (v) => Math.round(v).toLocaleString("en");
  const pct = (a, b) => Math.round(100 * (1 - a / b));
  const redraws = [];
  window.addEventListener("resize", () => redraws.forEach((f) => f()));
  document.getElementById("theme") && document.getElementById("theme").addEventListener("click", () => setTimeout(() => redraws.forEach((f) => f()), 30));

  /* ---------- 2. Time machine ---------- */
  (function () {
    const cnv = $("#t-cnv"), reg = $("#t-region"), sc = $("#t-scen");
    L.opts(reg, R, "CHI", rname); L.opts(sc, SC4, "Ambitious (<2 °C)");
    const LIFE = 15, KM = 200000, KWH = P.kwh_per_km.BEV; let p = 0, raf = null, t0 = 0;
    function series() { return Array.from({ length: 61 }, (_, i) => { const y = 2025 + i / 4; return [y, M.intens(reg.value, sc.value, y).grid]; }); }
    function cum(prog, stat) { let s = 0; const g0 = P.grid_2025[reg.value]; for (let y = 0; y < LIFE; y++) { const f = Math.max(0, Math.min(1, prog - y)); if (!f) break; const g = stat ? g0 : M.intens(reg.value, sc.value, 2025 + y + 0.5).grid; s += f * KM / LIFE * KWH * g; } return s / 1000; }
    function draw() {
      const { ctx, w, h } = L.canvas(cnv, 0.42), g0 = P.grid_2025[reg.value], ser = series();
      const box = { x0: 56, y0: 16, x1: w - 16, y1: h - 44 };
      const { X, Y } = L.axes(ctx, box, [2025, 2040], [0, Math.max(0.1, g0 * 1.2)], { xticks: [2025, 2028, 2031, 2034, 2037, 2040], xfmt: (v) => v, ylab: "kg CO₂e per kWh", xlab: "year" });
      const yr = 2025 + p;
      // shaded avoided area
      ctx.fillStyle = L.cv("--land-t"); ctx.beginPath(); ctx.moveTo(X(2025), Y(g0));
      ser.filter(([y]) => y <= yr).forEach(([y, g]) => ctx.lineTo(X(y), Y(g)));
      const gNow = M.intens(reg.value, sc.value, yr).grid; ctx.lineTo(X(yr), Y(gNow)); ctx.lineTo(X(yr), Y(g0)); ctx.closePath(); ctx.fill();
      // static line
      ctx.setLineDash([6, 6]); ctx.strokeStyle = L.cv("--data"); ctx.lineWidth = 2.5; ctx.beginPath(); ctx.moveTo(X(2025), Y(g0)); ctx.lineTo(X(2040), Y(g0)); ctx.stroke(); ctx.setLineDash([]);
      // scenario line: faint full + bold progress
      ctx.strokeStyle = L.cv(L.SCC[sc.value]); ctx.globalAlpha = 0.25; ctx.beginPath(); ser.forEach(([y, g], i) => i ? ctx.lineTo(X(y), Y(g)) : ctx.moveTo(X(y), Y(g))); ctx.stroke(); ctx.globalAlpha = 1;
      ctx.lineWidth = 3.5; ctx.beginPath(); ser.filter(([y]) => y <= yr).forEach(([y, g], i) => i ? ctx.lineTo(X(y), Y(g)) : ctx.moveTo(X(y), Y(g))); ctx.lineTo(X(yr), Y(gNow)); ctx.stroke();
      // car
      const cx = X(yr), cy = Y(gNow) - 14; ctx.fillStyle = L.cv("--land"); ctx.beginPath(); ctx.roundRect ? ctx.roundRect(cx - 16, cy - 8, 32, 12, 4) : ctx.rect(cx - 16, cy - 8, 32, 12); ctx.fill();
      ctx.beginPath(); ctx.roundRect ? ctx.roundRect(cx - 9, cy - 15, 18, 9, 3) : ctx.rect(cx - 9, cy - 15, 18, 9); ctx.fill();
      ctx.fillStyle = L.cv("--ink"); [-9, 9].forEach((d) => { ctx.beginPath(); ctx.arc(cx + d, cy + 5, 3.6, 0, 7); ctx.fill(); });
      ctx.fillStyle = L.cv("--paper"); ctx.font = "bold 8px sans-serif"; ctx.textAlign = "center"; ctx.textBaseline = "middle"; ctx.fillText("BEV", cx, cy - 2);
      const cs = cum(p, true), cp = cum(p, false);
      $("#t-year").textContent = Math.floor(yr); $("#t-static").textContent = cs.toFixed(1) + " t"; $("#t-plca").textContent = cp.toFixed(1) + " t";
      $("#t-diff").textContent = cs ? pct(cp, cs) + "%" : "0%";
      L.legend($("#t-leg"), [["Typical LCA: 2025 grid all life", "--data", true], ["Scenario grid (" + sc.value + ")", L.SCC[sc.value]], ["Carbon a typical LCA over-counts", "--land-t"]]);
      const fs = cum(LIFE, true), fp = cum(LIFE, false);
      $("#t-read").innerHTML = `Over the whole 15 years, charging this BEV in <b>${rname(reg.value)}</b> emits <b>${fp.toFixed(1)} t</b> CO₂e with the time-adjusted grid, against <b>${fs.toFixed(1)} t</b> if you pretend it is 2025 forever. That is <b>${pct(fp, fs)}% less</b>. Try a clean grid (Canada) and a dirty one (Eastern Europe): dirty grids have the most to gain.`;
    }
    function step(ts) { if (!t0) t0 = ts - p / LIFE * 7000; p = Math.min(LIFE, (ts - t0) / 7000 * LIFE); draw(); if (p < LIFE) raf = requestAnimationFrame(step); else { raf = null; $("#t-play").textContent = "Play again"; } }
    $("#t-play").addEventListener("click", () => { if (raf) { cancelAnimationFrame(raf); raf = null; t0 = 0; $("#t-play").textContent = "Play"; return; } if (p >= LIFE) p = 0; t0 = 0; $("#t-play").textContent = "Pause"; raf = requestAnimationFrame(step); });
    $("#t-reset").addEventListener("click", () => { if (raf) cancelAnimationFrame(raf); raf = null; p = 0; t0 = 0; $("#t-play").textContent = "Play"; draw(); });
    [reg, sc].forEach((e) => e.addEventListener("change", draw));
    redraws.push(draw); draw();
  })();

  /* ---------- 3. Calculator ---------- */
  (function () {
    const cnv = $("#c-cnv"), reg = $("#c-region"), sc = $("#c-scen"), sz = $("#c-size"), km = $("#c-km"), life = $("#c-life"), bld = $("#c-build");
    L.opts(reg, R, "CHI", rname); L.opts(sc, SC4, "Ambitious (<2 °C)"); L.opts(sz, Object.keys(P.sizes), "Medium SUV");
    const PARTS = Object.keys(L.PARTC);
    function draw() {
      $("#c-kmo").textContent = n0(+km.value); $("#c-lifeo").textContent = life.value;
      const base = { region: reg.value, size: sz.value, km: +km.value, lifetime: +life.value, build_year: +bld.value };
      const res = PT.map((pt) => [pt, M.footprint(pt, Object.assign({}, base, { scenario: "No scenario" })), M.footprint(pt, Object.assign({}, base, { scenario: sc.value }))]);
      let lo = 0, hi = 0; res.forEach(([, a, b]) => [a, b].forEach((r) => { let pos = 0, neg = 0; PARTS.forEach((k) => r.parts[k] > 0 ? pos += r.parts[k] : neg += r.parts[k]); hi = Math.max(hi, pos); lo = Math.min(lo, neg); }));
      const { ctx, w, h } = L.canvas(cnv, 0.5), box = { x0: 56, y0: 22, x1: w - 10, y1: h - 46 };
      const { Y } = L.axes(ctx, box, [0, 1], [lo * 1.1, hi * 1.12], { xticks: [], ylab: "g CO₂e per km" });
      const gw = (box.x1 - box.x0) / PT.length, bw = Math.min(46, gw * 0.3);
      ctx.strokeStyle = L.cv("--ink-soft"); ctx.beginPath(); ctx.moveTo(box.x0, Y(0)); ctx.lineTo(box.x1, Y(0)); ctx.stroke();
      res.forEach(([pt, a, b], i) => {
        const cxg = box.x0 + gw * (i + 0.5);
        [[a, cxg - bw - 3, 0.4, "static"], [b, cxg + 3, 1, "pLCA"]].forEach(([r, x, al, lab]) => {
          let pos = 0, neg = 0; ctx.globalAlpha = al;
          PARTS.forEach((k) => { const v = r.parts[k]; if (!v) return; ctx.fillStyle = L.cv(L.PARTC[k]); if (v > 0) { ctx.fillRect(x, Y(pos + v), bw, Y(pos) - Y(pos + v)); pos += v; } else { ctx.fillRect(x, Y(neg), bw, Y(neg + v) - Y(neg)); neg += v; } });
          ctx.globalAlpha = 1; ctx.fillStyle = L.cv("--ink"); ctx.font = "bold 12px " + L.cv("--body"); ctx.textAlign = "center"; ctx.textBaseline = "bottom";
          ctx.fillText(Math.round(r.total), x + bw / 2, Y(pos) - 3);
          ctx.fillStyle = L.cv("--muted"); ctx.font = "11px " + L.cv("--body"); ctx.textBaseline = "top"; ctx.fillText(lab, x + bw / 2, box.y1 + 4);
          if (neg < 0) { ctx.strokeStyle = L.cv("--ink"); ctx.beginPath(); ctx.arc(x + bw / 2, Y(r.total), 4, 0, 7); ctx.stroke(); }
        });
        ctx.fillStyle = L.cv(L.PTC[pt]); ctx.font = "bold 14px " + L.cv("--body"); ctx.textBaseline = "top"; ctx.fillText(pt, cxg, box.y1 + 20);
      });
      L.legend($("#c-leg"), PARTS.map((k) => [k, L.PARTC[k]]));
      const rank = res.slice().sort((x, y) => x[2].total - y[2].total), bev = res[0], hev = res[2];
      const drop = res.map(([pt, a, b]) => `${pt} ${pct(b.total, a.total)}%`).join(", ");
      $("#c-read").innerHTML = `<b>Ranking with pLCA:</b> ${rank.map((r) => `<b style="color:${L.cv(L.PTC[r[0]])}">${r[0]}</b> ${Math.round(r[2].total)}`).join(" &lt; ")} g/km. ` +
        `The BEV is <b>${pct(bev[2].total, hev[2].total)}%</b> below the HEV (typical LCA: ${pct(bev[1].total, hev[1].total)}%). ` +
        `How much each footprint shrinks when time is accounted for: ${drop}. ` + (lo < 0 ? "<br>The hydrogen bar dips <b>below zero</b>: BECCS hydrogen removes CO₂ from the air. The circle marks the net total." : "");
    }
    [reg, sc, sz, km, life, bld].forEach((e) => e.addEventListener("input", draw));
    redraws.push(draw); draw();
  })();

  /* ---------- 4. Breakeven race + Fig 5 ---------- */
  (function () {
    const cnv = $("#b-cnv"), reg = $("#b-region"), sc = $("#b-scen");
    L.opts(reg, R, "CHI", rname); L.opts(sc, SC4, "Ambitious (<2 °C)");
    let prog = 1, raf = null;
    const KMS = Array.from({ length: 61 }, (_, i) => 5000 * i);
    function life(pt, s, k) { return k ? M.footprint(pt, { region: reg.value, scenario: s, km: k }).total * k / 1e6 : (P.production_t[pt] + P.eol_t); }
    function draw() {
      const lines = [["BEV", sc.value, false], ["HEV", sc.value, false], ["BEV", "No scenario", true], ["HEV", "No scenario", true]].map(([pt, s, d]) => ({ pt, s, d, pts: KMS.map((k) => [k, life(pt, s, k)]) }));
      const ymax = Math.max(...lines.flatMap((l) => l.pts.map((p) => p[1])));
      const { ctx, w, h } = L.canvas(cnv, 0.62), box = { x0: 50, y0: 14, x1: w - 12, y1: h - 44 };
      const { X, Y } = L.axes(ctx, box, [0, 300000], [0, ymax * 1.05], { xticks: [0, 100000, 200000, 300000], ylab: "whole-life t CO₂e", xlab: "lifetime mileage (km)" });
      const kmax = 300000 * prog;
      lines.forEach((l) => { ctx.strokeStyle = L.cv(L.PTC[l.pt]); ctx.lineWidth = l.d ? 2 : 3.5; ctx.setLineDash(l.d ? [6, 5] : []); ctx.globalAlpha = l.d ? 0.6 : 1; ctx.beginPath(); l.pts.filter((p) => p[0] <= kmax).forEach((p, i) => i ? ctx.lineTo(X(p[0]), Y(p[1])) : ctx.moveTo(X(p[0]), Y(p[1]))); ctx.stroke(); });
      ctx.setLineDash([]); ctx.globalAlpha = 1;
      const be = M.breakeven({ region: reg.value, scenario: sc.value }), bs = M.breakeven({ region: reg.value, scenario: "No scenario" });
      [[be, false], [bs, true]].forEach(([b, d]) => { if (b && b <= kmax && b <= 300000) { const y = life("BEV", d ? "No scenario" : sc.value, b); ctx.fillStyle = d ? L.cv("--paper") : L.cv("--ink"); ctx.strokeStyle = L.cv("--ink"); ctx.lineWidth = 2; ctx.beginPath(); ctx.arc(X(b), Y(y), 6, 0, 7); ctx.fill(); ctx.stroke(); ctx.fillStyle = L.cv("--ink"); ctx.font = "bold 12px " + L.cv("--body"); ctx.textAlign = "left"; ctx.textBaseline = "bottom"; ctx.textAlign = d ? "right" : "left"; ctx.textBaseline = d ? "bottom" : "top"; ctx.fillText((d ? "typical LCA " : "pLCA ") + Math.round(b / 1000) + "k km", X(b) + (d ? -10 : 10), Y(y) + (d ? -8 : 8)); } });
      L.legend($("#b-leg"), [["BEV (scenario)", L.PTC.BEV], ["HEV (scenario)", L.PTC.HEV], ["BEV, typical LCA", L.PTC.BEV, true], ["HEV, typical LCA", L.PTC.HEV, true]]);
      $("#b-read").innerHTML = `Lines start where production + end-of-life put them (BEV ${(P.production_t.BEV + P.eol_t).toFixed(1)} t, HEV ${(P.production_t.HEV + P.eol_t).toFixed(1)} t). The BEV line is <b>less steep</b> because each km emits less. Breakeven: <b>${be ? n0(be) + " km" : "never (within 1,000,000 km)"}</b> with the scenario, against <b>${bs ? n0(bs) + " km" : "never"}</b> in a typical LCA.`;
    }
    function step() { prog = Math.min(1, prog + 0.012); draw(); if (prog < 1) raf = requestAnimationFrame(step); else raf = null; }
    $("#b-play").addEventListener("click", () => { if (raf) cancelAnimationFrame(raf); prog = 0; raf = requestAnimationFrame(step); });
    [reg, sc].forEach((e) => e.addEventListener("change", () => { prog = 1; draw(); }));
    redraws.push(draw); draw();

    // Fig 5 cloud
    const fc = $("#f5-cnv"); let shown = Infinity, fr = null;
    const pts = []; S.forEach((s) => R.forEach((r) => { const b = M.breakeven({ region: r, scenario: s }); let g = 0; for (let y = 0; y < 15; y++) g += M.intens(r, s, 2025.5 + y).grid / 15; if (b) pts.push({ r, s, b, g }); }));
    function drawF() {
      const { ctx, w, h } = L.canvas(fc, 0.62), box = { x0: 50, y0: 14, x1: w - 12, y1: h - 44 };
      const { X, Y } = L.axes(ctx, box, [0, 200000], [0, 0.7], { xticks: [0, 50000, 100000, 150000, 200000], ylab: "average grid kg CO₂e/kWh", xlab: "breakeven mileage (km)" });
      ctx.setLineDash([4, 4]); ctx.strokeStyle = L.cv("--climate"); ctx.beginPath(); ctx.moveTo(X(100000), box.y0); ctx.lineTo(X(100000), box.y1); ctx.stroke(); ctx.setLineDash([]);
      ctx.fillStyle = L.cv("--climate"); ctx.font = "11px " + L.cv("--body"); ctx.textAlign = "left"; ctx.fillText("100,000 km", X(100000) + 4, box.y0 + 8);
      pts.slice(0, shown).forEach((p) => { ctx.fillStyle = L.cv(L.SCC[p.s]); ctx.globalAlpha = 0.85; ctx.beginPath(); ctx.arc(X(Math.min(p.b, 199000)), Y(p.g), p.s === "No scenario" ? 5 : 4.5, 0, 7); ctx.fill(); });
      ctx.globalAlpha = 1;
      L.legend($("#f5-leg"), S.map((s) => [s, L.SCC[s]]));
    }
    $("#f5-play").addEventListener("click", () => { if (fr) clearInterval(fr); shown = 0; fr = setInterval(() => { shown += 2; drawF(); if (shown >= pts.length) { clearInterval(fr); fr = null; const avg = S.map((s) => { const q = pts.filter((p) => p.s === s); return `${s}: ${Math.round(q.reduce((a, p) => a + p.b, 0) / q.length / 1000)}k km`; }); $("#f5-read").innerHTML = "Average breakeven in the toy model: " + avg.join(" · ") + ". (Paper: 87k → 70k → 64k → 63k → 51k km.)"; } }, 40); });
    redraws.push(drawF); drawF();
  })();

  /* ---------- shared Monte Carlo sample ---------- */
  const MC = (() => { const r = M.rng(2025), out = []; for (let i = 0; i < 5000; i++) { const s = M.sample(r); const f = {}; PT.forEach((pt) => f[pt] = M.footprint(pt, s).total); out.push(Object.assign(s, f)); } return out; })();

  /* ---------- 5. Monte Carlo ---------- */
  (function () {
    const cnv = $("#m-cnv"), pair = $("#m-pair"), nIn = $("#m-n"); let shown = 0, timer = null;
    function draw() {
      const [A, B] = pair.value.split("|"), N = +nIn.value, data = MC.slice(0, N);
      const all = data.flatMap((d) => [d[A], d[B]]), lo = Math.min(0, ...all), hi = Math.max(...all) * 1.05;
      const { ctx, w, h } = L.canvas(cnv, 1), box = { x0: 52, y0: 10, x1: w - 10, y1: h - 44 };
      const { X, Y } = L.axes(ctx, box, [lo, hi], [lo, hi], { xlab: B + " g CO₂e/km", ylab: A + " g CO₂e/km" });
      ctx.globalAlpha = 0.5; ctx.fillStyle = L.cv("--energy-t"); ctx.beginPath(); ctx.moveTo(X(lo), Y(lo)); ctx.lineTo(X(hi), Y(hi)); ctx.lineTo(X(hi), Y(lo)); ctx.fill();
      ctx.fillStyle = L.cv("--land-t"); ctx.beginPath(); ctx.moveTo(X(lo), Y(lo)); ctx.lineTo(X(hi), Y(hi)); ctx.lineTo(X(lo), Y(hi)); ctx.fill(); ctx.globalAlpha = 1;
      ctx.fillStyle = L.cv("--muted"); ctx.font = "12px " + L.cv("--body"); ctx.textAlign = "left"; ctx.fillText(`${A} has the bigger footprint`, X(lo) + 8, Y(hi) + 14); ctx.textAlign = "right"; ctx.fillText(`${B} has the bigger footprint`, X(hi) - 8, Y(lo) - 10);
      ctx.strokeStyle = L.cv("--ink-soft"); ctx.beginPath(); ctx.moveTo(X(lo), Y(lo)); ctx.lineTo(X(hi), Y(hi)); ctx.stroke();
      data.slice(0, shown).forEach((d) => { ctx.fillStyle = L.cv(L.SCC[d.scenario]); ctx.globalAlpha = 0.55; ctx.fillRect(X(d[B]) - 1.5, Y(d[A]) - 1.5, 3, 3); });
      ctx.globalAlpha = 1;
      // mean markers
      S.forEach((s) => { const q = data.slice(0, shown).filter((d) => d.scenario === s); if (!q.length) return; const ma = q.reduce((a, d) => a + d[A], 0) / q.length, mb = q.reduce((a, d) => a + d[B], 0) / q.length; ctx.fillStyle = L.cv(L.SCC[s]); ctx.strokeStyle = L.cv("--ink"); ctx.lineWidth = 2; ctx.beginPath(); ctx.arc(X(mb), Y(ma), 7, 0, 7); ctx.fill(); ctx.stroke(); });
      L.legend($("#m-leg"), S.map((s) => [s, L.SCC[s]]));
      const rows = S.map((s) => { const q = data.slice(0, shown).filter((d) => d.scenario === s); if (!q.length) return ""; const ma = q.reduce((a, d) => a + d[A], 0) / q.length, mb = q.reduce((a, d) => a + d[B], 0) / q.length, win = q.filter((d) => d[A] < d[B]).length / q.length * 100;
        return `<tr><td><span class="pl-chip" style="background:${L.cv(L.SCC[s])}">&nbsp;</span> ${s}</td><td>${Math.round(ma)}</td><td>${Math.round(mb)}</td><td>${win.toFixed(1)}%</td><td>${pct(ma, mb)}%</td></tr>`; }).join("");
      $("#m-tbl").innerHTML = `<thead><tr><th>Scenario</th><th>Mean ${A}</th><th>Mean ${B}</th><th>${A} lower in</th><th>${A} below ${B} (mean)</th></tr></thead><tbody>${rows}</tbody>`;
    }
    function run() { if (timer) cancelAnimationFrame(timer); shown = 0; const N = +nIn.value; const tick = () => { shown = Math.min(N, shown + Math.ceil(N / 90)); draw(); if (shown < N) timer = requestAnimationFrame(tick); else { timer = null; const [A, B] = pair.value.split("|"); $("#m-read").innerHTML = `Big circles are the scenario means. In the toy model ${A} vs ${B} behaves like the paper's Fig. 2: the more ambitious the scenario, the further the cloud moves from the diagonal. ${A === "BEV" && B === "FCEV" ? "Look at the green 1.5 °C cloud: FCEVs win only there (BECCS hydrogen)." : ""}`; } }; timer = requestAnimationFrame(tick); }
    $("#m-run").addEventListener("click", run); pair.addEventListener("change", () => { shown = +nIn.value; draw(); });
    nIn.addEventListener("input", () => { $("#m-no").textContent = n0(+nIn.value); shown = Math.min(shown, +nIn.value); draw(); });
    redraws.push(draw); draw();
  })();

  /* ---------- 6. First-order sensitivity ---------- */
  (function () {
    const cnv = $("#g-cnv"), out = $("#g-out"), regF = $("#g-reg");
    function data() {
      if (!regF.value) return MC;
      const r = M.rng(77), arr = []; for (let i = 0; i < 4000; i++) { const s = M.sample(r); s.region = regF.value; const f = {}; PT.forEach((pt) => f[pt] = M.footprint(pt, s).total); arr.push(Object.assign(s, f)); } return arr;
    }
    function y(d) { const o = out.value; if (o === "BEV" || o === "HEV") return d[o]; const A = o.slice(1); return (d[A] - d.HEV) / d.HEV * 100; }
    function run() {
      const D = data(), ys = D.map(y), mu = ys.reduce((a, b) => a + b, 0) / ys.length, V = ys.reduce((a, b) => a + (b - mu) ** 2, 0) / ys.length;
      const keys = { "Vehicle size": (d) => d.size, "Region": (d) => d.region, "Mileage": (d) => Math.min(4, Math.floor((d.km - 100000) / 40000)), "Lifetime": (d) => d.lifetime, "Future scenario": (d) => d.scenario };
      if (regF.value) delete keys.Region;
      const res = Object.entries(keys).map(([k, f]) => { const g = {}; D.forEach((d, i) => { const key = f(d); (g[key] = g[key] || []).push(ys[i]); }); let vb = 0; Object.values(g).forEach((a) => { const m = a.reduce((x, z) => x + z, 0) / a.length; vb += a.length * (m - mu) ** 2; }); return [k, vb / D.length / V]; }).sort((a, b) => b[1] - a[1]);
      const { ctx, w, h } = L.canvas(cnv, 0.4), box = { x0: 130, y0: 10, x1: w - 50, y1: h - 42 };
      const { X } = L.axes(ctx, box, [0, 1], [0, 1], { yticks: [], xticks: [0, .2, .4, .6, .8, 1], xlab: "first-order index (share of the spread explained)" });
      const bh = (box.y1 - box.y0) / res.length;
      res.forEach(([k, s], i) => { const yy = box.y0 + i * bh + bh * 0.2; ctx.fillStyle = L.cv(i === 0 ? "--climate" : "--policy"); ctx.fillRect(X(0), yy, X(s) - X(0), bh * 0.6); ctx.fillStyle = L.cv("--ink"); ctx.textAlign = "right"; ctx.textBaseline = "middle"; ctx.font = "13px " + L.cv("--body"); ctx.fillText(k, box.x0 - 8, yy + bh * 0.3); ctx.textAlign = "left"; ctx.fillText(s.toFixed(2), X(s) + 6, yy + bh * 0.3); });
      const lab = out.options[out.selectedIndex].text;
      $("#g-read").innerHTML = `For <b>${lab}</b>${regF.value ? " in " + rname(regF.value) : ""}, the input that explains most of the spread is <b>${res[0][0]}</b> (${res[0][1].toFixed(2)}). The paper found <b>size and mileage</b> dominate absolute footprints, while <b>region and scenario</b> dominate the BEV-vs-HEV difference. The scenario matters most where the grid is dirty (EEU) and much less where it is already clean (CSA). The indices add up to less than 1 because inputs also interact (that is what the paper's total-order indices capture).`;
    }
    [out, regF].forEach((e) => e.addEventListener("change", run)); $("#g-run").addEventListener("click", run);
    redraws.push(run); run();
  })();

  /* ---------- 7. Exercises (answers computed by the model) ---------- */
  (function () {
    const F = (pt, o) => M.footprint(pt, o || {});
    const bs = F("BEV", { scenario: "No scenario" }).total, bp = F("BEV").total;
    const parts = F("BEV").parts, share = parts.Production / bp * 100;
    const be1 = M.breakeven({ region: "CHI", scenario: "No scenario" }), be2 = M.breakeven({ region: "CHI", scenario: "Ambitious (<2 °C)" });
    const q15 = MC.filter((d) => d.scenario === "Very ambitious (1.5 °C)"), m15b = q15.reduce((a, d) => a + d.BEV, 0) / q15.length, m15h = q15.reduce((a, d) => a + d.HEV, 0) / q15.length;
    const b35 = F("BEV", { build_year: 2035 }).total;
    const uf2 = F("PHEV", { uf: 0.2 }).total, uf8 = F("PHEV", { uf: 0.8 }).total, hev = F("HEV").total;
    const tbl = (rows) => `<table>${rows.map((r) => `<tr>${r.map((c) => `<td>${c}</td>`).join("")}</tr>`).join("")}</table>`;
    const ex = [
      { t: "Typical vs time-adjusted", q: "A Medium SUV BEV in China is driven 200,000 km over 15 years. By what <b>percentage</b> does its footprint fall when you switch from a typical LCA to the &lt;2 °C pLCA? (Type a negative number, e.g. −20.)", a: (bp / bs - 1) * 100, show: ((bp / bs - 1) * 100).toFixed(1) + "%", tol: 0.15,
        hint: "Use the calculator with region China and scenario Ambitious (<2 °C), and read the two BEV bars. % change = (pLCA − static) ÷ static × 100.",
        sol: `Static = ${bs.toFixed(1)} g/km; pLCA = ${bp.toFixed(1)} g/km. Change = (${bp.toFixed(1)} − ${bs.toFixed(1)}) ÷ ${bs.toFixed(1)} = <b>${((bp / bs - 1) * 100).toFixed(1)}%</b>. Only the electricity part changes: production and end-of-life happen at the same time in both methods. (Paper, Fig. 3: −31%.)` },
      { t: "Where is the hotspot?", q: "In the same pLCA case, what <b>share (%)</b> of the BEV's footprint comes from production?", a: share, show: share.toFixed(0) + "%", tol: 0.1,
        hint: "Production per km = production in kg ÷ km × 1000. Here: 15,000 kg ÷ 200,000 km.",
        sol: tbl(Object.entries(parts).filter(([, v]) => v).map(([k, v]) => [k, v.toFixed(1) + " g/km", (v / bp * 100).toFixed(0) + "%"])) + `Production = 15.0 t × 1,000,000 ÷ 200,000 km = 75 g/km, which is <b>${share.toFixed(0)}%</b> of ${bp.toFixed(1)}. As the grid cleans up, production becomes the hotspot. That is why the paper ends by saying BEV manufacturing still needs to get cleaner.` },
      { t: "Breakeven mileage", q: "What is the BEV-vs-HEV breakeven mileage (km) for China, Medium SUV, 15 years, under <b>&lt;2 °C</b>?", a: be2, show: n0(be2) + " km", tol: 0.08,
        hint: "Breakeven: production gap ÷ use-phase saving per km. Production gap = 15.3 − 7.8 = 7.5 t. Saving per km = HEV use − BEV use (both in kg/km).",
        sol: (() => { const h = F("HEV"), b = F("BEV"); const hu = (h.parts["Diesel supply"] + h.parts.Exhaust) / 1000, bu = b.parts.Electricity / 1000; return `HEV use ≈ ${(hu * 1000).toFixed(1)} g/km; BEV use ≈ ${(bu * 1000).toFixed(1)} g/km; saving ≈ ${((hu - bu) * 1000).toFixed(1)} g/km.<br>7,500 kg ÷ ${(hu - bu).toFixed(4)} kg/km ≈ <b>${n0(7500 / (hu - bu))} km</b> (model, by bisection: ${n0(be2)} km). Typical LCA: ${n0(be1)} km. Because the time-adjusted grid is cleaner, the BEV pays back its debt much sooner.`; })() },
      { t: "Read the Monte Carlo", q: "Run the 5,000-car Monte Carlo (BEV vs HEV). In the <b>1.5 °C</b> scenario, by what percentage is the mean BEV footprint below the mean HEV footprint?", a: (1 - m15b / m15h) * 100, show: ((1 - m15b / m15h) * 100).toFixed(0) + "%", tol: 0.12,
        hint: "Set samples to 5,000, press Run, and read the last column of the 1.5 °C row.",
        sol: `Mean BEV = ${m15b.toFixed(0)}, mean HEV = ${m15h.toFixed(0)} g/km, so 1 − ${m15b.toFixed(0)}/${m15h.toFixed(0)} = <b>${((1 - m15b / m15h) * 100).toFixed(0)}%</b>. Paper: 47% (142 vs 270). The toy is gentler because it leaves out how production gets cleaner upstream. The Python file uses a different random stream, so its value differs by a point or so.` },
      { t: "A car built in 2035", q: "Switch <b>Built in</b> to 2035 (China, &lt;2 °C). By what percentage does the BEV footprint fall compared with a 2025-built BEV? (Type a positive number.)", a: (1 - b35 / bp) * 100, show: ((1 - b35 / bp) * 100).toFixed(0) + "%", tol: 0.12,
        hint: "Two things change: production is 23% cleaner (factor 0.77) and the car is 5% more efficient. It is also driven on the 2035–2050 grid.",
        sol: `2025 build: ${bp.toFixed(1)} g/km. 2035 build: ${b35.toFixed(1)} g/km. Fall = <b>${((1 - b35 / bp) * 100).toFixed(0)}%</b>. Three effects stack: cleaner manufacturing, better efficiency, and a cleaner grid during 2035–2050. This matches the paper's Fig. 3c, where the ranking stays the same (BEV &lt; PHEV/FCEV &lt; HEV).` },
      { t: "PHEV driver behaviour", q: "The paper assumes PHEVs drive 47% of km on electricity (the <b>utility factor</b>). What is the PHEV footprint (g/km) if the driver rarely charges (utility factor 0.2)? China, &lt;2 °C.", a: uf2, show: uf2.toFixed(0) + " g/km", tol: 0.06,
        hint: "In the toy model: kWh/km = 0.36 × UF and L/km = 0.053 × (1 − UF). Or run Exercise 6 in the Python file.",
        sol: tbl([["UF 0.2", uf2.toFixed(1) + " g/km"], ["UF 0.47 (paper)", F("PHEV").total.toFixed(1) + " g/km"], ["UF 0.8", uf8.toFixed(1) + " g/km"], ["BEV", bp.toFixed(1) + " g/km"], ["HEV", hev.toFixed(1) + " g/km"]]) + `With little charging, the PHEV moves towards the HEV and carries a bigger battery for nothing. That is why the paper calls PHEVs a <b>high-risk</b> option: the result depends on the driver.` },
    ];
    $("#ex-list").innerHTML = ex.map((e, i) => `<div class="pl-ex" data-answer="${e.a}" data-tol="${e.tol}" data-show="${e.show}"><h3>Exercise ${i + 1}: ${e.t}</h3><p>${e.q}</p>
<div class="pl-row"><input class="pl-ans" type="text" inputmode="decimal" aria-label="Your answer to exercise ${i + 1}" placeholder="your answer"><button class="btn quiet pl-checkbtn" type="button">Check</button></div><p class="pl-check" aria-live="polite"></p>
<details><summary>Hint</summary><div class="pl-sol">${e.hint}</div></details><details><summary>Worked solution</summary><div class="pl-sol">${e.sol}</div></details></div>`).join("");
  })();

  L.quiz($("#pq"));
})();
