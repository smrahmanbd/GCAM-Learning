"""Generate the animated concept figures (SVG with CSS + SMIL animation) into assets/img/fig/.
Colours use the site's CSS variables with fallbacks, so the files look right both inlined (themed) and as <img>.
Usage: python3 content/figgen.py"""
import json, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "assets", "img", "fig")
ICONS = json.load(open(os.path.join(ROOT, "content", "icons.json")))
C = dict(ink="var(--ink,#14283a)", soft="var(--ink-soft,#3d5263)", mute="var(--muted,#5d6f7d)", line="var(--line,#d3dde3)", paper="var(--card,#ffffff)", p2="var(--paper-2,#f1f5f7)",
         ec="var(--economy,#5a4e8c)", en="var(--energy,#b8790f)", la="var(--land,#4e7f2f)", wa="var(--water,#2470a8)", cl="var(--climate,#a8323e)", po="var(--policy,#3d5a6c)",
         ect="var(--economy-t,#ece9f6)", ent="var(--energy-t,#fbf0dc)", lat="var(--land-t,#e6f0dd)", wat="var(--water-t,#e1edf7)", clt="var(--climate-t,#f7e3e5)", pot="var(--policy-t,#e3eaee)")
STYLE = f"""<style>
.fg-t{{font-family:"Atkinson Hyperlegible Next",Arial,sans-serif;font-size:15px;fill:{C['ink']}}}
.fg-h{{font-family:Archivo,"Arial Narrow",Arial,sans-serif;font-weight:700;font-size:18px;fill:{C['ink']}}}
.fg-s{{font-family:"Atkinson Hyperlegible Next",Arial,sans-serif;font-size:12.5px;fill:{C['mute']}}}
.fg-box{{fill:{C['paper']};stroke-width:2.5}}
.fg-ln{{fill:none;stroke-width:3;stroke-linecap:round;stroke-linejoin:round}}
.fg-ic{{fill:none;stroke-width:2;stroke-linecap:round;stroke-linejoin:round}}
.fg-draw{{stroke-dasharray:1400;stroke-dashoffset:1400;animation:fgDraw 3.2s ease-out infinite}}
.fg-pop{{transform-box:fill-box;transform-origin:center;animation:fgPop 4s ease-in-out infinite}}
.fg-pulse{{transform-box:fill-box;transform-origin:center;animation:fgPulse 2.4s ease-in-out infinite}}
.fg-swing{{transform-box:view-box;animation:fgSwing 3.6s ease-in-out infinite}}
.fg-spin{{transform-box:fill-box;transform-origin:center;animation:fgSpin 9s linear infinite}}
.fg-flow{{stroke-dasharray:10 10;animation:fgFlow 1s linear infinite}}
.fg-grow{{transform-box:fill-box;transform-origin:bottom;animation:fgGrow 4.5s ease-out infinite}}
.fg-fade{{animation:fgFade 4.5s ease-in-out infinite}}
@keyframes fgDraw{{0%{{stroke-dashoffset:1400}}60%,100%{{stroke-dashoffset:0}}}}
@keyframes fgPop{{0%,8%{{opacity:0;transform:scale(.5)}}18%,85%{{opacity:1;transform:scale(1)}}100%{{opacity:0;transform:scale(.9)}}}}
@keyframes fgPulse{{0%,100%{{transform:scale(1)}}50%{{transform:scale(1.08)}}}}
@keyframes fgSwing{{0%,100%{{transform:rotate(-3deg)}}50%{{transform:rotate(3deg)}}}}
@keyframes fgSpin{{to{{transform:rotate(360deg)}}}}
@keyframes fgFlow{{to{{stroke-dashoffset:-20}}}}
@keyframes fgGrow{{0%{{transform:scaleY(0)}}35%,90%{{transform:scaleY(1)}}100%{{transform:scaleY(1);opacity:.4}}}}
@keyframes fgFade{{0%,10%{{opacity:0}}25%,85%{{opacity:1}}100%{{opacity:0}}}}
@media (prefers-reduced-motion:reduce){{*{{animation:none!important}}.fg-draw{{stroke-dashoffset:0}}}}
</style>"""


def svg(body, h=360, title=""):
    return f'<svg class="fig-anim" viewBox="0 0 900 {h}" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="{title}"><title>{title}</title>{STYLE}{body}</svg>'


def ic(name, x, y, s=28, col="ink", cls=""):
    k = s / 24
    return f'<path class="fg-ic {cls}" d="{ICONS[name]}" transform="translate({x - s / 2},{y - s / 2}) scale({k})" stroke="{C[col]}" stroke-width="{2 / k * 1.1:.2f}"/>'


def box(x, y, w, h, col, label, sub="", icon=None, cls="", delay=0, fill=None):
    st = f' style="animation-delay:{delay}s"' if delay else ""
    out = f'<g class="{cls}"{st}><rect class="fg-box" x="{x - w / 2}" y="{y - h / 2}" width="{w}" height="{h}" rx="14" stroke="{C[col]}" fill="{C[fill] if fill else C["paper"]}"/>'
    ty = y + (5 if not sub else -4)
    if icon:
        out += ic(icon, x - w / 2 + 26, y, 26, col)
        out += f'<text class="fg-h" x="{x + 14}" y="{ty}" text-anchor="middle" style="font-size:16px">{label}</text>'
        if sub: out += f'<text class="fg-s" x="{x + 14}" y="{y + 16}" text-anchor="middle">{sub}</text>'
    else:
        out += f'<text class="fg-h" x="{x}" y="{ty}" text-anchor="middle" style="font-size:16px">{label}</text>'
        if sub: out += f'<text class="fg-s" x="{x}" y="{y + 16}" text-anchor="middle">{sub}</text>'
    return out + "</g>"


