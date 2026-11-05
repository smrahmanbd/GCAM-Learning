"""Simulation challenges per module (rendered by assets/js/challenges.js). Every challenge has a 'solution' that build-time
browser tests check against the toy model. Models: see window.IAMToyModels in challenges.js."""


def S(id, label, mn, mx, val, step=1, unit="", digits=0, hint=None):
    d = dict(id=id, label=label, min=mn, max=mx, value=val, step=step, unit=unit, digits=digits)
    if hint: d["hint"] = hint
    return d


def P(q, options, answer):
    return dict(q=q, options=options, answer=answer)


CH = {}
# ------------------------------------------------------------------ Go 1
CH["1.1"] = [
    dict(title="Keep the whole world consistent", level="Warm-up", icon="link", model="kaya", metric="co2", metricLabel="CO2 in 2050", unit=" Gt", digits=1, view="bars",
         fixed=dict(pop=9.7, gdp=20), controls=[S("ei", "Energy per $ (MJ)", 2, 7, 6.5, 0.1, digits=1), S("ci", "CO2 per energy (g/MJ)", 5, 70, 59)],
         op="<=", target=20, goal="People (9.7 bn) and income ($20k each) are fixed by the scenario. Change only the energy system so 2050 CO2 is <b>20 Gt or less</b>.",
         predict=P("Population and income both rise. Can CO2 still fall?", ["No, it must rise", "Yes, if energy per $ or CO2 per energy fall enough", "Only if population falls"], 1),
         hint="Each factor multiplies: halving CO2 per unit of energy halves emissions.", explain="An IAM keeps every part consistent: with more people and more income, only a cleaner, more efficient energy system can lower CO2.",
         solution=dict(ei=4, ci=25)),
    dict(title="What-if, not forecast", level="Core", icon="thermo", model="warming", metric="t2100", metricLabel="Warming in 2100", unit=" °C", digits=2, view="gauge", gmin=1, gmax=3,
         fixed=dict(peak=2025, grow=0, line=1.7), controls=[S("nz", "Year CO2 reaches zero", 2035, 2100, 2100)],
         op="<=", target=1.7, goal="Find a net-zero year that keeps warming in 2100 at <b>1.7 °C or below</b>.",
         hint="Cumulative CO2 must stay below about 1,330 Gt from 2020. A straight-line fall from 40 Gt emits 20 × years.", explain="Earlier net zero means a smaller running total. The model answers 'what if', it does not say which year will happen.",
         solution=dict(nz=2060)),
]
CH["1.2"] = [
    dict(title="Hit the 1.5 °C line", level="Core", icon="thermo", model="warming", metric="t2100", metricLabel="Warming in 2100", unit=" °C", digits=2, view="gauge", gmin=1, gmax=3,
         fixed=dict(grow=0, line=1.5), controls=[S("peak", "Year emissions peak", 2020, 2040, 2025), S("nz", "Year CO2 reaches zero", 2030, 2100, 2080)],
         op="<=", target=1.6, goal="Keep 2100 warming at <b>1.6 °C or less</b> (close to 1.5 °C).",
         predict=P("Which matters more for 2100 warming?", ["How fast emissions fall this year", "The total CO2 emitted until net zero", "The peak year only"], 1),
         hint="1.6 °C allows about (1.6 − 1.1) ÷ 0.45 × 1,000 ≈ 1,100 Gt. Peak early and reach zero by about 2045–2050.", explain="Warming follows the running total, so both an early peak and an early net zero are needed.",
         solution=dict(peak=2020, nz=2045)),
    dict(title="The cost of waiting", level="Stretch", icon="clock", model="warming", metric="t2100", metricLabel="Warming in 2100", unit=" °C", digits=2, view="gauge", gmin=1, gmax=3.5,
         fixed=dict(peak=2035, grow=1, line=1.8), controls=[S("nz", "Year CO2 reaches zero", 2040, 2100, 2090)],
         op="<=", target=1.8, goal="Emissions keep growing 1% a year until 2035. How early must net zero come to keep 2100 warming at <b>1.8 °C or below</b>?",
         hint="Growth until 2035 uses a lot of the budget, so the fall afterwards must be steep.", explain="Every year of delay uses budget, so the remaining path has to be steeper: the stock logic of the bathtub.",
         solution=dict(nz=2070)),
]
CH["1.3"] = [
    dict(title="Halve emissions with a growing economy", level="Core", icon="flame", model="kaya", metric="co2", metricLabel="CO2 in 2050", unit=" Gt", digits=1, view="bars",
         fixed=dict(pop=9.7), controls=[S("gdp", "GDP per person (k$)", 10, 30, 20), S("ei", "Energy per $ (MJ)", 2, 7, 6.5, 0.1, digits=1), S("ci", "CO2 per energy (g/MJ)", 5, 70, 59)],
         op="<=", target=16.5, goal="Population reaches 9.7 bn. Keep GDP per person at $20k or more and bring 2050 CO2 to <b>half of today (16.5 Gt) or less</b>.",
         predict=P("If people double their income, what must happen to CO2 per unit of GDP to keep emissions flat?", ["Fall by half", "Fall by a quarter", "Stay the same"], 0),
         hint="Kaya multiplies: 9.7 × 20 × 6.5 × 59 ÷ 1000 ≈ 74 Gt. You need the last two factors to fall by about 78% together.", explain="With people and income growing, only energy intensity and carbon intensity can do the work, and they must fall a lot.",
         solution=dict(gdp=20, ei=3.5, ci=24)),
]
CH["1.4"] = [
    dict(title="Set the toll", level="Warm-up", icon="scale", model="market", metric="q", metricLabel="Quantity of the dirty good sold", digits=0, view="gauge", gmin=0, gmax=50,
         controls=[S("tax", "Tax per unit", 0, 80, 0)], op="~", target=35, tol=1,
         goal="Demand is Q = 100 − P and supply Q = P − tax. Set the tax so that <b>35 units</b> are sold (± 1).",
         hint="Equilibrium quantity = (100 − tax) ÷ 2.", explain="A tax lifts the supply curve: buyers pay more, less is sold, and the government collects revenue.", solution=dict(tax=30)),
    dict(title="A price that halves emissions by 2050", level="Core", icon="coin", model="carbonprice", metric="cut2050", metricLabel="Cut below Reference in 2050", unit="%", view="line",
         fixed=dict(line=50), controls=[S("p0", "Carbon price in 2025 ($/t)", 0, 100, 10), S("g", "Yearly growth (%)", 0, 10, 2, 0.5, digits=1)], op=">=", target=50,
         goal="With the course's straight-line cost curve (price = 2 × cut%), reach a <b>50% cut in 2050</b>.", xTitle="Year",
         predict=P("A 50% cut needs what price in 2050 on this curve?", ["$50", "$100", "$200"], 1),
         hint="You need about $100 in 2050: e.g. $30 in 2025 growing 5% a year.", explain="Price and quantity are mirrors: to deliver a cut you need the price that buys it.", solution=dict(p0=30, g=5)),
]
CH["1.5"] = [
    dict(title="Which story fits a 2 °C world?", level="Core", icon="book", model="warming", metric="t2100", metricLabel="Warming in 2100", unit=" °C", digits=2, view="line",
         fixed=dict(line=2), controls=[S("peak", "Year emissions peak", 2020, 2060, 2050), S("grow", "Growth until the peak (%/yr)", 0, 3, 1.5, 0.1, digits=1), S("nz", "Net-zero year", 2040, 2100, 2100)],
         op="~", target=1.9, tol=0.1, goal="Build a path that ends between <b>1.8 and 2.0 °C</b> in 2100, roughly the band of SSP1-2.6.", xTitle="Year",
         predict=P("SSP1-2.6 means…", ["2.6 °C of warming", "A sustainability story with 2.6 W/m² forcing in 2100", "2.6% growth"], 1),
         hint="Aim for about 1,750 Gt from 2020: for example, peak in 2030 after 1% growth and reach net zero around 2090.", explain="A forcing label like 2.6 corresponds to a warming band; the SSP tells the social story that makes the path plausible.",
         solution=dict(peak=2030, grow=1, nz=2090)),
]
CH["1.6"] = [
    dict(title="Read it as Policy minus Reference", level="Core", icon="chart", model="carbonprice", metric="cut2050", metricLabel="Policy minus Reference in 2050", unit="%", view="line",
         fixed=dict(line=60), controls=[S("p0", "Carbon price in 2025 ($/t)", 0, 100, 25), S("g", "Yearly growth (%)", 0, 10, 3, 0.5, digits=1)], op=">=", target=60,
         goal="GCAM results are read as a difference from Reference. Design a carbon price that makes the policy run <b>60% below Reference in 2050</b>.", xTitle="Year",
         hint="A 60% cut needs $120 in 2050.", explain="The effect of a policy is the gap between two runs of the same world, with and without it.", solution=dict(p0=40, g=4.5)),
]
CH["1.7"] = [
    dict(title="Keep CO2 below 450 ppm", level="Core", icon="loop", model="feedback", metric="peak", metricLabel="Peak CO2", unit=" ppm", view="line",
         fixed=dict(line=450), controls=[S("nz", "Year emissions reach zero", 2040, 2120, 2090), S("k", "Strength of sinks (%/yr)", 0.5, 3, 1.5, 0.1, digits=1), S("f", "Feedback: sinks weaken per °C (%)", 0, 30, 10)],
         op="<=", target=450, goal="Keep the CO2 stock's peak at <b>450 ppm or below</b>. You cannot make sinks stronger than 1.5% (leave it there or lower).", xTitle="Year",
         predict=P("Emissions fall in a straight line to zero in 2070. When does CO2 peak?", ["In 2070", "Well before 2070", "After 2070"], 1),
         hint="Bring net zero forward to about 2055.", explain="The stock peaks when emissions fall to the level the sinks absorb, before net zero. A stronger feedback raises the peak.",
         solution=dict(nz=2055, k=1.5, f=10)),
    dict(title="Feel the reinforcing loop", level="Stretch", icon="warn", model="feedback", metric="end", metricLabel="CO2 in 2150", unit=" ppm", view="line",
         fixed=dict(nz=2080, k=1.0, line=400), controls=[S("f", "Feedback: sinks weaken per °C (%)", 0, 30, 0)], op=">=", target=400,
         goal="With net zero in 2080 and weak sinks (1% a year), find the feedback strength at which CO2 is <b>still above 400 ppm in 2150</b>.", xTitle="Year",
         hint="Try values above 20%.", explain="A reinforcing loop slows the recovery: weaker sinks keep CO2 high for longer after emissions stop.", solution=dict(f=25)),
]
CH["1.8"] = [
    dict(title="Buy 20 Gt of cuts", level="Core", icon="coin", model="macc", metric="ab", metricLabel="Cut bought", unit=" Gt", digits=1, view="bars",
         controls=[S("price", "Carbon price ($/t)", -20, 320, 0, 5)], op=">=", target=20,
         goal="Find the <b>lowest</b> carbon price that buys at least 20 Gt CO2 a year of cuts. (Three stars if you also stay at or below $100.)",
         predict=P("At $100 per tonne, is the average cost of the tonnes bought above, equal to or below $100?", ["Above", "Equal", "Below"], 2),
         hint="Read the bars from the left and add up widths until you pass 20.", explain="The price buys every bar below it: efficiency, methane, renewables, EVs and industry switching reach 21 Gt at $90.", solution=dict(price=90)),
]
CH["1.9"] = [
    dict(title="Feed more people without desalination", level="Core", icon="drop", model="nexus", metric="stress", metricLabel="Water demand (% of renewable supply)", unit="%", view="bars",
         fixed=dict(food=150, power=100, pop=100, bio=0, dry=False), controls=[S("eff", "Irrigation efficiency gain (%)", 0, 50, 0)], op="<=", target=100,
         goal="Food demand rises to 150%. Keep the basin within its <b>renewable supply (≤ 100%)</b> using irrigation efficiency.",
         predict=P("Without any change, does the basin need costlier water?", ["Yes", "No"], 0),
         hint="Irrigation is 60 × 1.5 = 90 units; with cooling and cities you need it below about 73.", explain="Efficiency in the largest user frees water for everyone; otherwise the basin climbs to groundwater and desalination.", solution=dict(eff=20)),
]
CH["1.10"] = [
    dict(title="A two-in-three chance of staying under 2 °C", level="Core", icon="dice", model="uncertainty", metric="prob", metricLabel="Chance of exceeding the threshold", unit="%", view="line",
         fixed=dict(thr=2.0), controls=[S("cum", "CO2 emitted 2020–2100 (Gt)", 300, 4000, 2500, 50)], op="<=", target=33,
         goal="Find the cumulative CO2 that keeps the chance of exceeding 2 °C at <b>33% or less</b>.", xTitle="Warming in 2100 (°C)",
         predict=P("Can you emit as much as the median says, and still be 67% safe?", ["Yes", "No, you must emit less"], 1),
         hint="The median line hits 2 °C at 2,000 Gt; for a 67% chance you need noticeably less.", explain="Raising your confidence shrinks the budget: uncertainty is not a reason to wait, it is a reason to be cautious.", solution=dict(cum=1700)),
]
# ------------------------------------------------------------------ Go 2 (one per module: the same concepts, one level deeper)
CH["2.1"] = [dict(title="Drivers decide the baseline", level="Core", icon="people", model="kaya", metric="co2", metricLabel="CO2 in 2050", unit=" Gt", digits=1, view="bars",
         fixed=dict(ei=4.5, ci=50), controls=[S("pop", "Population (bn)", 8, 11, 9.7, 0.1, digits=1), S("gdp", "GDP per person (k$)", 10, 30, 20)], op="<=", target=35,
         goal="Technology is fixed. Which population and income combination keeps 2050 CO2 at <b>35 Gt or less</b>? (This is what switching SSP does.)",
         hint="CO2 = pop × gdp × 4.5 × 50 ÷ 1000.", explain="Socioeconomic drivers alone can swing the baseline widely, which is why the SSP choice matters.", solution=dict(pop=9, gdp=17))]
