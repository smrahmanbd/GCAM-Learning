"""Build 'GCAM in three goes' (static site) from content/m*.json.  Usage: python3 build.py"""
import json, glob, os, html, re

ROOT = os.path.dirname(os.path.abspath(__file__))
SYS = ["economy", "energy", "land", "water", "climate", "policy"]
SYSNAME = dict(economy="Economy and people", energy="Energy", land="Land and food", water="Water", climate="Emissions and climate", policy="Policy")
SITE = "GCAM in three goes"
esc = lambda s: html.escape(str(s), quote=True)

# ------------------------------------------------------------------ the three goes
GO = {
    1: dict(name="See the whole picture", short="Big picture", depth="Surface",
            promise="Understand what GCAM and other integrated assessment models are for, what goes in, what comes out, and how to read a scenario.",
            style="Pictures first. Every idea is a diagram you can click and a small explorer where you predict an answer, then check it. No code needed and no maths beyond percentages.",
            need="Nothing. Curiosity about climate and energy, and comfort reading a simple chart.",
            produce=["A one-page explanation, in your own words, of what an IAM is and is not",
                     "Your own reading of one IPCC scenario chart: what the labels mean and what the band shows",
                     "A first walk through GCAM: its regions, markets, land, water and climate model"],
            entry=[("An integrated assessment model is best described as…", ["A forecast of the future", "A consistent what-if machine", "A weather model run longer", "A tool that chooses climate policy"], 1, "It works out what follows from assumptions, consistently. It does not predict or decide."),
                   ("Warming depends mostly on…", ["This year's emissions", "The running total of CO2 emitted", "The price of oil", "The number of models"], 1, "Warming tracks cumulative CO2: about 0.45 °C per 1,000 Gt."),
                   ("In 'SSP2-4.5', the 4.5 is…", ["4.5 °C of warming", "Forcing of 4.5 W/m² in 2100", "4.5 billion people", "4.5 Gt of CO2"], 1, "SSP is the story about society; the number is the radiative forcing in 2100.")],
            exit=["I can explain in two sentences what an IAM is and is not", "I can explain why warming follows cumulative emissions, and use a carbon budget",
                  "I can split CO2 into people, income, energy per $ and CO2 per energy", "I can explain what a carbon price does and why the discount rate matters",
                  "I can decode an SSP-RCP label and an AR6 category", "I can describe GCAM's main parts and why results are read as Policy minus Reference"],
            handbook="downloads/Go1-Study-Guide-See-the-Whole-Picture.pdf", kit=None),
    2: dict(name="Open the boxes", short="Components", depth="Inside",
            promise="Open each GCAM component, see the rule it follows and the numbers it needs, and trace how it pushes on the others.",
            style="Every module starts from a connections map, explains the mechanism with a worked calculation, and ends with a small model you build and run, in Python in the browser or in R on your machine.",
            need="Go 1, or its exit check. Basic Python or R: variables, functions, a loop.",
            produce=["Nine small working models of GCAM's mechanisms, in Python and R", "A note tracing one feedback between components through real GCAM output",
                     "Your first GCAM run read into R or Python with rgcam or gcamreader"],
            entry=[("In GCAM, the marketplace…", ["Sets prices by government rule", "Adjusts prices until supply equals demand in every market", "Uses perfect foresight", "Only covers energy"], 1, "The solver moves prices until all markets clear at once, period by period."),
                   ("A logit share rule means that…", ["The cheapest option takes everything", "Cheaper options get larger, but not all, shares", "Shares are fixed", "Shares follow population"], 1, "The logit spreads the market by relative cost; the exponent sets how sharply."),
                   ("A carbon price and an emissions cap are…", ["Unrelated", "Two ways to reach the same outcome", "Only used for land", "Inputs to Hector"], 1, "A cap is met by finding the carbon price that delivers it.")],
            exit=["I can describe each GCAM component, its main rule and its inputs and outputs", "I can calculate logit shares and calibrate share weights by hand",
                  "I can explain how GCAM's solver clears many markets in each period", "I can trace at least three feedbacks, such as bioenergy to land to food prices",
                  "I can run the toy models and change an assumption", "I can read GCAM output into R or Python and compare a policy run with the Reference"],
            handbook="downloads/Go2-Component-Handbook-Open-the-Boxes.pdf", kit="downloads/go2-kit.zip"),
    3: dict(name="Research with GCAM: transport", short="Research", depth="Research",
            promise="Design, build and defend a research study with GCAM, using the transport sector as the running case.",
            style="Each module reads like a research brief: the question, the method, the implementation in GCAM's XML and code, the evidence from the literature, and the pitfalls.",
            need="Go 2, or its exit check. A GCAM 9.x installation for the implementation steps, plus R or Python.",
            produce=["A research proposal with a scenario design matrix and an uncertainty plan", "Add-on XML scenarios for transport technologies and policies, run as a batch",
                     "A reproducible analysis: decomposition, sensitivity and scenario discovery", "A short paper and talk following the GCAM community guidelines"],
            entry=[("Passenger mode choice in GCAM includes…", ["Only fuel cost", "Money cost plus the value of time", "Only vehicle price", "Only speed"], 1, "The generalised cost adds wage-based time cost to money cost."),
                   ("An add-on XML file…", ["Replaces GCAM's source code", "Changes selected inputs and is loaded after the base files", "Is a query", "Must contain every region"], 1, "Add-ons override the base inputs they name; load order matters."),
                   ("Scenario discovery finds…", ["The single best scenario", "Which combinations of inputs lead to an outcome of interest", "The base year", "The solver tolerance"], 1, "It searches an ensemble for the input ranges that explain, say, high emissions.")],
            exit=["I can explain how GCAM represents passenger and freight transport, including value of time", "I can write and load add-on XML for costs, load factors, share weights and policies",
                  "I can design a scenario matrix with an uncertainty plan", "I can decompose a change in transport CO2 and run scenario discovery",
                  "I can place my question in the literature and state what GCAM cannot see", "I can report results reproducibly and in IAMC format"],
            handbook="downloads/Go3-Research-Handbook-GCAM-Transport.pdf", kit="downloads/go3-transport-kit.zip"),
}