def arrow(x1, y1, x2, y2, col="soft", flow=True, dot=True, dur=1.6, label="", lx=None, ly=None):
    pid = f"p{abs(hash((x1, y1, x2, y2))) % 10**6}"
    out = f'<path id="{pid}" d="M{x1},{y1} L{x2},{y2}" class="fg-ln {"fg-flow" if flow else ""}" stroke="{C[col]}"/>'
    import math
    a = math.atan2(y2 - y1, x2 - x1)
    hx, hy = x2, y2
    out += f'<path d="M{hx - 12 * math.cos(a - .45)},{hy - 12 * math.sin(a - .45)} L{hx},{hy} L{hx - 12 * math.cos(a + .45)},{hy - 12 * math.sin(a + .45)}" class="fg-ln" stroke="{C[col]}"/>'
    if dot:
        out += f'<circle r="6" fill="{C[col]}"><animateMotion dur="{dur}s" repeatCount="indefinite"><mpath href="#{pid}"/></animateMotion></circle>'
    if label:
        out += f'<text class="fg-s" x="{lx if lx is not None else (x1 + x2) / 2}" y="{ly if ly is not None else (y1 + y2) / 2 - 10}" text-anchor="middle">{label}</text>'
    return out


def title(t, s=""):
    return f'<text class="fg-h" x="24" y="34">{t}</text>' + (f'<text class="fg-s" x="24" y="54">{s}</text>' if s else "")


F = {}

# ------------------------------------------------------------------ Go 1
F["1.1"] = ("A mobile, not a list", svg(
    title("Integrated: tap one part and every part moves", "An IAM keeps economy, energy, land, water and climate in one consistent calculation") +
    f'<g class="fg-swing" style="transform-origin:450px 70px"><line x1="450" y1="70" x2="450" y2="100" stroke="{C["ink"]}" stroke-width="3"/><line x1="130" y1="100" x2="770" y2="100" stroke="{C["ink"]}" stroke-width="4" stroke-linecap="round"/>' +
    "".join(f'<line x1="{x}" y1="100" x2="{x}" y2="{y - 40}" stroke="{C["soft"]}" stroke-width="2"/><g class="fg-pulse" style="animation-delay:{i * .3}s"><circle cx="{x}" cy="{y}" r="40" fill="{C[c + "t"]}" stroke="{C[c]}" stroke-width="3"/>{ic(n, x, y - 6, 30, c)}<text class="fg-s" x="{x}" y="{y + 26}" text-anchor="middle">{l}</text></g>'
            for i, (x, y, c, n, l) in enumerate([(150, 220, "ec", "people", "Economy"), (300, 260, "en", "bolt", "Energy"), (450, 210, "la", "leaf", "Land"), (600, 260, "wa", "drop", "Water"), (750, 220, "cl", "thermo", "Climate")])) +
    '</g>' + f'<text class="fg-t" x="450" y="345" text-anchor="middle">A what-if machine: you choose the assumptions, it returns a world that adds up.</text>', title="An integrated assessment model as a mobile"),
    "Like a baby's mobile: touch one piece (say, a carbon price on energy) and land, water and climate all respond.")

F["1.2"] = ("From fuel to fever", svg(
    title("The climate chain", "Each link turns one quantity into the next; CO2 stays for centuries, so the running total matters") +
    box(110, 180, 170, 80, "en", "Emissions", "Gt CO2 per year", "flame") + box(330, 180, 170, 80, "cl", "Concentration", "ppm in the air", "cloud") +
    box(550, 180, 170, 80, "cl", "Forcing", "W per m²", "sun") + box(770, 180, 170, 80, "cl", "Warming", "°C", "thermo") +
    arrow(197, 180, 243, 180, "en") + arrow(417, 180, 463, 180, "cl", dur=1.9) + arrow(637, 180, 683, 180, "cl", dur=2.2) +
    f'<rect x="745" y="250" width="50" height="90" rx="10" fill="{C["p2"]}" stroke="{C["cl"]}" stroke-width="2"/><rect x="755" y="260" width="30" height="72" rx="6" fill="{C["cl"]}" class="fg-grow"/>' +
    f'<text class="fg-t" x="380" y="300" text-anchor="middle">≈ 0.45 °C of warming for every 1,000 Gt of CO2 emitted</text>', title="Climate chain"),
    "Emissions become concentration, forcing and warming. Watch the dots: they never leave the air, so the stock keeps climbing.")

F["1.3"] = ("Kaya: a four-carriage train", svg(
    title("Multiply, never add", "CO2 = people × income per person × energy per dollar × CO2 per unit of energy") +
    f'<g><animateTransform attributeName="transform" type="translate" values="-60 0;30 0;-60 0" dur="6s" repeatCount="indefinite"/>' +
    "".join(f'<g><rect x="{60 + i * 170}" y="150" width="150" height="90" rx="12" fill="{C[c + "t"]}" stroke="{C[c]}" stroke-width="3"/>{ic(n, 135 + i * 170, 180, 30, c)}<text class="fg-t" x="{135 + i * 170}" y="222" text-anchor="middle">{l}</text>'
            f'<circle cx="{90 + i * 170}" cy="250" r="12" fill="{C["ink"]}"/><circle cx="{180 + i * 170}" cy="250" r="12" fill="{C["ink"]}"/></g>' + (f'<text class="fg-h" x="{220 + i * 170}" y="200" text-anchor="middle" style="font-size:26px">×</text>' if i < 3 else "")
            for i, (c, n, l) in enumerate([("ec", "people", "People"), ("ec", "coin", "$ per person"), ("en", "bolt", "Energy per $"), ("cl", "flame", "CO2 per energy")])) +
    '</g>' + f'<g class="fg-pulse"><path d="{ICONS["cloud"]}" transform="translate(760,120) scale(4.4)" fill="{C["clt"]}" stroke="{C["cl"]}" stroke-width=".6"/><text class="fg-h" x="812" y="190" text-anchor="middle">= CO2</text></g>' +
    f'<line x1="20" y1="264" x2="880" y2="264" stroke="{C["line"]}" stroke-width="4"/><text class="fg-t" x="450" y="320" text-anchor="middle">Halve any one carriage and the whole train halves: 10% fewer people or 10% cleaner energy cut CO2 by 10%.</text>', title="Kaya identity train"),
    "The Kaya identity splits emissions into four drivers that multiply. Cutting any one factor cuts the product in proportion.")