CH["2.3"] = [dict(title="Calibrate a share by cost", level="Core", icon="dice", model="logit", metric="s0", metricLabel="Electric share", unit="%", digits=0, view="bars",
         fixed=dict(names=["Electric", "Petrol", "Diesel"], c1=50, c2=55), controls=[S("c0", "Electric cost", 30, 90, 70), S("lam", "Logit exponent", -12, -1, -6, 0.5, digits=1)], op="~", target=50, tol=3,
         goal="Make the electric option take about <b>half the market (47–53%)</b>.",
         hint="Electric must be cheaper than both rivals; a steeper exponent amplifies small cost gaps.", explain="The relative-cost logit spreads the market by cost ratios; the exponent sets how sharply buyers respond.", solution=dict(c0=46, lam=-6))]
CH["2.5"] = [dict(title="Richer travellers value time", level="Core", icon="car", model="trncost", metric="rail", metricLabel="Rail share", unit="%", view="bars",
         fixed=dict(carMoney=8, carT=1.0, busMoney=2, busT=1.8, railMoney=5, railT=0.9, beta=0.25), controls=[S("wage", "Hourly wage ($)", 2, 40, 2)], op=">=", target=40,
         goal="Rail is fast but not cheap. At what wage does rail win <b>at least 40%</b> of trips?",
         hint="Value of time = half the wage per hour in this toy.", explain="As wages rise, time costs dominate money costs, so fast modes gain share.", solution=dict(wage=30))]