# module page section names differ by go: the same content, a different reading order and voice
LABELS = {
    1: dict(overview="Start here", picture="Look", explore="Predict, then check", parts="The parts", code="Try a quick calculation", take="Remember", quiz="Check yourself", more="Words and links"),
    2: dict(overview="Start here", picture="Connections map", explore="Play with it", parts="The parts", code="Build it", take="Remember", quiz="Check yourself", more="Words and links"),
    3: dict(overview="Research brief", picture="The system under study", explore="Stress-test it", parts="Key elements", code="Implement it", take="Research notes", quiz="Check yourself", more="Reading list"),
}
ORDER = {1: ["overview", "picture", "explore", "sections", "parts", "code", "take", "quiz", "more"],
         2: ["overview", "picture", "parts", "sections", "code", "explore", "take", "quiz", "more"],
         3: ["overview", "picture", "sections", "parts", "code", "explore", "take", "quiz", "more"]}


def load():
    mods = [json.load(open(f)) for f in sorted(glob.glob(os.path.join(ROOT, "content", "m*.json")))]
    mods.sort(key=lambda m: (m["go"], [int(x) for x in m["id"].split(".")]))
    return mods


def head(title, desc, depth=0, extra=""):
    up = "../" * depth
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Archivo:wdth,wght@62..125,400..800&family=Atkinson+Hyperlegible+Mono:wght@400;600&family=Atkinson+Hyperlegible+Next:wght@400;600;700&family=Noto+Naskh+Arabic:wght@400;600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{up}assets/css/site.css">
<link rel="icon" href="{up}assets/img/icon.svg" type="image/svg+xml">
{extra}</head>
"""


def topbar(depth, current, bodyattr=""):
    up = "../" * depth
    items = [("go1.html", "Go 1 · Big picture"), ("go2.html", "Go 2 · Components"), ("go3.html", "Go 3 · Research"), ("toolkit.html", "Toolkit"), ("glossary.html", "Glossary")]
    nav = "".join(f'<a href="{up}{h}"{" aria-current=page" if h == current else ""}>{t}</a>' for h, t in items)
    dots = "".join(f'<i class="c-{s}"></i>' for s in SYS)
    return f"""<body{bodyattr}>