F["1.4"] = ("A toll on carbon", svg(
    title("Prices balance markets; a carbon price moves the balance", "Supply rises with price, demand falls; a tax lifts the supply curve") +
    f'<line x1="120" y1="320" x2="560" y2="320" stroke="{C["ink"]}" stroke-width="2.5"/><line x1="120" y1="320" x2="120" y2="70" stroke="{C["ink"]}" stroke-width="2.5"/>'
    f'<text class="fg-s" x="540" y="340">quantity</text><text class="fg-s" x="80" y="80">price</text>'
    f'<line x1="140" y1="90" x2="540" y2="300" class="fg-ln" stroke="{C["wa"]}"/><text class="fg-s" x="470" y="250" fill="{C["wa"]}">demand</text>'
    f'<g><animateTransform attributeName="transform" type="translate" values="0 0;0 0;0 -70;0 -70;0 0" keyTimes="0;.2;.5;.8;1" dur="6s" repeatCount="indefinite"/><line x1="140" y1="300" x2="540" y2="100" class="fg-ln" stroke="{C["en"]}"/><text class="fg-s" x="400" y="140">supply + tax</text></g>'
    f'<circle r="9" fill="{C["cl"]}"><animate attributeName="cx" values="337;337;288;288;337" keyTimes="0;.2;.5;.8;1" dur="6s" repeatCount="indefinite"/><animate attributeName="cy" values="194;194;169;169;194" keyTimes="0;.2;.5;.8;1" dur="6s" repeatCount="indefinite"/></circle>' +
    box(730, 140, 260, 70, "po", "Carbon tax", "added to dirty options' cost", "scale") + box(730, 240, 260, 70, "la", "Cleaner options win", "more of the market, not all", "leaf") + arrow(730, 176, 730, 204, "po"),
    title="Market with a carbon tax"),
    "The red dot is the market's balance point. When the tax lifts supply, less is sold at a higher price, and cleaner options gain share.")

F["1.5"] = ("A fan of futures", svg(
    title("Scenarios: a story (SSP) and a number (forcing in 2100)", "Same starting point, different choices: each line is one consistent what-if") +
    f'<line x1="80" y1="320" x2="620" y2="320" stroke="{C["ink"]}" stroke-width="2"/><text class="fg-s" x="80" y="340">2020</text><text class="fg-s" x="590" y="340">2100</text>' +
    "".join(f'<path d="M80,230 C250,{230 - d * 0.3} 420,{230 - d} 610,{230 - d * 1.4}" class="fg-ln fg-draw" stroke="{C[c]}" style="animation-delay:{i * .35}s"/><text class="fg-s" x="630" y="{230 - d * 1.4 + 4}" style="fill:{C[c]}">{l}</text>'
            for i, (d, c, l) in enumerate([(100, "cl", "SSP5-8.5"), (55, "en", "SSP3-7.0"), (20, "ec", "SSP2-4.5"), (-40, "wa", "SSP1-2.6"), (-70, "la", "SSP1-1.9")])) +
    box(800, 120, 160, 64, "ec", "SSP 1–5", "the social story", "book") + box(800, 230, 160, 64, "cl", "1.9 … 8.5", "W/m² in 2100", "sun"), title="Scenario fan"),
    "Five storylines fan out from today. The label pairs the story (SSP) with the forcing it reaches in 2100, not a temperature.")

F["1.6"] = ("GCAM: an auction every five years", svg(
    title("One marketplace links every system", "In each 5-year step, prices move until supply equals demand in every market") +
    f'<g class="fg-pulse"><circle cx="450" cy="200" r="70" fill="{C["p2"]}" stroke="{C["ink"]}" stroke-width="3"/>{ic("market", 450, 188, 40)}<text class="fg-h" x="450" y="236" text-anchor="middle" style="font-size:15px">Marketplace</text></g>'
    f'<g class="fg-spin" style="transform-origin:450px 200px;animation-duration:24s">' +
    "".join(f'<g><circle cx="{450 + 150 * __import__("math").cos(a)}" cy="{200 + 120 * __import__("math").sin(a)}" r="34" fill="{C[c + "t"]}" stroke="{C[c]}" stroke-width="3"/>{ic(n, 450 + 150 * __import__("math").cos(a), 200 + 120 * __import__("math").sin(a), 28, c)}</g>'
            for a, c, n in [(-1.57, "ec", "people"), (-0.3, "en", "bolt"), (0.95, "la", "leaf"), (2.2, "wa", "drop"), (3.45, "cl", "thermo")]) + "</g>" +
    "".join(f'<rect x="{680 + i * 40}" y="{300 - i * 30}" width="40" height="{20 + i * 30}" fill="{C["pot"]}" stroke="{C["po"]}"/><text class="fg-s" x="{700 + i * 40}" y="{295 - i * 30}" text-anchor="middle">{2025 + i * 5}</text>' for i in range(5)) +
    f'<text class="fg-s" x="760" y="345" text-anchor="middle">five-year staircase, no foresight</text>', title="GCAM marketplace"),
    "People, energy, land, water and climate orbit one marketplace. GCAM solves one five-year step at a time, without seeing the future.")