CH["2.8"] = [dict(title="Cap or price: find the mirror", level="Core", icon="scale", model="carbonprice", metric="cut2050", metricLabel="Cut in 2050", unit="%", view="line",
         fixed=dict(line=70), controls=[S("p0", "Carbon price in 2025 ($/t)", 0, 100, 20), S("g", "Yearly growth (%)", 0, 10, 3, 0.5, digits=1)], op="~", target=70, tol=2, xTitle="Year",
         goal="A cap demands a <b>70% cut in 2050</b> (± 2). Find a carbon price path that delivers exactly it: this is the shadow price GCAM would report.",
         hint="70% needs $140 in 2050.", explain="A constraint solved as a market gives the price that meets it: price and cap are mirrors.", solution=dict(p0=42, g=5))]
# ------------------------------------------------------------------ Go 3
CH["3.1"] = [dict(title="Is your run trustworthy? Converge the solver", level="Core", icon="gear", model="logit", metric="s0", metricLabel="Share computed", unit="%", view="bars",
         fixed=dict(names=["Solar", "Gas", "Coal"], c1=60, c2=70), controls=[S("c0", "Solar cost (after the add-on)", 30, 90, 60), S("lam", "Logit exponent", -12, -1, -3, 0.5, digits=1)], op="~", target=60, tol=3,
         goal="A colleague reports a <b>60% solar share</b> (± 3) and you must reproduce it. Find settings that rebuild their number, then note them: this is reproducibility.",
         hint="With costs 60/70 you need cheaper solar or a steeper exponent.", explain="Rebuilding a number needs every input: version, add-ons, logit settings. Record them all.", solution=dict(c0=48, lam=-4))]