<a class="skip" href="#main">Skip to content</a>
<header class="top"><div class="wrap">
<a class="brand" href="{up}index.html"><span class="dots" aria-hidden="true">{dots}</span>GCAM in three goes</a>
<nav class="nav" aria-label="Main">{nav}<button class="iconbtn" id="theme" type="button" aria-label="Switch between light and dark theme">Light / dark</button></nav>
</div></header>
"""


def foot(depth, scripts=True):
    up = "../" * depth
    s = f'<script src="{up}assets/js/diagrams.js"></script><script src="{up}assets/js/widgets.js"></script><script src="{up}assets/js/site.js"></script>' if scripts else ""
    return f"""<footer class="site"><div class="wrap">An open course on the Global Change Analysis Model (GCAM), taught in three goes. GCAM is developed by the Joint Global Change Research Institute (PNNL); this is independent teaching material. GCAM facts follow the GCAM v8.2 documentation and the gcam-core v9.1 source; explorers and toy models are teaching versions with illustrative numbers.</div></footer>
{s}
</body></html>"""


def sysdots(systems):
    return '<span class="sysdots" aria-hidden="true">' + "".join(f'<i class="c-{s}"></i>' for s in systems) + "</span>"


def chips(systems):
    return "".join(f'<span class="sys-chip"><i class="c-{s}"></i>{SYSNAME[s]}</span>' for s in systems)


def module_list(mods, depth=0):
    up = "../" * depth
    out = ['<ol class="mlist">']
    for m in mods:
        out.append(f'<li><a href="{up}modules/{m["slug"]}.html"><span class="num">{m["id"]}</span>'
                   f'<span><span class="t">{esc(m["title"])}</span>{sysdots(m["systems"])}<span class="state" data-progress-for="{m["id"]}" aria-hidden="true"></span>'
                   f'<span class="d">{esc(m["summary"])}</span></span><span class="meta">{m["minutes"]} min<br>{esc(m["tag"])}</span></a></li>')
    out.append("</ol>")
    return "".join(out)


def code_html(c, mid, depth=1):
    up = "../" * depth
    src = c.get("source")
    if c.get("file"):
        src = open(os.path.join(ROOT, c["file"]), encoding="utf-8").read()
    runnable = c.get("runnable") and c.get("lang") == "python"
    lang = {"python": "Python", "r": "R", "xml": "XML", "bash": "Shell"}.get(c.get("lang"), c.get("lang", ""))
    btns = '<button class="btn quiet code-copy" type="button">Copy</button>'
    if c.get("file"): btns += f'<a class="btn quiet" href="{up}{c["file"]}" download>Download</a>'
    if runnable:
        btns = '<button class="btn code-run" type="button">Run in browser</button><button class="btn quiet code-reset" type="button">Reset</button>' + btns
        body = f'<textarea spellcheck="false" aria-label="Editable Python code">{esc(src)}</textarea>'
    else:
        body = f"<pre><code>{esc(src)}</code></pre>"
    exp = f'<div class="expected"><p class="small muted" style="margin:0 0 4px">Expected output</p><pre>{esc(c["expected"])}</pre></div>' if c.get("expected") else ""
    runs = '<span class="runs">Runs in your browser</span>' if runnable else ""
    return (f'<div class="codeblock" data-module="{mid}"><div class="codehead"><b>{esc(c["title"])}</b><span class="lang">{lang}</span>{runs}{btns}</div>'
            f'{body}<div class="explain-code">{c.get("explain", "")}</div>{exp}<div class="code-out" hidden aria-live="polite"></div></div>')


def module_page(m, prev, nxt, diagrams):
    mid, depth, g = m["id"], 1, m["go"]
    L = LABELS[g]
    diagrams[f"m{mid}"] = m["diagram"]
    toc, body = [], []

    def sec(anchor, title, content):
        toc.append(f'<li><a href="#{anchor}">{esc(title)}</a></li>')
        body.append(f'<section id="{anchor}"><h2>{esc(title)}</h2>{content}</section>')

    narr = (f'<div class="narration" data-module="{mid}"><div class="narr-bar"><button class="btn narr-play" type="button">Listen</button>'
            f'<button class="btn quiet narr-stop" type="button">Stop</button><span class="muted small">Spoken overview</span>'
            f'<button class="narr-lang" type="button" data-lang="en" aria-pressed="true">English</button><button class="narr-lang" type="button" data-lang="ar" aria-pressed="false">العربية</button>'
            f'<span class="narr-status" aria-live="polite"></span></div><details><summary>Read the transcript</summary>'
            f'<p class="narr-en">{esc(m["narration_en"])}</p><p class="narr-ar" lang="ar" dir="rtl" hidden>{esc(m["narration_ar"])}</p></details></div>')
    lead = {1: "By the end you can", 2: "By the end you can", 3: "In this module you will"}[g]
    outcomes = "<ul class='outcomes'>" + "".join(f"<li>{esc(o)}</li>" for o in m["outcomes"]) + "</ul>"
    d = m["diagram"]
    blocks = {}
    blocks["overview"] = lambda: sec("start", L["overview"], f'<h3 style="margin-top:0">{lead}</h3>{outcomes}{narr}')
    intro = {1: "Select any box to see what it is, or play the walkthrough to see the idea unfold.",
             2: "This component and the parts of GCAM it trades with. Select a box for detail, or play the walkthrough to follow the mechanism.",
             3: "Select a box for detail, or play the walkthrough."}[g]
    blocks["picture"] = lambda: sec("picture", L["picture"], f'<p class="prose"><b>{esc(d.get("title", ""))}.</b> {intro}</p>'
                                    f'<div class="diagram-box"><div id="dg-{mid.replace(".", "-")}" data-diagram="m{mid}"><p class="muted">This diagram needs JavaScript. {esc(d.get("caption", ""))}</p></div></div>')

    def parts():
        if not m.get("components"): return
        rows = "".join(f'<tr><td><b>{esc(r["name"])}</b></td><td>{esc(r["purpose"])}</td><td>{esc(r["analogy"])}</td></tr>' for r in m["components"]["rows"])
        sec("parts", L["parts"], f'<p class="prose">{esc(m["components"].get("caption", ""))}</p><div class="tscroll"><table class="tbl"><thead><tr><th>Part</th><th>What it does</th><th>Think of it as</th></tr></thead><tbody>{rows}</tbody></table></div>')
    blocks["parts"] = parts

    def sections():
        callouts = m.get("callouts", [])
        for i, s in enumerate(m["sections"]):
            extra = "".join(f'<div class="callout {c["kind"]}"><h4>{esc(c["title"])}</h4>{c["html"]}</div>' for c in callouts if c["after"] == i)
            sec(f"s{i + 1}", s["heading"], f'<div class="prose">{s["html"]}</div>{extra}')
    blocks["sections"] = sections

    def explore():
        if not m.get("explorer"): return
        e = m["explorer"]
        pr = f'<div class="predict"><b>Predict first:</b> {esc(e.get("predict", ""))}</div>' if e.get("predict") else ""
        sec("explore", L["explore"], f'<div class="explorer" data-widget="{e["widget"]}" data-module="{mid}"><p class="prose">{esc(e.get("intro", ""))}</p>{pr}<div class="explorer-box"><p class="muted">This explorer needs JavaScript.</p></div></div>')
    blocks["explore"] = explore

    def code():
        if not m.get("code"): return
        lead2 = {1: "A few lines of Python that do the arithmetic above. Press Run: nothing to install.",
                 2: "Examples marked 'Runs in your browser' run here; edit a number and run again. The R version is identical; download it for RStudio.",
                 3: "Real files from the Go 3 transport kit. XML and analysis scripts are for your own GCAM installation; Python marked 'Runs in your browser' runs here."}[g]
        sec("code", L["code"], f'<p class="prose">{lead2}</p>' + "".join(code_html(c, mid) for c in m["code"]))
    blocks["code"] = code
    blocks["take"] = lambda: sec("takeaways", L["take"], "<ul class='takeaways'>" + "".join(f"<li>{esc(t)}</li>" for t in m["takeaways"]) + "</ul>")

    def quiz():
        qs = []
        for i, q in enumerate(m["quiz"]):
            opts = "".join(f'<button class="opt" type="button">{esc(o)}</button>' for o in q["options"])
            qs.append(f'<div class="q" data-answer="{q["answer"]}"><p>{i + 1}. {esc(q["q"])}</p><div class="opts">{opts}</div><p class="fb" hidden><b class="verdict"></b>{esc(q["explain"])}</p></div>')
        sec("check", L["quiz"], f'<div class="quiz" data-module="{mid}">{"".join(qs)}<p class="quiz-result" hidden aria-live="polite"></p><button class="btn quiet quiz-again" type="button">Try the questions again</button></div>')
    blocks["quiz"] = quiz

    def more():
        words = "<dl class='glist'>" + "".join(f'<div class="gterm"><dt>{esc(x["term"])}</dt><dd>{esc(x["def"])}</dd></div>' for x in m["glossary"]) + "</dl>"
        res = "<ul class='reslist'>" + "".join(f'<li><a href="{esc(r["url"])}" target="_blank" rel="noopener">{esc(r["title"])}</a><span class="why">{esc(r["why"])}</span></li>' for r in m["resources"]) + "</ul>"
        dls = ("<h3>Downloads</h3><div class='dl'>" + "".join(f'<a class="btn quiet" href="../{esc(x["path"])}">{esc(x["label"])}</a>' for x in m["downloads"]) + "</div>") if m.get("downloads") else ""
        sec("more", L["more"], f"<h3 style='margin-top:0'>New words</h3>{words}<h3>Read further</h3>{res}{dls}")
    blocks["more"] = more
    for k in ORDER[g]: blocks[k]()

    pager = '<nav class="pager" aria-label="Module navigation">'
    pager += f'<a href="{prev["slug"]}.html"><span class="dir">Previous</span>{prev["id"]} {esc(prev["title"])}</a>' if prev else f'<a href="../go{g}.html"><span class="dir">Back to</span>Go {g}: {esc(GO[g]["name"])}</a>'
    pager += f'<a class="next" href="{nxt["slug"]}.html"><span class="dir">Next</span>{nxt["id"]} {esc(nxt["title"])}</a>' if nxt else f'<a class="next" href="../go{g}.html#exit"><span class="dir">End of Go {g}</span>Take the exit check</a>'
    pager += "</nav>"
    page = head(f'{mid} {m["title"]} · {SITE}', m["summary"], depth) + topbar(depth, f"go{g}.html", f' data-module="{mid}" data-go="{g}"')
    page += f"""<main id="main" class="wrap">