F["1.7"] = ("Stocks, flows and loops", svg(
    title("A bathtub with a feedback loop", "The stock (CO2 in the air) changes by inflow minus outflow; warming weakens the drain") +
    f'<path d="M180,140 L180,300 Q180,320 200,320 L440,320 Q460,320 460,300 L460,140" fill="none" stroke="{C["ink"]}" stroke-width="5"/>'
    f'<rect x="185" y="200" width="270" height="117" fill="{C["clt"]}"><animate attributeName="y" values="250;180;250" dur="8s" repeatCount="indefinite"/><animate attributeName="height" values="67;137;67" dur="8s" repeatCount="indefinite"/></rect>'
    f'<path d="M140,90 L250,90 L250,120" fill="none" stroke="{C["en"]}" stroke-width="8"/>{ic("flame", 120, 90, 30, "en")}' +
    "".join(f'<circle cx="250" r="5" fill="{C["cl"]}"><animate attributeName="cy" values="125;250" dur="1s" begin="{i * .25}s" repeatCount="indefinite"/></circle>' for i in range(4)) +
    f'<path d="M455,300 L560,300" fill="none" stroke="{C["la"]}" stroke-width="8" class="fg-flow"/>{ic("tree", 590, 300, 34, "la")}<text class="fg-s" x="520" y="285" text-anchor="middle">sinks: oceans, forests</text>'
    f'<text class="fg-t" x="320" y="350" text-anchor="middle">stock = CO2 in the air</text><text class="fg-s" x="200" y="80">inflow: emissions</text>'
    f'<g class="fg-spin" style="transform-origin:760px 190px;animation-duration:6s">{ic("loop", 760, 190, 120, "cl")}</g>'
    f'<text class="fg-h" x="760" y="196" text-anchor="middle" style="font-size:22px">+</text><text class="fg-t" x="760" y="290" text-anchor="middle">warmer → weaker sinks</text><text class="fg-t" x="760" y="310" text-anchor="middle">→ more CO2 stays → warmer</text>', title="Stock and flow bathtub with feedback"),
    "The level only falls when outflow beats inflow. A reinforcing loop (warming weakens sinks) makes the tub fill faster.")

F["1.8"] = ("Cheapest cuts first", svg(
    title("The marginal abatement cost curve", "Each bar is an option: width = tonnes it can cut, height = cost per tonne; a carbon price buys everything below it") +
    f'<line x1="80" y1="250" x2="800" y2="250" stroke="{C["ink"]}" stroke-width="2"/><line x1="80" y1="90" x2="80" y2="330" stroke="{C["ink"]}" stroke-width="2"/><text class="fg-s" x="20" y="100">$ per t</text><text class="fg-s" x="720" y="275">tonnes cut →</text>' +
    "".join(f'<rect class="fg-grow" style="animation-delay:{i * .25}s;transform-origin:{"top" if h < 0 else "bottom"}" x="{x}" y="{250 - max(h, 0)}" width="{w}" height="{abs(h)}" fill="{C[c + "t"]}" stroke="{C[c]}" stroke-width="2"/><text class="fg-s" x="{x + w / 2}" y="{250 - max(h, 0) - 6 if h > 0 else 250 + abs(h) + 16}" text-anchor="middle">{l}</text>'
            for i, (x, w, h, c, l) in enumerate([(82, 110, -30, "la", "efficiency"), (192, 70, 15, "la", "methane"), (262, 170, 35, "en", "wind, solar"), (432, 90, 70, "wa", "EVs"), (522, 100, 100, "ec", "industry"), (622, 80, 125, "po", "CCS"), (702, 90, 150, "cl", "air capture")])) +
    f'<g><animateTransform attributeName="transform" type="translate" values="0 0;0 -110;0 -110;0 0" keyTimes="0;.45;.8;1" dur="7s" repeatCount="indefinite"/><line x1="80" y1="245" x2="820" y2="245" stroke="{C["cl"]}" stroke-width="3" stroke-dasharray="8 6"/><text class="fg-t" x="820" y="238" text-anchor="end" style="fill:{C["cl"]}">carbon price</text></g>', title="Marginal abatement cost curve"),
    "As the dashed carbon price rises, every option whose bar sits below it becomes worth doing. Some cuts even save money.")

F["1.9"] = ("One basin, three thirsts", svg(
    title("The water–energy–food nexus", "Farms, power plants and towns draw on the same river basin; bioenergy links land to energy") +
    f'<circle cx="330" cy="170" r="105" fill="{C["wat"]}" stroke="{C["wa"]}" stroke-width="3" opacity=".9" class="fg-pulse"/><circle cx="470" cy="170" r="105" fill="{C["ent"]}" stroke="{C["en"]}" stroke-width="3" opacity=".75" class="fg-pulse" style="animation-delay:.8s"/>'
    f'<circle cx="400" cy="275" r="105" fill="{C["lat"]}" stroke="{C["la"]}" stroke-width="3" opacity=".75" class="fg-pulse" style="animation-delay:1.6s"/>'
    f'{ic("drop", 290, 140, 36, "wa")}<text class="fg-h" x="290" y="185" text-anchor="middle">Water</text>{ic("bolt", 510, 140, 36, "en")}<text class="fg-h" x="510" y="185" text-anchor="middle">Energy</text>{ic("wheat", 400, 300, 36, "la")}<text class="fg-h" x="400" y="345" text-anchor="middle">Food</text>' +
    f'<text class="fg-s" x="400" y="160" text-anchor="middle">cooling</text><text class="fg-s" x="335" y="245" text-anchor="middle">irrigation</text><text class="fg-s" x="470" y="245" text-anchor="middle">bioenergy</text>' +
    box(750, 120, 220, 64, "wa", "Basin limit", "renewable water first", "drop") + box(750, 230, 220, 64, "cl", "Scarcity price", "rises when demand nears limit", "coin") + arrow(750, 156, 750, 194, "wa"), title="Water energy food nexus"),
    "Every overlap is a trade-off: more irrigated food or more cooled power both pull on the same basin's water.")

