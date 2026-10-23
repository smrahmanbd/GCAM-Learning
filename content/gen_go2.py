"""Generate Go 2 module JSON files (m21..m28) for the GCAM learning site."""
import json, os

OUT = os.path.dirname(os.path.abspath(__file__))
DOC = "https://jgcri.github.io/gcam-doc/"
D = lambda p: DOC + p  # doc page URL
def cite(p): return f'<a href="{D(p)}">{p}</a>'

HANDBOOK = {"label": "Go 2 handbook: Open the boxes (PDF)", "path": "downloads/Go2-Component-Handbook-Open-the-Boxes.pdf"}
KIT = {"label": "Go 2 toy-model kit, R and Python (zip)", "path": "downloads/go2-kit.zip"}
def deck(name, label): return {"label": label, "path": f"downloads/slides/{name}"}

R_GCAMREADER = {"title": "gcamreader (Python)", "url": "https://github.com/JGCRI/gcamreader", "why": "Read GCAM output databases into pandas; version 1.5.0, needs Java."}
R_RGCAM = {"title": "rgcam (R)", "url": "https://github.com/JGCRI/rgcam", "why": "Query GCAM databases from R and save shareable project files."}

# canvas helpers: positions (centre x, y)
P = dict(c=(450, 260), n=(450, 70), s=(450, 450), nw=(130, 90), ne=(770, 90), sw=(130, 430), se=(770, 430), w=(130, 260), e=(770, 260))
def node(id, label, sub, pos, sys, detail, w=180, h=64):
    x, y = P[pos] if isinstance(pos, str) else pos
    return {"id": id, "label": label, "sub": sub, "x": x, "y": y, "w": w, "h": h, "sys": sys, "detail": detail}
def edge(a, b, label="", sys=None):
    e = {"from": a, "to": b, "label": label}
    if sys: e["sys"] = sys
    return e

mods = []

# ---------------------------------------------------------------- 2.1
mods.append({
 "id": "2.1", "go": 2, "slug": "socioeconomic-drivers", "title": "Socioeconomic drivers", "minutes": 40, "tag": "Drivers",
 "systems": ["economy", "energy", "land", "water"],
 "summary": "How many people there are and how rich they become set the size of every demand in GCAM. Learn where population and GDP come from, and how the Kaya identity splits emissions into drivers.",
 "outcomes": ["You can name the exogenous inputs behind GCAM's population and GDP",
              "You can explain how GDP per person drives food, energy and water demand",
              "You can decompose an emissions change with the Kaya identity, by hand and in code",
              "You can describe what GCAM's macro module (KLEM, now KLEAM) adds"],
 "narration_en": ("Every number that comes out of GCAM starts with two quiet assumptions: how many people there will be, and how rich they will become. "
   "Population comes from the Shared Socioeconomic Pathways, a set of five stories about the future. Income comes from labour productivity growth, "
   "and together they give gross domestic product for each of GCAM's thirty-two regions. These drivers then push on everything else. "
   "Richer people want more floor space, more travel, more meat and more water, so demand in every sector grows with income per person. "
   "In this module you will grow population and income for two invented storylines, a green road and a rocky road, and see how far apart their emissions end up. "
   "You will use the Kaya identity, which writes emissions as people times income per person times energy per dollar times carbon per unit of energy. "
   "The four factors multiply, they do not add, so small changes compound over eighty years. "
   "Finally, you will meet GCAM's macro module, which since version seven can let energy prices feed back into GDP itself."),
 "narration_ar": ("كل رقم يخرج من نموذج GCAM يبدأ بافتراضين هادئين: كم عدد الناس الذين سيعيشون في المستقبل، وإلى أي حد سيصبحون أغنياء. "
   "يأتي عدد السكان من مسارات التنمية الاجتماعية والاقتصادية المشتركة، وهي خمس قصص عن المستقبل. ويأتي الدخل من نمو إنتاجية العمل، "
   "ومعًا يعطيان الناتج المحلي الإجمالي لكل منطقة من مناطق النموذج الاثنتين والثلاثين. ثم تدفع هذه المحركات كل شيء آخر. "
   "فالناس الأغنى يريدون مساحة سكنية أكبر وسفرًا أكثر ولحومًا أكثر وماءً أكثر، لذلك ينمو الطلب في كل قطاع مع دخل الفرد. "
   "في هذه الوحدة ستُنمّي السكان والدخل لقصتين مُتخيَّلتين، الطريق الأخضر والطريق الوعر، وترى إلى أي مدى تتباعد انبعاثاتهما. "
   "وستستخدم متطابقة كايا، التي تكتب الانبعاثات على أنها عدد السكان مضروبًا في دخل الفرد مضروبًا في الطاقة لكل دولار مضروبًا في الكربون لكل وحدة طاقة. "
   "العوامل الأربعة تُضرب ولا تُجمع، لذا تتراكم التغيرات الصغيرة على مدى ثمانين عامًا. "
   "وأخيرًا ستتعرف على الوحدة الاقتصادية الكلية في النموذج، التي تسمح منذ الإصدار السابع بأن تؤثر أسعار الطاقة في الناتج المحلي الإجمالي نفسه."),
 "diagram": {
   "title": "Drivers in, demands out", "caption": "Population and labour productivity are inputs; GDP per person then drives every demand. Click a box, or press Play.",
   "nodes": [
     node("pop", "Population", "SSP database, by region", "nw", "economy", "Population by region comes from the SSP database for 2015 to 2100 (UN data before that). In 2100: SSP1 6.9, SSP2 9, SSP3 12.7, SSP5 7.4 billion (ssp.html)."),
     node("lab", "Labour productivity", "growth rate, exogenous", "w", "economy", "An exogenous growth rate per region. With labour force participation it sets how fast output per worker grows (economy.html, Table 1)."),
     node("gdp", "GDP and GDP per person", "32 regions, 5-year steps", "c", "economy", "Regional GDP is the scale of economic activity. Calibrated to history up to the 2021 base year, then projected to 2100 in 5-year steps.", w=210),
     node("bld", "Buildings", "floorspace, services", "ne", "energy", "Floorspace per person follows a Gompertz curve in income; services per m² saturate as income rises (demand_energy.html)."),
     node("trn", "Transport and industry", "service demand", "e", "energy", "Service output grows with income (elasticity α) and falls with price (β): D_t = D_t-1 (Y ratio)^α (P ratio)^β (N ratio)."),
     node("food", "Food and land", "staples, non-staples", "se", "land", "Food demand uses an income-dependent demand system (Edmonds et al. 2017): richer diets shift from staples to meat and dairy (demand_land.html)."),
     node("wat", "Municipal water", "per-person demand", "s", "water", "Per-capita municipal water grows with GDP per person (elasticity 0.37) and falls with price (−0.33) and technology (demand_water.html)."),
     node("macro", "Macro module", "KLEM → KLEAM (v9.0)", "sw", "economy", "Since GCAM v7 a CES production function can make GDP respond to energy: energy service efficiency, energy investment and net exports enter (economy.html). v9.0 adds agriculture (KLEAM).")],
   "edges": [edge("pop", "gdp", "people", "economy"), edge("lab", "gdp", "output per worker", "economy"), edge("gdp", "bld", "income", "economy"),
             edge("gdp", "trn", "income", "economy"), edge("gdp", "food", "income", "economy"), edge("gdp", "wat", "income", "economy"),
             edge("macro", "gdp", "energy feedback", "economy")],
   "tour": [
     {"focus": ["pop"], "edges": [["pop", "gdp"]], "text": "Start with people. Population is an input from the SSP database, different in each storyline."},
     {"focus": ["lab"], "edges": [["lab", "gdp"]], "text": "Labour productivity growth decides how much each worker produces. Together with population it sets GDP."},
     {"focus": ["gdp"], "edges": [], "text": "GDP per person is the single most important driver in GCAM. Watch where it flows next."},
     {"focus": ["bld", "trn"], "edges": [["gdp", "bld"], ["gdp", "trn"]], "text": "Energy services grow with income: more floorspace, more travel, more industrial output."},
     {"focus": ["food", "wat"], "edges": [["gdp", "food"], ["gdp", "wat"]], "text": "Diets and municipal water use also follow income, so land and water demand grow too."},
     {"focus": ["macro"], "edges": [["macro", "gdp"]], "text": "Optional feedback: the macro module lets energy costs change GDP, closing the loop."}]},
 "components": {"caption": "The pieces of the socioeconomic module", "rows": [
     {"name": "Population", "purpose": "Number of people per region and year", "analogy": "How many guests are coming to dinner"},
     {"name": "Labour productivity", "purpose": "Output per worker; grows at an assumed rate", "analogy": "How fast each cook can work"},
     {"name": "GDP", "purpose": "Scale of the regional economy", "analogy": "The size of the whole kitchen's budget"},
     {"name": "GDP per person", "purpose": "Drives demand for energy services, food and water", "analogy": "How much each guest can afford to order"},
     {"name": "SSP storyline", "purpose": "A consistent set of population, income and technology assumptions", "analogy": "The menu theme for the evening"},
     {"name": "Macro module (KLEM/KLEAM)", "purpose": "Optional: lets energy and policy change GDP", "analogy": "A kitchen whose budget shrinks if gas gets dear"}]},
 "sections": [
   {"heading": "What this component represents", "html": "<p>The <b>socioeconomic drivers</b> are the number of people and their income, region by region and period by period. They are not results of the energy or land model in the standard setup: they are assumptions you choose, usually from one of the five <b>Shared Socioeconomic Pathways</b> (SSPs).</p><p>GCAM uses <b>32 geopolitical regions</b> and steps forward in <b>5-year periods from 2025 to 2100</b>, after a base year of <b>2021</b>. Population and GDP set the overall scale of activity that every other module must serve (" + cite("overview.html") + ", " + cite("common_assumptions.html") + ").</p>"},
   {"heading": "How GCAM builds population and GDP", "html": "<p>The economy module reads a small set of exogenous inputs: population (thousands), labour productivity growth, labour force participation, base-year GDP and national accounts (" + cite("economy.html") + "). Population before 2015 comes from Maddison and the UN; from 2015 the SSP database supplies it. Future GDP comes from the SSP database (OECD model).</p><div class=\"eq\">GDP<sub>r,t</sub> = population<sub>r,t</sub> × labour force share × output per worker<sub>r,t</sub></div><div class=\"eq\">output per worker<sub>t</sub> = output per worker<sub>t−1</sub> × (1 + g)<sup>5</sup></div><p>Here g is the yearly labour productivity growth rate. Five years of growth compound in each model step.</p>"},
   {"heading": "Income drives every demand", "html": "<p>GDP per person is the bridge to the rest of the model. Buildings floorspace follows a Gompertz curve in income, so it rises fast and then saturates. Industry and transport service output follow</p><div class=\"eq\">D<sub>t</sub> = D<sub>t−1</sub> · (Y<sub>t</sub>/Y<sub>t−1</sub>)<sup>α</sup> · (P<sub>t</sub>/P<sub>t−1</sub>)<sup>β</sup> · (N<sub>t</sub>/N<sub>t−1</sub>)</div><p>where Y is GDP per person, P the service price, N population, α the income elasticity and β the price elasticity (" + cite("demand_energy.html") + "). Food demand, municipal water (income elasticity 0.37) and air-pollution controls also depend on income (" + cite("demand_land.html") + ", " + cite("demand_water.html") + ").</p>"},
   {"heading": "The Kaya identity: splitting emissions into drivers", "html": "<p>The <b>Kaya identity</b> writes CO<sub>2</sub> as a product of four factors. It is always true, because the units cancel:</p><div class=\"eq\">CO<sub>2</sub> = population × (GDP / person) × (energy / GDP) × (CO<sub>2</sub> / energy)</div><p>Because the factors multiply, their <i>ratios</i> multiply too. In the kit's invented <i>Green road</i>, population grows 1.10×, income per person 5.70×, energy per dollar falls to 0.132× and carbon per unit of energy to 0.087×. The product is <b>0.072</b>: emissions in 2100 are 7% of 2020. On the <i>Rocky road</i> the ratios are 1.52, 2.22, 0.53 and 0.79, giving <b>1.393</b>, a 39% rise.</p>"},
   {"heading": "When GDP stops being fixed: the macro module", "html": "<p>Since GCAM v7 a macroeconomic module (KLEM: capital, labour, energy, materials) can make GDP respond to the energy system. A nested CES production function uses an energy-service efficiency index from the energy module, and capital accumulates with depreciation (" + cite("economy.html") + "). In <b>open-GDP</b> mode a carbon policy changes GDP and consumption directly. GCAM v9.0 extended it to <b>KLEAM</b>, adding agriculture with its own labour and capital. The CES parameter values are not given on the documentation pages.</p>"}],
 "callouts": [
   {"after": 1, "kind": "gcam", "title": "In GCAM", "html": "<p>Population and GDP inputs are built by gcamdata from <code>SSP_database_2024.csv.gz</code>, <code>USDA_GDP_MER.csv</code> and <code>pwt91.csv</code> (" + cite("inputs_economy.html") + "). In a run, query <b>GDP by region</b> and <b>Population by region</b> in ModelInterface, or with rgcam/gcamreader. All five SSPs are implemented; GCAM was the marker model for SSP4 (" + cite("ssp.html") + ").</p>"},
   {"after": 3, "kind": "trap", "title": "Adding instead of multiplying", "html": "<p>Avalon's factors change by +20%, +50%, −30% and −20%. Adding gives +20%, which is wrong. Multiply: 1.2 × 1.5 × 0.7 × 0.8 = <b>1.008</b>, so CO<sub>2</sub> rises by only 0.8%.</p>"},
   {"after": 4, "kind": "research", "title": "Version note", "html": "<p>The online documentation describes GCAM v8.2; the latest release is <b>GCAM 9.1</b> (2 June 2026), which includes KLEAM (v9.0). The overview page still calls 2015 the final calibration year; other pages and the v8.0 notes say <b>2021</b>, which is current.</p>"}],
 "explorer": {"widget": "kaya", "intro": "Set how population, income, energy per dollar and CO₂ per unit of energy change over 30 years, and watch the CO₂ ratio.", "predict": "If income per person doubles and the other three factors stay the same, what happens to CO₂? Then: how much must energy per dollar fall to hold CO₂ flat?"},
 "code": [
   {"title": "Two storylines and a Kaya check", "lang": "python", "file": "labs/go2/m21_drivers.py", "runnable": True,
    "explain": "Grows population (logistic) and income for two invented storylines, builds CO₂ with the Kaya identity and checks that the factor ratios multiply to the CO₂ ratio. Try: set the Rocky road income growth to 0.022 and predict the new CO₂ ratio before running.",
    "expected": "Green road: product = 0.072, CO2 ratio = 0.072\nRocky road: product = 1.393, CO2 ratio = 1.393"},
   {"title": "The same model in R", "lang": "r", "file": "labs/go2/m21_drivers.R", "runnable": False, "explain": "Identical numbers in base R. Run with Rscript m21_drivers.R."},
   {"title": "Read GDP and population from a GCAM run (R)", "lang": "r", "runnable": False,
    "source": "library(rgcam)\nconn <- localDBConn('path/to/gcam/output', 'database_basexdb')\nprj  <- addScenario(conn, 'go2.dat', 'Reference', 'go2_queries.xml')\ngdp  <- getQuery(prj, 'GDP by region')   # add this query from Main_queries.xml\nhead(gdp)",
    "explain": "Not run against a live database. 'GDP by region' is a standard ModelInterface query; copy it from output/queries/Main_queries.xml into your query file."}],
 "takeaways": ["Population and labour productivity are inputs, usually taken from an SSP storyline",
               "GDP per person drives demand for buildings, transport, industry, food and water",
               "The Kaya factors multiply, so their ratios multiply: never add percentages",
               "GCAM runs 32 regions in 5-year steps from a 2021 base year to 2100",
               "The macro module (KLEM, KLEAM from v9.0) can let energy and policy change GDP"],
 "quiz": [
   {"q": "In standard GCAM runs, regional population is…", "options": ["solved by the model each period", "an exogenous input, usually from an SSP", "calculated from food supply", "fixed at 2021 levels"], "answer": 1, "explain": "Population is an assumption read from the SSP database, not a model result."},
   {"q": "Population ×1.2, income per person ×1.5, energy per $ ×0.7, CO₂ per energy ×0.8. CO₂ changes by a factor of…", "options": ["1.20", "0.80", "1.008", "4.2"], "answer": 2, "explain": "Multiply the ratios: 1.2 × 1.5 × 0.7 × 0.8 = 1.008."},
   {"q": "Which equation form does GCAM use for industry and transport service growth?", "options": ["Demand grows with income ratio to the power α and price ratio to the power β", "Demand is fixed per person", "Demand follows a linear trend in time", "Demand is chosen by optimisation over the century"], "answer": 0, "explain": "D_t = D_t−1 (Y ratio)^α (P ratio)^β (N ratio), from the energy demand page."},
   {"q": "What does the macro module (KLEM/KLEAM) add?", "options": ["More regions", "A way for energy and policy to change GDP", "A detailed transport model", "A climate model"], "answer": 1, "explain": "In open-GDP mode energy costs and efficiency feed back into GDP and consumption."}],
 "glossary": [
   {"term": "Exogenous", "def": "Decided outside the model and fed in as an assumption, such as population."},
   {"term": "Endogenous", "def": "Calculated by the model itself, such as energy prices."},
   {"term": "Labour productivity", "def": "Output per worker; its growth rate is a key GDP assumption."},
   {"term": "Income elasticity", "def": "The % change in demand for a 1% change in income per person."},
   {"term": "KLEAM", "def": "GCAM's v9.0 macro module: capital, labour, energy, agriculture and materials."}],
 "resources": [
   {"title": "GCAM documentation: Economy", "url": D("economy.html"), "why": "Inputs, the macro module and how GDP is built."},
   {"title": "GCAM documentation: Shared Socioeconomic Pathways", "url": D("ssp.html"), "why": "How each SSP is implemented, with 2100 population and income."},
   {"title": "GCAM documentation: Economy inputs", "url": D("inputs_economy.html"), "why": "The raw data files behind population and GDP."},
   R_RGCAM],
 "downloads": [HANDBOOK, KIT, deck("Week03-Energy-primer.pdf", "Week 3 slides: Energy primer and Kaya (PDF)"), deck("Week06-The-scenario-framework.pdf", "Week 6 slides: Scenario framework (PDF)")]})