<p class="crumbs"><a href="../index.html">Home</a> / <a href="../go{g}.html">Go {g}: {esc(GO[g]["name"])}</a> / Module {mid}</p>
<header class="mhead go{g}"><p class="eyebrow"><span class="golevel">Go {g} · {GO[g]["depth"]}</span> Module {mid}, {m["minutes"]} minutes, {esc(m["tag"].lower())}</p><h1>{esc(m["title"])}</h1><p class="summary">{esc(m["summary"])}</p><div>{chips(m["systems"])}</div></header>
<div class="mlayout"><nav class="outline" aria-label="On this page"><p>On this page</p><ol>{"".join(toc)}</ol><p><a href="../mindmap-go{g}.html">Go {g} mind map</a></p></nav>
<div class="mmain">{"".join(body)}
<div class="done-row"><button class="btn" id="mark-done" type="button" aria-pressed="false">Mark this module as studied</button><span class="muted small">Saved in this browser only.</span></div>
{pager}</div></div></main>
""" + foot(depth)
    return page


# ------------------------------------------------------------------ the GCAM system, seen at three depths
def node(id, label, sub, x, y, sys, d1, d2, d3, w=200):
    return {"id": id, "label": label, "sub": sub, "x": x, "y": y, "w": w, "h": 64, "sys": sys, "detail": {"1": d1, "2": d2, "3": d3}}


HERO = {
    "title": "The GCAM system", "caption": "People, energy, land and water trade through one marketplace every five years; emissions go to the Hector climate model. Choose a depth, then select a box.",
    "nodes": [
        node("soc", "People and economy", "population, GDP", 130, 80, "economy",
             "How many people, and how rich. More people and higher incomes mean more demand for energy, food and water.",
             "Population and labour productivity per region come from the Shared Socioeconomic Pathways; GDP drives every demand through income elasticities. GCAM 9.0 added the KLEAM macro module.",
             "Research angle: income and wage growth set the value of travel time, so they shift transport mode choice. Test faster and slower GDP paths as a sensitivity."),
        node("en", "Energy", "resources, power, fuels, demand", 450, 80, "energy",
             "Coal, oil, gas, sun, wind and biomass become electricity and fuels that homes, factories and vehicles use.",
             "Graded resource supply curves; electricity with a value-factor adjustment for wind and solar; refining, hydrogen; buildings, industry and transport demands. Technologies compete by nested logit.",
             "Research angle: transport sits here, as passenger and freight sectors nested by mode, size class and technology, with costs from OTAQ_trn_data_EMF37.csv and absolute-cost logits inside modes."),
        node("mk", "Marketplace", "prices clear every market", 450, 250, "neutral",
             "Every good has a price. The model keeps adjusting prices until what is supplied equals what is wanted.",
             "Recursive-dynamic partial equilibrium: in each 5-year period the solver (Broyden's method) adjusts all prices until excess demand is below tolerance in every market. No foresight.",
             "Research angle: check the solver log for unsolved markets before you trust a run; constraints (caps) add markets whose prices are shadow prices."),
        node("land", "Land and food", "crops, forests, bioenergy", 130, 250, "land",
             "Land is shared between crops, animals, forests and energy crops, depending on what earns the most.",
             "More than 300 land units; nested logit on expected profit per hectare; yields, land carbon, and a land-carbon price when carbon is priced.",
             "Research angle: biofuels for aviation and shipping pull on this land; trace the land and food-price side effects of transport policy."),
        node("wat", "Water", "235 basins", 130, 420, "water",
             "Farms, power plants, factories and towns all need water; each river basin has only so much.",
             "Withdrawals and consumption by sector in 235 basins; supply from renewable water, then groundwater, then desalination, with a basin water price.",
             "Research angle: electrifying transport raises power demand, and power plants need cooling water in water-stressed basins."),
        node("em", "Emissions", "CO2 and other gases", 450, 420, "climate",
             "Burning fuel, clearing land and some industries release CO2 and other gases.",
             "Emissions are activity × emission factor, with marginal abatement cost curves for non-CO2 gases and land-use change emissions from the land model.",
             "Research angle: tailpipe CO2 vs upstream emissions in power and hydrogen; report both, and decompose changes into activity, structure, intensity and carbon."),
        node("cl", "Climate (Hector)", "concentrations, warming", 770, 420, "climate",
             "Emissions add up in the air and warm the planet.",
             "Hector, a simple climate model run inside GCAM each period, turns emissions into concentrations, radiative forcing and temperature.",
             "Research angle: climate targets can be imposed as constraints; for uncertainty, pair GCAM with an emulator such as FaIR or MAGICC."),
        node("pol", "Policy", "carbon price, limits, standards", 770, 165, "policy",
             "A policy changes the rules: a price on carbon, a limit on emissions, or a standard on technologies.",
             "Carbon prices (in 1990$ per tonne of carbon), emissions constraints solved as markets, climate targets, and portfolio standards built as credit markets.",
             "Research angle: a zero-emission-vehicle standard can be built as a credit market in add-on XML; test it against a carbon price that gives the same emissions.")],
    "edges": [
        {"from": "soc", "to": "en", "label": "energy demand"}, {"from": "soc", "to": "land", "label": "food demand"},
        {"from": "en", "to": "mk", "label": "supply, demand"}, {"from": "land", "to": "mk", "label": "crops, biomass"},
        {"from": "mk", "to": "en", "label": "prices", "sys": "neutral"}, {"from": "wat", "to": "land", "label": "irrigation"},
        {"from": "en", "to": "em", "label": "fuel CO2"}, {"from": "land", "to": "em", "label": "land-use CO2"},
        {"from": "em", "to": "cl", "label": "emissions"}, {"from": "pol", "to": "mk", "label": "carbon price"}, {"from": "wat", "to": "em", "sys": "water", "label": "cooling water"}],
    "tour": [
        {"focus": ["soc"], "text": "Start with people: how many, and how rich. These come from the Shared Socioeconomic Pathways."},
        {"focus": ["soc", "en", "land"], "edges": [["soc", "en"], ["soc", "land"]], "text": "People need energy services and food, so demand flows into the energy system and onto the land."},
        {"focus": ["en", "land", "mk"], "edges": [["en", "mk"], ["land", "mk"], ["mk", "en"]], "text": "Every good is traded in a market. The solver moves prices until supply meets demand everywhere at once."},
        {"focus": ["wat", "land", "em"], "edges": [["wat", "land"], ["wat", "em"]], "text": "Water links farms and power plants: irrigation and cooling compete for each basin's supply."},
        {"focus": ["en", "land", "em", "cl"], "edges": [["en", "em"], ["land", "em"], ["em", "cl"]], "text": "Activities release emissions, and Hector turns them into warming."},
        {"focus": ["pol", "mk"], "edges": [["pol", "mk"]], "text": "A policy changes prices. Run the same world with and without it: the difference is the policy's effect."}]}


# ------------------------------------------------------------------ zooming mind maps (Prezi-style)
def short(t, n=46):
    t = re.sub(r"<[^>]+>", "", t).strip()
    return t if len(t) <= n else t[:n - 1].rsplit(" ", 1)[0] + "…"


def mindmap_data(g, mods):
    return {"title": f"Go {g}: {GO[g]['name']}", "center": f"Go {g}", "subtitle": GO[g]["name"], "promise": GO[g]["promise"],
            "branches": [{"id": m["id"], "title": m["title"], "sys": m["systems"][0], "href": f"modules/{m['slug']}.html", "summary": m["summary"],
                          "leaves": [short(s["heading"]) for s in m["sections"]][:6], "notes": m["takeaways"][:4]} for m in mods]}


def mindmap_page(g, data):
    page = head(f"Go {g} mind map · {SITE}", f"Zooming mind map of Go {g}: {GO[g]['name']}", 0) + topbar(0, f"go{g}.html", ' class="mm-page"')
    page += f"""<main id="main" class="mm-main">