F["1.10"] = ("A band, not a line", svg(
    title("Uncertainty: many plausible runs, one honest range", "Vary the uncertain inputs, run the model many times, and report the spread") +
    f'<line x1="80" y1="320" x2="560" y2="320" stroke="{C["ink"]}" stroke-width="2"/><path d="M80,250 C250,220 400,130 560,80 L560,230 C400,240 250,250 80,250 Z" fill="{C["wat"]}" stroke="none"/>' +
    "".join(f'<path d="M80,250 C250,{235 - k * 6} 400,{200 - k * 14} 560,{215 - k * 30}" class="fg-ln fg-draw" stroke="{C["wa"]}" style="stroke-width:1.6;animation-delay:{k * .3}s;opacity:.8"/>' for k in range(6)) +
    f'<path d="M80,250 C250,228 400,170 560,150" class="fg-ln" stroke="{C["ink"]}" stroke-width="4"/><text class="fg-s" x="566" y="152">median</text><text class="fg-s" x="566" y="84">high end</text><text class="fg-s" x="566" y="232">low end</text>'
    f'<path d="M660,310 C700,310 720,140 760,140 C800,140 820,310 860,310" class="fg-ln fg-draw" stroke="{C["cl"]}" stroke-width="3"/>{ic("dice", 830, 120, 40, "ec", "fg-spin")}<text class="fg-t" x="760" y="340" text-anchor="middle">spread of outcomes</text>', title="Uncertainty fan"),
    "Each thin line is one model run with different assumptions. The shaded band, not any single line, is the honest answer.")

# ------------------------------------------------------------------ Go 3
F["3.1"] = ("The research pipeline", svg(
    title("GCAM as research software", "Raw data → gcamdata → XML inputs → the solver → database → queries and analysis") +
    "".join(box(100 + i * 140, 190, 120, 80, c, l, s, n) for i, (c, l, s, n) in enumerate([("ec", "Raw data", "csv", "stack"), ("ec", "gcamdata", "R package", "code"), ("en", "XML", "inputs", "layers"), ("po", "Solver", "clears markets", "gear"), ("wa", "Database", "results", "stack"), ("la", "Analysis", "R / Python", "chart")])) +
    "".join(arrow(160 + i * 140, 190, 180 + i * 140, 190, "soft", dot=False) for i in range(5)) +
    f'<circle r="9" fill="{C["en"]}"><animateMotion dur="6s" repeatCount="indefinite" path="M40,190 L860,190"/></circle><g class="fg-spin" style="transform-origin:520px 190px;animation-duration:4s;opacity:.25">{ic("gear", 520, 190, 110, "po")}</g>'
    f'<text class="fg-t" x="450" y="300" text-anchor="middle">Reproducible means anyone can rebuild every step: version, inputs, config and queries.</text>', title="GCAM research pipeline"),
    "A run is a pipeline. Each stage must be versioned so another researcher can rebuild your exact numbers.")

F["3.2"] = ("Transport as a nesting tree", svg(
    title("Passenger travel in GCAM, nest by nest", "Service demand splits by mode, then size class, then technology, each by a logit on cost") +
    box(450, 80, 220, 54, "en", "Passenger-km", "set by income and price", "people") +
    "".join(box(x, 180, 130, 54, "en", l, "", n) for x, l, n in [(180, "Car", "car"), (360, "Bus", "truck"), (540, "Rail", "map"), (720, "Air", "plane")]) +
    "".join(arrow(450, 108, x, 152, "en", dur=1.4 + i * .3) for i, x in enumerate([180, 360, 540, 720])) +
    "".join(box(x, 290, 110, 50, c, l) for x, c, l in [(100, "cl", "ICE"), (230, "en", "Hybrid"), (360, "wa", "Battery EV"), (490, "la", "Hydrogen")]) +
    "".join(arrow(180, 208, x, 264, "soft", dur=1.8) for x in [100, 230, 360, 490]) +
    f'<text class="fg-s" x="720" y="285" text-anchor="middle">cost per pkm = vehicle cost ÷ load factor</text><text class="fg-s" x="720" y="305" text-anchor="middle">+ value of time for each mode</text>', title="Transport nesting tree"),
    "Demand flows down the tree: each split is a logit on the generalised cost, which adds the value of travel time.")

F["3.3"] = ("What the literature says", svg(
    title("Many studies, one evidence map", "Place your question: where do models agree, disagree, or stay silent?") +
    "".join(f'<rect x="{90 + i * 34}" y="{140 + (i % 3) * 8}" width="28" height="{170 - (i % 3) * 8}" rx="3" fill="{C[c + "t"]}" stroke="{C[c]}" stroke-width="2"/>' for i, c in enumerate(["ec", "en", "la", "wa", "cl", "po", "ec", "en"])) +
    f'<line x1="420" y1="320" x2="860" y2="320" stroke="{C["ink"]}" stroke-width="2"/><rect x="420" y="170" width="440" height="60" fill="{C["lat"]}"/><text class="fg-s" x="430" y="165">range where most studies agree</text>' +
    "".join(f'<circle cx="{440 + i * 34}" cy="{200 + ((i * 37) % 70 - 35) * 1.6}" r="8" fill="{C["en"]}" class="fg-pop" style="animation-delay:{i * .2}s"/>' for i in range(13)) +
    f'<text class="fg-t" x="640" y="345" text-anchor="middle">each dot = one model estimate of 2050 transport CO2</text>', title="Literature evidence map"),
    "Read the literature as data: estimates cluster where evidence is strong and scatter where models disagree.")

F["3.4"] = ("A scenario design matrix", svg(
    title("Design before you run", "Rows: transport levers. Columns: policy. Each filled cell is one run in your batch") +
    "".join(f'<text class="fg-s" x="{260 + j * 130}" y="100" text-anchor="middle">{c}</text>' for j, c in enumerate(["Reference", "Carbon tax", "Net-zero cap", "ZEV standard"])) +
    "".join(f'<text class="fg-s" x="180" y="{150 + i * 60}" text-anchor="end">{r}</text>' for i, r in enumerate(["Core", "Cheap batteries", "Fuller vehicles", "Both"])) +
    "".join(f'<rect x="{200 + j * 130}" y="{120 + i * 60}" width="120" height="50" rx="8" fill="{C["wat"] if (i + j) % 2 else C["ent"]}" stroke="{C["wa"] if (i + j) % 2 else C["en"]}" stroke-width="2" class="fg-pop" style="animation-delay:{(i * 4 + j) * .18}s"/>' for i in range(4) for j in range(4)) +
    box(790, 210, 150, 70, "ec", "16 runs", "+ uncertainty plan", "grid"), title="Scenario design matrix"),
    "Cells light up one by one: a clear matrix keeps every run tied to a question you can defend.")

