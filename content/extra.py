"""Additions for the November 2026 update: mind maps, question bank entries, memory hooks and palace stations
for modules 1.7–1.10 and 3.9. Imported by build.py after qbank, qhooks and mindmaps (it extends their objects)."""
from mindmaps import MM
from qbank import Q, add
from qhooks import H, PALACE

# ------------------------------------------------------------------ mind maps (one branch per section; leaves = (label, note))
MM["1.7"] = [
    ("Stocks and flows", "climate", "A stock accumulates; a flow is a rate that fills or drains it.", [
        ("Stock: photograph it", "CO2 in the air, cars on the road, plants standing."),
        ("Flow: needs a stopwatch", "Emissions per year, cars sold per year."),
        ("Next = now + in − out", "The one equation behind every stock.")]),
    ("Rising while falling", "climate", "CO2 rises until emissions drop below what sinks absorb.", [
        ("Inflow 30 > outflow 20", "Emissions fell, but the stock still rises."),
        ("Peak when in = out", "The stock peaks before emissions reach zero."),
        ("Same as the budget tub", "Module 1.2's bathtub, written as a model.")]),
    ("Two kinds of loop", "energy", "Reinforcing loops amplify; balancing loops damp.", [
        ("Reinforcing: warming → weak sinks", "More CO2 stays, so more warming."),
        ("Reinforcing: learning", "Cheaper solar → more built → cheaper still."),
        ("Balancing: price → demand", "GCAM's markets settle where loops balance.")]),
    ("Delays and inertia", "land", "Long-lived capital and slow climate response make timing matter.", [
        ("Plants last 40 years", "Today's investments emit for decades."),
        ("Vintages in GCAM", "Capital built in one period runs in later ones."),
        ("Late action costs more", "The old stock keeps emitting.")]),
]
MM["1.8"] = [
    ("Many ways to cut", "energy", "Options range from money-saving to very expensive.", [
        ("Efficiency: negative cost", "Saves money over its life."),
        ("Wind, solar, EVs", "Mid-cost options, falling fast."),
        ("CCS, air capture", "Expensive tail of the curve.")]),
    ("Reading the curve", "policy", "Width = tonnes; height = $ per tonne; sorted cheapest first.", [
        ("Width = potential", "Tonnes the option can cut each year."),
        ("Height = cost per tonne", "Below zero means it pays for itself."),
        ("Price line = cut-off", "Buy every bar below it.")]),
    ("Marginal vs average", "economy", "The price is the cost of the last tonne; most tonnes were cheaper.", [
        ("Marginal = price", "The last tonne bought."),
        ("Average far below", "$100 price, maybe $33 average."),
        ("Total = area of bars", "Not price × tonnes.")]),
    ("Technology moves bars", "energy", "Falling costs drop bars down the curve.", [
        ("Solar fell steeply", "Moved toward the cheap end."),
        ("Same price, more cut", "Cheaper tech buys more abatement."),
        ("GCAM: emerges by logit", "MAC curves only for non-CO2 gases.")]),
]
MM["1.9"] = [
    ("Three circles", "water", "Water, energy and food overlap at irrigation, cooling and bioenergy.", [
        ("Water for food", "Irrigation, the largest use."),
        ("Water for energy", "Cooling thermal plants."),
        ("Energy for water", "Pumping, treatment, desalination.")]),
    ("Bioenergy link", "land", "Energy crops tie land and food to the energy system.", [
        ("BECCS removes CO2", "Bioenergy plus carbon capture."),
        ("Competes with food", "Can raise land and food prices."),
        ("Big in deep cuts", "Many 1.5 °C scenarios rely on it.")]),
    ("Water has a price", "water", "GCAM prices water in 235 basins with three supply tiers.", [
        ("Renewable first", "Rivers, lakes, renewable groundwater."),
        ("Then groundwater, desal", "Costlier tiers as demand rises."),
        ("Price steers use", "Scarcity shows up as a rising price.")]),
    ("Side effects", "policy", "A policy in one system shows up in the others.", [
        ("Carbon price → bioenergy", "→ land and food prices."),
        ("Dry basin + thermal power", "→ water stress."),
        ("EVs → power → cooling", "Electrifying moves water demand.")]),
]
MM["1.10"] = [
    ("Three uncertainties", "climate", "Parameter, structural and scenario uncertainty.", [
        ("Parameter: numbers", "e.g. 0.27–0.63 °C per 1,000 Gt."),
        ("Structural: how built", "Different models, different answers."),
        ("Scenario: choices", "Society has not decided yet.")]),
    ("Ensembles", "economy", "Many runs or many models turn a line into a band.", [
        ("Perturbed parameters", "One model, sampled inputs."),
        ("Multi-model", "Many models, same scenario."),
        ("AR6 database", "A real multi-model ensemble.")]),
    ("Reading the range", "climate", "Median, likely range and probability of a threshold.", [
        ("Median = middle run", "Half above, half below."),
        ("Likely = middle 2/3", "17th to 83rd percentile."),
        ("P(>2 °C) = share of runs", "Holds only under the assumptions.")]),
    ("Scenarios ≠ forecasts", "policy", "Compare choices side by side; no probabilities.", [
        ("No odds on SSPs", "They describe choices."),
        ("Ask: what was varied?", "And what was held fixed?"),
        ("Back in 3.4 and 3.6", "Uncertainty plans and scenario discovery.")]),
]
MM["3.9"] = [
    ("Three defining choices", "neutral", "Foresight, economic scope and solution method.", [
        ("Foresight: myopic or perfect", "One period at a time, or all at once."),
        ("Scope: partial or general", "Energy-land markets, or the whole economy."),
        ("Method: clear, minimise, maximise", "Market clearing, LP, welfare, simulation, game.")]),
    ("How each solves", "energy", "One sentence per model.", [
        ("GCAM: auction per period", "Prices clear markets; logit shares."),
        ("MESSAGEix: one big LP", "Least discounted cost, perfect foresight."),
        ("REMIND: max welfare", "Ramsey planner over the century."),
        ("IMAGE: grid simulation", "Land allocated to suitable cells."),
        ("AIM-Hub: CGE", "Every market clears each year."),
        ("WITCH: regional game", "Nash or coalitions.")]),
    ("Structure shapes results", "economy", "Foresight, scope and logit vs LP leave fingerprints on results.", [
        ("Hotelling price path", "Rises at the discount rate under a budget."),
        ("GDP loss vs curve area", "Different cost measures."),
        ("Logit smooth, LP abrupt", "Unless constrained.")]),
    ("Transport across models", "energy", "Shared ancestry links GCAM and REMIND transport.", [
        ("GCAM: value of time + logit", "Module 3.2."),
        ("REMIND: EDGE-T", "A fork of GCAM's transport module."),
        ("MESSAGEix-Transport", "Detailed IIASA variant.")]),
    ("Choosing a model", "policy", "Match the model to the question; compare when structure matters.", [
        ("What-if detail → GCAM", "Open, energy-land-water."),
        ("Optimal price → DICE", "Cost–benefit."),
        ("Robust claim → compare", "Harmonised inputs, several models.")]),
]