<div class="mm-bar wrap"><div><h1 class="mm-title">Go {g} mind map</h1><p class="muted small">Press Start, then use the arrow keys or the buttons to zoom from the whole go into each module. Press F for full screen. Select a module on the map to jump to it.</p></div>
<div class="btnrow"><button class="btn" id="mm-start" type="button">Start</button><button class="btn quiet" id="mm-prev" type="button">Back</button><button class="btn quiet" id="mm-next" type="button">Next</button><button class="btn quiet" id="mm-all" type="button">Whole map</button><button class="btn quiet" id="mm-full" type="button">Full screen</button><a class="btn quiet" href="downloads/mindmaps/Go{g}-mind-map-path.pdf">PDF (for Prezi import)</a></div></div>
<div class="mm-stage" id="mm-stage" tabindex="0" aria-label="Zooming mind map"><svg id="mm-svg" role="img" aria-label="Mind map of Go {g}"></svg>
<aside class="mm-notes" id="mm-notes" aria-live="polite"></aside><p class="mm-step" id="mm-step"></p></div>
</main>
<script>window.MINDMAP = {json.dumps(data, ensure_ascii=False)};</script>
<script src="assets/js/mindmap.js"></script>
""" + foot(0)
    return page


# ------------------------------------------------------------------ build
def build():
    mods = load()
    os.makedirs(os.path.join(ROOT, "modules"), exist_ok=True)
    for f in glob.glob(os.path.join(ROOT, "modules", "*.html")): os.remove(f)
    diagrams = {"hero": HERO}
    for i, m in enumerate(mods):
        same = [x for x in mods if x["go"] == m["go"]]
        j = same.index(m)
        open(os.path.join(ROOT, "modules", m["slug"] + ".html"), "w").write(module_page(m, same[j - 1] if j else None, same[j + 1] if j + 1 < len(same) else None, diagrams))
    open(os.path.join(ROOT, "assets/js/diagrams.js"), "w").write("window.GCAM_DIAGRAMS = " + json.dumps(diagrams, ensure_ascii=False) + ";\n")
    for f in ("progress.html", "labs.html", "resources.html", "downloads.html"):
        p = os.path.join(ROOT, f)
        if os.path.exists(p): os.remove(p)

    ncode = sum(len(m.get("code", [])) for m in mods); nrun = sum(1 for m in mods for c in m.get("code", []) if c.get("runnable"))
    terms = {}
    for m in mods:
        for x in m["glossary"]: terms.setdefault(x["term"].strip(), (x["def"], m))

    # ---- home
    bands = []
    for g in (1, 2, 3):
        ms = [m for m in mods if m["go"] == g]
        hrs = round(sum(m["minutes"] for m in ms) / 60, 1) if ms else 0
        bands.append(f"""<a class="goband go{g}" href="go{g}.html"><span class="gb-n">Go {g}</span><span class="gb-body"><span class="gb-depth">{GO[g]["depth"]}</span>