F["3.5"] = ("Add-on XML overrides", svg(
    title("Building scenarios with add-on files", "Base files load first; your add-on changes only what it names. Order matters.") +
    "".join(f'<rect x="{120 + i * 14}" y="{110 + i * 14}" width="240" height="170" rx="10" fill="{C["paper"]}" stroke="{C["po"]}" stroke-width="2"/>' for i in range(3)) +
    f'<text class="fg-h" x="275" y="200" text-anchor="middle">base XML</text><text class="fg-s" x="275" y="222" text-anchor="middle">thousands of inputs</text>'
    f'<g><animateTransform attributeName="transform" type="translate" values="200 0;0 0;0 0;200 0" keyTimes="0;.35;.8;1" dur="6s" repeatCount="indefinite"/><rect x="250" y="160" width="220" height="120" rx="10" fill="{C["ent"]}" stroke="{C["en"]}" stroke-width="3"/>{ic("pen", 280, 190, 26, "en")}<text class="fg-h" x="370" y="196" text-anchor="middle" style="font-size:15px">add-on</text><text class="fg-s" x="360" y="222" text-anchor="middle">BEV cost × 0.7</text><text class="fg-s" x="360" y="242" text-anchor="middle">load factor + 10%</text></g>'
    + box(760, 140, 200, 60, "la", "Same names", "override the base", "link") + box(760, 250, 200, 60, "cl", "Misspelt name", "creates a ghost", "warn"), title="Add-on XML"),
    "The add-on slides over the base inputs and replaces only the values it names; a misspelt name silently adds a new, unused object.")

F["3.6"] = ("Decompose the change", svg(
    title("Why did transport CO2 change? An LMDI waterfall", "Activity, mode structure, energy intensity and carbon factor add up exactly to the total") +
    f'<line x1="80" y1="300" x2="860" y2="300" stroke="{C["ink"]}" stroke-width="2"/>' +
    "".join(f'<rect class="fg-grow" style="animation-delay:{i * .4}s;transform-origin:{o}" x="{100 + i * 140}" y="{y}" width="100" height="{hh}" fill="{C[c + "t"]}" stroke="{C[c]}" stroke-width="2"/><text class="fg-s" x="{150 + i * 140}" y="325" text-anchor="middle">{l}</text>'
            for i, (y, hh, c, l, o) in enumerate([(160, 140, "po", "2020", "bottom"), (100, 60, "ec", "activity", "bottom"), (100, 30, "en", "structure", "top"), (130, 50, "wa", "intensity", "top"), (180, 60, "la", "carbon", "top"), (240, 60, "po", "2050", "bottom")])), title="LMDI waterfall"),
    "Each bar grows in turn: rising activity pushes CO2 up, while cleaner modes, efficiency and fuels pull it down to 2050.")

F["3.7"] = ("From region to country", svg(
    title("Going finer: downscaling and coupling", "Split a GCAM region's results into countries, or link GCAM to a fleet or grid model") +
    f'<rect x="80" y="110" width="260" height="180" rx="14" fill="{C["ent"]}" stroke="{C["en"]}" stroke-width="3" class="fg-pulse"/><text class="fg-h" x="210" y="205" text-anchor="middle">GCAM region</text>' +
    arrow(350, 200, 440, 200, "en") +
    "".join(f'<rect x="{460 + (i % 3) * 90}" y="{110 + (i // 3) * 92}" width="80" height="82" rx="10" fill="{C["wat"]}" stroke="{C["wa"]}" stroke-width="2" class="fg-pop" style="animation-delay:{i * .25}s"/><text class="fg-s" x="{500 + (i % 3) * 90}" y="{156 + (i // 3) * 92}" text-anchor="middle">country {i + 1}</text>' for i in range(6)) +
    box(800, 140, 150, 60, "la", "Fleet model", "stock, ages", "car") + box(800, 260, 150, 60, "po", "Grid model", "hours, peaks", "bolt") + arrow(800, 172, 800, 228, "soft"), title="Downscaling"),
    "A region's totals are shared among its countries by rules that converge over time; coupled models add what GCAM cannot see.")

F["3.8"] = ("Write it up, honestly", svg(
    title("Limits, ethics and a reproducible paper", "State what the model cannot see, whose costs count, and how to rebuild every number") +
    f'<rect x="100" y="80" width="260" height="250" rx="12" fill="{C["paper"]}" stroke="{C["ink"]}" stroke-width="2"/>{ic("pen", 330, 110, 26)}' +
    "".join(f'<g class="fg-pop" style="animation-delay:{i * .45}s"><circle cx="135" cy="{130 + i * 45}" r="12" fill="{C["lat"]}" stroke="{C["la"]}" stroke-width="2"/><path d="M129,{130 + i * 45} l5,5 l9,-10" class="fg-ln" stroke="{C["la"]}"/></g><text class="fg-t" x="160" y="{135 + i * 45}">{l}</text>'
            for i, l in enumerate(["GCAM version and config", "Limits stated", "Who gains, who pays", "IAMC-format results", "Code and data archived"])) +
    box(640, 140, 300, 70, "cl", "What GCAM cannot see", "fleets, congestion, behaviour", "warn") + box(640, 260, 300, 70, "ec", "Whose future?", "equity across regions", "scale"), title="Writing up checklist"),
    "Ticks appear one by one: a credible study reports its version, its limits and its distributional effects, and shares its package.")