# ---------------------------------------------------------------- 2.2
mods.append({
 "id": "2.2", "go": 2, "slug": "markets-and-solving", "title": "Markets, equilibrium and solving", "minutes": 45, "tag": "Solver",
 "systems": ["economy", "energy", "land", "water"],
 "summary": "GCAM is a giant auction: in each 5-year period it searches for the prices that make supply equal demand in every market at once. See how one market clears, then many linked markets.",
 "outcomes": ["You can define market equilibrium and excess demand",
              "You can solve one market by hand and with a root finder",
              "You can explain how GCAM's Broyden solver finds prices for hundreds of markets",
              "You can say why GCAM is recursive-dynamic, not an optimisation"],
 "narration_en": ("Imagine an auction hall that never sleeps. In every five-year period GCAM calls out prices for oil, electricity, crops, land and water. "
   "Producers say how much they would supply at those prices, consumers say how much they would buy, and the auctioneer raises prices where buyers want more than sellers offer, "
   "and lowers them where there is too much. When every market balances at the same time, the period is solved and the model moves on. "
   "That balance is called equilibrium, and the gap between demand and supply is called excess demand. "
   "In this module you first clear one market by hand, finding the price where demand equals supply. Then you solve three linked markets together, "
   "because a change in the oil price shifts demand for electricity and biomass too. GCAM does this for a few hundred markets at once, "
   "using Broyden's method, a clever cousin of Newton's method that works in log prices. "
   "You will also see why GCAM is recursive-dynamic: it solves one period at a time, without knowing the future."),
 "narration_ar": ("تخيّل قاعة مزاد لا تنام أبدًا. في كل فترة من خمس سنوات يعلن نموذج GCAM أسعارًا للنفط والكهرباء والمحاصيل والأرض والماء. "
   "يقول المنتجون كم سيعرضون عند هذه الأسعار، ويقول المستهلكون كم سيشترون، فيرفع الدلّال الأسعار حيث يريد المشترون أكثر مما يعرضه البائعون، "
   "ويخفضها حيث يوجد فائض. وعندما تتوازن كل الأسواق في الوقت نفسه تُحَلّ الفترة وينتقل النموذج إلى ما بعدها. "
   "يسمى هذا التوازن بالتوازن السوقي، وتسمى الفجوة بين الطلب والعرض بفائض الطلب. "
   "في هذه الوحدة ستوازن أولًا سوقًا واحدة يدويًا، فتجد السعر الذي يتساوى عنده الطلب مع العرض. ثم تحل ثلاث أسواق مترابطة معًا، "
   "لأن تغيّر سعر النفط يغيّر الطلب على الكهرباء والكتلة الحيوية أيضًا. ويفعل النموذج ذلك لبضع مئات من الأسواق في آن واحد، "
   "مستخدمًا طريقة برويدن، وهي قريبة ذكية من طريقة نيوتن تعمل على لوغاريتمات الأسعار. "
   "وسترى أيضًا لماذا يُعدّ النموذج ديناميكيًا تتابعيًا: فهو يحل فترة واحدة في كل مرة دون أن يعرف المستقبل."),
 "diagram": {
   "title": "One period of the GCAM auction", "caption": "Each period the solver adjusts prices until excess demand is near zero in every market, then the model steps 5 years ahead.",
   "nodes": [
     node("guess", "Trial prices", "log prices, all markets", "nw", "economy", "The solver starts from the previous period's prices (plus a preconditioner that nudges bad starting guesses, for example resource turn-on prices) (solver.html)."),
     node("sup", "Supply bids", "energy, crops, water", "ne", "energy", "Every supply sector reports how much it would produce at the trial prices: resource curves, power plants, farms, water sources."),
     node("dem", "Demand bids", "buildings, transport, food", "e", "land", "Every demand sector reports how much it would buy at those prices."),
     node("ed", "Excess demand F(p)", "demand − supply, scaled", "c", "economy", "F(p) = D(p) − S(p) for each market. GCAM scales excess demand so markets of different sizes are comparable, and works in log prices.", w=200),
     node("broy", "Broyden update", "B·δx = −F(x)", "sw", "economy", "Broyden's method solves B·δx = −F(x) with B a secant approximation of the Jacobian, cutting the step back if it makes things worse. Bisection helps near singular regions (solver.html)."),
     node("ok", "All markets clear?", "tolerance 0.001 (example)", "s", "policy", "Solved when relative excess demand is below solution-tolerance (example 0.001) with a floor (0.0001). Otherwise iterate, up to max-model-calcs (example 2500)."),
     node("next", "Next period", "+5 years, no foresight", "se", "climate", "Recursive dynamics: the solved period is fixed, emissions go to Hector, and the model moves to the next 5-year step using what it knows now (overview.html).")],
   "edges": [edge("guess", "sup", "prices", "economy"), edge("guess", "dem", "", "economy"), edge("sup", "ed", "quantities"), edge("dem", "ed", "quantities"),
             edge("ed", "broy", "residuals", "economy"), edge("broy", "guess", "new prices", "economy"), edge("ed", "ok", "check"), edge("ok", "next", "yes")],
   "tour": [
     {"focus": ["guess"], "edges": [], "text": "The auctioneer calls out a trial price for every market: energy, crops, land, water, and any policy markets."},
     {"focus": ["sup", "dem"], "edges": [["guess", "sup"], ["guess", "dem"]], "text": "Every supplier and every buyer answers: this is how much I would sell, or buy, at those prices."},
     {"focus": ["ed"], "edges": [["sup", "ed"], ["dem", "ed"]], "text": "The gap demand minus supply, market by market, is the excess-demand vector F(p). The target is F(p) ≈ 0 everywhere."},
     {"focus": ["broy"], "edges": [["ed", "broy"], ["broy", "guess"]], "text": "Broyden's method uses the gaps to move all prices together, learning how markets react to each other as it goes."},
     {"focus": ["ok"], "edges": [["ed", "ok"]], "text": "When every gap is within tolerance, the period is solved. If not, iterate again."},
     {"focus": ["next"], "edges": [["ok", "next"]], "text": "Then step 5 years ahead. Decisions already made stay made: GCAM does not see the future."}]},
 "components": {"caption": "Words for the auction", "rows": [
     {"name": "Market", "purpose": "One good in one place, e.g. crude oil (global) or corn in the USA", "analogy": "One stall in the auction hall"},
     {"name": "Price", "purpose": "The unknown the solver adjusts", "analogy": "The number the auctioneer shouts"},
     {"name": "Excess demand", "purpose": "Demand minus supply at a trial price", "analogy": "How many bidders are left unhappy"},
     {"name": "Solver", "purpose": "Algorithm that moves prices toward F(p) = 0", "analogy": "The auctioneer's strategy"},
     {"name": "Tolerance", "purpose": "How small the gaps must be to count as solved", "analogy": "Close enough to bang the hammer"},
     {"name": "Recursive dynamics", "purpose": "Solve period by period, no foresight", "analogy": "Each auction day ignores tomorrow's prices"}]},
 "sections": [
   {"heading": "What this component represents", "html": "<p>\"GCAM operates by determining a set of prices that ensure supply is equal to demand for all time steps\" (" + cite("marketplace.html") + "). Each <b>market</b> is a good in a place: energy carriers in EJ per year, crops and land, and water by basin. Supply and demand sectors are representative agents that submit bids; the solver adjusts prices until all markets clear.</p><p>This is <b>partial equilibrium</b>: the energy, land and water markets are solved in detail, while the wider economy enters through GDP.</p>"},
   {"heading": "One market by hand", "html": "<p>Take the toy electricity market from week 4: demand 1000 − 4p and supply 6(p − 0.9·tax). Excess demand is</p><div class=\"eq\">F(p) = (1000 − 4p) − 6(p − 0.9·tax)</div><p>With no tax, set F = 0: 1000 − 4p = 6p, so 10p = 1000 and <b>p = 100</b>, quantity 600. With a $50 tax: 1000 − 4p = 6p − 270, so 10p = 1270 and <b>p = 127</b>, quantity 492. A root finder (bisection, Brent) finds the same answer by searching for the sign change of F.</p>"},
   {"heading": "Many linked markets at once", "html": "<p>Real markets are linked: a carbon price raises the cost of burning oil, which shifts demand toward electricity and biomass, which changes their prices, which feeds back on oil. So all prices must be found <i>together</i>. The kit's three-market toy (oil, electricity, biomass) needs a vector root finder. With a $50 carbon price it settles at oil 9.04, electricity 31.60 and biomass 5.25, with every excess demand below 2×10<sup>−10</sup>.</p><div class=\"eq\">find p such that F<sub>m</sub>(p<sub>1</sub>, …, p<sub>M</sub>) = 0 for every market m</div>"},
   {"heading": "How GCAM's solver works", "html": "<p>GCAM works in <b>log prices</b> with excess demand scaled to a common size. Its main method is <b>Broyden's method</b>: it solves B·δx = −F(x), where B is a cheap secant approximation of the Jacobian (how every market's gap reacts to every price), and shortens the step if a step makes ‖F‖ worse. Bisection moves prices out of flat or singular regions, and a preconditioner fixes bad starting guesses (" + cite("solver.html") + ").</p><p>The Jacobian covers \"usually a few hundred\" solved markets. Example settings from the sample configuration: solution-tolerance 0.001, solution-floor 0.0001, max-model-calcs 2500 (the defaults themselves are not stated in the docs).</p>"},
   {"heading": "Recursive dynamics: no crystal ball", "html": "<p>GCAM is <b>dynamic recursive</b>: agents decide with what they know in the current period, then the model steps forward. It is not an intertemporal optimisation, so it can build a coal plant in 2030 that a policy in 2040 makes regrettable (" + cite("overview.html") + "). Optimisation models such as MESSAGEix instead choose the whole century at once with perfect foresight (Go 2.8 compares the two).</p>"}],
 "callouts": [
   {"after": 1, "kind": "model", "title": "A useful mental model", "html": "<p>Picture a thermostat for each market. Too much demand: the price heats up. Too much supply: it cools down. The solver turns all the thermostats at once, knowing that warming one room changes the others.</p>"},
   {"after": 3, "kind": "gcam", "title": "In GCAM", "html": "<p>The solver is configured in <code>input/solution/cal_solver_config.xml</code> (pointed to by <code>solver_config</code> in <code>configuration.xml</code>). Check <code>exe/logs/main_log.txt</code>: a good run ends with \"Model exiting successfully\" and lists any unsolved markets. Query <b>prices of all markets</b> to see the solved prices (energy in 1975$/GJ) (" + cite("user-guide.html") + ", " + cite("outputs_prices.html") + ").</p>"},
   {"after": 4, "kind": "trap", "title": "\"The model failed, so the result is still usable\"", "html": "<p>An unsolved period means some market did not clear: its prices and quantities are not an equilibrium. Never report results from a run with unsolved markets; fix tolerances, starting prices or the input that caused it.</p>"}],
 "explorer": {"widget": "solver", "intro": "Watch a solver iterate prices for two linked markets until both gaps close.", "predict": "If the two markets are strongly linked, will the solver need more or fewer iterations than if they were independent?"},
 "code": [
   {"title": "One market, then three linked markets", "lang": "python", "file": "labs/go2/m22_markets.py", "runnable": True,
    "explain": "Part A solves the week 4 market with Brent's method. Part B solves oil, electricity and biomass together with Broyden's method in log prices. Try: change the carbon price to 100 and predict which price falls and which rises.",
    "expected": "One market, tax  0: price  100.0, quantity  600.0\nOne market, tax 50: price  127.0, quantity  492.0\nThree markets, carbon 50: prices oil 9.04, electricity 31.60, biomass 5.25; converged=True"},
   {"title": "The same model in R (with a hand-written Newton solver)", "lang": "r", "file": "labs/go2/m22_markets.R", "runnable": False, "explain": "Base R: uniroot for one market, then a small Newton iteration in log prices. Converges in 5 iterations."}],
 "takeaways": ["Equilibrium means supply equals demand in every market at the same time",
               "Excess demand F(p) is the gap the solver drives to zero",
               "Linked markets must be solved together; GCAM uses Broyden's method in log prices",
               "A solved period needs every market within tolerance; check the log",
               "GCAM solves one 5-year period at a time with no foresight"],
 "quiz": [
   {"q": "Demand 1000 − 4p, supply 6p. The equilibrium price is…", "options": ["60", "100", "127", "167"], "answer": 1, "explain": "1000 − 4p = 6p gives p = 100."},
   {"q": "GCAM's primary solution method is…", "options": ["Linear programming", "Broyden's method", "Gradient descent", "Monte Carlo search"], "answer": 1, "explain": "Broyden's quasi-Newton method, helped by bisection and a preconditioner (solver.html)."},
   {"q": "Why must linked markets be solved together?", "options": ["Because they share a currency", "Because one price changes demand or supply in other markets", "Because GCAM has one market only", "They don't: they can be solved one by one exactly"], "answer": 1, "explain": "Cross-effects (oil vs electricity vs biomass) mean each market's balance depends on the other prices."},
   {"q": "\"Recursive-dynamic\" means GCAM…", "options": ["optimises the whole century at once", "solves each period with current information, then moves on", "repeats the same year", "uses random prices"], "answer": 1, "explain": "No foresight: each period is solved and then fixed."},
   {"q": "A run ends with unsolved markets in 2050. You should…", "options": ["Report the results with a footnote", "Ignore 2050 only", "Diagnose and fix before using any results", "Increase the number of regions"], "answer": 2, "explain": "Unsolved markets are not an equilibrium; downstream periods are affected too."}],
 "glossary": [
   {"term": "Equilibrium", "def": "A set of prices at which supply equals demand in every market."},
   {"term": "Excess demand", "def": "Demand minus supply at a given price; zero at equilibrium."},
   {"term": "Broyden's method", "def": "A quasi-Newton root finder that updates an approximate Jacobian cheaply each step."},
   {"term": "Jacobian", "def": "The table of how each market's excess demand changes when each price changes."},
   {"term": "Recursive dynamics", "def": "Solving one period at a time using only current information."},
   {"term": "Partial equilibrium", "def": "Detailed markets for some sectors, with the rest of the economy taken as given."}],
 "resources": [
   {"title": "GCAM documentation: Marketplace", "url": D("marketplace.html"), "why": "How markets are defined and cleared."},
   {"title": "GCAM documentation: Solution and computation", "url": D("solver.html"), "why": "Broyden, bisection, preconditioner and tolerances."},
   {"title": "GCAM documentation: Model overview", "url": D("overview.html"), "why": "Recursive dynamics and the scope of the model."},
   {"title": "gcamwrapper", "url": "https://github.com/JGCRI/gcamwrapper", "why": "Instructor demo: step a compiled GCAM and inspect prices and the Jacobian."}],
 "downloads": [HANDBOOK, KIT, deck("Week04-Economics-primer.pdf", "Week 4 slides: Economics primer (PDF)"), deck("Week07-Inside-GCAM.pdf", "Week 7 slides: Inside GCAM (PDF)")]})

