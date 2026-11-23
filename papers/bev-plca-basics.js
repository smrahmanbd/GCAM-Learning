/* Basics page: car animations, efficiency, grid and hydrogen mixers, sorting game, LCA animation, scenarios, problems. */
(function () {
  const M = window.PLCA, P = M.P, L = window.PL, $ = (s) => document.querySelector(s), $$ = (s) => [...document.querySelectorAll(s)];
  const redraws = []; window.addEventListener("resize", () => redraws.forEach((f) => f()));
  document.getElementById("theme") && document.getElementById("theme").addEventListener("click", () => setTimeout(() => redraws.forEach((f) => f()), 30));

  /* ---------- 1. cars ---------- */
  const CARS = {
    ICEV: { name: "Internal combustion (ICEV)", short: "Engine only. The classic petrol or diesel car.", comp: ["engine", "tank", "exhaust"], bat: null,
      modes: { "Drive": { f: ["tank-eng", "eng-wheel"], ex: 1, spin: 1, cap: "Diesel → engine → wheels. About 3/4 of the fuel's energy is lost as heat." }, "Brake": { f: [], spin: 2, cap: "Braking turns all that motion into wasted heat in the brake pads." } },
      rows: [["Energy in", "Diesel or petrol"], ["Tailpipe CO₂", "Yes, all of it"], ["Battery", "Only a 12 V starter battery"], ["In the paper", "Not modelled. The HEV stands in as the main combustion car."]],
      text: "The reference point. Every litre of diesel burned releases about <b>2.68 kg CO₂</b> from the exhaust, plus about 0.5 kg from producing and transporting the fuel." },
    HEV: { name: "Hybrid electric (HEV)", short: "Engine plus a small battery charged by braking.", comp: ["engine", "tank", "exhaust", "motor", "battery"], bat: [80, "< 5 kWh"],
      modes: { "Pull away": { f: ["bat-mot", "mot-wheel"], spin: 1, cap: "At low speed the motor moves the car on battery power alone." },
        "Accelerate": { f: ["tank-eng", "eng-wheel", "bat-mot", "mot-wheel"], ex: 1, spin: 1, cap: "Engine and motor work together, so a smaller engine is enough." },
        "Cruise & charge": { f: ["tank-eng", "eng-wheel", "eng-mot", "bat-mot:rev"], ex: 1, spin: 1, cap: "The engine drives the wheels and tops up the battery through the generator." },
        "Brake (regen)": { f: ["mot-wheel:rev", "bat-mot:rev"], spin: 2, cap: "Regenerative braking: the wheels turn the motor as a generator and refill the battery." } },
      rows: [["Energy in", "Diesel only (cannot plug in)"], ["Tailpipe CO₂", "Yes"], ["Battery", "< 5 kWh"], ["Energy use (paper)", "3.7–7.5 L per 100 km"], ["In the paper", "The main combustion car. It had the highest footprint in almost every case."]],
      text: "A hybrid saves fuel by recovering braking energy and running the engine more efficiently. But <b>all</b> its energy still comes from diesel, so it gains little from a cleaner electricity grid." },
    PHEV: { name: "Plug-in hybrid (PHEV)", short: "A bigger battery you can plug in, plus an engine.", comp: ["engine", "tank", "exhaust", "motor", "battery", "plug"], bat: [120, "Battery ~10–20 kWh"],
      modes: { "Electric mode": { f: ["bat-mot", "mot-wheel"], spin: 1, cap: "With a charged battery it drives like a BEV, for perhaps 40–80 km." },
        "Hybrid mode": { f: ["tank-eng", "eng-wheel", "bat-mot", "mot-wheel"], ex: 1, spin: 1, cap: "With the battery empty it behaves like an HEV." },
        "Brake (regen)": { f: ["mot-wheel:rev", "bat-mot:rev"], spin: 2, cap: "Regenerative braking refills the battery." },
        "Plugged in": { f: ["plug-bat"], cap: "Charging from the grid. How clean this is depends on the grid's mix." } },
      rows: [["Energy in", "Electricity and diesel"], ["Tailpipe CO₂", "Only in hybrid mode"], ["Utility factor", "47% of km electric (paper's assumption)"], ["Energy use (paper)", "11.8–21.4 kWh and 2.0–3.0 L per 100 km"], ["In the paper", "In between BEV and HEV, and 'high-risk' because it depends on how often drivers charge."]],
      text: "The <b>utility factor</b> is the share of kilometres driven on electricity. Drivers who rarely charge carry a heavy battery around and burn diesel anyway." },
    BEV: { name: "Battery electric (BEV)", short: "Big battery, electric motor, no engine.", comp: ["motor", "battery", "plug"], bat: [190, "Battery 14–80 kWh (NMC-811)"],
      modes: { "Drive": { f: ["bat-mot", "mot-wheel"], spin: 1, cap: "Battery → motor → wheels. About 3/4 of the battery's energy reaches the wheels." },
        "Brake (regen)": { f: ["mot-wheel:rev", "bat-mot:rev"], spin: 2, cap: "Regenerative braking recovers energy that would otherwise become heat." },
        "Plugged in": { f: ["plug-bat"], cap: "All its use-phase emissions happen at the power station, so the grid is what matters." } },
      rows: [["Energy in", "Electricity only"], ["Tailpipe CO₂", "None"], ["Battery", "14–80 kWh, NMC-811 lithium-ion"], ["Energy use (paper)", "19.2–28.5 kWh per 100 km"], ["In the paper", "Lowest footprint in about 99% of cases. Highest production footprint."]],
      text: "A BEV has a big <b>carbon debt</b> from making its battery. It pays that debt back with every km, because charging emits less than burning diesel, and the payback gets faster as grids clean up." },
    FCEV: { name: "Fuel cell electric (FCEV)", short: "Makes its own electricity from hydrogen.", comp: ["fc", "h2", "motor", "battery", "water", "pump"], bat: [80, "Buffer"],
      modes: { "Drive": { f: ["h2-fc", "fc-mot", "mot-wheel"], water: 1, spin: 1, cap: "Hydrogen + oxygen in the fuel cell → electricity → motor. Only water comes out." },
        "Accelerate": { f: ["h2-fc", "fc-mot", "bat-mot", "mot-wheel"], water: 1, spin: 1, cap: "A small buffer battery helps with sudden power demand." },
        "Brake (regen)": { f: ["mot-wheel:rev", "bat-mot:rev"], spin: 2, cap: "Braking energy goes into the buffer battery." },
        "Refuel": { f: ["pump-h2"], cap: "A few minutes at a hydrogen pump. How green is the hydrogen? That decides the footprint." } },
      rows: [["Energy in", "Hydrogen"], ["Tailpipe CO₂", "None (water only)"], ["Fuel cell", "Proton exchange membrane (PEM)"], ["In the paper", "Second best in most scenarios; best only in 1.5 °C (BECCS hydrogen)"]],
      text: "Today almost all hydrogen is made from natural gas, which emits roughly <b>10–12 kg CO₂e per kg H₂</b>. Making it by electrolysis with clean power, or from biomass with carbon capture, changes the picture completely." },
  };
  const ALLC = ["engine", "tank", "exhaust", "motor", "battery", "plug", "fc", "h2", "water", "pump"];
  const ALLF = ["tank-eng", "eng-wheel", "mot-wheel", "bat-mot", "plug-bat", "h2-fc", "fc-mot", "fc-bat", "pump-h2", "eng-mot"];
  let car = "BEV", mode = "Drive";
  $("#car-cards").innerHTML = Object.entries(CARS).map(([k, c]) => `<button class="pl-card" type="button" data-car="${k}" aria-pressed="${k === car}"><span class="pl-chip" style="background:${L.cv(L.PTC[k])}">${k}</span><h4>${c.name}</h4><p>${c.short}</p></button>`).join("");
  function showCar() {
    const c = CARS[car], m = c.modes[mode];
    $$("#car-cards .pl-card").forEach((b) => b.setAttribute("aria-pressed", b.dataset.car === car));
    $("#mode-row").innerHTML = Object.keys(c.modes).map((k) => `<button class="btn ${k === mode ? "" : "quiet"}" type="button" data-mode="${k}">${k}</button>`).join("");
    ALLC.forEach((id) => { const el = document.getElementById("c-" + id); if (el) el.toggleAttribute("hidden", !c.comp.includes(id)); });
    if (c.bat) { document.getElementById("bat-rect").setAttribute("width", c.bat[0]); const lb = document.getElementById("bat-label"); lb.setAttribute("x", 270 + c.bat[0] / 2); lb.textContent = c.bat[1]; lb.setAttribute("font-size", c.bat[0] < 100 ? 10 : 11); }
    const on = {}; m.f.forEach((f) => { const [id, r] = f.split(":"); on[id] = r || "fwd"; });
    ALLF.forEach((id) => { const el = document.getElementById("f-" + id); el.toggleAttribute("hidden", !on[id]); el.classList.toggle("rev", on[id] === "rev"); });
    document.getElementById("puffs").toggleAttribute("hidden", !m.ex);
    const svg = $("#car-svg"); svg.classList.toggle("spin", m.spin === 1); svg.classList.toggle("spin-rev", m.spin === 2);
    document.getElementById("c-water").toggleAttribute("hidden", !(c.comp.includes("water") && m.water));
    $("#mode-caption").textContent = m.cap;
    $("#car-text").innerHTML = `<h3 style="margin-top:0;color:${L.cv(L.PTC[car])}">${c.name}</h3><p>${c.text}</p>`;
    $("#car-tbl").innerHTML = c.rows.map(([a, b]) => `<tr><th>${a}</th><td>${b}</td></tr>`).join("");
  }
  $("#car-cards").addEventListener("click", (e) => { const b = e.target.closest("[data-car]"); if (!b) return; car = b.dataset.car; mode = Object.keys(CARS[car].modes)[0]; showCar(); });
  $("#mode-row").addEventListener("click", (e) => { const b = e.target.closest("[data-mode]"); if (!b) return; mode = b.dataset.mode; showCar(); });
  showCar(); redraws.push(showCar);

  /* ---------- 2. efficiency ---------- */
  const EFF = [["ICEV", 25, "heat from the engine and exhaust, friction, idling"], ["HEV", 35, "engine heat (less waste, thanks to regen and engine-off)"], ["PHEV", 72, "in electric mode: charging, battery and motor losses"], ["BEV", 77, "charging, battery and motor losses; some regen recovered"], ["FCEV", 45, "about half the hydrogen's energy is lost as heat in the fuel cell"]];
  $("#eff-bars").innerHTML = EFF.map(([k, v, why]) => `<div style="margin:10px 0"><div style="display:flex;justify-content:space-between;font-size:.92rem"><b style="color:${L.cv(L.PTC[k])}">${k}</b><span class="muted">${why}</span></div>
<div style="display:flex;height:26px;border-radius:6px;overflow:hidden;background:var(--paper-3)"><div class="effw" data-v="${v}" style="width:0;background:${L.cv(L.PTC[k])};transition:width 1.6s ease;color:#fff;font-weight:700;font-size:.85rem;display:flex;align-items:center;padding-left:6px;white-space:nowrap">${v} to the wheels</div><div class="effl" style="flex:1;display:flex;align-items:center;justify-content:flex-end;padding-right:6px;font-size:.85rem;color:var(--muted);opacity:0;transition:opacity .6s 1.4s">${100 - v} lost</div></div></div>`).join("");
  $("#eff-play").addEventListener("click", () => { $$(".effw").forEach((d) => { d.style.width = 0; }); $$(".effl").forEach((d) => d.style.opacity = 0); setTimeout(() => { $$(".effw").forEach((d) => d.style.width = d.dataset.v + "%"); $$(".effl").forEach((d) => d.style.opacity = 1); }, 60); });

  /* ---------- 3. grid mixer ---------- */
  const GS = [["Coal", 0.82, "--data"], ["Gas", 0.49, "--energy"], ["Nuclear", 0.012, "--economy"], ["Hydro", 0.024, "--water"], ["Wind", 0.011, "--land"], ["Solar", 0.048, "--climate"]];
  const PRE = { "Coal-heavy (like China or India today)": [60, 15, 4, 13, 5, 3], "Gas-heavy": [5, 60, 10, 10, 10, 5], "Hydro & nuclear (like Canada)": [5, 8, 15, 62, 7, 3], "A 1.5 °C grid around 2040": [0, 8, 15, 15, 35, 27] };
  let gmix = PRE["Coal-heavy (like China or India today)"].slice();
  $("#grid-presets").innerHTML = Object.keys(PRE).map((k) => `<button class="btn quiet" type="button" data-pre="${k}">${k}</button>`).join("");
  $("#grid-sliders").innerHTML = GS.map(([n], i) => `<label>${n} <output id="gs-o${i}"></output><input type="range" min="0" max="100" step="1" id="gs-${i}" aria-label="${n} share"></label>`).join("");
  const gridI = () => { const s = gmix.reduce((a, b) => a + b, 0) || 1; return gmix.reduce((a, v, i) => a + v / s * GS[i][1], 0) / 0.92; };
  const HEVUSE = 0.055 * (2.68 + 0.55) * 1000;
  function drawGrid() {
    const s = gmix.reduce((a, b) => a + b, 0) || 1; GS.forEach((g, i) => { $("#gs-" + i).value = gmix[i]; $("#gs-o" + i).textContent = Math.round(gmix[i] / s * 100) + "%"; });
    const I = gridI(), bev = 0.2 * I * 1000;
    const { ctx, w, h } = L.canvas($("#grid-cnv"), 0.62), box = { x0: 70, y0: 16, x1: w - 60, y1: h - 40 };
    const max = 300; const { X } = L.axes(ctx, box, [0, max], [0, 1], { yticks: [], xlab: "g CO₂e per km (200,000 km life)" });
    const rows = [["BEV", 75, bev, "--land"], ["HEV", 37.5, HEVUSE, "--energy"]]; const bh = (box.y1 - box.y0) / 2;
    rows.forEach(([k, prod, use, c], i) => { const y = box.y0 + i * bh + bh * 0.22, hh = bh * 0.56; ctx.globalAlpha = 0.35; ctx.fillStyle = L.cv(c); ctx.fillRect(X(0), y, X(prod) - X(0), hh); ctx.globalAlpha = 1; ctx.fillRect(X(prod), y, X(prod + use) - X(prod), hh);
      ctx.fillStyle = L.cv("--ink"); ctx.font = "bold 14px " + L.cv("--body"); ctx.textAlign = "right"; ctx.textBaseline = "middle"; ctx.fillText(k, box.x0 - 8, y + hh / 2); ctx.textAlign = "left"; ctx.font = "13px " + L.cv("--body"); ctx.fillText(Math.round(prod + use), X(prod + use) + 6, y + hh / 2);
      ctx.fillStyle = L.cv("--paper"); ctx.font = "11px " + L.cv("--body"); if (X(prod) - X(0) > 60) ctx.fillText("production", X(0) + 4, y + hh / 2); if (X(prod + use) - X(prod) > 40) ctx.fillText("use", X(prod) + 4, y + hh / 2); });
    $("#grid-read").innerHTML = `Grid intensity: <b>${I.toFixed(3)} kg CO₂e/kWh</b>. BEV charging: <b>${Math.round(bev)} g/km</b> against <b>${Math.round(HEVUSE)} g/km</b> for the hybrid's diesel. ` + (75 + bev < 37.5 + HEVUSE ? `With production included, the BEV is <b>${Math.round(100 * (1 - (75 + bev) / (37.5 + HEVUSE)))}% lower</b> over 200,000 km.` : `<b>The hybrid wins</b> on this very dirty grid, the edge case the paper mentions for grids above about 0.6 kg/kWh.`);
  }
  $("#grid-sliders").addEventListener("input", (e) => { const i = +e.target.id.split("-")[1]; gmix[i] = +e.target.value; drawGrid(); drawH2(); });
  $("#grid-presets").addEventListener("click", (e) => { const b = e.target.closest("[data-pre]"); if (!b) return; gmix = PRE[b.dataset.pre].slice(); drawGrid(); drawH2(); });

  /* ---------- 4. hydrogen mixer ---------- */
  const HS = [["Natural gas reforming (SMR)", () => 11], ["Coal gasification", () => 20], ["Electrolysis on YOUR grid", () => 52 * gridI()], ["Electrolysis, wind/solar", () => 1], ["Biomass + CCS (BECCS)", () => -15]];
  let hmix = [80, 15, 5, 0, 0];
  $("#h2-sliders").innerHTML = HS.map(([n], i) => `<label>${n} <output id="hs-o${i}"></output><input type="range" min="0" max="100" step="1" id="hs-${i}" aria-label="${n} share"></label>`).join("");
  function drawH2() {
    const s = hmix.reduce((a, b) => a + b, 0) || 1; HS.forEach((g, i) => { $("#hs-" + i).value = hmix[i]; $("#hs-o" + i).textContent = Math.round(hmix[i] / s * 100) + "% · " + g[1]().toFixed(1) + " kg/kg"; });
    const H = hmix.reduce((a, v, i) => a + v / s * HS[i][1](), 0), fc = 0.01 * H * 1000, bev = 0.2 * gridI() * 1000;
    const { ctx, w, h } = L.canvas($("#h2-cnv"), 0.62), box = { x0: 70, y0: 16, x1: w - 60, y1: h - 40 };
    const lo = Math.min(0, fc) - 10; const { X } = L.axes(ctx, box, [lo, 260], [0, 1], { yticks: [], xlab: "use-phase g CO₂e per km" });
    const rows = [["FCEV", fc, "--economy"], ["BEV", bev, "--land"], ["HEV", HEVUSE, "--energy"]], bh = (box.y1 - box.y0) / 3;
    ctx.strokeStyle = L.cv("--ink-soft"); ctx.beginPath(); ctx.moveTo(X(0), box.y0); ctx.lineTo(X(0), box.y1); ctx.stroke();
    rows.forEach(([k, v, c], i) => { const y = box.y0 + i * bh + bh * 0.22, hh = bh * 0.56; ctx.fillStyle = L.cv(c); ctx.fillRect(Math.min(X(0), X(v)), y, Math.abs(X(v) - X(0)), hh); ctx.fillStyle = L.cv("--ink"); ctx.font = "bold 14px " + L.cv("--body"); ctx.textAlign = "right"; ctx.textBaseline = "middle"; ctx.fillText(k, box.x0 - 8, y + hh / 2); ctx.textAlign = "left"; ctx.font = "13px " + L.cv("--body"); ctx.fillText(Math.round(v), Math.max(X(v), X(0)) + 6, y + hh / 2); });
    $("#h2-read").innerHTML = `Hydrogen: <b>${H.toFixed(1)} kg CO₂e per kg H₂</b>, so the FCEV emits <b>${Math.round(fc)} g/km</b> in use. ` + (fc < 0 ? "Below zero: the BECCS share removes more CO₂ than everything else emits." : fc > bev ? "Higher than the BEV on the same grid. Making hydrogen and turning it back into electricity loses a lot of energy." : "Lower than the BEV here.") + " Try: set everything to grid electrolysis, then switch the grid preset to coal-heavy.";
  }
  $("#h2-sliders").addEventListener("input", (e) => { const i = +e.target.id.split("-")[1]; hmix[i] = +e.target.value; drawH2(); });
  drawGrid(); drawH2(); redraws.push(drawGrid, drawH2);

  /* ---------- 5. sorting game ---------- */
  const BINS = [["hi", "High carbon (fossil)"], ["lo", "Low carbon"], ["neg", "Carbon-negative"]];
  const CARDS = [["Coal power plant", "hi", "~820 g/kWh: the dirtiest electricity."], ["Gas power plant", "hi", "~490 g/kWh: cleaner than coal, still fossil."], ["Wind turbines", "lo", "~11 g/kWh over their life (making the steel and blades)."], ["Solar panels", "lo", "~48 g/kWh, mostly from manufacturing."], ["Nuclear power", "lo", "~12 g/kWh over its life."],
    ["Hydrogen from natural gas (SMR)", "hi", "Most hydrogen today; ~10–12 kg CO₂e per kg."], ["Electrolysis with wind power", "lo", "Clean electricity in, clean hydrogen out."], ["Electrolysis on a coal-heavy grid", "hi", "~52 kWh/kg × a dirty grid: often WORSE than SMR."], ["Fossil diesel", "hi", "2.68 kg CO₂ per litre at the tailpipe, plus supply."],
    ["Biodiesel", "lo", "Its tailpipe CO₂ was taken from the air by plants. Growing and processing still emit some."], ["Biomass power with CCS (BECCS)", "neg", "Plants absorb CO₂, which is then captured and stored underground: net removal."], ["Hydrogen from biomass with CCS", "neg", "The route that makes FCEVs win in the paper's 1.5 °C scenario."]];
  let sel = null;
  function resetSort() {
    $("#sort-pool").innerHTML = CARDS.map((c, i) => `<span class="pl-tag" draggable="true" tabindex="0" role="button" data-i="${i}">${c[0]}</span>`).sort(() => Math.random() - 0.5).join("");
    $("#sort-bins").innerHTML = BINS.map(([k, t]) => `<div class="pl-bin" data-bin="${k}" tabindex="0" role="button" aria-label="Box: ${t}"><h5>${t}</h5><div class="pl-sort"></div></div>`).join("");
    $("#sort-fb").textContent = "Sort all 12 cards, then press Check."; sel = null;
  }
  const place = (tag, bin) => { tag.classList.remove("sel", "ok", "no"); bin.querySelector(".pl-sort").appendChild(tag); };
  document.addEventListener("dragstart", (e) => { if (e.target.classList && e.target.classList.contains("pl-tag")) e.dataTransfer.setData("text", e.target.dataset.i); });
  $("#sort-bins").addEventListener("dragover", (e) => { const b = e.target.closest(".pl-bin"); if (b) { e.preventDefault(); b.classList.add("over"); } });
  $("#sort-bins").addEventListener("dragleave", (e) => { const b = e.target.closest(".pl-bin"); if (b) b.classList.remove("over"); });
  $("#sort-bins").addEventListener("drop", (e) => { const b = e.target.closest(".pl-bin"); if (!b) return; e.preventDefault(); b.classList.remove("over"); place(document.querySelector(`.pl-tag[data-i="${e.dataTransfer.getData("text")}"]`), b); });
  document.addEventListener("click", (e) => { const t = e.target.closest(".pl-tag"); if (t && sel && sel !== t && t.closest(".pl-bin")) { place(sel, t.closest(".pl-bin")); sel = null; return; } if (t && t.closest("#sort")) { $$(".pl-tag").forEach((x) => x.classList.remove("sel")); sel = t; t.classList.add("sel"); return; } const b = e.target.closest(".pl-bin"); if (b && sel) { place(sel, b); sel = null; } });
  document.addEventListener("keydown", (e) => { if ((e.key === "Enter" || e.key === " ") && (e.target.matches(".pl-tag") || e.target.matches(".pl-bin"))) { e.preventDefault(); e.target.click(); } });
  $("#sort-check").addEventListener("click", () => { let ok = 0, placed = 0; const notes = []; $$("#sort-bins .pl-tag").forEach((t) => { placed++; const c = CARDS[+t.dataset.i], good = t.closest(".pl-bin").dataset.bin === c[1]; t.classList.toggle("ok", good); t.classList.toggle("no", !good); if (good) ok++; else notes.push(`<li><b>${c[0]}</b> → ${BINS.find((b) => b[0] === c[1])[1]}: ${c[2]}</li>`); });
    $("#sort-fb").innerHTML = `<b>${ok} of ${placed}</b> placed correctly${placed < CARDS.length ? ` (${CARDS.length - placed} still to sort)` : ""}. ` + (notes.length ? `<ul>${notes.join("")}</ul>` : ok === CARDS.length ? "Perfect! The key lesson is that the same technology, electrolysis, can be clean or dirty depending on the electricity it uses." : ""); });
  $("#sort-reset").addEventListener("click", resetSort); resetSort();

  /* ---------- 6. LCA animation ---------- */
  (function () {
    const cnv = $("#lca-cnv"), meth = $("#lca-meth"); let t = 1, raf = null;
    const STAGES = ["Production\n(2025)", "Use\n2025–30", "Use\n2030–35", "Use\n2035–40", "End of life\n(2040)"];
    function data(pt) { const r = M.footprint(pt, { region: "CHI", scenario: meth.value }); const y = r.yearly; return [r.kg.Production, y.slice(0, 5).reduce((a, b) => a + b, 0), y.slice(5, 10).reduce((a, b) => a + b, 0), y.slice(10, 15).reduce((a, b) => a + b, 0), r.kg["End of life"]].map((v) => v / 1000); }
    const SC = ["--data", "--water", "--water", "--water", "--policy"];
    function draw() {
      const D = { BEV: data("BEV"), HEV: data("HEV") }, { ctx, w, h } = L.canvas(cnv, 0.62), box = { x0: 50, y0: 16, x1: w - 150, y1: h - 30 };
      const { Y } = L.axes(ctx, box, [0, 1], [0, 50], { xticks: [], ylab: "t CO₂e (cumulative)" });
      const k = t * STAGES.length;
      ["BEV", "HEV"].forEach((pt, j) => { const x = box.x0 + (box.x1 - box.x0) * (0.22 + j * 0.42), bw = (box.x1 - box.x0) * 0.22; let acc = 0;
        D[pt].forEach((v, i) => { const f = Math.max(0, Math.min(1, k - i)); if (!f) return; const c = pt === "HEV" && i > 0 && i < 4 ? "--climate" : SC[i]; ctx.fillStyle = L.cv(c); ctx.globalAlpha = i % 2 ? 0.75 : 1; ctx.fillRect(x, Y(acc + v * f), bw, Y(acc) - Y(acc + v * f)); ctx.globalAlpha = 1; acc += v * f; });
        ctx.fillStyle = L.cv(L.PTC[pt]); ctx.font = "bold 14px " + L.cv("--body"); ctx.textAlign = "center"; ctx.textBaseline = "top"; ctx.fillText(pt, x + bw / 2, box.y1 + 6); ctx.textBaseline = "bottom"; ctx.fillStyle = L.cv("--ink"); ctx.fillText(acc.toFixed(1) + " t", x + bw / 2, Y(acc) - 4); });
      const si = Math.min(STAGES.length - 1, Math.floor(k)); ctx.fillStyle = L.cv("--ink"); ctx.font = "bold 13px " + L.cv("--body"); ctx.textAlign = "left"; ctx.textBaseline = "top";
      STAGES[si].split("\n").forEach((s, i) => ctx.fillText(s, box.x1 + 12, box.y0 + 10 + i * 18));
      ctx.font = "11px " + L.cv("--body"); ctx.fillStyle = L.cv("--muted"); ["grey = production", "blue = electricity", "red = diesel + exhaust", "slate = end of life"].forEach((s, i) => ctx.fillText(s, box.x1 + 12, box.y0 + 70 + i * 16));
      if (t >= 1) { const b = D.BEV.reduce((a, c) => a + c, 0), hh = D.HEV.reduce((a, c) => a + c, 0); $("#lca-read").innerHTML = `Totals over 200,000 km: BEV <b>${b.toFixed(1)} t</b> = <b>${Math.round(b / 0.2)} g/km</b>; HEV <b>${hh.toFixed(1)} t</b> = <b>${Math.round(hh / 0.2)} g/km</b>. ` + (meth.value === "No scenario" ? "Now switch to the time-adjusted pLCA and press Play again: the BEV's later use years shrink." : "Each 5-year block of the BEV gets smaller as the grid cleans up. The HEV barely changes."); }
    }
    function step() { t = Math.min(1, t + 0.006); draw(); if (t < 1) raf = requestAnimationFrame(step); else raf = null; }
    $("#lca-play").addEventListener("click", () => { if (raf) cancelAnimationFrame(raf); t = 0; raf = requestAnimationFrame(step); });
    meth.addEventListener("change", () => { t = 1; draw(); }); redraws.push(draw); draw();
  })();

  /* ---------- 7. scenarios ---------- */
  (function () {
    const D = { "No climate action": ["SSP2-RCP6.0", "≈ 3 °C (2.6–4.8 °C) by 2100. Slow move away from fossil fuels."], "Baseline (NDCs)": ["SSP2-RCP4.5", "≈ 2.0–2.5 °C. Today's national pledges; emissions peak, then decline slowly."], "Ambitious (<2 °C)": ["SSP2-RCP2.6", "Well below 2 °C. Fast renewables and carbon capture."], "Very ambitious (1.5 °C)": ["SSP2-RCP1.9", "1.5 °C. Rapid fossil phase-out and large carbon dioxide removal, including BECCS."] };
    let cur = "Ambitious (<2 °C)";
    $("#scen-cards").innerHTML = Object.entries(D).map(([k, [r, d]]) => `<button class="pl-card" type="button" data-sc="${k}"><span class="pl-chip" style="background:${L.cv(L.SCC[k])}">${r}</span><h4>${k}</h4><p>${d}</p></button>`).join("");
    function draw() {
      $$("#scen-cards .pl-card").forEach((b) => b.setAttribute("aria-pressed", b.dataset.sc === cur));
      const { ctx, w, h } = L.canvas($("#scen-cnv"), 0.7), box = { x0: 50, y0: 16, x1: w - 12, y1: h - 40 };
      const { X, Y } = L.axes(ctx, box, [2025, 2050], [-240, 110], { xticks: [2025, 2030, 2035, 2040, 2045, 2050], xfmt: (v) => v, ylab: "index, 2025 = 100", yticks: [-200, -100, 0, 100] });
      const lines = [["Electricity", (s) => P.grid_factor[s].map((v) => v * 100), "--water"], ["Diesel (exhaust + supply)", (s) => P.bio_share[s].map((b) => (2.68 * (1 - b) + 0.55 * (1 - b) + 1.0 * b) / 3.23 * 100), "--energy"], ["Hydrogen", (s) => P.h2_kg_per_kg[s].map((v) => v / 13 * 100), "--economy"]];
      Object.keys(D).forEach((s) => lines.forEach(([n, f, c]) => { const v = f(s); ctx.strokeStyle = L.cv(c); ctx.globalAlpha = s === cur ? 1 : 0.13; ctx.lineWidth = s === cur ? 3.5 : 2; ctx.beginPath(); v.forEach((y, i) => i ? ctx.lineTo(X(M.YEARS[i]), Y(y)) : ctx.moveTo(X(M.YEARS[i]), Y(y))); ctx.stroke(); }));
      ctx.globalAlpha = 1; ctx.font = "bold 12px " + L.cv("--body"); ctx.textAlign = "right";
      lines.forEach(([n, f, c]) => { const v = f(cur); ctx.fillStyle = L.cv(c); ctx.textBaseline = n === "Hydrogen" && v[5] < 0 ? "top" : "bottom"; ctx.fillText(n, X(2050) - 4, Y(v[5]) + (n === "Diesel (exhaust + supply)" ? -4 : n === "Electricity" ? 16 : 4)); });
      $("#scen-read").innerHTML = `<b>${cur}</b> (teaching model): by 2050, electricity carbon falls to <b>${Math.round(P.grid_factor[cur][5] * 100)}%</b> of 2025, diesel to <b>${Math.round(lines[1][1](cur)[5])}%</b>, and hydrogen to <b>${Math.round(lines[2][1](cur)[5])}%</b>. In every scenario electricity cleans up far faster than diesel. That one fact drives the paper's result. Hydrogen only collapses (below zero) in the 1.5 °C case, thanks to BECCS.`;
    }
    $("#scen-cards").addEventListener("click", (e) => { const b = e.target.closest("[data-sc]"); if (b) { cur = b.dataset.sc; draw(); } });
    redraws.push(draw); draw();
  })();

  /* ---------- 8. problems ---------- */
  const PR = [
    { t: "Diesel to CO₂", q: "A hybrid uses <b>6.0 L of diesel per 100 km</b>. Burning 1 L releases 2.68 kg CO₂. How many <b>g CO₂ per km</b> come out of the exhaust?", a: 160.8, show: "≈ 161 g/km", tol: 0.04,
      h: "Litres per km = 6.0 ÷ 100. Then × 2.68 kg/L, and × 1000 to get grams.", s: "6.0 ÷ 100 = 0.060 L/km. 0.060 × 2.68 = 0.1608 kg = <b>161 g CO₂/km</b>. Adding fuel supply (~0.55 kg/L) gives 0.060 × 3.23 ≈ 194 g/km for the whole fuel cycle." },
    { t: "Electricity to CO₂", q: "A BEV uses <b>20 kWh per 100 km</b>. The grid emits <b>0.50 kg CO₂e per kWh</b>. What is the charging footprint in g/km?", a: 100, show: "100 g/km", tol: 0.04,
      h: "kWh per km = 20 ÷ 100 = 0.20. Multiply by the grid intensity.", s: "0.20 kWh/km × 0.50 kg/kWh = 0.10 kg = <b>100 g/km</b>. On a 0.10 kg/kWh grid it would be only 20 g/km. The same car can be 5× cleaner, depending only on the grid." },
    { t: "The battery's carbon debt", q: "Making a <b>75 kWh</b> battery emits about <b>90 kg CO₂e per kWh</b> of capacity. Spread over 200,000 km, how many g/km is that?", a: 33.75, show: "≈ 34 g/km", tol: 0.05,
      h: "Total = 75 × 90 kg. Then divide by 200,000 km and × 1000 for grams.", s: "75 × 90 = 6,750 kg. 6,750 ÷ 200,000 = 0.03375 kg/km = <b>≈ 34 g/km</b>. If the car is driven only 100,000 km, this doubles to 68 g/km. That is why mileage matters so much in the paper's sensitivity analysis." },
    { t: "Hydrogen footprint", q: "An FCEV uses <b>1.0 kg H₂ per 100 km</b>. Hydrogen from natural gas emits <b>12 kg CO₂e per kg</b>. What is the use-phase footprint (g/km)?", a: 120, show: "120 g/km", tol: 0.04,
      h: "kg H₂ per km = 1.0 ÷ 100 = 0.01.", s: "0.01 × 12 = 0.12 kg = <b>120 g/km</b>. With electrolysis on a 0.05 kg/kWh grid: 52 kWh × 0.05 = 2.6 kg CO₂e per kg H₂, so 0.01 × 2.6 = 26 g/km." },
    { t: "Plug-in hybrid mix", q: "A PHEV drives <b>50%</b> of km on electricity (18 kWh/100 km, grid 0.40 kg/kWh) and 50% on diesel (5.5 L/100 km, 3.23 kg CO₂e/L including supply). Use-phase g/km?", a: 124.8, show: "≈ 125 g/km", tol: 0.05,
      h: "Electric part: 0.5 × 0.18 × 0.40. Diesel part: 0.5 × 0.055 × 3.23. Add them and × 1000.", s: "Electric: 0.5 × 0.18 × 0.40 = 0.036 kg. Diesel: 0.5 × 0.055 × 3.23 = 0.0888 kg. Total 0.1248 kg = <b>≈ 125 g/km</b>. At a 20% utility factor: 0.2 × 0.072 + 0.8 × 0.1777 ≈ 157 g/km." },
    { t: "Time-adjusting (the key idea!)", q: "A BEV (0.20 kWh/km) is driven the same distance in each of three periods. The grid is <b>0.60</b>, <b>0.45</b> and <b>0.30</b> kg/kWh in 2025–30, 2030–35 and 2035–40. What is the time-adjusted charging footprint (g/km)? A typical LCA would use 0.60 for all three.", a: 90, show: "90 g/km", tol: 0.03,
      h: "Equal distance in each period, so take the simple average grid intensity.", s: "Average grid = (0.60 + 0.45 + 0.30) ÷ 3 = 0.45 kg/kWh. 0.20 × 0.45 = 0.09 kg = <b>90 g/km</b>. A typical LCA gives 0.20 × 0.60 = 120 g/km, overstating it by 33%. This is exactly what the paper does, using TIAM-UCL's grid for each 5-year period." },
  ];
  $("#prob-list").innerHTML = PR.map((e, i) => `<div class="pl-ex" data-answer="${e.a}" data-tol="${e.tol}" data-show="${e.show}"><h3>Problem ${i + 1}: ${e.t}</h3><p>${e.q}</p><div class="pl-row"><input class="pl-ans" type="text" inputmode="decimal" aria-label="Your answer to problem ${i + 1}" placeholder="your answer"><button class="btn quiet pl-checkbtn" type="button">Check</button></div><p class="pl-check" aria-live="polite"></p><details><summary>Hint</summary><div class="pl-sol">${e.h}</div></details><details><summary>Worked solution</summary><div class="pl-sol">${e.s}</div></details></div>`).join("");
  L.quiz($("#bq"));
})();