F["3.9"] = ("The IAM family", svg(
    title("Seven integrated assessment models, two big choices", "How far each model sees ahead (foresight) and how much of the economy it covers") +
    f'<line x1="120" y1="320" x2="820" y2="320" stroke="{C["ink"]}" stroke-width="2"/><line x1="120" y1="320" x2="120" y2="70" stroke="{C["ink"]}" stroke-width="2"/>'
    f'<text class="fg-s" x="650" y="345">foresight: myopic → perfect</text><text class="fg-s" x="20" y="80">economy:</text><text class="fg-s" x="20" y="96">whole</text><text class="fg-s" x="20" y="310">energy + land</text>' +
    "".join(f'<g class="fg-pop" style="animation-delay:{i * .3}s"><circle cx="{x}" cy="{y}" r="40" fill="{C[c + "t"]}" stroke="{C[c]}" stroke-width="3"/><text class="fg-h" x="{x}" y="{y + 5}" text-anchor="middle" style="font-size:12px">{l}</text></g>'
            for i, (x, y, c, l) in enumerate([(200, 260, "en", "GCAM"), (330, 245, "la", "IMAGE"), (250, 130, "ec", "AIM-Hub"), (600, 220, "wa", "MESSAGEix"), (700, 120, "po", "REMIND"), (760, 200, "cl", "WITCH"), (560, 100, "ec", "DICE")])), title="IAM family map"),
    "Each model makes different trade-offs. Knowing where a model sits tells you what its results can and cannot mean.")

# ------------------------------------------------------------------ model atlas: how each model solves
A = {}
A["gcam"] = svg(title("GCAM: prices bounce until markets clear, one period at a time", "Recursive dynamic, partial equilibrium; logit shares; no foresight") +
    f'<line x1="80" y1="300" x2="520" y2="300" stroke="{C["ink"]}" stroke-width="2"/><line x1="80" y1="300" x2="80" y2="80" stroke="{C["ink"]}" stroke-width="2"/>'
    f'<line x1="100" y1="100" x2="500" y2="280" class="fg-ln" stroke="{C["wa"]}"/><line x1="100" y1="280" x2="500" y2="100" class="fg-ln" stroke="{C["en"]}"/><text class="fg-s" x="470" y="275">demand</text><text class="fg-s" x="470" y="95">supply</text>'
    f'<circle r="9" fill="{C["cl"]}"><animateMotion dur="5s" repeatCount="indefinite" path="M120,120 L480,120 L150,250 L420,150 L230,220 L330,180 L290,192 L300,190"/></circle><text class="fg-s" x="300" y="320" text-anchor="middle">solver iterations (Broyden)</text>' +
    "".join(f'<rect x="{600 + i * 55}" y="{250 - i * 32}" width="50" height="{40 + i * 32}" fill="{C["ent"]}" stroke="{C["en"]}" class="fg-pop" style="animation-delay:{i * .5}s"/><text class="fg-s" x="{625 + i * 55}" y="{243 - i * 32}" text-anchor="middle">{2025 + 5 * i}</text>' for i in range(5)) +
    f'<text class="fg-t" x="710" y="330" text-anchor="middle">solve 2025, then 2030, then 2035…</text>', title="How GCAM solves")
A["message"] = svg(title("MESSAGEix: one big linear programme with perfect foresight", "Choose every technology in every period at once to meet demand at least total discounted cost") +
    f'<line x1="80" y1="310" x2="460" y2="310" stroke="{C["ink"]}" stroke-width="2"/><line x1="80" y1="310" x2="80" y2="80" stroke="{C["ink"]}" stroke-width="2"/><text class="fg-s" x="400" y="330">coal power</text><text class="fg-s" x="20" y="90">solar</text>'
    f'<polygon points="80,310 80,150 200,110 380,190 430,310" fill="{C["wat"]}" stroke="{C["wa"]}" stroke-width="2"/><text class="fg-s" x="200" y="250" text-anchor="middle">feasible: meets demand,</text><text class="fg-s" x="200" y="266" text-anchor="middle">respects the CO2 cap</text>'
    f'<g><animateTransform attributeName="transform" type="translate" values="-160 160;0 0;0 0;-160 160" keyTimes="0;.5;.85;1" dur="6s" repeatCount="indefinite"/><line x1="80" y1="40" x2="420" y2="260" stroke="{C["cl"]}" stroke-width="3" stroke-dasharray="8 6" transform="translate(-40,-40)"/></g>'
    f'<circle cx="200" cy="110" r="10" fill="{C["cl"]}" class="fg-pulse"/><text class="fg-s" x="215" y="100">least-cost corner</text>' +
    box(700, 120, 280, 64, "wa", "Sees 2100 from 2020", "invests early if cheaper overall", "clock") + box(700, 240, 280, 64, "po", "Shadow price of CO2 cap", "= the carbon price", "coin"), title="How MESSAGEix solves")
A["remind"] = svg(title("REMIND: a planner maximises welfare over the whole century", "Intertemporal Ramsey growth model, perfect foresight, coupled to MAgPIE (land) and EDGE-T (transport)") +
    f'<line x1="80" y1="300" x2="560" y2="300" stroke="{C["ink"]}" stroke-width="2"/>' +
    "".join(f'<rect x="{90 + i * 46}" y="{300 - 60 - i * 8}" width="34" height="{60 + i * 8}" fill="{C["ect"]}" stroke="{C["ec"]}"/><rect x="{90 + i * 46}" y="{300 - 60 - i * 8 - (24 - i * 2)}" width="34" height="{24 - i * 2}" fill="{C["ent"]}" stroke="{C["en"]}"/>' for i in range(10)) +
    f'<text class="fg-s" x="320" y="320" text-anchor="middle">consumption (purple) and energy investment (gold) per period</text>'
    f'<path d="M560,120 C450,60 220,60 110,120" class="fg-ln fg-flow" stroke="{C["po"]}"/><text class="fg-s" x="335" y="70" text-anchor="middle">foresight: 2100 informs today</text>' +
    box(740, 120, 240, 60, "ec", "Max Σ discounted utility", "of consumption", "target") + box(740, 220, 240, 60, "la", "MAgPIE ↔ REMIND", "soft-linked land", "leaf") + box(740, 310, 240, 50, "en", "EDGE-T", "transport (GCAM fork)", "car"), title="How REMIND solves")