# ---------------------------------------------------------------- 2.3
mods.append({
 "id": "2.3", "go": 2, "slug": "choice-the-logit", "title": "Choice: the logit", "minutes": 40, "tag": "Choice",
 "systems": ["energy", "land", "economy"],
 "summary": "GCAM never gives the whole market to the cheapest option. A logit shares it out by relative cost, with share weights calibrated to history. Learn the formula, the exponent and nesting.",
 "outcomes": ["You can compute logit shares for three technologies by hand",
              "You can explain what the logit exponent and share weights do",
              "You can tell the relative-cost and absolute-cost logit apart",
              "You can describe GCAM's nested choice from sector to technology"],
 "narration_en": ("If coal costs sixty dollars, gas seventy and solar eighty, a simple model would build only coal. Real investors do not behave like that. "
   "Sites differ, preferences differ, costs vary from place to place, so cheaper options win more of the market but not all of it. "
   "GCAM captures this with the logit, a formula that turns costs into market shares. Each option's cost is raised to a negative power, called the logit exponent, "
   "and divided by the sum over all options. A small exponent spreads the market widely. A large exponent behaves almost like winner takes all. "
   "Share weights are extra numbers calibrated so that the base year reproduces the shares we actually observe; they carry everything the costs leave out. "
   "Choices are also nested: electricity first chooses between fuels, then between technologies within each fuel, then between cooling systems. "
   "In this module you will compute shares by hand, calibrate share weights, and build a two-level nest in code."),
 "narration_ar": ("إذا كانت تكلفة الفحم ستين دولارًا والغاز سبعين والطاقة الشمسية ثمانين، فإن نموذجًا بسيطًا سيبني الفحم فقط. لكن المستثمرين الحقيقيين لا يتصرفون هكذا. "
   "فالمواقع تختلف والتفضيلات تختلف والتكاليف تتفاوت من مكان لآخر، لذلك يفوز الخيار الأرخص بحصة أكبر من السوق لكن ليس بكاملها. "
   "يلتقط نموذج GCAM ذلك بدالة اللوجيت، وهي صيغة تحوّل التكاليف إلى حصص سوقية. تُرفع تكلفة كل خيار إلى قوة سالبة تسمى أُس اللوجيت، "
   "وتُقسم على مجموع كل الخيارات. الأُس الصغير يوزع السوق توزيعًا واسعًا، والأُس الكبير يقترب من أن يأخذ الفائز كل شيء. "
   "أوزان الحصص أرقام إضافية تُعايَر بحيث تعيد سنة الأساس إنتاج الحصص المرصودة فعلًا، وهي تحمل كل ما لا تعبّر عنه التكاليف. "
   "والاختيارات متداخلة أيضًا: فالكهرباء تختار أولًا بين أنواع الوقود، ثم بين التقنيات داخل كل وقود، ثم بين أنظمة التبريد. "
   "في هذه الوحدة ستحسب الحصص يدويًا، وتعاير أوزان الحصص، وتبني تداخلًا من مستويين بالشيفرة."),
 "diagram": {
   "title": "Nested choice for electricity", "caption": "Each level of the tree has its own logit. Costs flow up the tree; shares flow down it.",
   "nodes": [
     node("elec", "Electricity sector", "demand to be met", "n", "energy", "The sector's output must meet demand. It splits its market among subsectors (fuels) with a logit; electricity subsector exponent in the reference example is −3 (choice.html).", w=200),
     node("coal", "Coal subsector", "logit among plants", "nw", "energy", "Within coal, technologies compete with an aggressive exponent (−10 in the reference example): small cost differences swing shares a lot."),
     node("gas", "Gas subsector", "", "c", "energy", "Gas plants (combined cycle, turbines, with or without CCS) share the gas subsector by their own logit."),
     node("sol", "Solar subsector", "PV, CSP, rooftop", "ne", "energy", "Solar technologies; their effective cost includes a value-factor adjustment that rises with market share (Go 2.4)."),
     node("pc", "Pulverised coal", "cost incl. fuel + carbon", "w", "energy", "A technology: cost = non-energy cost + fuel cost + emissions cost (en_technologies.html)."),
     node("ccs", "Coal with CCS", "", (130, 400), "energy", "Higher non-energy cost, but much lower emissions cost under a carbon price."),
     node("cool", "Cooling system", "once-through, recirculating…", (450, 440), "water", "For thermal plants the last level chooses one of up to five cooling systems, by a cost logit that includes water prices (demand_water.html).", w=210),
     node("sw", "Share weights", "calibrated to 2021", "e", "data", "Share weights scale each option so base-year shares match history; they also phase in new technologies (choice.html).")],
   "edges": [edge("elec", "coal", "share", "energy"), edge("elec", "gas", "share", "energy"), edge("elec", "sol", "share", "energy"),
             edge("coal", "pc", "", "energy"), edge("coal", "ccs", "", "energy"), edge("gas", "cool", "", "water"), edge("sw", "sol", "calibrates", "neutral")],
   "tour": [
     {"focus": ["elec"], "edges": [], "text": "Electricity demand must be met. The sector does not pick one fuel: it shares the market."},
     {"focus": ["coal", "gas", "sol"], "edges": [["elec", "coal"], ["elec", "gas"], ["elec", "sol"]], "text": "First level: fuels compete by cost with a moderate exponent (−3 in the reference example)."},
     {"focus": ["pc", "ccs"], "edges": [["coal", "pc"], ["coal", "ccs"]], "text": "Inside coal, technologies compete with a steep exponent (−10): close substitutes switch quickly."},
     {"focus": ["cool"], "edges": [["gas", "cool"]], "text": "Thermal plants then choose a cooling system, linking electricity to water prices."},
     {"focus": ["sw"], "edges": [["sw", "sol"]], "text": "Share weights calibrate each branch to 2021 data and phase new options in."}]},
 "components": {"caption": "Pieces of a logit choice", "rows": [
     {"name": "Cost (c)", "purpose": "Levelised cost of each option, incl. fuel and carbon", "analogy": "The price tag on each menu item"},
     {"name": "Logit exponent (γ)", "purpose": "How strongly shares react to cost differences", "analogy": "How price-sensitive the diners are"},
     {"name": "Share weight (α)", "purpose": "Calibrated preference not captured by cost", "analogy": "The house favourite everyone orders anyway"},
     {"name": "Share (s)", "purpose": "Fraction of the market each option wins", "analogy": "How many plates of each dish are served"},
     {"name": "Nest", "purpose": "A level of the choice tree with its own logit", "analogy": "Choose a cuisine first, then a dish"}]},
 "sections": [
   {"heading": "Why not cheapest-takes-all?", "html": "<p>A model that always picks the single cheapest technology flips its whole mix when costs cross, which real markets never do. Costs vary across sites and investors; some preferences are unmeasured. The <b>logit</b> turns costs into smooth market shares: cheaper wins more, never everything (" + cite("choice.html") + ").</p>"},
   {"heading": "The relative-cost logit", "html": "<div class=\"eq\">s<sub>i</sub> = α<sub>i</sub> · c<sub>i</sub><sup>γ</sup> / Σ<sub>j</sub> α<sub>j</sub> · c<sub>j</sub><sup>γ</sup>,  γ &lt; 0</div><p>With equal share weights and γ = −4, coal $60, gas $70, solar $80: 60<sup>−4</sup> = 7.72×10<sup>−8</sup>, 70<sup>−4</sup> = 4.16×10<sup>−8</sup>, 80<sup>−4</sup> = 2.44×10<sup>−8</sup>. The sum is 14.32×10<sup>−8</sup>, so the shares are <b>54%, 29% and 17%</b>. With γ = −1 they are 38/33/29%; with γ = −10, 79/17/4%.</p>"},
   {"heading": "The absolute-cost logit", "html": "<div class=\"eq\">s<sub>i</sub> = α<sub>i</sub> · exp(β · c<sub>i</sub>) / Σ<sub>j</sub> α<sub>j</sub> · exp(β · c<sub>j</sub>)</div><p>Here the share ratio depends on the cost <i>difference</i> rather than the ratio. GCAM users always enter a logit exponent; for the absolute form GCAM derives β from it. The absolute form behaves well when costs can be near zero or negative, and GCAM uses it in places such as direct air capture and the passenger transport nests (" + cite("choice.html") + ").</p>"},
   {"heading": "Share weights and calibration", "html": "<p>Share weights are set so that, at base-year costs, the logit reproduces the observed 2021 shares. If observed shares are 30/50/20% at costs 60/70/80 and γ = −4, then α ∝ share / c<sup>γ</sup>, giving weights <b>1 : 3.088 : 2.107</b> (normalised to coal). They also phase in new technologies: low in their first year, rising toward a neutral value. Future share weights are <i>assumptions</i>, so treat them as a scenario lever, not a fact.</p>"},
   {"heading": "Nesting", "html": "<p>Choice in GCAM is layered: sector → subsector → technology → (for thermal power) cooling system, each with its own logit (" + cite("details_energy.html") + "). The reference example uses γ = −3 between electricity subsectors and γ = −10 among coal technologies. In the kit's two-level nest (fossil nest with γ = −6 inside, then fossil vs solar with γ = −3) the result is coal 48.2%, gas 19.1%, solar 32.6%. Land and trade use logits too (Go 2.6).</p>"}],
 "callouts": [
   {"after": 1, "kind": "try", "title": "Try it", "html": "<p>Coal $60 and gas $70, γ = −2, equal weights. Coal's share? 60<sup>−2</sup> = 2.78×10<sup>−4</sup>, 70<sup>−2</sup> = 2.04×10<sup>−4</sup>, so coal = 2.78 / 4.82 = <b>58%</b>.</p>"},
   {"after": 3, "kind": "gcam", "title": "In GCAM", "html": "<p>Logit exponents are in gcamdata assumption files <code>A21.subsector_logit.csv</code> … <code>A26.subsector_logit.csv</code>; share-weight interpolation rules in <code>A21.subsector_interp.csv</code> and similar (" + cite("inputs_supply.html") + "). In XML they appear as <code>&lt;logit-exponent&gt;</code> and <code>&lt;share-weight&gt;</code> under each subsector and technology.</p>"},
   {"after": 4, "kind": "trap", "title": "\"A share weight is a subsidy\"", "html": "<p>No. A share weight is a calibrated preference multiplier with no money attached. Changing future share weights changes results without changing any cost, so state those assumptions openly.</p>"}],
 "explorer": {"widget": "logit", "intro": "Set three costs and the logit exponent, and watch the market shares.", "predict": "Coal $60, gas $70, solar $80. Roughly what exponent gives coal 90% of the market?"},
 "code": [
   {"title": "Relative logit, calibration and a two-level nest", "lang": "python", "file": "labs/go2/m23_logit.py", "runnable": True,
    "explain": "Computes shares for three exponents, calibrates share weights to observed shares and builds a nest. Try: make solar $55 and predict whether it becomes the largest share at γ = −4.",
    "expected": "relative logit, exponent  -4:  {'coal': 0.539, 'gas': 0.291, 'solar': 0.17}\ncalibrated share weights: {'coal': 1.0, 'gas': 3.088, 'solar': 2.107}\nnested: fossil nest 0.674 (coal 0.482, gas 0.191), solar 0.326"},
   {"title": "The same in R", "lang": "r", "file": "labs/go2/m23_logit.R", "runnable": False, "explain": "Identical numbers in base R."}],
 "takeaways": ["The logit turns costs into smooth shares: cheaper wins more, never everything",
               "The exponent sets how sensitive shares are to cost differences",
               "Share weights calibrate the base year and phase in new options; future values are assumptions",
               "GCAM uses relative-cost and absolute-cost logits, nested from sector to technology",
               "Example exponents: −3 between electricity fuels, −10 among coal technologies"],
 "quiz": [
   {"q": "Costs 60, 70, 80; γ = −4; equal weights. Coal's share is about…", "options": ["33%", "54%", "79%", "100%"], "answer": 1, "explain": "7.72 / 14.32 = 0.539."},
   {"q": "Making the exponent more negative (−4 to −10) makes shares…", "options": ["more even", "more concentrated on the cheapest", "unchanged", "random"], "answer": 1, "explain": "Steeper exponents amplify cost differences."},
   {"q": "Share weights are…", "options": ["subsidies paid to technologies", "calibrated multipliers that reproduce base-year shares", "the same as costs", "always equal to 1"], "answer": 1, "explain": "They absorb unmeasured preferences and phase new options in."},
   {"q": "In the absolute-cost logit, shares depend on…", "options": ["cost ratios", "cost differences", "only share weights", "only the cheapest cost"], "answer": 1, "explain": "exp(β c) makes share ratios depend on c_i − c_j."},
   {"q": "Which order matches GCAM's electricity nest?", "options": ["technology → subsector → sector", "sector → subsector → technology → cooling", "cooling → sector → subsector", "one flat choice"], "answer": 1, "explain": "Sector, then fuel subsector, then technology, then cooling system."}],
 "glossary": [
   {"term": "Logit", "def": "A formula that turns costs (or profits) into market shares."},
   {"term": "Logit exponent", "def": "The parameter that sets how strongly shares respond to cost differences."},
   {"term": "Share weight", "def": "A calibrated multiplier on each option's attractiveness, set to match base-year data."},
   {"term": "Nest", "def": "One level of a choice tree, with its own logit."},
   {"term": "Calibration", "def": "Setting parameters so the model reproduces observed base-year data."}],
 "resources": [
   {"title": "GCAM documentation: Economic choice", "url": D("choice.html"), "why": "Both logit forms, share weights and example exponents."},
   {"title": "GCAM documentation: Energy system details", "url": D("details_energy.html"), "why": "The nesting of the electricity sector."},
   {"title": "GCAM documentation: Supply inputs", "url": D("inputs_supply.html"), "why": "Where exponents and interpolation rules live in gcamdata."}],
 "downloads": [HANDBOOK, KIT, deck("Week07-Inside-GCAM.pdf", "Week 7 slides: Inside GCAM (PDF)")]})