CH["3.2"] = [
    dict(title="Load factors decide the cost per passenger", level="Core", icon="people", model="loadfactor", metric="ratio", metricLabel="Car cost ÷ bus cost per pkm", digits=2, view="bars",
         fixed=dict(carVkm=0.5, busVkm=2.0), controls=[S("lf", "Car load factor (persons)", 1, 4, 1.5, 0.1, digits=1), S("blf", "Bus load factor (persons)", 5, 60, 15)], op="<=", target=1,
         goal="Make the car <b>no more expensive per passenger-km than the bus</b>.",
         predict=P("Cost per passenger-km equals…", ["Vehicle cost × load factor", "Vehicle cost ÷ load factor", "Fuel cost only"], 1),
         hint="Car $/pkm = 0.5 ÷ load factor; bus = 2.0 ÷ load factor.", explain="An emptier bus is expensive per passenger; load factors are a strong and uncertain lever in transport studies.", solution=dict(lf=2.5, blf=8)),
    dict(title="Value of time shifts the modes", level="Stretch", icon="clock", model="trncost", metric="car", metricLabel="Car share", unit="%", view="bars",
         fixed=dict(carMoney=6, carT=0.8, busMoney=1.5, busT=1.6, railT=1.0, beta=0.3, wage=15), controls=[S("railMoney", "Rail fare ($)", 1, 10, 6, 0.5, digits=1), S("votf", "Value of time (share of wage)", 0.2, 1, 0.5, 0.05, digits=2)], op="<=", target=40,
         goal="Wage is $15/h. Use the rail fare and the value-of-time assumption to bring the <b>car share to 40% or less</b>.",
         hint="Cheaper rail helps; a higher value of time favours the fast modes (car and rail).", explain="GCAM's generalised cost adds wage-based time cost, so the value-of-time assumption shapes mode shares.", solution=dict(railMoney=2, votf=0.5)),
]
CH["3.3"] = [dict(title="Where does your estimate sit?", level="Core", icon="book", model="uncertainty", metric="prob", metricLabel="Share of studies above your result", unit="%", view="line",
         fixed=dict(cum=2000), controls=[S("thr", "Your study's 2100 warming (°C)", 1.5, 3.5, 2.5, 0.05, digits=2)], op="~", target=50, tol=5, xTitle="Warming in 2100 (°C)",
         goal="Treat the distribution as the literature's estimates. Place your result <b>in the middle of the literature (45–55% above it)</b>.",
         hint="The median is at 1.1 + 0.45 × 2 = 2.0 °C.", explain="Reading the literature as a distribution tells you whether a result is central or an outlier that needs explaining.", solution=dict(thr=2.0))]