A["image"] = svg(title("IMAGE: simulate land and environment on a fine grid", "Recursive simulation: TIMER (energy) + land on grid cells + MAGNET (agro-economy) + earth system") +
    "".join(f'<rect x="{90 + (i % 10) * 34}" y="{90 + (i // 10) * 34}" width="32" height="32" fill="{C["lat"] if (i * 7) % 10 > 3 else C["ent"]}" stroke="{C["paper"]}"><animate attributeName="fill" values="{C["lat"]};{C["lat"]};{C["ent"] if (i * 13) % 10 > 4 else C["lat"]};{C["lat"]}" dur="7s" begin="{(i % 17) * .2}s" repeatCount="indefinite"/></rect>' for i in range(70)) +
    f'<text class="fg-s" x="260" y="345" text-anchor="middle">grid cells switch from forest (green) to cropland (gold) as food demand grows</text>' +
    box(700, 110, 260, 60, "en", "TIMER", "energy, simulated year by year", "bolt") + box(700, 200, 260, 60, "la", "Land on a grid", "suitability-ranked cells", "grid") + box(700, 290, 260, 60, "wa", "Earth system", "carbon, water, nutrients", "globe"), title="How IMAGE works")
A["aim"] = svg(title("AIM-Hub (AIM/CGE): the whole economy in general equilibrium", "Every market clears, including labour and capital; recursive dynamic, one-year steps") +
    f'<circle cx="300" cy="200" r="120" fill="none" stroke="{C["line"]}" stroke-width="18"/>' +
    box(300, 90, 170, 56, "ec", "Households", "", "people") + box(300, 310, 170, 56, "en", "Firms (sectors)", "", "factory") +
    f'<path id="aimL" d="M200,240 A120,120 0 0 1 200,160" fill="none"/><path id="aimR" d="M400,160 A120,120 0 0 1 400,240" fill="none"/>' +
    "".join(f'<circle r="7" fill="{C["ec"]}"><animateMotion dur="3s" begin="{k}s" repeatCount="indefinite" path="M300,118 A120,120 0 0 1 300,282"/></circle><circle r="7" fill="{C["en"]}"><animateMotion dur="3s" begin="{k}s" repeatCount="indefinite" path="M300,282 A120,120 0 0 1 300,118"/></circle>' for k in (0, 1, 2)) +
    f'<text class="fg-s" x="440" y="205">goods</text><text class="fg-s" x="120" y="205">labour, capital</text>' +
    box(700, 140, 270, 64, "po", "Carbon tax", "raises costs, revenue recycled", "scale") + box(700, 250, 270, 64, "la", "GDP loss emerges", "from the whole economy", "chart"), title="How AIM-Hub works")
A["witch"] = svg(title("WITCH: regions play a game", "Each region maximises its own welfare given the others' choices (Nash), or a coalition maximises joint welfare") +
    box(200, 130, 190, 60, "wa", "Region A", "cuts a_A", "globe") + box(200, 270, 190, 60, "en", "Region B", "cuts a_B", "globe") +
    f'<path d="M300,130 C420,130 420,270 300,270" class="fg-ln fg-flow" stroke="{C["po"]}"/><path d="M300,270 C380,270 380,130 300,130" class="fg-ln fg-flow" stroke="{C["po"]}" style="animation-direction:reverse"/>'
    f'<text class="fg-s" x="440" y="205">best response</text>' +
    f'<line x1="560" y1="300" x2="840" y2="300" stroke="{C["ink"]}" stroke-width="2"/><rect x="590" y="220" width="90" height="80" fill="{C["clt"]}" stroke="{C["cl"]}" class="fg-grow"/><rect x="720" y="140" width="90" height="160" fill="{C["lat"]}" stroke="{C["la"]}" class="fg-grow" style="animation-delay:.6s"/>'
    f'<text class="fg-s" x="635" y="320" text-anchor="middle">Nash</text><text class="fg-s" x="765" y="320" text-anchor="middle">cooperation</text><text class="fg-s" x="700" y="120" text-anchor="middle">global abatement</text>', title="How WITCH works")
A["dice"] = svg(title("DICE: weigh the cost of cutting against the damage avoided", "One world region, optimal growth; the optimum is where marginal cost = marginal benefit") +
    f'<line x1="100" y1="310" x2="600" y2="310" stroke="{C["ink"]}" stroke-width="2"/><line x1="100" y1="310" x2="100" y2="70" stroke="{C["ink"]}" stroke-width="2"/><text class="fg-s" x="470" y="332">share of emissions cut</text>'
    f'<path d="M100,305 C300,300 450,230 590,80" class="fg-ln fg-draw" stroke="{C["en"]}"/><text class="fg-s" x="520" y="90">marginal cost</text>'
    f'<path d="M100,150 C250,170 420,200 590,215" class="fg-ln fg-draw" stroke="{C["cl"]}" style="animation-delay:.5s"/><text class="fg-s" x="520" y="235">marginal benefit</text>'
    f'<circle cx="398" cy="197" r="11" fill="{C["la"]}" class="fg-pulse"/><text class="fg-s" x="398" y="180" text-anchor="middle">optimum</text>' +
    box(760, 130, 240, 64, "ec", "Social cost of carbon", "damage of one more tonne", "coin") + box(760, 250, 240, 64, "po", "Discount rate", "sets how much 2100 counts", "clock"), title="How DICE works")


def write():
    os.makedirs(OUT, exist_ok=True)
    for k, (t, s, cap) in F.items():
        open(os.path.join(OUT, f"m{k}.svg"), "w").write(s)
    for k, s in A.items():
        open(os.path.join(OUT, f"model-{k}.svg"), "w").write(s)
    json.dump({k: [t, cap] for k, (t, s, cap) in F.items()}, open(os.path.join(OUT, "captions.json"), "w"), indent=1, ensure_ascii=False)


if __name__ == "__main__":
    write(); print(len(F), "figures,", len(A), "model animations")