# ---------------------------------------------------------------- 2.4
mods.append({
 "id": "2.4", "go": 2, "slug": "energy-supply", "title": "Energy supply", "minutes": 50, "tag": "Supply",
 "systems": ["energy", "economy", "climate"],
 "summary": "Where energy comes from in GCAM: graded fossil resources, renewable supply curves, power plants with levelised costs, and the value-factor rule that makes wind and solar dearer as they grow.",
 "outcomes": ["You can compute a levelised cost of electricity with a carbon price",
              "You can explain graded resource supply curves",
              "You can describe the value-factor method for wind and solar (v7.3 onward)",
              "You can name where GCAM's technology cost assumptions live"],
 "narration_en": ("Energy supply in GCAM starts in the ground and in the sky. Coal, oil, gas and uranium are depletable resources described by graded supply curves: "
   "the cheap grades are used first, and the price climbs as more is extracted. Wind and solar are flows rather than stocks, described by renewable supply curves. "
   "These primary resources feed conversion sectors such as power plants, refineries and hydrogen production. "
   "Each technology has a cost built from three parts: a non-energy cost that covers building and running the plant, a fuel cost, and an emissions cost under any carbon price. "
   "In this module you will compute a levelised cost of electricity for a gas plant and a solar farm, and see the gas cost rise by about eighteen dollars for every fifty dollars of carbon price. "
   "You will also meet the value factor. As wind and solar take a larger share of the grid, each extra unit is worth less, so GCAM divides their cost by a value factor that falls with market share. "
   "That simple rule keeps renewables from taking over unrealistically fast."),
 "narration_ar": ("يبدأ إمداد الطاقة في نموذج GCAM من باطن الأرض ومن السماء. الفحم والنفط والغاز واليورانيوم موارد ناضبة تصفها منحنيات عرض متدرجة: "
   "تُستخدم الدرجات الرخيصة أولًا، ويرتفع السعر كلما استُخرج المزيد. أما الرياح والشمس فهي تدفقات لا مخزونات، وتصفها منحنيات عرض للطاقة المتجددة. "
   "تغذي هذه الموارد الأولية قطاعات التحويل مثل محطات الكهرباء والمصافي وإنتاج الهيدروجين. "
   "ولكل تقنية تكلفة من ثلاثة أجزاء: تكلفة غير طاقية تغطي بناء المحطة وتشغيلها، وتكلفة الوقود، وتكلفة الانبعاثات في ظل أي سعر للكربون. "
   "في هذه الوحدة ستحسب التكلفة المستوية للكهرباء لمحطة غاز ولمزرعة شمسية، وترى تكلفة الغاز ترتفع بنحو ثمانية عشر دولارًا لكل خمسين دولارًا من سعر الكربون. "
   "وستتعرف أيضًا على معامل القيمة. فكلما أخذت الرياح والشمس حصة أكبر من الشبكة قلّت قيمة كل وحدة إضافية، لذلك يقسم النموذج تكلفتهما على معامل قيمة ينخفض مع الحصة السوقية. "
   "هذه القاعدة البسيطة تمنع الطاقة المتجددة من السيطرة بسرعة غير واقعية."),
 "diagram": {
   "title": "From resources to delivered electricity", "caption": "Resources feed conversion technologies; each technology's cost includes fuel and carbon, and wind/solar get a value-factor adjustment.",
   "nodes": [
     node("fos", "Fossil resources", "graded supply curves", "nw", "energy", "Coal, oil, gas, uranium: graded curves inside a resource/reserve model; cheap grades first, price rises with use (supply_energy.html). Files A11.fos_curves.csv, A12.U_curves.csv."),
     node("ren", "Renewable resources", "wind, solar, geothermal, hydro", "w", "energy", "Annual flows with supply curves Q = max·P^b/(Mid^b + P^b). Hydropower is exogenous fixed output; utility solar is nearly unlimited at low price (supply_energy.html)."),
     node("bio", "Bioenergy", "from land (Go 2.6)", "sw", "land", "Purpose-grown energy crops, residues and waste come from the land module and compete with food for land."),
     node("plant", "Power plants", "cost = non-energy + fuel + carbon", "c", "energy", "Non-energy cost is levelised: overnight capital × capital recovery factor ÷ capacity factor + O&M. Costs from NREL ATB, updated in v8.8 (en_technologies.html).", w=220),
     node("vf", "Value factor", "PLCOE = LCOE / VF", "ne", "energy", "Since v7.3 wind and solar cost is divided by a value factor that falls linearly with market share, e.g. PV intercept 0.972, slope −1.443 (CMP 394)."),
     node("ccs", "Carbon capture", "remove-fraction → storage", "e", "climate", "CCS is a remove-fraction on a technology's emissions, sent to a storage market (en_technologies.html)."),
     node("grid", "Electricity market", "sector logit, price", "se", "economy", "Technologies share the electricity market by nested logit; the solved price feeds buildings, industry and transport."),
     node("cp", "Carbon price", "$/t added to cost", "s", "policy", "Adds emission factor × carbon price to each technology's cost.")],
   "edges": [edge("fos", "plant", "fuel", "energy"), edge("ren", "plant", "resource", "energy"), edge("bio", "plant", "biomass", "land"),
             edge("plant", "grid", "output", "energy"), edge("vf", "plant", "adjusts VRE cost", "energy"), edge("plant", "ccs", "captured CO₂", "climate"), edge("cp", "plant", "+ ef × price", "policy")],
   "tour": [
     {"focus": ["fos"], "edges": [["fos", "plant"]], "text": "Fossil fuels come from graded curves: the more you extract, the higher the cost of the next grade."},
     {"focus": ["ren", "bio"], "edges": [["ren", "plant"], ["bio", "plant"]], "text": "Renewables are flows with their own curves; bioenergy arrives from the land module."},
     {"focus": ["plant"], "edges": [], "text": "Each plant's cost = non-energy (capital, O&M) + fuel ÷ efficiency + emissions cost."},
     {"focus": ["cp"], "edges": [["cp", "plant"]], "text": "A carbon price adds emission factor × price: gas rises ~$18/MWh per $50/t in the kit example."},
     {"focus": ["vf"], "edges": [["vf", "plant"]], "text": "Wind and solar cost is divided by a value factor that shrinks as their share grows, slowing their growth."},
     {"focus": ["ccs", "grid"], "edges": [["plant", "ccs"], ["plant", "grid"]], "text": "CCS sends captured CO₂ to storage; technologies share the electricity market by logit."}]},
 "components": {"caption": "Supply-side building blocks", "rows": [
     {"name": "Depletable resource", "purpose": "Fossil and uranium stocks on graded cost curves", "analogy": "A fruit tree: the low branches first"},
     {"name": "Renewable resource", "purpose": "Annual flows (wind, sun, geothermal) with supply curves", "analogy": "Rain into a barrel each year"},
     {"name": "Technology", "purpose": "Converts inputs to outputs at a cost and efficiency", "analogy": "A machine in the factory"},
     {"name": "Levelised cost", "purpose": "All costs per unit of output over the plant's life", "analogy": "Price per slice, not per oven"},
     {"name": "Value factor", "purpose": "Lowers the value of variable renewables as their share grows", "analogy": "The 10th umbrella seller at the same corner"},
     {"name": "Vintage", "purpose": "Plants built in a period that keep running for their lifetime", "analogy": "Cars on the road, not just cars in the showroom"}]},
 "sections": [
   {"heading": "Resources: stocks and flows", "html": "<p>Depletable resources (coal, oil, unconventional oil, gas, uranium) sit on <b>graded supply curves</b>: as the price rises, more of the resource becomes economic. Technical change can lower extraction costs over time (" + cite("supply_energy.html") + "). In the kit's toy curve, cost rises from $3/GJ to $12/GJ across four grades, so the price at 200, 800 and 1400 EJ of cumulative use is <b>3.6, 6.0 and 11.0 $/GJ</b>.</p><p>Renewables are annual flows:</p><div class=\"eq\">Q = Q<sub>max</sub> · P<sup>b</sup> / (P<sub>mid</sub><sup>b</sup> + P<sup>b</sup>)</div><p>where P<sub>mid</sub> is the price at which half the maximum is produced.</p>"},
   {"heading": "Technology cost", "html": "<p>Every technology's cost per unit of output is</p><div class=\"eq\">C = non-energy cost + Σ (input price × input coefficient) + Σ (GHG price × emissions) − secondary output value</div><p>For power plants, non-energy cost is levelised: overnight capital × capital recovery factor ÷ (capacity factor × 8.76) + fixed and variable O&M (" + cite("en_technologies.html") + "). The kit's gas plant (capex $1,000/kW, capacity factor 0.55, fuel $6/GJ, efficiency 55%) costs <b>61.2 $/MWh</b> with no carbon price, <b>79.5</b> at $50/t and <b>97.9</b> at $100/t. The solar farm (capex $900/kW, CF 0.22) costs 45.4 $/MWh at any carbon price. Illustrative numbers.</p>"},
   {"heading": "Wind and solar: the value factor", "html": "<p>Since v7.3 GCAM no longer pairs wind and solar with backup turbines. Instead their levelised cost is divided by a <b>value factor</b> that falls linearly with their market share (CMP 394):</p><div class=\"eq\">PLCOE = LCOE / VF,  VF = intercept + slope × share</div><p>For PV the intercept is 0.972 and the slope −1.443 (then divided by 0.903, the non-VRE average); onshore wind 0.91 and −1.2. The relationships come from ReEDS for the contiguous US and may break down above about 75% VRE. Storage is not modelled explicitly.</p>"},
   {"heading": "Electricity, fuels and hydrogen", "html": "<p>Electricity is nested: fuel subsector → technology → cooling system (up to five types). Refining covers oil, biomass liquids (up to 8 technologies per region, some with CCS), coal-to-liquids and gas-to-liquids. Hydrogen has 10 central and 2 forecourt routes from up to 7 primary sources. CCS is a <code>remove-fraction</code> on emissions sent to a storage market; direct air capture enters with a share weight rising to 1 by 2050 (" + cite("supply_energy.html") + ", " + cite("details_energy.html") + ").</p>"},
   {"heading": "Vintages and retirement", "html": "<p>Plants built in one period keep running: GCAM tracks <b>vintages</b>. Three shutdown rules exist: profit shutdown (output falls as variable cost approaches price), an S-curve lifetime, and exogenous output scalars, such as a 2015 US coal plant at 0.5 in 2021 falling to 0 by 2040 (" + cite("en_technologies.html") + "). This is why the fleet changes more slowly than new investment.</p>"}],
 "callouts": [
   {"after": 1, "kind": "gcam", "title": "In GCAM", "html": "<p>Power plant costs come from NREL ATB files (<code>NREL_ATB_capital.csv</code>, <code>NREL_ATB_OMfixed.csv</code>, <code>NREL_ATB_OMvar.csv</code>); efficiencies, capture rates and retirement in <code>A23.globaltech_*.csv</code> (" + cite("inputs_supply.html") + "). Units: capital-overnight in 1975$/kW, prices in 1975$/GJ. Query <b>elec gen by subsector</b> to see the mix. Plant-specific values are not printed on the doc pages.</p>"},
   {"after": 2, "kind": "model", "title": "A useful mental model", "html": "<p>The first solar farm in a region sells power at midday when it is valuable. The hundredth floods the same hours and earns less. The value factor charges that crowding as a higher effective cost.</p>"},
   {"after": 4, "kind": "trap", "title": "\"GCAM learns: costs fall as capacity grows\"", "html": "<p>In the released model, future technology costs are <b>inputs</b> you choose; the model does not learn during a run. Learning curves are one way to <i>write</i> those inputs (the kit computes $900/kW falling to $460.8/kW after three doublings at 20%).</p>"}],
 "explorer": {"widget": "valuefactor", "intro": "Move solar's market share and see how the value factor raises its effective cost.", "predict": "At what market share does solar's effective cost double its plain levelised cost?"},
 "code": [
   {"title": "Levelised cost, resource curve and learning", "lang": "python", "file": "labs/go2/m24_supply.py", "runnable": True,
    "explain": "LCOE for gas and solar with a carbon price, a graded resource curve, and a learning curve. Try: set the solar capacity factor to 0.30 and predict its new LCOE.",
    "expected": "carbon   0 $/t: gas  61.2 $/MWh, solar  45.4 $/MWh\ncarbon  50 $/t: gas  79.5 $/MWh, solar  45.4 $/MWh\nresource price at 200, 800, 1400 EJ: [3.6, 6.0, 11.0] $/GJ\nsolar capex after 3 doublings at 20%: 460.8 $/kW"},
   {"title": "The same in R", "lang": "r", "file": "labs/go2/m24_supply.R", "runnable": False, "explain": "Identical numbers in base R."},
   {"title": "Cheap solar add-on used in lab 8", "lang": "xml", "file": "labs/iam-course/gcam-files/lab8_cheapsolar_config_snippet.xml", "runnable": False, "explain": "How a cost-change add-on file is added last in configuration.xml so it overrides the reference input."}],
 "takeaways": ["Fossil fuels come from graded supply curves; renewables from flow supply curves",
               "Technology cost = non-energy cost + fuel cost + emissions cost",
               "A carbon price raises each option's cost in proportion to its emissions",
               "Wind and solar costs are divided by a value factor that falls with their share (v7.3+)",
               "Future costs are inputs, not learned by the model; vintages make the fleet change slowly"],
 "quiz": [
   {"q": "In GCAM v8.2/9.1, the integration cost of wind and solar is represented by…", "options": ["a backup turbine for every VRE plant", "a value factor that falls with market share", "an explicit hourly storage model", "nothing"], "answer": 1, "explain": "PLCOE = LCOE / VF since v7.3; storage is not explicit."},
   {"q": "The kit gas plant costs 61.2 $/MWh at zero carbon price and 79.5 at $50/t. At $100/t it costs about…", "options": ["79.5", "88", "97.9", "122"], "answer": 2, "explain": "Each $50/t adds about 18.3 $/MWh, so 61.2 + 36.7 ≈ 97.9."},
   {"q": "A graded resource supply curve means…", "options": ["all of the resource costs the same", "cheap grades are used first, so price rises with use", "the resource is renewable", "the price falls as you use more"], "answer": 1, "explain": "Higher grades are dearer to extract."},
   {"q": "Does GCAM compute technology learning during a run?", "options": ["Yes, from cumulative capacity", "No: future costs are input assumptions", "Only for solar", "Only under a carbon price"], "answer": 1, "explain": "Costs are inputs; learning curves can be used to choose them."}],
 "glossary": [
   {"term": "Levelised cost (LCOE)", "def": "All lifetime costs of a plant divided by its lifetime output, in $/MWh."},
   {"term": "Capacity factor", "def": "Actual output divided by the output if the plant ran at full power all year."},
   {"term": "Value factor", "def": "The value of variable renewable output relative to average power; falls as their share grows."},
   {"term": "Graded supply curve", "def": "A resource split into grades of rising extraction cost."},
   {"term": "Vintage", "def": "The cohort of plants built in one period, which keeps operating for its lifetime."}],
 "resources": [
   {"title": "GCAM documentation: Energy supply", "url": D("supply_energy.html"), "why": "Resources, electricity, refining, hydrogen and CCS."},
   {"title": "GCAM documentation: Technology representation", "url": D("en_technologies.html"), "why": "Cost equation, vintages, shutdown rules."},
   {"title": "CMP 394: Intermittent electricity integration", "url": "https://jgcri.github.io/gcam-doc/cmp/394-Intermittent_electricity_integration.pdf", "why": "The value-factor method and its coefficients."},
   {"title": "GCAM releases (latest 9.1)", "url": "https://github.com/JGCRI/gcam-core/releases", "why": "Download GCAM and its input files."}],
 "downloads": [HANDBOOK, KIT, deck("Week08-The-energy-system-in-GCAM.pdf", "Week 8 slides: The energy system in GCAM (PDF)")]})