<span class="gb-name">{esc(GO[g]["name"])}</span><span class="gb-promise">{esc(GO[g]["promise"])}</span>
<span class="gb-meta">{(str(len(ms)) + " modules · about " + str(hrs) + " hours") if ms else "Modules being added"} · you need: {esc(GO[g]["need"].split(".")[0].lower())}</span></span></a>""")
    idx = head(f"{SITE}: learn the Global Change Analysis Model", "Learn GCAM three times, each time deeper: the big picture, the components and how they interact, and research with the model.", 0) + topbar(0, "index.html")
    idx += f"""<main id="main">
<section class="hero3"><div class="wrap">
<h1>Learn GCAM three times, each time deeper</h1>
<p class="lede">GCAM links people, energy, land, water and climate in one model of the world. You will meet the whole system three times: first as a picture, then as working parts that push on each other, then as a research tool you change and test.</p>
<div class="gobands">{"".join(bands)}</div>
</div></section>
<section class="section"><div class="wrap">
<h2>The same system, three depths</h2>
<p class="prose muted">Every go covers the whole model. Choose a depth and select any part of GCAM to see how the course treats it at that level.</p>
<div class="levels"><div class="btnrow" role="group" aria-label="Choose a depth">
<button class="narr-lang lv" type="button" data-level="1" aria-pressed="true" data-blurb="Go 1: what each part is and why it matters.">Go 1 · Big picture</button>
<button class="narr-lang lv" type="button" data-level="2" aria-pressed="false" data-blurb="Go 2: the rule each part follows and what it trades with the others.">Go 2 · Components</button>
<button class="narr-lang lv" type="button" data-level="3" aria-pressed="false" data-blurb="Go 3: what a transport researcher changes, measures or worries about here.">Go 3 · Research</button></div>
<p class="lv-blurb muted">Go 1: what each part is and why it matters.</p>
<div class="diagram-box"><div id="dg-hero" data-diagram="hero" data-intro="1" data-level="1" data-hint="Select a part of GCAM."><p class="muted">GCAM connects people, energy, land, water, emissions and climate through markets.</p></div></div></div>
</div></section>
<section class="section"><div class="wrap"><h2>How the goes fit together</h2>
<div class="cols3">
<div><h3>Start where you are</h3><p>Each go opens with a three-question check. If you already know the answers, skip ahead. Each go closes with an exit check: tick off what you can do before moving on.</p></div>
<div><h3>Each go works differently</h3><p>Go 1 is pictures and predict-then-check explorers. Go 2 is connection maps and small models you build. Go 3 is a research brief for each step of a real study, with GCAM files and code.</p></div>
<div><h3>Real model, honest toys</h3><p>GCAM facts follow the v8.2 documentation and the gcam-core v9.1 source. Explorers and toy models are small teaching versions; their numbers are illustrative and say so.</p></div></div>
<p style="margin-top:18px"><a href="mindmap-go1.html">Go 1 mind map</a> · <a href="mindmap-go2.html">Go 2 mind map</a> · <a href="mindmap-go3.html">Go 3 mind map</a> · <a href="toolkit.html">Toolkit: {ncode} code examples, handbooks and slides</a> · <a href="glossary.html">Glossary: {len(terms)} terms</a></p>
</div></section>
</main>
""" + foot(0)
    open(os.path.join(ROOT, "index.html"), "w").write(idx)

    # ---- go landing pages
    for g in (1, 2, 3):
        ms = [m for m in mods if m["go"] == g]
        info = GO[g]
        eq = "".join(f'<div class="q" data-answer="{a}"><p>{i + 1}. {esc(q)}</p><div class="opts">' + "".join(f'<button class="opt" type="button">{esc(o)}</button>' for o in opts) + f'</div><p class="fb" hidden><b class="verdict"></b>{esc(ex)}</p></div>' for i, (q, opts, a, ex) in enumerate(info["entry"]))
        seen, res = set(), []
        for m in ms:
            for r in m["resources"]:
                if r["url"] in seen: continue
                seen.add(r["url"]); res.append(f'<li><a href="{esc(r["url"])}" target="_blank" rel="noopener">{esc(r["title"])}</a><span class="why">{esc(r["why"])} <span class="muted">· module {m["id"]}</span></span></li>')
        mats = [f'<a class="btn" href="{info["handbook"]}">Go {g} handbook (PDF)</a>', f'<a class="btn quiet" href="mindmap-go{g}.html">Zooming mind map</a>']
        if info["kit"]: mats.append(f'<a class="btn quiet" href="{info["kit"]}">Go {g} code kit (zip)</a>')
        prev_go = f'<a href="go{g - 1}.html">Go {g - 1}</a>' if g > 1 else ""
        nxt = f'<a class="btn" href="go{g + 1}.html">Go on to Go {g + 1}: {esc(GO[g + 1]["name"])}</a>' if g < 3 else '<a class="btn" href="toolkit.html">Start your project with the toolkit</a>'
        skip = f'All three right? You could <a href="go{g + 1}.html">skip ahead to Go {g + 1}</a>, or use this go as revision.' if g < 3 else "All three right? You are ready for the research modules."
        exitl = "".join(f'<li><label><input type="checkbox"> {esc(x)}</label></li>' for x in info["exit"])
        first = ms[0]["slug"] if ms else ""
        page = head(f"Go {g}: {info['name']} · {SITE}", info["promise"], 0) + topbar(0, f"go{g}.html", f' data-go="{g}"')
        page += f"""<main id="main" class="wrap">
