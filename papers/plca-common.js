/* Shared helpers for the paper-study pages (canvas drawing, colours, quizzes, exercises). */
(function () {
  const cv = (n) => getComputedStyle(document.documentElement).getPropertyValue(n).trim() || "#888";
  const PTC = { BEV: "--land", PHEV: "--water", HEV: "--energy", FCEV: "--economy", ICEV: "--climate" };
  const SCC = { "No scenario": "--data", "No climate action": "--climate", "Baseline (NDCs)": "--energy", "Ambitious (<2 °C)": "--water", "Very ambitious (1.5 °C)": "--land" };
  const PARTC = { "Production": "--data", "Electricity": "--water", "Diesel supply": "--energy", "Exhaust": "--climate", "Hydrogen": "--economy", "End of life": "--policy" };
  function canvas(cnv, hRatio) {
    const dpr = window.devicePixelRatio || 1, w = cnv.clientWidth || 600, h = Math.round(w * (hRatio || 0.5));
    cnv.width = w * dpr; cnv.height = h * dpr; cnv.style.height = h + "px";
    const ctx = cnv.getContext("2d"); ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    ctx.font = "13px " + (cv("--body") || "sans-serif"); return { ctx, w, h };
  }
  function axes(ctx, box, xr, yr, opt) {
    opt = opt || {}; const { x0, y0, x1, y1 } = box;
    const X = (v) => x0 + (v - xr[0]) / (xr[1] - xr[0]) * (x1 - x0), Y = (v) => y1 - (v - yr[0]) / (yr[1] - yr[0]) * (y1 - y0);
    ctx.strokeStyle = cv("--grid"); ctx.fillStyle = cv("--muted"); ctx.lineWidth = 1; ctx.font = "12px " + cv("--body");
    const yt = opt.yticks || nice(yr, 5), xt = opt.xticks || nice(xr, 6);
    ctx.textAlign = "right"; ctx.textBaseline = "middle";
    yt.forEach((v) => { ctx.beginPath(); ctx.moveTo(x0, Y(v)); ctx.lineTo(x1, Y(v)); ctx.stroke(); ctx.fillText((opt.yfmt || fmt)(v), x0 - 6, Y(v)); });
    ctx.textAlign = "center"; ctx.textBaseline = "top";
    xt.forEach((v) => ctx.fillText((opt.xfmt || fmt)(v), X(v), y1 + 6));
    ctx.strokeStyle = cv("--line"); ctx.beginPath(); ctx.moveTo(x0, y0); ctx.lineTo(x0, y1); ctx.lineTo(x1, y1); ctx.stroke();
    if (opt.xlab) { ctx.fillText(opt.xlab, (x0 + x1) / 2, y1 + 24); }
    if (opt.ylab) { ctx.save(); ctx.translate(14, (y0 + y1) / 2); ctx.rotate(-Math.PI / 2); ctx.textBaseline = "middle"; ctx.fillText(opt.ylab, 0, 0); ctx.restore(); }
    return { X, Y };
  }
  function nice(r, n) {
    const span = r[1] - r[0], raw = span / n, mag = Math.pow(10, Math.floor(Math.log10(raw))), st = [1, 2, 2.5, 5, 10].map((m) => m * mag).find((s) => span / s <= n) || raw;
    const out = []; for (let v = Math.ceil(r[0] / st) * st; v <= r[1] + 1e-9; v += st) out.push(+v.toFixed(10)); return out;
  }
  const fmt = (v) => Math.abs(v) >= 1000 ? (v / 1000).toFixed(v % 1000 ? 1 : 0) + "k" : (Math.round(v * 100) / 100).toString();
  function legend(el, items) { el.innerHTML = items.map(([t, c, dash]) => `<span class="pl-key"><i style="background:${dash ? "transparent" : cv(c)};border-color:${cv(c)}${dash ? ";border-style:dashed" : ""}"></i>${t}</span>`).join(""); }
  function opts(sel, arr, val, lab) { sel.innerHTML = arr.map((a) => `<option value="${a}"${a === val ? " selected" : ""}>${lab ? lab(a) : a}</option>`).join(""); }

  /* Multiple-choice quiz: <div class="pl-quiz" data-q='[{q,o:[..],a:idx,e}]'> */
  function quiz(root) {
    const qs = JSON.parse(root.dataset.q); let score = 0, done = 0;
    root.innerHTML = qs.map((q, i) => `<fieldset class="pl-q"><legend><b>${i + 1}.</b> ${q.q}</legend>${q.o.map((o, j) => `<label><input type="radio" name="${root.id}-${i}" value="${j}"> ${o}</label>`).join("")}<p class="pl-fb" hidden aria-live="polite"></p></fieldset>`).join("") + `<p class="pl-score muted" aria-live="polite"></p>`;
    root.querySelectorAll(".pl-q").forEach((fs, i) => fs.addEventListener("change", (ev) => {
      if (fs.dataset.done) return; fs.dataset.done = 1; done++;
      const ok = +ev.target.value === qs[i].a; if (ok) score++;
      fs.querySelectorAll("input").forEach((inp) => { inp.disabled = true; if (+inp.value === qs[i].a) inp.parentElement.classList.add("pl-right"); else if (inp.checked) inp.parentElement.classList.add("pl-wrong"); });
      const fb = fs.querySelector(".pl-fb"); fb.hidden = false; fb.innerHTML = `<b>${ok ? "Right." : "Not quite."}</b> ${qs[i].e}`;
      root.querySelector(".pl-score").textContent = `Score so far: ${score} / ${done}` + (done === qs.length ? (score === qs.length ? " — perfect!" : " — review the explanations above.") : "");
    }));
  }
  /* Numeric exercise: check an answer within a tolerance (relative) */
  function numCheck(btn) {
    const box = btn.closest(".pl-ex"), inp = box.querySelector("input.pl-ans"), out = box.querySelector(".pl-check");
    const want = +box.dataset.answer, tol = +(box.dataset.tol || 0.1), v = parseFloat(String(inp.value).replace(/[, ]/g, ""));
    if (isNaN(v)) { out.textContent = "Type a number first."; return; }
    const ok = Math.abs(v - want) <= Math.abs(want) * tol;
    out.innerHTML = ok ? `<b class="pl-good">Close enough!</b> The model gives ${box.dataset.show || want}.` : `<b class="pl-bad">Not yet.</b> ${v > want ? "Too high" : "Too low"} — open the hint, or the worked solution.`;
  }
  document.addEventListener("click", (e) => { if (e.target.matches(".pl-checkbtn")) numCheck(e.target); });
  window.PL = { cv, PTC, SCC, PARTC, canvas, axes, nice, fmt, legend, opts, quiz };
})();