# ---------------------------------------------------------------- 2.5
mods.append({
 "id": "2.5", "go": 2, "slug": "energy-demand", "title": "Energy demand: buildings, industry, transport", "minutes": 45, "tag": "Demand",
 "systems": ["energy", "economy", "climate"],
 "summary": "People want services, not energy: warm rooms, steel, passenger-kilometres. See how GCAM grows service demand with income and price, and how transport modes compete on money plus time.",
 "outcomes": ["You can explain service demand with income and price elasticities",
              "You can compute a mode's generalised cost including the value of time",
              "You can describe GCAM's buildings, industry and transport demand structure",
              "You can trace how the electricity price reaches electric cars and heat pumps"],
 "narration_en": ("Nobody wants a gigajoule for its own sake. People want warm and cool rooms, light, steel for buildings, and trips to work and school. "
   "GCAM therefore models demand for energy services first, and only then the fuels needed to deliver them. "
   "Service demand grows with income and falls when services get more expensive, through income and price elasticities. "
   "Buildings demand depends on floor space, which rises with income and then levels off, and on heating and cooling degree days. "
   "Industry is split into sectors such as steel, cement, chemicals and fertiliser. "
   "Transport is special because time matters. A trip by bus is cheap in money but slow, while a car or a train is faster. "
   "GCAM adds the value of time to the money cost of each mode, using the wage, so as people get richer they move toward faster modes. "
   "In this module you will compute service demand, then mode shares for walking, bus, rail and car at three wage levels, and watch the car share grow from three percent to sixty-two percent."),
 "narration_ar": ("لا أحد يريد جيجاجول من الطاقة لذاته. يريد الناس غرفًا دافئة وباردة، وإضاءة، وفولاذًا للمباني، ورحلات إلى العمل والمدرسة. "
   "لذلك يُنمذج GCAM الطلب على خدمات الطاقة أولًا، ثم الوقود اللازم لتقديمها. "
   "ينمو الطلب على الخدمات مع الدخل وينخفض عندما ترتفع تكلفتها، عبر مرونات الدخل والسعر. "
   "ويعتمد الطلب في المباني على المساحة الأرضية، التي ترتفع مع الدخل ثم تستقر، وعلى أيام التدفئة والتبريد. "
   "وتنقسم الصناعة إلى قطاعات مثل الحديد والصلب والإسمنت والكيماويات والأسمدة. "
   "أما النقل فحالة خاصة لأن الوقت مهم. فالرحلة بالحافلة رخيصة نقدًا لكنها بطيئة، بينما السيارة أو القطار أسرع. "
   "يضيف النموذج قيمة الوقت إلى التكلفة النقدية لكل وسيلة، مستخدمًا الأجر، لذلك ينتقل الناس إلى الوسائل الأسرع كلما زاد ثراؤهم. "
   "في هذه الوحدة ستحسب الطلب على الخدمات، ثم حصص المشي والحافلة والقطار والسيارة عند ثلاثة مستويات للأجور، وترى حصة السيارة تنمو من ثلاثة بالمئة إلى اثنين وستين بالمئة."),
 "diagram": {
   "title": "Energy demand: services first, fuels second", "caption": "Income and prices set service demand; technologies then choose fuels. Electricity prices reach every end use.",
   "nodes": [
     node("inc", "Income and population", "from Go 2.1", "w", "economy", "GDP per person drives floorspace, industrial output and passenger travel through income elasticities (demand_energy.html)."),
     node("bld", "Buildings", "floorspace × services", "nw", "energy", "Residential split into 10 income deciles since v7.1. Floorspace follows a Gompertz curve; heating and cooling depend on degree-days (demand_energy.html)."),
     node("ind", "Industry", "steel, cement, chemicals…", "n", "energy", "Iron and steel, chemicals, aluminium, cement, fertiliser, food processing and other industry, plus construction, mining and agricultural energy use."),
     node("trn", "Transport", "passenger + freight", "c", "energy", "Four final demands: passenger aviation, other passenger, international shipping, other freight. Nested modes, size classes and drivetrains (Go 3 goes deep)."),
     node("vot", "Value of time", "wage ÷ speed", "sw", "economy", "Passenger mode cost adds W·V/S: wage per hour × time-value multiplier ÷ speed. Faster modes win as wages rise."),
     node("elecp", "Electricity price", "from Go 2.4", "ne", "energy", "Electric technologies (heat pumps, EVs, electric arc furnaces) pay the solved electricity price, so cheaper power pulls demand toward electricity."),
     node("fuel", "Final energy by fuel", "EJ by sector", "e", "energy", "Technology choice inside each service turns service demand into final energy by fuel."),
     node("co2", "Emissions", "fuel × carbon coefficient", "se", "climate", "Combustion CO₂ = fuel use × carbon coefficient; cooling electricity also drives HFC134a (emissions.html).")],
   "edges": [edge("inc", "bld", "income", "economy"), edge("inc", "ind", "", "economy"), edge("inc", "trn", "income", "economy"), edge("vot", "trn", "time cost", "economy"),
             edge("elecp", "fuel", "price signal", "energy"), edge("trn", "fuel", "service → fuel", "energy"), edge("bld", "fuel", "", "energy"), edge("fuel", "co2", "", "climate")],
   "tour": [
     {"focus": ["inc"], "edges": [], "text": "Income per person, from Go 2.1, is the main driver of how much service people demand."},
     {"focus": ["bld", "ind"], "edges": [["inc", "bld"], ["inc", "ind"]], "text": "Buildings and industry grow with income and fall with service price; floorspace saturates."},
     {"focus": ["trn", "vot"], "edges": [["inc", "trn"], ["vot", "trn"]], "text": "Transport adds the value of time: richer travellers choose faster modes even if dearer."},
     {"focus": ["elecp", "fuel"], "edges": [["elecp", "fuel"], ["trn", "fuel"], ["bld", "fuel"]], "text": "Inside each service, technologies compete by cost, so electricity prices steer heat pumps and EVs."},
     {"focus": ["co2"], "edges": [["fuel", "co2"]], "text": "Final energy by fuel times carbon coefficients gives demand-side emissions."}]},
 "components": {"caption": "Demand-side building blocks", "rows": [
     {"name": "Energy service", "purpose": "What people want: warmth, steel, passenger-km", "analogy": "The meal, not the gas in the stove"},
     {"name": "Income elasticity", "purpose": "% change in service demand per 1% income", "analogy": "Ordering more as your salary rises"},
     {"name": "Price elasticity", "purpose": "% change in service demand per 1% price", "analogy": "Ordering less when the menu gets dearer"},
     {"name": "Floorspace", "purpose": "Buildings activity; Gompertz curve in income", "analogy": "Rooms to heat and cool"},
     {"name": "Value of time", "purpose": "Wage-based cost of travel time", "analogy": "Paying for a taxi to save an hour"},
     {"name": "Load factor", "purpose": "Passengers or tonnes per vehicle", "analogy": "How full each bus is"}]},
 "sections": [
   {"heading": "Services, not fuels", "html": "<p>GCAM's demand sectors produce <b>energy services</b> (floorspace heated and cooled, industrial output, passenger-km and tonne-km), then choose technologies and fuels to supply them (" + cite("demand_energy.html") + "). Service demand changes with income and price:</p><div class=\"eq\">D<sub>t</sub> = D<sub>t−1</sub> · (Y<sub>t</sub>/Y<sub>t−1</sub>)<sup>α</sup> · (P<sub>t</sub>/P<sub>t−1</sub>)<sup>β</sup> · (N<sub>t</sub>/N<sub>t−1</sub>)</div><p>With α = 0.6 and β = −0.3, doubling income raises passenger-km from 100 to <b>151.6</b>; if travel also becomes 50% dearer it is <b>134.2</b>.</p>"},
   {"heading": "Buildings", "html": "<p>Residential demand is split into 10 income deciles (since v7.1). Floorspace per person follows a Gompertz curve in income and population density; services per m² saturate; heating and cooling scale with degree-days and shell efficiency (" + cite("demand_energy.html") + "). Degree-days link buildings to climate; the helios tool computes them from gridded data. Parameter values for these curves are not given on the doc pages.</p>"},
   {"heading": "Industry", "html": "<p>Industry includes iron and steel (BOF, EAF with scrap, EAF with DRI), chemicals, aluminium, cement, fertiliser, food processing and other industry, plus construction, mining and agricultural energy. Fertiliser demand is the sum of crop production × fertiliser coefficient: a direct link from farms to the energy system (" + cite("demand_energy.html") + ").</p>"},
   {"heading": "Transport: money plus time", "html": "<p>Each vehicle technology has a cost per passenger-km or tonne-km:</p><div class=\"eq\">P<sub>j</sub> = (P<sub>fuel</sub> · I<sub>j</sub> + N<sub>j</sub>) / L<sub>j</sub></div><p>with fuel intensity I, non-fuel cost per vehicle-km N and load factor L. Passenger modes then add the <b>value of time</b>:</p><div class=\"eq\">P<sub>mode</sub> = Σ α<sub>j</sub> P<sub>j</sub> + W · V / S</div><p>W is wage per hour (GDP per person ÷ working hours), V a time-value multiplier, S speed. In the kit toy (value of time = half the wage), car share rises from <b>3%</b> at $2/h to <b>22.5%</b> at $10/h and <b>61.7%</b> at $40/h.</p>"}],
 "callouts": [
   {"after": 0, "kind": "model", "title": "A useful mental model", "html": "<p>A restaurant plans meals before it orders gas. GCAM does the same: meals = services, gas = fuels. Change the menu (services) or the stove (technology) and the gas bill changes.</p>"},
   {"after": 3, "kind": "gcam", "title": "In GCAM", "html": "<p>Query <b>final energy consumption by sector and fuel</b> and <b>transport service output by mode</b> (" + cite("outputs_quantity.html") + "). Transport inputs are built by gcamdata from the UCD transportation database (<code>UCD_trn_data_SSP*.csv</code>) (" + cite("ssp.html") + "). Note: transport units changed in v8.5 (billion pkm, 1975$); Go 3.2 covers the details.</p>"},
   {"after": 3, "kind": "trap", "title": "\"Richer people always drive more\"", "html": "<p>Not necessarily: they choose <i>faster</i> modes. Where high-speed rail is fast and frequent, rising wages can favour rail. The value of time rewards speed, not cars as such.</p>"}],
 "explorer": {"widget": "trncost", "intro": "Change the wage, speeds and money costs, and watch the generalised cost and mode shares.", "predict": "If wages quadruple from $10 to $40 an hour, does the bus share rise or fall? By roughly how much?"},
 "code": [
   {"title": "Service demand and mode choice with time cost", "lang": "python", "file": "labs/go2/m25_demand.py", "runnable": True,
    "explain": "Service demand with elasticities, then mode shares from money cost + value of time at three wages. Try: double rail speed and predict the new rail share at $40/h.",
    "expected": "passenger-km if income doubles, price same: 151.6\n...and if fuel makes travel 50% dearer:      134.2\nwage 40 $/h -> shares {'walk': 0.002, 'bus': 0.059, 'rail': 0.322, 'car': 0.617}"},
   {"title": "The same in R", "lang": "r", "file": "labs/go2/m25_demand.R", "runnable": False, "explain": "Identical numbers in base R."}],
 "takeaways": ["GCAM models energy services first, then the fuels that supply them",
               "Service demand rises with income (α) and falls with price (β)",
               "Buildings use floorspace and degree-days; industry is split into subsectors",
               "Passenger modes compete on money cost plus wage-based time cost",
               "The electricity price reaches heat pumps, EVs and electric furnaces through technology choice"],
 "quiz": [
   {"q": "Income doubles, α = 0.6, price unchanged. Service demand rises by a factor of…", "options": ["1.2", "1.52", "2.0", "0.6"], "answer": 1, "explain": "2^0.6 = 1.516."},
   {"q": "In GCAM's passenger cost, W·V/S represents…", "options": ["fuel tax", "the value of travel time", "vehicle depreciation", "carbon price"], "answer": 1, "explain": "Wage × time-value multiplier ÷ speed."},
   {"q": "Why do faster modes gain share as wages rise?", "options": ["They become cheaper in money", "Time becomes more valuable", "Fuel gets cheaper", "Load factors rise"], "answer": 1, "explain": "The time term grows with the wage and is smaller for fast modes."},
   {"q": "Which is a link from land to the energy system in the industry module?", "options": ["Cement", "Fertiliser demand driven by crop production", "Aluminium", "Mining"], "answer": 1, "explain": "Fertiliser = Σ crop production × coefficient."}],
 "glossary": [
   {"term": "Energy service", "def": "The useful outcome of energy use: warmth, light, motion, materials."},
   {"term": "Price elasticity", "def": "The % change in demand for a 1% change in its price."},
   {"term": "Degree-days", "def": "A measure of how much heating or cooling a climate needs."},
   {"term": "Value of time", "def": "The money value travellers place on time spent travelling, tied to the wage."},
   {"term": "Generalised cost", "def": "Money cost plus the money value of travel time."}],
 "resources": [
   {"title": "GCAM documentation: Energy demand", "url": D("demand_energy.html"), "why": "Buildings, industry and transport equations."},
   {"title": "GCAM documentation: Demand inputs", "url": D("inputs_demand.html"), "why": "Data sources behind the demand sectors."},
   {"title": "helios (degree-days for GCAM)", "url": "https://github.com/JGCRI/helios", "why": "Compute heating and cooling degree-days for GCAM regions."}],
 "downloads": [HANDBOOK, KIT, deck("Week08-The-energy-system-in-GCAM.pdf", "Week 8 slides: The energy system in GCAM (PDF)")]})