CH["3.4"] = [dict(title="Design the policy matrix: price versus cap", level="Core", icon="grid", model="carbonprice", metric="cut2050", metricLabel="Cut in 2050", unit="%", view="line",
         fixed=dict(line=80), controls=[S("p0", "Carbon price 2025 ($/t)", 0, 100, 20), S("g", "Growth (%/yr)", 0, 10, 4, 0.5, digits=1)], op=">=", target=80, xTitle="Year",
         goal="Your matrix has a 'net-zero-consistent' carbon tax column. Find a price path giving at least an <b>80% cut in 2050</b>, so it matches the cap column.",
         hint="80% needs $160 in 2050.", explain="Pairing a cap with an equivalent price lets you compare instruments that reach the same outcome.", solution=dict(p0=50, g=5))]
CH["3.5"] = [dict(title="Write the cost add-on", level="Core", icon="pen", model="logit", metric="s0", metricLabel="Battery-electric share", unit="%", view="bars",
         fixed=dict(names=["Battery EV", "Petrol car", "Hybrid"], c1=0.45, c2=0.48, lam=-6), controls=[S("c0", "BEV cost after add-on ($/vkm)", 0.25, 0.7, 0.6, 0.01, digits=2)], op=">=", target=50,
         goal="Your add-on scales the BEV cost. Find the cost at which BEVs reach <b>at least 50% share</b>.",
         predict=P("An add-on XML…", ["Replaces the whole input set", "Overrides only the values it names", "Must contain every region"], 1),
         hint="BEV must be clearly cheaper than both rivals: try about 0.36.", explain="Add-ons override named inputs; a cost multiplier is the simplest transport technology lever.", solution=dict(c0=0.36))]