<header class="gohead go{g}"><p class="eyebrow"><span class="golevel">Go {g} · {info["depth"]}</span></p><h1>{esc(info["name"])}</h1><p class="summary">{esc(info["promise"])}</p>
<div class="cta">{"<a class='btn' href='modules/" + first + ".html'>Start module " + str(g) + ".1</a>" if first else ""}{"".join(mats)}</div></header>
<div class="go-grid">
<section><h2>Is this go for you?</h2><p class="prose"><b>You need:</b> {esc(info["need"])}</p><p class="prose"><b>How it works:</b> {esc(info["style"])}</p>
<h3>Quick entry check</h3><div class="quiz" data-module="go{g}-entry">{eq}<p class="quiz-result" hidden aria-live="polite"></p></div><p class="small muted">{skip} {("Not sure? Revisit " + prev_go + ".") if prev_go else ""}</p></section>
<section><h2>What you will produce</h2><ul class="prose">{"".join(f"<li>{esc(x)}</li>" for x in info["produce"])}</ul>
<h2>The path</h2>{module_list(ms)}</section></div>
<section id="exit"><h2>Exit check</h2><p class="prose muted">Tick each statement you can honestly say. Your ticks are saved in this browser.</p>
<ul class="exitcheck checklist" data-key="go{g}-exit">{exitl}</ul><p class="exit-msg muted"></p><div class="cta">{nxt}</div></section>
<section><h2>Readings and tools for Go {g}</h2><ul class="reslist">{"".join(res)}</ul></section>
</main>""" + foot(0)
        open(os.path.join(ROOT, f"go{g}.html"), "w").write(page)
        open(os.path.join(ROOT, f"mindmap-go{g}.html"), "w").write(mindmap_page(g, mindmap_data(g, ms)))

    # ---- toolkit (code, handbooks, kits, slides, tools, progress)
    rows = []
    for m in mods:
        for c in m.get("code", []):
            run = c.get("runnable") and c.get("lang") == "python"
            tags = f'go{m["go"]} {c.get("lang", "")} {"browser" if run else "local"}'
            where = '<span class="runs">Runs in your browser</span>' if run else ("Download" if c.get("file") else "Copy from the page")
            fl = f' · <a href="{esc(c["file"])}" download>file</a>' if c.get("file") else ""
            rows.append(f'<tr class="labrow" data-tags="{tags}"><td>Go {m["go"]} · {m["id"]}</td><td><a href="modules/{m["slug"]}.html#code">{esc(c["title"])}</a>{fl}</td><td>{ {"python": "Python", "r": "R", "xml": "XML", "bash": "Shell"}.get(c.get("lang"), c.get("lang"))}</td><td>{where}</td></tr>')
    flt = "".join(f'<button class="lab-filter" type="button" data-filter="{f}" aria-pressed="{"true" if f == "all" else "false"}">{t}</button>' for f, t in [("all", "All"), ("go1", "Go 1"), ("go2", "Go 2"), ("go3", "Go 3"), ("browser", "Runs in browser"), ("python", "Python"), ("r", "R"), ("xml", "GCAM XML")])

    def size(p):
        try: return f'{os.path.getsize(os.path.join(ROOT, p)) / 1e6:.1f} MB'
        except OSError: return ""

    def item(p, t, d):
        return f'<li><a href="{p}">{esc(t)}</a> <span class="muted small">{size(p)}</span><span class="why">{esc(d)}</span></li>' if os.path.exists(os.path.join(ROOT, p)) else ""
    hand = "".join([item(GO[1]["handbook"], "Go 1 study guide: See the whole picture (35 pages)", "Visual overview with predict-then-check activities, a quiz and a cheat sheet."),
                    item(GO[2]["handbook"], "Go 2 handbook: Open the boxes (48 pages)", "Each GCAM component, its links to the others, and the toy models."),
                    item(GO[3]["handbook"], "Go 3 handbook: Research with GCAM, transport (68 pages)", "GCAM transport in full, literature review, scenario building, analysis, downscaling."),
                    item("downloads/Course-Structure-3-Goes.pdf", "Course structure in three goes", "Modules, outcomes, assessment, and how the original 15 weeks map onto the goes.")])
    kits = "".join([item("downloads/go2-kit.zip", "Go 2 kit: toy models in Python and R", "Nine toy models with identical Python and R versions, plus GCAM reader scripts."),
                    item("downloads/go3-transport-kit.zip", "Go 3 transport research kit", "Transport toy model, add-on XML templates, batch file, queries, decomposition, scenario discovery, downscaling, templates."),
                    item("downloads/iam-course-labs.zip", "R lab project (labs 1 to 14)", "RStudio project with lab scripts, solutions and GCAM files.")])
    mm = "".join(item(f"downloads/mindmaps/Go{g}-mind-map-path.pdf", f"Go {g} mind map, zoom path (PDF)", "Each zoom step as a page; import into Prezi or present as is.") for g in (1, 2, 3))
    slides = "".join(item(f"downloads/slides/{os.path.basename(p)}", os.path.basename(p)[:-4].replace("-", " ").replace("Week", "Week "), "Lecture and lab slides (PDF); the editable PowerPoint has the same name.") for p in sorted(glob.glob(os.path.join(ROOT, "downloads", "slides", "*.pdf"))))
    trs = "".join(f'<tr data-id="{m["id"]}"><td>{m["id"]}</td><td><a href="modules/{m["slug"]}.html">{esc(m["title"])}</a></td>' + '<td class="k">–</td>' * 7 + "</tr>" for m in mods)
    page = head(f"Toolkit · {SITE}", "Code, handbooks, kits, slides and tools for learning GCAM in three goes.", 0) + topbar(0, "toolkit.html")
    page += f"""<main id="main" class="wrap"><header class="page-head"><h1>Toolkit</h1><p>Everything you can run, download or install, in one place. The GCAM XML templates and reader scripts have not yet been run against a live GCAM installation; test them on your setup first.</p></header>