# ---------------------------------------------------------------- 2.6
mods.append({
 "id": "2.6", "go": 2, "slug": "land-food-bioenergy", "title": "Land, food and bioenergy", "minutes": 45, "tag": "Land",
 "systems": ["land", "energy", "climate", "water"],
 "summary": "Land is shared among crops, pasture, forest and energy crops by a logit on profit per hectare. See why bioenergy demand raises food prices and how a carbon price can grow forests.",
 "outcomes": ["You can compute profit per hectare and logit land shares",
              "You can estimate the land needed for a bioenergy target",
              "You can describe GCAM's land nest and its geographic land units",
              "You can explain how land carbon is priced and how land-use emissions arise"],
 "narration_en": ("Every hectare of land can only do one job at a time: grow wheat, feed cattle, carry a forest, or grow grass for bioenergy. "
   "GCAM divides land among these uses according to how profitable each one is, using a logit, the same family of formulas used for energy technologies but now with a positive exponent on profit. "
   "Land is resolved by geographic land units, the overlap of thirty-two regions and river basins, and arranged in a nest, so close substitutes like different crops compete more strongly than cropland and forest. "
   "When the energy system wants more bioenergy, the price of energy grass rises, its profit per hectare rises, and land shifts toward it, which pushes up food prices. "
   "A carbon price can also be applied to land as a subsidy for holding carbon, which makes forests more profitable and can expand them. "
   "In this module you will compute profits and land shares by hand, estimate how many million hectares a bioenergy target needs, and see how yield changes the answer."),
 "narration_ar": ("لا يمكن لكل هكتار من الأرض أن يؤدي إلا وظيفة واحدة في الوقت نفسه: زراعة القمح، أو تغذية الماشية، أو حمل غابة، أو زراعة العشب للطاقة الحيوية. "
   "يقسم نموذج GCAM الأرض بين هذه الاستخدامات بحسب ربحية كل منها، مستخدمًا دالة لوجيت، من العائلة نفسها المستخدمة لتقنيات الطاقة لكن بأُس موجب على الربح. "
   "وتُمثَّل الأرض بوحدات أرضية جغرافية، هي تقاطع المناطق الاثنتين والثلاثين مع أحواض الأنهار، وتُرتَّب في شجرة متداخلة، بحيث تتنافس البدائل القريبة مثل المحاصيل المختلفة بقوة أكبر من تنافس الأراضي الزراعية والغابات. "
   "وعندما يريد نظام الطاقة مزيدًا من الطاقة الحيوية يرتفع سعر عشب الطاقة، فيرتفع ربحه لكل هكتار، وتنتقل الأرض نحوه، مما يرفع أسعار الغذاء. "
   "ويمكن أيضًا تطبيق سعر الكربون على الأرض كإعانة مقابل الاحتفاظ بالكربون، مما يجعل الغابات أكثر ربحية وقد يوسّعها. "
   "في هذه الوحدة ستحسب الأرباح وحصص الأرض يدويًا، وتقدّر كم مليون هكتار يحتاجه هدف للطاقة الحيوية، وترى كيف تغيّر الإنتاجية الجواب."),
 "diagram": {
   "title": "Land competition and its links", "caption": "Profit per hectare sets land shares; bioenergy demand and carbon prices change profits, and land change releases or stores carbon.",
   "nodes": [
     node("price", "Crop and biomass prices", "from food and energy markets", "nw", "economy", "Crop prices clear food markets; the biomass price clears the bioenergy market that the energy system demands from (supply_land.html)."),
     node("profit", "Profit per hectare", "(price − cost) × yield", "n", "land", "Profit rate = (price + subsidy − variable cost − input costs) × yield, in 1975$ per area; input costs include fertiliser and water (supply_land.html)."),
     node("cpr", "Carbon price on land", "subsidy for carbon stock", "ne", "policy", "Landowners receive carbon price × carbon density (discounted, annualised): forests gain relative to cropland (land.html)."),
     node("nest", "Land nest (logit)", "s = (λπ)^ρ / Σ(λπ)^ρ", "c", "land", "Shares by profit with exponent ρ > 0; tighter substitution inside nests than across them. Calibrated profit scalers λ reproduce base-year land (land.html).", w=210),
     node("crop", "Cropland and food", "irrigated/rainfed × hi/lo", "w", "land", "Every crop splits into irrigated/rainfed × high/low management, allowing price-induced intensification."),
     node("bioc", "Energy crops", "herbaceous grass from 2025", "sw", "energy", "Dedicated energy grass enters the cropland nest; woody biomass sits in the forest nest (details_land.html)."),
     node("forest", "Forest and natural land", "managed / unmanaged", "e", "land", "Forests grow back slowly: uptake follows a sigmoid with mature age of about 30–100 years (land.html)."),
     node("luc", "Land-use change CO₂", "ΔA × carbon density", "se", "climate", "E_t = A_t·D_t − A_t−1·D_t−1 for vegetation and soil. Releases are immediate; regrowth uptake is slow (land.html).")],
   "edges": [edge("price", "profit", "price", "economy"), edge("profit", "nest", "profit", "land"), edge("cpr", "nest", "subsidy", "policy"),
             edge("nest", "crop", "share", "land"), edge("nest", "bioc", "share", "land"), edge("nest", "forest", "share", "land"),
             edge("forest", "luc", "", "climate"), edge("bioc", "price", "supply", "energy")],
   "tour": [
     {"focus": ["price", "profit"], "edges": [["price", "profit"]], "text": "Prices from food and bioenergy markets set each land use's profit per hectare."},
     {"focus": ["nest"], "edges": [["profit", "nest"]], "text": "A logit on profit shares the land: more profitable uses expand, but not all at once."},
     {"focus": ["crop", "bioc"], "edges": [["nest", "crop"], ["nest", "bioc"]], "text": "Energy grass and food crops compete in the same cropland nest: bioenergy demand raises food prices."},
     {"focus": ["cpr", "forest"], "edges": [["cpr", "nest"], ["nest", "forest"]], "text": "A carbon price on land pays for stored carbon, so forests become more profitable and can expand."},
     {"focus": ["luc"], "edges": [["forest", "luc"]], "text": "Every change in land cover changes carbon stocks: clearing releases CO₂ fast, regrowth takes it back slowly."},
     {"focus": ["bioc", "price"], "edges": [["bioc", "price"]], "text": "Biomass supply feeds back to the bioenergy market, closing the energy–land loop."}]},
 "components": {"caption": "Land module building blocks", "rows": [
     {"name": "Geographic land unit", "purpose": "Region × river basin; the spatial unit for land", "analogy": "A plot on the map"},
     {"name": "Land nest", "purpose": "Tree of land uses with logit sharing at each node", "analogy": "Family tree of land uses"},
     {"name": "Profit per hectare", "purpose": "What drives each land use's share", "analogy": "Rent the plot would earn"},
     {"name": "Profit scaler (λ)", "purpose": "Calibrated so 2021 land matches data", "analogy": "Local preference for a crop"},
     {"name": "Yield", "purpose": "Output per hectare; grows by assumed productivity", "analogy": "Harvest per field"},
     {"name": "Carbon density", "purpose": "Vegetation and soil carbon per area by land type", "analogy": "How much carbon each plot stores"}]},
 "sections": [
   {"heading": "What this component represents", "html": "<p>The agriculture and land use module (AgLU) decides how land is used, what crops and livestock are produced, and how much carbon land stores. Land is resolved by water-basin-based <b>geographic land units</b>: the overview text says more than 300, its table 396 land subregions (" + cite("overview.html") + "). Every crop is split into irrigated/rainfed × high/low management, so production can intensify when prices rise.</p>"},
   {"heading": "Profit and land shares", "html": "<div class=\"eq\">π = (price − cost) × yield</div><div class=\"eq\">s<sub>i</sub> = (λ<sub>i</sub> π<sub>i</sub>)<sup>ρ</sup> / Σ<sub>j</sub> (λ<sub>j</sub> π<sub>j</sub>)<sup>ρ</sup>,  a<sub>i</sub> = a<sub>parent</sub> · s<sub>i</sub></div><p>Worked example (exponent 1, equal scalers): wheat sells at $200/t, costs $120/t, yields 3 t/ha → profit (200 − 120) × 3 = <b>$240/ha</b>. Energy grass at $60/t, cost $30/t, 10 t/ha → (60 − 30) × 10 = <b>$300/ha</b>. Shares: 240 / 540 = <b>44%</b> wheat, 300 / 540 = <b>56%</b> grass. At a grass price of $40/t grass gets 29%; at $90/t, 71% (" + cite("land.html") + ").</p>"},
   {"heading": "How much land does bioenergy need?", "html": "<div class=\"eq\">land (ha) = energy (GJ) / (yield (t/ha) × energy content (GJ/t))</div><p>With 18 GJ per tonne: 10 EJ at 10 t/ha needs 10×10<sup>9</sup> / 180 = <b>55.6 million ha</b>; 100 EJ needs <b>555.6 million ha</b>; halve the yield and it doubles to <b>1,111 million ha</b>. World cropland is roughly 1.5 billion ha, so large bioenergy targets compete seriously with food. GCAM includes default limits: a negative-emissions budget capped at a share of GDP and a biomass externality cost curve (" + cite("policies.html") + ").</p>"},
   {"heading": "Land carbon and land-use change emissions", "html": "<p>Vegetation and soil carbon densities by land unit come from the moirai data system. Land-use change emissions are</p><div class=\"eq\">E<sub>t</sub> = A<sub>t</sub> · D<sub>t</sub> − A<sub>t−1</sub> · D<sub>t−1</sub></div><p>computed separately for vegetation and soil. Clearing releases carbon immediately; regrowth follows a slow sigmoid with forest mature ages of about 30 to 100 years. A <b>carbon price on land</b> works as a subsidy for holding carbon stock: carbon price × carbon density × discounting and annualisation (" + cite("land.html") + ").</p>"},
   {"heading": "Calibration and yields", "html": "<p>Profit scalers λ are calibrated by inverting the share equation with base-year land shares, then carried forward. Future yields grow by agricultural productivity growth from FAO projections, scaled by SSP (+50% in SSP1/5, −50% in SSP3) (" + cite("supply_land.html") + ", " + cite("ssp.html") + "). Numeric land logit exponents are not on the doc pages; they are in the input files.</p>"}],
 "callouts": [
   {"after": 1, "kind": "model", "title": "A useful mental model", "html": "<p>Think of plots on a market street. Each landowner rents to whoever pays most per hectare, but habits, soils and contracts mean some keep their old tenants. The logit is the street's average behaviour.</p>"},
   {"after": 3, "kind": "gcam", "title": "In GCAM", "html": "<p>Query <b>aggregated land allocation</b> and <b>LUC emissions by region</b>; net CO₂ = CO₂ emissions by region + LUC emissions (" + cite("outputs_emissions.html") + "). Carbon state is set by <code>aglu.CARBON_STATE</code> in gcamdata's constants; maps by basin with <code>rmap::mapGCAMLand</code>.</p>"},
   {"after": 2, "kind": "trap", "title": "\"Bioenergy is carbon-free, so more is always better\"", "html": "<p>Land conversion can release large stocks of carbon immediately, while regrowth takes decades, and energy crops displace food. GCAM accounts for both through land competition and LUC emissions.</p>"},
   {"after": 4, "kind": "research", "title": "Docs disagree", "html": "<p>Protected land: the policies page says 90% of non-commercial ecosystems by default; the land page describes a suitability × IUCN method. The land page reads as the newer method. Check your release's input files.</p>"}],
 "explorer": {"widget": "land", "intro": "Choose a bioenergy target, a yield and the energy-grass price, and see the land needed and the share of contested land.", "predict": "If yields fall from 10 to 5 t/ha, how much more land does 100 EJ need?"},
 "code": [
   {"title": "Land shares and land for bioenergy", "lang": "python", "file": "labs/go2/m26_land.py", "runnable": True,
    "explain": "Profit per hectare, logit land shares at three grass prices, and land needed for bioenergy. Try: raise the logit exponent to 3 and predict how the $60/t grass share changes.",
    "expected": "grass $60/t: profits wheat 240, grass 300 $/ha -> shares wheat 0.444, grass 0.556\n100 EJ at 10 t/ha ->  555.6 million ha\n100 EJ at  5 t/ha -> 1111.1 million ha"},
   {"title": "The same in R", "lang": "r", "file": "labs/go2/m26_land.R", "runnable": False, "explain": "Identical numbers in base R."},
   {"title": "Lab 9: map land and water results", "lang": "r", "file": "labs/iam-course/labs/lab9.R", "runnable": False, "explain": "rgcam + rmap lab from the 15-week course (gaps to fill; solution in labs/iam-course/solutions/lab9_solution.R)."}],
 "takeaways": ["Land is shared among uses by a logit on profit per hectare, inside a nest",
               "Bioenergy and food compete for cropland, so bioenergy demand can raise food prices",
               "Land needed = energy ÷ (yield × energy content): yield matters as much as the target",
               "Land-use change emits carbon fast and regrowth absorbs it slowly",
               "A carbon price on land pays for stored carbon and can expand forests"],
 "quiz": [
   {"q": "Wheat (200 − 120) × 3 and grass (60 − 30) × 10, exponent 1. Grass's land share is…", "options": ["30%", "44%", "56%", "71%"], "answer": 2, "explain": "300 / (240 + 300) = 0.556."},
   {"q": "100 EJ of energy grass at 10 t/ha and 18 GJ/t needs about…", "options": ["56 million ha", "556 million ha", "5.6 billion ha", "18 million ha"], "answer": 1, "explain": "100×10⁹ / 180 ≈ 556 million ha."},
   {"q": "In GCAM, a carbon price applied to land works as…", "options": ["a tax on crops", "a subsidy for holding carbon stock", "a ban on deforestation", "nothing"], "answer": 1, "explain": "Carbon price × carbon density, discounted and annualised (land.html)."},
   {"q": "Why can GCAM's land model intensify production?", "options": ["Crops split into irrigated/rainfed × high/low management", "It assumes yields double", "It ignores land limits", "It imports land"], "answer": 0, "explain": "Management options let higher prices shift land to high-input practices."}],
 "glossary": [
   {"term": "AgLU", "def": "GCAM's agriculture and land use module."},
   {"term": "Geographic land unit (GLU)", "def": "The overlap of a GCAM region and a river basin; GCAM's spatial unit for land."},
   {"term": "Profit rate", "def": "Revenue minus costs per unit of land."},
   {"term": "Land-use change emissions", "def": "CO₂ released or absorbed when land cover changes."},
   {"term": "Carbon density", "def": "Carbon stored per area in vegetation and soil."}],
 "resources": [
   {"title": "GCAM documentation: Land", "url": D("land.html"), "why": "Land nesting, allocation equations and land carbon."},
   {"title": "GCAM documentation: Land supply", "url": D("supply_land.html"), "why": "Profit rate, yields and livestock."},
   {"title": "GCAM documentation: Land demand", "url": D("demand_land.html"), "why": "Food, feed and non-food demand."},
   {"title": "rmap", "url": "https://github.com/JGCRI/rmap", "why": "Built-in GCAM region, basin and land maps for results."}],
 "downloads": [HANDBOOK, KIT, deck("Week09-Land-water-and-bioenergy.pdf", "Week 9 slides: Land, water and bioenergy (PDF)")]})