# ------------------------------------------------------------------ question bank (kind, question, model answer) + hooks (intuition, image)
NEWQ = {
    "1.7": [
        ("Recall", "What is the difference between a stock and a flow?", "A stock is an accumulated amount measured at one instant (CO2 in the air); a flow is a rate that adds to or drains it (emissions per year)."),
        ("Explain", "Why does atmospheric CO2 keep rising after emissions start to fall?", "Because the stock rises whenever inflow (emissions) exceeds outflow (sinks). Falling emissions still above what sinks absorb keep adding to the stock."),
        ("Recall", "Give one reinforcing loop and one balancing loop from the climate–energy system.", "Reinforcing: warming weakens carbon sinks, so more CO2 stays, causing more warming. Balancing: higher energy prices reduce demand, which lowers prices."),
        ("Apply", "Emissions are 30 Gt a year and sinks absorb 20. A friend says CO2 is now falling. Correct them.", "Inflow 30 exceeds outflow 20, so the stock still rises by about 10 Gt a year; it only falls once emissions drop below 20."),
        ("Explain", "What are vintages and why do they matter for policy timing?", "Capital built in one period that keeps running in later ones. Long-lived plants and vehicles lock in emissions, so delayed policy must work harder."),
        ("Calculate", "A stock is 100, inflow 12 a year, outflow 8 a year. What is it after 5 years?", "100 + 5 × (12 − 8) = 120."),
        ("Apply", "Where in GCAM would you find stocks and flows of carbon?", "In Hector, GCAM's climate model, which links atmosphere, ocean and land carbon stocks with flows; and in land carbon stocks in the land model."),
        ("Explain", "Why is learning-by-doing a reinforcing loop?", "More installations lower costs through experience, and lower costs lead to more installations, so the change feeds itself."),
    ],
    "1.8": [
        ("Recall", "On a marginal abatement cost curve, what do the width and height of a bar show?", "Width: how many tonnes the option can cut per year. Height: its cost per tonne."),
        ("Explain", "Why does a carbon price buy every option cheaper than itself?", "For any option costing less than the price, cutting a tonne is cheaper than paying the price on it, so it is worth doing."),
        ("Calculate", "Options: 4 Gt at −$20, 2.5 Gt at $10, 7 Gt at $25. What is cut at $30, and the average cost?", "13.5 Gt; total cost = −80 + 25 + 175 = $120 per 13.5 Gt-year ≈ $8.9 per tonne."),
        ("Explain", "Why is the average cost of abatement below the carbon price?", "The price equals the cost of the last tonne; cheaper and negative-cost options were bought first, pulling the average down."),
        ("Apply", "Solar costs fall by half. What happens on the MAC curve and to the price needed for a given cut?", "Solar's bar drops down the curve, so more abatement is available cheaply and a lower carbon price achieves the same cut."),
        ("Recall", "Does GCAM use MAC curves for CO2 from energy?", "No. CO2 abatement emerges from technology competition by logit; GCAM uses MAC curves for non-CO2 gases."),
        ("Explain", "What does a negative-cost option mean?", "It saves money over its lifetime even without a carbon price, for example many efficiency measures, yet may not happen because of barriers."),
        ("Apply", "A minister says a $100 carbon price costs $100 for every tonne cut. Respond.", "Only the last tonne costs $100; the total cost is the area under the curve, much less than $100 × tonnes."),
    ],
    "1.9": [
        ("Recall", "Name the three main links in the water–energy–food nexus.", "Irrigation (water for food), cooling and fuel production (water for energy), and bioenergy (land for energy); also energy for pumping and desalination."),
        ("Explain", "Why does bioenergy link climate policy to food prices?", "Energy crops compete with food crops for land; a carbon price that rewards bioenergy raises land demand and can raise food prices."),
        ("Recall", "How many water basins does GCAM represent, and what are its supply tiers?", "235 basins; renewable water first, then non-renewable groundwater, then desalination, at rising cost."),
        ("Apply", "A dry basin builds more thermal power plants. What might GCAM show, and what option reduces it?", "Rising water demand and a higher water price, possibly groundwater or desalination use; dry cooling cuts water use at higher cost."),
        ("Explain", "Why might electrifying transport increase water demand?", "Electricity demand rises, and thermal power plants that generate it need cooling water."),
        ("Calculate", "Irrigation 60, cooling 15, cities 12; renewable supply 100. Food demand rises 30%. Is renewable water enough?", "Irrigation becomes 78; total 105 > 100, so the basin needs costlier groundwater."),
        ("Explain", "What is BECCS and why does it matter in deep mitigation?", "Bioenergy with carbon capture and storage; it can remove CO2 from the air, so many deep scenarios rely on it, with large land needs."),
        ("Apply", "Name one side effect to check when you add a carbon price in GCAM.", "Land-use change toward bioenergy or forest, food prices, and water demand in irrigated basins."),
    ],
    "1.10": [
        ("Recall", "Name the three kinds of uncertainty in IAM results.", "Parameter (numbers in the model), structural (how the model is built) and scenario (choices not yet made)."),
        ("Explain", "What is an ensemble and what does it give you?", "A set of runs differing in inputs or in model; it gives a distribution of results, a band instead of a line."),
        ("Recall", "What does the IPCC 'likely range' cover?", "About two thirds of outcomes, roughly the 17th to 83rd percentile."),
        ("Apply", "300 of 1,000 runs exceed 2 °C. How do you report it?", "About a 30% chance of exceeding 2 °C under the ensemble's assumptions."),
        ("Explain", "Why are scenarios not given probabilities?", "They describe choices society can still make; we compare them rather than predict which happens."),
        ("Explain", "Doubling the uncertainty in the climate response mainly changes what?", "The width of the range (the tails), much more than the median."),
        ("Apply", "Two models give different answers for the same scenario. What kind of uncertainty is this, and what do you do?", "Structural uncertainty; report both, explain the structural differences, and consider a wider multi-model comparison."),
        ("Recall", "Name a public multi-model scenario database.", "The IPCC AR6 Scenario Explorer hosted by IIASA."),
    ],
    "3.9": [
        ("Recall", "Classify GCAM by foresight, economic scope and solution method.", "Recursive dynamic (myopic), partial equilibrium, market clearing with logit choice."),
        ("Recall", "How does MESSAGEix solve?", "A linear programme minimising total discounted system cost over all periods at once (perfect foresight), linked to GLOBIOM and MACRO."),
        ("Explain", "Why do foresight models under a carbon budget give carbon prices rising at the discount rate?", "On a least-cost path, cutting a tonne must be equally costly in present value in every period, so the price grows at the discount rate (Hotelling rule)."),
        ("Recall", "What is WITCH's distinctive game-theoretic feature?", "Regions maximise their own welfare strategically given others' choices (Nash equilibrium), or jointly in coalitions."),
        ("Explain", "How does a CGE model such as AIM-Hub measure the cost of a policy, compared with GCAM?", "As lost GDP or consumption from all markets adjusting; GCAM reports the area under marginal abatement cost curves (partial equilibrium)."),
        ("Recall", "What is the link between REMIND's EDGE-T and GCAM?", "EDGE-T is described by its developers as a fork of the GCAM transport module."),
        ("Apply", "You need the optimal global carbon price from damages. Which model family, and why?", "A cost–benefit model such as DICE, because it weighs abatement costs against climate damages to find the optimum."),
        ("Apply", "Your result is driven by technology timing. How would you test whether model structure explains it?", "Run or compare a foresight model (MESSAGEix or REMIND) and a recursive one (GCAM) with harmonised inputs, and examine the differences."),
        ("Explain", "How does IMAGE represent land differently from GCAM?", "IMAGE allocates land on a spatial grid by suitability in a simulation framework; GCAM shares land among uses in land units by a profit-based logit."),
    ],
}
NEWH = {
    "1.7": [("Snapshot vs stopwatch.", "A camera photographs the bathtub; a stopwatch times the tap."),
            ("Inflow above outflow means up.", "A leaking boat still sinks if water pours in faster than you bail."),
            ("Loops feed or fight.", "A microphone squealing (reinforcing) vs a thermostat clicking off (balancing)."),
            ("Compare the tap and the drain.", "Tap at 30, drain at 20: the water still rises."),
            ("Old capital keeps running.", "A 40-year-old coal plant with a birthday cake still puffing smoke."),
            ("Net flow times years.", "Four extra marbles a year for five years: twenty more marbles."),
            ("Hector is made of boxes.", "Three jars, air, sea and soil, with straws between them."),
            ("Experience cuts cost.", "A pizza chef who gets faster with every pizza, so sells more pizzas.")],
    "1.8": [("Width is how much, height is how dear.", "A row of bars like a city skyline, wide warehouses and tall towers."),
            ("Cheaper than the price, do it.", "A limbo bar: every option that fits under the price passes."),
            ("Sum the bars below the line.", "Count the warehouses under the water line."),
            ("The last one is the dearest.", "Buying apples: the last one from the top branch costs most."),
            ("Cheaper tech sinks its bar.", "A solar panel bar sinking like a lift going down."),
            ("Logit for CO2, curves for the rest.", "A methane cow standing on a staircase-shaped curve."),
            ("Pays for itself.", "An LED bulb handing you money."),
            ("Area, not rectangle.", "Paint only the bars, not the whole wall up to the price line.")],
    "1.9": [("Three thirsts on one river.", "A farmer, a power plant and a city all sipping from one straw."),
            ("Fields can feed cars or people.", "A corn field with a fuel pump in the middle."),
            ("Cheapest water first.", "Three taps on the wall: free, dearer, very dear."),
            ("Heat needs cooling.", "A steaming power plant drinking from a dwindling river."),
            ("Electric cars drink indirectly.", "A plug-in car with a straw to a cooling tower."),
            ("Add the demands, compare with supply.", "Buckets lined up at a well that holds 100."),
            ("Grow, burn, capture.", "A tree going into a chimney and a pipe going underground."),
            ("Ripples in other ponds.", "A stone in the energy pond sends waves into the food pond.")],
    "1.10": [("Numbers, structure, choices.", "Three dice: one of numbers, one of shapes, one of ballot papers."),
             ("Many runs make a band.", "A hundred spaghetti strands forming a ribbon."),
             ("Two thirds in the middle.", "A pizza with the outer third of slices removed."),
             ("Share of runs is the chance.", "300 red marbles in a jar of 1,000."),
             ("Choices are compared, not bet on.", "A menu, not a betting slip."),
             ("Uncertainty widens tails.", "Stretching a rubber band from both ends: the middle stays put."),
             ("Different builds, different answers.", "Two chefs, same ingredients, different dishes."),
             ("A library of futures.", "A vast library where each book is a scenario.")],
    "3.9": [("Myopic, partial, market.", "An auctioneer with blinkers on, selling only energy and land."),
            ("One big optimisation.", "An engineer with a century-long spreadsheet."),
            ("Equal cost in present value.", "A price snowball growing at the bank's interest rate."),
            ("Regions as players.", "Seventeen chess players each guarding their own board."),
            ("GDP loss vs triangle area.", "A shrinking economy pie vs a triangle under a curve."),
            ("Same family tree.", "A GCAM car with a REMIND number plate."),
            ("Weigh costs and damages.", "A single brass scale with dollars on one side and storms on the other."),
            ("Compare structures, same inputs.", "Two cooks given identical baskets."),
            ("Grid vs shares.", "A chessboard of fields vs a pie of land.")],
}
for mid in NEWQ:
    add(mid, NEWQ[mid]); H[mid] = NEWH[mid]
    assert len(NEWQ[mid]) == len(NEWH[mid]), mid

PALACE[1]["stations"] += [
    ("1.7", "Hallway", "A bathtub in the hallway with the tap running and a plant drinking from the drain; a microphone squeals beside it."),
    ("1.8", "Study", "A city skyline of books on the desk, a limbo bar labelled with a carbon price sliding up through it."),
    ("1.9", "Laundry room", "A washing machine, a kettle and a flower pot all sharing one dripping tap."),
    ("1.10", "Attic", "A hundred strands of spaghetti hanging from the rafters, forming a ribbon; three dice on the floor."),
]
PALACE[3]["stations"] += [("3.9", "Common room", "Seven scientists at one table: an auctioneer, an engineer, a planner, a mapmaker, a market trader, a chess player and a judge with brass scales.")]