<h2>Code examples</h2><p class="prose muted">{ncode} examples. Python marked "Runs in your browser" runs on its module page with nothing to install.</p>
<div class="filters" role="group" aria-label="Filter code examples">{flt}</div>
<div class="tscroll"><table class="tbl"><thead><tr><th>Where</th><th>Example</th><th>Language</th><th>How to use</th></tr></thead><tbody>{"".join(rows)}</tbody></table></div>
<h2>Handbooks</h2><ul class="reslist">{hand}</ul>
<h2>Code kits</h2><ul class="reslist">{kits}</ul>
<h2>Mind maps</h2><ul class="reslist">{mm}<li><a href="mindmap-go1.html">Zooming mind maps in the browser</a><span class="why">Go 1, Go 2 and Go 3, presentable full screen.</span></li></ul>
<h2>GCAM itself</h2><ul class="reslist">
<li><a href="https://jgcri.github.io/gcam-doc/toc.html" target="_blank" rel="noopener">GCAM v8.2 documentation</a><span class="why">The official documentation: overview, every component, policies, the data system and user guides.</span></li>
<li><a href="https://github.com/JGCRI/gcam-core/releases" target="_blank" rel="noopener">GCAM releases on GitHub</a><span class="why">Download GCAM; version 9.1 was released on 2 June 2026.</span></li>
<li><a href="https://jgcri.github.io/gcam-doc/user-guide.html" target="_blank" rel="noopener">How to get started running GCAM</a><span class="why">Install, configure, run and read results.</span></li>
<li><a href="https://github.com/JGCRI/gcamreader" target="_blank" rel="noopener">gcamreader (Python)</a> · <a href="https://github.com/JGCRI/rgcam" target="_blank" rel="noopener">rgcam (R)</a><span class="why">Read GCAM output databases into data frames.</span></li></ul>
<h2>Weekly slides from the 15-week version</h2><ul class="reslist">{slides}</ul>
<h2 id="progress">Your progress</h2><p class="prose muted">Saved only in this browser on this device; nothing is sent anywhere.</p>
<p id="progress-summary" class="muted"></p><div class="meter"><i id="progress-meter" style="width:0"></i></div>
<div class="tscroll"><table class="tbl" id="progress-table"><thead><tr><th>Module</th><th>Title</th><th>Opened</th><th>Listened</th><th>Walkthrough</th><th>Explorer</th><th>Ran code</th><th>Quiz</th><th>Studied</th></tr></thead><tbody>{trs}</tbody></table></div>
<div class="btnrow"><button class="btn quiet" id="progress-export" type="button">Download my progress</button><button class="btn quiet" id="progress-reset" type="button">Clear my progress</button></div>
</main>""" + foot(0)
    open(os.path.join(ROOT, "toolkit.html"), "w").write(page)

    # ---- glossary
    gl = "".join(f'<div class="gterm"><dt>{esc(t)}</dt><dd>{esc(d)} <a class="small" href="modules/{m["slug"]}.html#more">Go {m["go"]}, module {m["id"]}</a></dd></div>' for t, (d, m) in sorted(terms.items(), key=lambda x: x[0].lower()))
    page = head(f"Glossary · {SITE}", "Plain-language glossary of GCAM and integrated assessment terms.", 0) + topbar(0, "glossary.html")
    page += f"""<main id="main" class="wrap"><header class="page-head"><h1>Glossary</h1><p>Every new word in the three goes, in plain language, with the module where it first appears.</p>
<input class="searchbox" id="glossary-search" type="search" placeholder="Search the glossary" aria-label="Search the glossary"><p class="small muted" id="glossary-count">{len(terms)} terms</p></header>
<dl class="glist" style="margin-top:20px">{gl}</dl></main>""" + foot(0)
    open(os.path.join(ROOT, "glossary.html"), "w").write(page)
    print(f"built {len(mods)} modules, {ncode} code blocks ({nrun} runnable), {len(terms)} terms")


if __name__ == "__main__":
    build()