# ---------------------------------------------------------------- 2.7
mods.append({
 "id": "2.7", "go": 2, "slug": "water", "title": "Water", "minutes": 35, "tag": "Water",
 "systems": ["water", "energy", "land"],
 "summary": "GCAM balances water by river basin: cheap renewable water first, then groundwater, then desalination. See how withdrawals for farms, power and cities set the water price.",
 "outcomes": ["You can name GCAM's six water demand sectors",
              "You can explain the three supply tiers and the basin water price",
              "You can compute withdrawals for power cooling",
              "You can trace the water–energy and water–land links"],
 "narration_en": ("Water in GCAM is tracked river basin by river basin, two hundred and thirty-five of them. "
   "Six sectors withdraw water: agriculture for irrigation, electricity for cooling power plants, manufacturing, primary energy production, livestock and municipal supply. "
   "On the supply side, each basin first uses accessible renewable water, which is cheap. When that runs short, it pumps non-renewable groundwater, which costs more, "
   "and in the last resort cities and industry can use desalination, which is expensive and uses a lot of electricity. "
   "A water price for each basin rises until demand fits supply. That price then feeds back: power plants switch to cooling systems that use less water, "
   "and farms face higher costs for irrigation, although GCAM charges irrigation only five percent of the general water price. "
   "In this module you will add up withdrawals for a basin and see how switching from dry cooling to once-through cooling can push the basin from cheap renewable water into groundwater."),
 "narration_ar": ("يتتبع نموذج GCAM المياه حوضًا نهريًا بعد حوض، وعددها مئتان وخمسة وثلاثون حوضًا. "
   "تسحب ستة قطاعات المياه: الزراعة للري، والكهرباء لتبريد محطات التوليد، والصناعة التحويلية، وإنتاج الطاقة الأولية، والثروة الحيوانية، والإمداد البلدي. "
   "وعلى جانب العرض، يستخدم كل حوض أولًا المياه المتجددة المتاحة، وهي رخيصة. وعندما تنقص يضخ المياه الجوفية غير المتجددة، وهي أغلى، "
   "وكملاذ أخير يمكن للمدن والصناعة استخدام التحلية، وهي مكلفة وتستهلك كثيرًا من الكهرباء. "
   "ويرتفع سعر المياه في كل حوض حتى يتسع العرض للطلب. ثم يعود هذا السعر ليؤثر: فتنتقل محطات الكهرباء إلى أنظمة تبريد أقل استهلاكًا للمياه، "
   "وتواجه المزارع تكاليف أعلى للري، مع أن النموذج يحمّل الري خمسة بالمئة فقط من السعر العام للمياه. "
   "في هذه الوحدة ستجمع سحوبات المياه لحوض ما، وترى كيف يمكن أن يدفع التحول من التبريد الجاف إلى التبريد بالتدفق المفتوح الحوضَ من المياه المتجددة الرخيصة إلى المياه الجوفية."),
 "diagram": {
   "title": "A basin water market", "caption": "Six demand sectors withdraw water; three supply tiers meet it; the basin price feeds back to cooling choice and irrigation.",
   "nodes": [
     node("irr", "Irrigation", "km³ per Mt of crop", "nw", "land", "Irrigation withdrawals = exogenous coefficient × endogenous crop production, by basin (demand_water.html)."),
     node("pow", "Power cooling", "5 cooling options", "w", "energy", "Once-through, recirculating, pond, dry and seawater once-through, chosen by a cost logit; dry cooling lowers plant efficiency (demand_water.html)."),
     node("mun", "Municipal and industry", "grow with income", "sw", "economy", "Per-capita municipal water grows with GDP per person (elasticity 0.37) and falls with price (−0.33) and technology."),
     node("bas", "Basin water market", "price in 1975$/m³", "c", "water", "235 basins. A basin shadow price adjusts until demand equals supply (supply_water.html).", w=200),
     node("ren", "Renewable water", "accessible runoff (Xanthos)", "ne", "water", "Accessible water QA = max(0, min(QT − EFR, QB − EFR + RS)) from Xanthos runoff, environmental flows and reservoir storage. Cheap within the accessible amount."),
     node("gw", "Groundwater", "graded, Superwell", "e", "water", "Non-renewable groundwater as a graded depletable resource; Superwell gives 20 cost grades per region-basin."),
     node("des", "Desalination", "cities and industry only", "se", "energy", "Costs are energy, capital and O&M; reverse osmosis uses 2.75 kWh/m³. In core runs only municipal and industrial demand can use it."),
     node("efw", "Energy for water", "kWh per m³", "s", "energy", "Pumping, treatment and desalination use electricity: a water → energy link (demand_energy.html).")],
   "edges": [edge("irr", "bas", "withdrawals", "land"), edge("pow", "bas", "withdrawals", "energy"), edge("mun", "bas", "withdrawals", "economy"),
             edge("ren", "bas", "tier 1", "water"), edge("gw", "bas", "tier 2", "water"), edge("des", "bas", "tier 3", "water"), edge("bas", "pow", "price", "water"), edge("des", "efw", "electricity", "energy")],
   "tour": [
     {"focus": ["irr", "pow", "mun"], "edges": [["irr", "bas"], ["pow", "bas"], ["mun", "bas"]], "text": "Farms, power plants, cities and industry all withdraw from the same basin."},
     {"focus": ["ren"], "edges": [["ren", "bas"]], "text": "Accessible renewable water is used first, and it is cheap."},
     {"focus": ["gw"], "edges": [["gw", "bas"]], "text": "When it runs short, groundwater on graded cost curves fills the gap at a higher price."},
     {"focus": ["des", "efw"], "edges": [["des", "bas"], ["des", "efw"]], "text": "Desalination is the last resort for cities and industry, and it uses electricity."},
     {"focus": ["bas", "pow"], "edges": [["bas", "pow"]], "text": "The basin price feeds back: power plants shift to cooling that uses less water."}]},
 "components": {"caption": "Water module building blocks", "rows": [
     {"name": "Basin", "purpose": "235 river basins are the water accounting units", "analogy": "One shared tank per valley"},
     {"name": "Withdrawal", "purpose": "Water taken from a source", "analogy": "Water drawn from the tank"},
     {"name": "Consumption", "purpose": "Water not returned (evaporated, embodied)", "analogy": "Water that never comes back"},
     {"name": "Supply tiers", "purpose": "Renewable, groundwater, desalination at rising cost", "analogy": "Tap, well, then bottled water"},
     {"name": "Water price", "purpose": "Basin shadow price clearing the market", "analogy": "The meter rate in a dry year"}]},
 "sections": [
   {"heading": "What this component represents", "html": "<p>GCAM tracks water by <b>235 basins</b> (" + cite("common_assumptions.html") + "). Agricultural demand is modelled directly per basin; other sectors are modelled by region and mapped to basins. Demand is reported as withdrawals, consumption, biophysical consumption and seawater (" + cite("demand_water.html") + ").</p>"},
   {"heading": "Six demand sectors", "html": "<p>Agriculture (irrigation), electricity generation, manufacturing, primary energy, livestock and municipal. Irrigation = coefficient (km³ per Mt) × crop production. Municipal per-capita demand follows</p><div class=\"eq\">pcW<sub>t</sub> = pcW<sub>t−1</sub> · (pcGDP ratio)<sup>0.37</sup> · (price ratio)<sup>−0.33</sup> · (1 − Tech<sub>t</sub>)</div><p>Power plants choose among five cooling systems by a cost logit; water coefficients come from Macknick et al. (2011) (" + cite("demand_water.html") + ").</p>"},
   {"heading": "Three supply tiers and the water price", "html": "<p>Renewable water comes from Xanthos runoff. Accessible water is</p><div class=\"eq\">QA = max(0, min(QT − EFR, QB − EFR + RS))</div><p>with streamflow QT, baseflow QB, environmental flow requirement EFR and reservoir storage RS. Beyond it, non-renewable groundwater on graded curves, then desalination. A basin price in 1975$/m³ adjusts until demand equals supply; irrigation pays 5% of it (<code>water.IRR_PRICE_SUBSIDY_MULT</code>) (" + cite("supply_water.html") + ").</p>"},
   {"heading": "Worked example: cooling decides the tier", "html": "<p>Kit toy basin: 50 km³ of renewable water at $0.01/m³, 30 km³ of groundwater at $0.05/m³, then desalination at $0.80/m³. Irrigation 40 km³ and municipal 8 km³. Power at 300 TWh with dry-ish cooling (2 L/kWh) adds 0.6 km³ → total <b>48.6 km³</b>, price <b>$0.01/m³</b>. With once-through cooling (60 L/kWh) power adds 18 km³ → <b>66.0 km³</b>, which exceeds renewable supply: the price jumps to <b>$0.05/m³</b>.</p>"},
   {"heading": "Water–energy–land links", "html": "<p>Energy for water: desalination by reverse osmosis uses 2.75 kWh/m³, thermal desalination 58.3, groundwater pumping 0.185 (" + cite("demand_energy.html") + "). Water for energy: primary energy production withdraws water (withdrawal/consumption ratio 3.3; seawater share 95% in the Middle East). Water for land: water costs enter crop profit, shifting irrigated versus rainfed land.</p>"}],
 "callouts": [
   {"after": 2, "kind": "gcam", "title": "In GCAM", "html": "<p>Query <b>water withdrawals by region</b> and <b>water withdrawals by basin</b> (course query file). Map basins with <code>rmap::mapGCAMBasins</code>. The irrigation price multiplier is <code>water.IRR_PRICE_SUBSIDY_MULT</code> in gcamdata's constants.</p>"},
   {"after": 3, "kind": "trap", "title": "Withdrawal is not consumption", "html": "<p>A once-through cooled plant withdraws a lot but returns most of it warmer; a recirculating plant withdraws less but evaporates more of what it takes. Always say which measure you report.</p>"},
   {"after": 4, "kind": "research", "title": "Gulf angle", "html": "<p>In the Middle East region GCAM assumes 95% seawater for primary energy production, and desalination ties city water to electricity demand: a strong water–energy coupling for Saudi Arabia studies.</p>"}],
 "explorer": {"widget": "budget", "intro": "The same bathtub logic applies to a basin: a fixed renewable amount, filled by yearly withdrawals. Use the bathtub to build intuition for limits.", "predict": "If withdrawals double, does the time until the renewable limit is reached halve?"},
 "code": [
   {"title": "Basin supply tiers and cooling water", "lang": "python", "file": "labs/go2/m27_water.py", "runnable": True,
    "explain": "Adds withdrawals and prices them with three supply tiers. Try: raise irrigation to 60 km³ and predict the price with dry cooling.",
    "expected": "300 TWh at  2.0 L/kWh: withdrawals   48.6 km3 -> water price $0.01/m3\n300 TWh at 60.0 L/kWh: withdrawals   66.0 km3 -> water price $0.05/m3"},
   {"title": "The same in R", "lang": "r", "file": "labs/go2/m27_water.R", "runnable": False, "explain": "Identical numbers in base R."},
   {"title": "Pull basin withdrawals from a GCAM run (Python)", "lang": "python", "file": "labs/go2/gcam/read_gcam.py", "runnable": False, "explain": "gcamreader script for the course queries, including 'water withdrawals by basin'. Not run against a live database."}],
 "takeaways": ["Water is balanced by 235 basins with a basin price",
               "Six sectors withdraw: irrigation, electricity, manufacturing, primary energy, livestock, municipal",
               "Supply tiers: accessible renewable water, then groundwater, then desalination",
               "Cooling choice links electricity to water; desalination links water to electricity",
               "Irrigation pays only 5% of the general water price by default"],
 "quiz": [
   {"q": "How many water basins does GCAM use (common assumptions page)?", "options": ["32", "235", "396", "18"], "answer": 1, "explain": "235 basins; 396 is the number of land subregions."},
   {"q": "Which supply tier is used first?", "options": ["Desalination", "Groundwater", "Accessible renewable water", "Imported water"], "answer": 2, "explain": "Cheap renewable water first, then graded groundwater, then desalination."},
   {"q": "In core GCAM, who can use desalinated water?", "options": ["Everyone", "Only irrigation", "Municipal and industrial demand", "Only power plants"], "answer": 2, "explain": "Desalination competes inside the municipal and industrial distribution sectors."},
   {"q": "Switching from dry to once-through cooling mostly increases…", "options": ["withdrawals", "plant efficiency losses", "carbon emissions", "desalination use by farms"], "answer": 0, "explain": "Once-through cooling withdraws far more water per kWh."}],
 "glossary": [
   {"term": "Withdrawal", "def": "Water taken from a river, lake, aquifer or the sea."},
   {"term": "Consumption", "def": "The part of a withdrawal that is not returned to the source."},
   {"term": "Environmental flow requirement", "def": "Water left in rivers to protect ecosystems."},
   {"term": "Xanthos", "def": "The global hydrology model that supplies GCAM's runoff."},
   {"term": "Superwell", "def": "The groundwater extraction cost model behind GCAM's groundwater grades."}],
 "resources": [
   {"title": "GCAM documentation: Water supply", "url": D("supply_water.html"), "why": "Accessible water, groundwater, desalination and the basin price."},
   {"title": "GCAM documentation: Water demand", "url": D("demand_water.html"), "why": "The six sectors and cooling choice."},
   {"title": "GCAM documentation: Water details", "url": D("details_water.html"), "why": "Further detail on water accounting."}],
 "downloads": [HANDBOOK, KIT, deck("Week09-Land-water-and-bioenergy.pdf", "Week 9 slides: Land, water and bioenergy (PDF)")]})