CH["3.6"] = [dict(title="Explain the change with LMDI", level="Core", icon="chart", model="lmdi", metric="change", metricLabel="Change in transport CO2", unit="%", digits=0, view="bars",
         fixed=dict(a=60), controls=[S("s", "Mode-structure effect (%)", -30, 10, 0), S("i", "Energy-intensity effect (%)", -40, 0, -10), S("c", "Carbon-factor effect (%)", -80, 0, -10)], op="<=", target=-30,
         goal="Activity grows 60% by 2050. Combine structure, intensity and carbon effects so transport CO2 <b>falls by 30% or more</b>.",
         hint="Effects multiply: 1.6 × (1 + s) × (1 + i) × (1 + c) must be ≤ 0.7.", explain="Decomposition shows which lever does the work; in most deep scenarios the carbon factor (cleaner fuels) dominates.", solution=dict(s=-10, i=-25, c=-40))]
CH["3.7"] = [dict(title="Downscale to a country", level="Core", icon="map", model="downscale", metric="s2050", metricLabel="Country share in 2050", unit="%", digits=0, view="line",
         fixed=dict(s0=20), controls=[S("s1", "Target share at convergence (%)", 10, 60, 20), S("T", "Convergence year", 2030, 2100, 2100, 5)], op="~", target=30, tol=1, xTitle="Year",
         goal="The country has 20% of regional demand today. Choose a target share and convergence year so its <b>2050 share is 30%</b> (± 1).",
         hint="Share moves in a straight line from 20% to the target by the convergence year.", explain="Convergence downscaling is simple and transparent, but the target and year are assumptions to report and test.", solution=dict(s1=40, T=2080))]
CH["3.8"] = [dict(title="Report the range, not just the median", level="Core", icon="warn", model="uncertainty", metric="prob", metricLabel="Chance of exceeding 1.5 °C", unit="%", view="line",
         fixed=dict(thr=1.5), controls=[S("cum", "Cumulative CO2 in your scenario (Gt)", 300, 3000, 1500, 50)], op="<=", target=50, xTitle="Warming in 2100 (°C)",
         goal="Before you write 'consistent with 1.5 °C', find the emissions that give at most a <b>50% chance</b> of exceeding it.",
         hint="The median hits 1.5 °C at about 890 Gt.", explain="Honest reporting states the probability, not just the central estimate.", solution=dict(cum=850))]
CH["3.9"] = [
    dict(title="Foresight: the Hotelling price", level="Core", icon="clock", model="hotelling", metric="p2050", metricLabel="Carbon price 2050", unit=" $/t", view="line",
         controls=[S("p0", "Price in 2025 ($/t)", 10, 100, 10), S("r", "Discount rate (%)", 1, 8, 2, 0.5, digits=1)], op="~", target=100, tol=5, xTitle="Year",
         goal="A foresight model's price rises at the discount rate. Find a path reaching <b>$100 in 2050</b> (± 5).",
         predict=P("Under a fixed budget, a perfect-foresight least-cost carbon price…", ["Stays flat", "Rises at the discount rate", "Falls over time"], 1),
         hint="$30 × 1.05^25 ≈ $102.", explain="This Hotelling path is a fingerprint of intertemporal models such as MESSAGEix and REMIND.", solution=dict(p0=30, r=5)),
    dict(title="WITCH: close the free-rider gap", level="Core", icon="handshake", model="game", metric="total", metricLabel="Global abatement", digits=1, view="bars",
         fixed=dict(b=2), controls=[S("coop", "How far regions cooperate (%)", 0, 100, 0, 5)], op=">=", target=6,
         goal="Two regions each gain 2 per unit of global abatement. Find the cooperation level that reaches <b>global abatement of 6 or more</b>.",
         hint="Acting alone gives 2 each (4 total); full cooperation gives 4 each (8 total).", explain="Each region alone ignores the benefit it gives the other; cooperation internalises it.", solution=dict(coop=50)),
    dict(title="DICE: the optimal cut", level="Stretch", icon="scale", model="dice", metric="mu", metricLabel="Optimal share cut", unit="%", view="line",
         controls=[S("r", "Discount rate (%)", 1, 6, 4, 0.1, digits=1), S("dmg", "Damage coefficient (×)", 0.5, 3, 1, 0.1, digits=1)], op=">=", target=60, xTitle="Share cut (%)",
         goal="In this toy cost–benefit model, make the optimal cut <b>at least 60%</b>.",
         hint="A lower discount rate and higher damages both raise the optimum.", explain="In cost–benefit models the discount rate and damage function largely decide how much to cut.", solution=dict(r=1.5, dmg=1.5)),
]