# ---------------------------------------------------------------- 2.8
mods.append({
 "id": "2.8", "go": 2, "slug": "emissions-climate-policy-system", "title": "Emissions, climate and policy: the system together", "minutes": 60, "tag": "Whole system",
 "systems": ["economy", "energy", "land", "water", "climate", "policy"],
 "summary": "Put all the boxes back together. Follow emissions into Hector, see how GCAM implements carbon prices and caps, and trace five feedback loops that only an integrated model can show.",
 "outcomes": ["You can explain how GCAM's emissions reach Hector and become warming",
              "You can describe a carbon price, an emissions cap and a climate target in GCAM",
              "You can trace at least five cross-component feedback loops",
              "You can contrast GCAM's market equilibrium with an optimisation model"],
 "narration_en": ("This module puts all the boxes back together. Emissions come from burning fuels, from land use change and from other gases such as methane and nitrous oxide. "
   "In every period GCAM passes them to Hector, a simple climate model, which turns them into concentrations, radiative forcing and global temperature. "
   "Policies close the loop. A carbon price is the simplest: you choose the price path and the model finds the emissions. "
   "An emissions cap works the other way round: you choose the emissions and the model finds the price that achieves them, and a climate target goes one step further and finds the price path that meets a temperature or forcing goal. "
   "Because everything is linked, a single policy ripples through the system. A carbon price raises bioenergy demand, which raises land prices and food prices. "
   "It also pays landowners for carbon, which grows forests, and it raises the electricity price, which shifts transport and buildings. "
   "In this module you will run a tiny integrated model with a price and a cap, and see that both doors open onto the same room."),
 "narration_ar": ("تعيد هذه الوحدة تجميع كل الصناديق معًا. تأتي الانبعاثات من حرق الوقود، ومن تغيّر استخدام الأرض، ومن غازات أخرى مثل الميثان وأكسيد النيتروز. "
   "وفي كل فترة يمررها نموذج GCAM إلى نموذج هيكتور المناخي البسيط، الذي يحولها إلى تركيزات وتأثير إشعاعي ودرجة حرارة عالمية. "
   "وتُغلق السياسات الحلقة. أبسطها سعر الكربون: تختار مسار السعر ويجد النموذج الانبعاثات. "
   "أما سقف الانبعاثات فيعمل بالعكس: تختار الانبعاثات ويجد النموذج السعر الذي يحققها، ويذهب الهدف المناخي خطوة أبعد فيجد مسار السعر الذي يحقق هدفًا لدرجة الحرارة أو للتأثير الإشعاعي. "
   "ولأن كل شيء مترابط، تنتشر سياسة واحدة في النظام كله. فسعر الكربون يرفع الطلب على الطاقة الحيوية، مما يرفع أسعار الأرض والغذاء. "
   "ويدفع أيضًا لملاك الأراضي مقابل الكربون، فتنمو الغابات، ويرفع سعر الكهرباء، فيتغير النقل والمباني. "
   "في هذه الوحدة ستشغّل نموذجًا متكاملًا صغيرًا بسعر وبسقف، وترى أن البابين يفتحان على الغرفة نفسها."),
 "diagram": {
   "title": "The whole system and its feedbacks", "caption": "Five loops to trace: bioenergy–food, carbon–forest, electricity–transport, water–cooling, and emissions–climate–policy.",
   "nodes": [
     node("econ", "Economy", "population, GDP", "nw", "economy", "Population and GDP drive every demand (Go 2.1). In open-GDP mode energy feeds back to GDP.", w=160),
     node("mkt", "Markets and solver", "prices clear all markets", "n", "economy", "Broyden's method clears a few hundred markets each period (Go 2.2).", w=190),
     node("en", "Energy", "supply and demand", "ne", "energy", "Resources, conversion and end uses (Go 2.4, 2.5). Shares by nested logit (Go 2.3).", w=160),
     node("land", "Land and food", "profit-based logit", "w", "land", "Crops, pasture, forest and energy crops share land by profit (Go 2.6).", w=160),
     node("water", "Water", "235 basins", "sw", "water", "Basin prices from renewable, groundwater and desalination tiers (Go 2.7).", w=160),
     node("emis", "Emissions", "CO₂, LUC, non-CO₂", "c", "climate", "CO₂ from fuels × carbon coefficients, land-use change CO₂, and non-CO₂ gases with MAC curves (emissions.html).", w=180),
     node("hec", "Hector", "concentrations → °C", "se", "climate", "Each period GCAM passes emissions to Hector v3.2, which computes concentrations, forcing and global temperature (hector.html).", w=170),
     node("pol", "Policy", "price, cap, target", "e", "policy", "fixedTax price paths, emissions constraints solved for a price, or climate targets via target-finder mode (policies.html).", w=160),
     node("ref", "Reference vs policy", "the difference is the result", "s", "data", "Results are read as policy run minus reference run; never as forecasts.", w=200)],
   "edges": [edge("econ", "mkt", "demand drivers", "economy"), edge("mkt", "en", "prices", "economy"), edge("mkt", "land", "prices", "economy"),
             edge("en", "land", "bioenergy demand", "energy"), edge("water", "en", "cooling cost", "water"), edge("en", "emis", "fuel CO₂", "climate"), edge("land", "emis", "LUC CO₂", "climate"),
             edge("emis", "hec", "emissions", "climate"), edge("pol", "en", "carbon price", "policy"), edge("pol", "land", "land carbon", "policy"), edge("hec", "pol", "target check", "climate")],
   "tour": [
     {"focus": ["econ", "mkt"], "edges": [["econ", "mkt"]], "text": "Drivers set demands; the solver finds prices that clear every market in the period."},
     {"focus": ["en", "land"], "edges": [["mkt", "en"], ["mkt", "land"], ["en", "land"]], "text": "Loop 1, bioenergy–food: energy demand for biomass raises land and food prices."},
     {"focus": ["pol", "land"], "edges": [["pol", "land"]], "text": "Loop 2, carbon–forest: a carbon price on land pays for stored carbon and expands forests."},
     {"focus": ["water", "en"], "edges": [["water", "en"]], "text": "Loop 3, water–cooling: scarce basins raise water prices and shift power-plant cooling."},
     {"focus": ["pol", "en"], "edges": [["pol", "en"]], "text": "Loop 4, electricity–transport: carbon prices change electricity costs, shifting EVs and heat pumps."},
     {"focus": ["emis", "hec"], "edges": [["en", "emis"], ["land", "emis"], ["emis", "hec"]], "text": "All emissions go to Hector, which returns concentrations, forcing and temperature."},
     {"focus": ["hec", "pol", "ref"], "edges": [["hec", "pol"]], "text": "Loop 5, climate target: the price path is adjusted until the target is met. Read results as policy minus reference."}]},
 "components": {"caption": "Ways to tell GCAM about climate policy", "rows": [
     {"name": "Carbon price (fixedTax)", "purpose": "You set the price path; GCAM finds emissions", "analogy": "A toll at the door"},
     {"name": "Emissions constraint", "purpose": "You set emissions; GCAM finds the price", "analogy": "A gate that lets only so many through"},
     {"name": "Climate target", "purpose": "You set forcing, temperature or concentration; GCAM finds the price path", "analogy": "A thermostat setting"},
     {"name": "Linked GHG market", "purpose": "Non-CO₂ gases priced via GWPs", "analogy": "One currency for all gases"},
     {"name": "Standards (RPS, biofuel)", "purpose": "Bounds met by a solved tax or subsidy", "analogy": "A quota with a hidden price"}]},
 "sections": [
   {"heading": "Emissions", "html": "<p>CO₂ = fuel use × carbon coefficients (consistent with CDIAC), plus cement process CO₂, fugitive CO₂ and land-use change CO₂. Non-CO₂ greenhouse gases (CH₄, N₂O, F-gases) use marginal abatement cost (MAC) curves that read the carbon price:</p><div class=\"eq\">E<sub>t</sub> = A<sub>t</sub> · F<sub>t0</sub> · (1 − MAC(price<sub>t</sub>))</div><p>The MAC curves were updated in v8.9. Outputs: CO₂ in MtC/yr, non-CO₂ in Tg/yr; net CO₂ = CO₂ emissions by region + LUC emissions (" + cite("emissions.html") + ", " + cite("outputs_emissions.html") + ").</p>"},
   {"heading": "Climate: Hector inside GCAM", "html": "<p>Each period GCAM passes its emissions to <b>Hector v3.2</b>, which computes concentrations, radiative forcing and temperature. The coupling is one-way via emissions: climate impacts on yields or runoff are not automatic in core GCAM (" + cite("hector.html") + "). The kit's toy climate model (impulse-response carbon cycle + two-layer energy balance; not Hector) gives: flat 40 Gt/yr → <b>637 ppm and 2.53 °C</b> in 2100; net zero by 2050 → <b>443 ppm and 1.52 °C</b>.</p><div class=\"eq\">F = 5.35 · ln(C / C<sub>0</sub>) W/m²</div>"},
   {"heading": "Policy: price, cap, target", "html": "<p>A <b>carbon price</b> (<code>fixedTax</code>) is set by you; a <b>constraint</b> caps emissions and GCAM solves for the price; a <b>climate target</b> (target-finder mode, <code>find-path=1</code>) searches for the least-cost price path to a forcing, temperature or concentration goal and \"substantially increases run time\". Carbon prices are in 1990$ per tonne of carbon (" + cite("policies.html") + ", " + cite("user-guide.html") + ").</p><p>In the kit's toy system, a cap of −50% by 2050 is met by a price starting at <b>$2.5/t in 2025 growing 5% a year</b>: a price and a cap are two doors to the same room.</p>"},
   {"heading": "Five feedback loops", "html": "<ol><li><b>Bioenergy → land → food:</b> biomass demand raises energy-crop profit, shifting cropland and raising food prices.</li><li><b>Carbon price → land carbon → forests:</b> the land carbon subsidy expands forest; crops intensify.</li><li><b>Water scarcity → cooling:</b> rising basin prices move power from once-through to recirculating or dry cooling.</li><li><b>Electricity price → transport and buildings:</b> cheaper clean power pulls EVs and heat pumps in, raising electricity demand.</li><li><b>Emissions → Hector → target:</b> in target-finder mode the price path adjusts until the climate goal is met.</li></ol>"},
   {"heading": "Equilibrium versus optimisation", "html": "<p>GCAM finds market equilibria period by period with no foresight. Optimisation models such as MESSAGEix choose the least-cost system over the whole century with perfect foresight; the shadow price of an emissions cap plays the role of the carbon price. In the week 11 linear program (coal, gas, solar; 100 TWh) a 40 Mt cap gives coal 22.2, gas 50, solar 27.8 TWh at a shadow price of about $22 per tonne. Both paradigms answer \"what if\", not \"what will be\".</p>"}],
 "callouts": [
   {"after": 1, "kind": "gcam", "title": "In GCAM", "html": "<p>Queries: <b>CO2 emissions by region</b>, <b>global mean temperature</b>, <b>CO2 prices</b>. Policy example files ship in <code>input/policy</code>; the course carbon price file is <code>carbon_price_global.xml</code> and the net-zero setup is in <code>lab10_netzero_config_snippet.xml</code> (" + cite("policies_examples.html") + ").</p>"},
   {"after": 2, "kind": "trap", "title": "Units of the carbon price", "html": "<p>GCAM reports carbon prices in <b>1990$ per tonne of carbon</b>. Multiply by 12/44 to get $/tC from $/tCO₂, or by 44/12 the other way, and convert the dollar year before comparing with studies.</p>"},
   {"after": 3, "kind": "model", "title": "A useful mental model", "html": "<p>Push on one box of a mobile hanging from the ceiling and every other box moves. A single carbon price moves energy, land, water and emissions together; that movement is what an integrated model is for.</p>"}],
 "explorer": {"widget": "carbonprice", "intro": "Set a starting carbon price and its growth rate; watch the price path and the cut it buys on a simple cost curve.", "predict": "What yearly growth rate, from $25 in 2025, reaches a 60% cut by 2050?"},
 "code": [
   {"title": "A tiny integrated model: price vs cap", "lang": "python", "file": "labs/go2/m28_system.py", "runnable": True,
    "explain": "Power-sector logit, a land market for bioenergy with CCS, emissions and warming, under Reference, a carbon price and a cap. Try: lower the growth rate to 3% and predict whether the cap needs a higher or lower starting price.",
    "expected": "Reference         2050: CO2  15.92 Gt, solar share 0.54, bio land   40.8 Mha\nCarbon price      2050: CO2  -6.66 Gt, solar share 0.80, bio land  510.6 Mha\nCap -50% by 2050  2050: CO2   9.76 Gt, solar share 0.67, bio land   67.0 Mha\nThe cap is met by a carbon price starting at 2.5 $/t in 2025 and growing 5%/yr"},
   {"title": "Emissions to warming with a toy climate model", "lang": "python", "file": "labs/go2/m28a_climate.py", "runnable": True,
    "explain": "Impulse-response carbon cycle and two-layer energy balance (rounded textbook parameters; not Hector).",
    "expected": "Flat at 40 Gt  cumulative   3200 Gt -> CO2   637 ppm, warming 2100 2.53 C\nNet zero 2050  cumulative    580 Gt -> CO2   443 ppm, warming 2100 1.52 C"},
   {"title": "The same models in R", "lang": "r", "file": "labs/go2/m28_system.R", "runnable": False, "explain": "Identical numbers in base R; see also m28a_climate.R."},
   {"title": "Pull emissions, temperature and CO2 prices from GCAM (R)", "lang": "r", "file": "labs/go2/gcam/read_gcam.R", "runnable": False, "explain": "rgcam script for the course queries. Not run against a live database."}],
 "takeaways": ["Emissions from fuels, land and non-CO₂ gases go to Hector each period",
               "A carbon price fixes the price; a cap fixes emissions and GCAM finds the price",
               "Climate targets search for a price path and take much longer to run",
               "One policy moves energy, land, water and emissions together through feedback loops",
               "Read every result as policy minus reference, not as a forecast"],
 "quiz": [
   {"q": "Under an emissions constraint in GCAM, the carbon price is…", "options": ["set by the user", "solved by the model to meet the cap", "always zero", "taken from Hector"], "answer": 1, "explain": "The cap is a market; its solved price is the carbon price."},
   {"q": "Climate impacts on crop yields in core GCAM are…", "options": ["computed automatically by Hector", "not automatic; they must be imposed as inputs", "always included", "impossible"], "answer": 1, "explain": "The coupling is one-way via emissions (hector.html)."},
   {"q": "Which loop links bioenergy to food prices?", "options": ["Energy demand for biomass → land competition → crop prices", "Hector → yields", "Water → solar", "Trade → GDP"], "answer": 0, "explain": "Energy crops compete with food crops in the cropland nest."},
   {"q": "GCAM reports carbon prices in…", "options": ["2020$/tCO₂", "1990$/tC", "1975$/GJ", "€/t"], "answer": 1, "explain": "1990 dollars per tonne of carbon (outputs_prices.html)."},
   {"q": "The key difference between GCAM and MESSAGEix is that GCAM…", "options": ["has no prices", "solves period by period without foresight", "optimises the whole century", "has only one region"], "answer": 1, "explain": "Recursive-dynamic equilibrium versus intertemporal optimisation."}],
 "glossary": [
   {"term": "Hector", "def": "A simple open-source climate model coupled to GCAM."},
   {"term": "Radiative forcing", "def": "Extra energy trapped by greenhouse gases, in W/m²."},
   {"term": "MAC curve", "def": "Marginal abatement cost curve: how much of a gas is cut at each price."},
   {"term": "Emissions constraint", "def": "A cap on emissions met by a solved carbon price."},
   {"term": "Target finder", "def": "GCAM mode that searches for a price path meeting a climate target."},
   {"term": "Shadow price", "def": "In optimisation, the cost of tightening a constraint by one unit."}],
 "resources": [
   {"title": "GCAM documentation: Emissions", "url": D("emissions.html"), "why": "CO₂, non-CO₂, MAC curves and pollutants."},
   {"title": "GCAM documentation: Climate (Hector)", "url": D("hector.html"), "why": "How emissions reach Hector and what it returns."},
   {"title": "GCAM documentation: Policies", "url": D("policies.html"), "why": "Prices, constraints, targets and standards."},
   {"title": "GCAM documentation: Policy examples", "url": D("policies_examples.html"), "why": "XML templates for common policies."},
   {"title": "Hector", "url": "https://github.com/JGCRI/hector", "why": "The climate model itself, as an R package (v3.2.0)."},
   {"title": "FaIR (Python)", "url": "https://pypi.org/project/fair/", "why": "Another simple climate model, version 2.2.5, to compare with Hector."}],
 "downloads": [HANDBOOK, KIT, deck("Week10-Emissions-carbon-removal-and-policy.pdf", "Week 10 slides: Emissions, carbon removal and policy (PDF)"), deck("Week11-Optimisation-models.pdf", "Week 11 slides: Optimisation models (PDF)")]})

for m in mods:
    fn = os.path.join(OUT, "m" + m["id"].replace(".", "") + ".json")
    json.dump(m, open(fn, "w"), ensure_ascii=False, indent=1)
    print("wrote", fn)
