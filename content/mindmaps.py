"""Hand-written mind maps, one per module.

Each module maps to a list of branches, one per section, in the same order as the module's sections.
Branch = (short title, system or None for the module's first system, one-line summary, [(leaf label, leaf explanation), ...]).
Leaf labels stay short (about 36 characters) so they fit two lines; explanations show in the side panel.
"""

MM = {}

# ------------------------------------------------------------------ Go 1
MM["1.1"] = [
    ("A what-if machine", "neutral", "An IAM joins economy, energy, land, water, emissions and climate into one calculation, to inform decisions.", [
        ("Integrated: parts talk", "A change in one part shows up in all the others."),
        ("Assessment: informs decisions", "The purpose is to compare choices, not to predict the future."),
        ("Recipe calculator, not oracle", "You choose the ingredients; it returns a world that adds up. You judge it by consistency and assumptions."),
    ]),
    ("Consistency", "climate", "Every box must agree with every other: energy used = energy made, emissions match fuel burned.", [
        ("Energy used = energy made", "No energy appears or disappears between boxes."),
        ("CO2 = energy × CO2 per unit", "600 units at 0.06 Gt each gives 36 Gt; halve the 0.06 and emissions halve."),
        ("What a spreadsheet lacks", "Separate guesses can contradict each other; a consistent model cannot."),
    ]),
    ("Inputs and outputs", "policy", "Inputs are assumptions you choose; outputs are what the model works out from them.", [
        ("Inputs: people, income, costs, policy", "Population in 2050, income per person, solar cost, carbon price."),
        ("Outputs: mix, prices, CO2, warming", "The model calculates the energy mix, prices, emissions and temperature."),
        ("Test: could a modeller choose it?", "If another modeller could reasonably pick a different value, it is an input."),
    ]),
    ("Two families", "economy", "Cost-benefit models ask how much to cut; process-based models ask how a goal can be met.", [
        ("Cost-benefit: DICE", "A few equations for one world; weighs cutting cost against warming damage."),
        ("Process-based: GCAM, MESSAGEix", "Thousands of inputs, many regions; power plants, cars, crops, forests chosen by cost."),
        ("This course uses GCAM", "GCAM is process-based, open source, from PNNL's JGCRI."),
    ]),
]

MM["1.2"] = [
    ("Fuel to fever", "climate", "Emissions raise concentration, which raises forcing, which raises temperature.", [
        ("Emissions → concentration (ppm)", "Burning fuel and clearing land add CO2 to the air."),
        ("Forcing (W/m²) → temperature", "More CO2 traps more heat, which warms the planet."),
        ("CO2 stays for centuries", "So the total ever emitted matters, not this year's emissions."),
    ]),
    ("Running total", "climate", "Warming grows almost in a straight line with cumulative CO2.", [
        ("≈ 0.45 °C per 1,000 Gt CO2", "A best estimate; the IPCC likely range is about 0.27 to 0.63 °C."),
        ("2,000 Gt more ≈ +0.9 °C", "Double the emissions, double the extra warming."),
        ("Only net zero stops the rise", "Turning the tap down slows warming; it does not stop it."),
    ]),
    ("Carbon budget bathtub", "climate", "The tap is yearly emissions, the drain is slow nature, the rim is the budget.", [
        ("Tap ≈ 40 Gt CO2 a year", "Today's yearly emissions pour in."),
        ("1.5 °C: about 500 Gt from 2020", "50% chance; for 2 °C (67%) about 1,150 Gt."),
        ("Flat: 12.5 years; straight-line cut: 25", "500 ÷ 40 = 12.5. A straight line to zero is a triangle: ½ × 40 × T = 500 gives T = 25."),
    ]),
    ("In GCAM: Hector", "climate", "GCAM hands its emissions to Hector, a simple climate model, at every time step.", [
        ("Emissions from energy and land", "GCAM's sectors work out the emissions."),
        ("Hector: ppm, forcing, °C", "It computes concentrations, forcing and temperature."),
        ("You run Hector in Go 2", "Module 2.8 opens the climate box."),
    ]),
]

MM["1.3"] = [
    ("Services, not energy", "energy", "People want light, warmth and travel; energy flows from primary to final to services.", [
        ("Primary energy: what nature gives", "Coal, oil, gas, sunlight, wind."),
        ("Final energy: electricity, petrol", "Power plants and refineries convert primary into final energy."),
        ("IAMs choose at every step", "So they can compare supply options (solar) with demand options (better buildings)."),
    ]),
    ("Every step loses some", "energy", "Conversion and delivery lose energy at each step.", [
        ("100 coal → 40 electricity", "A 40%-efficient power plant."),
        ("10% grid loss → 36 reach homes", "About two thirds are lost on the way."),
        ("Save 1 at home, save 2.8 at source", "100 ÷ 36 ≈ 2.8 units of coal."),
    ]),
    ("Kaya identity", "economy", "CO2 = people × income per person × energy per $ × CO2 per energy.", [
        ("Always true: units cancel", "It is an accounting identity, not a theory."),
        ("Society: people, income", "The first two factors."),
        ("Technology: energy/$, CO2/energy", "The last two factors."),
    ]),
    ("Multiply, never add", "economy", "Combine changes in the factors by multiplying their ratios.", [
        ("Avalon: 1.2 × 1.5 × 0.7 × 0.8", "Population +20%, income +50%, energy per $ −30%, CO2 per energy −20%."),
        ("= 1.008: CO2 up under 1%", "Growth is almost exactly cancelled by cleaner technology."),
        ("Adding gives +20%: wrong", "+20 + 50 − 30 − 20 is not how ratios combine."),
    ]),
]

MM["1.4"] = [
    ("Prices balance markets", "economy", "Prices move until what is offered equals what is wanted.", [
        ("Farmers' market at closing", "Unsold tomatoes: cut the price; sold out by noon: raise it."),
        ("1000 − 4p = 6p → p = 100", "Toy market: quantity 600 at the equilibrium."),
        ("GCAM: every good, region, period", "A balancing price for every fuel and crop."),
    ]),
    ("Carbon price picks winners", "policy", "New cost = start cost + emission factor × carbon price.", [
        ("At $50/t: coal 105, gas 90", "60 + 0.9 × 50 and 70 + 0.4 × 50."),
        ("Solar stays at 80", "Zero emissions, so the carbon price adds nothing."),
        ("Gas beats coal above $20/t", "Solar beats gas above $25/t (illustrative)."),
    ]),
    ("Markets are shared", "energy", "Real models share each market by relative cost instead of picking one winner.", [
        ("Cheapest gets most, not all", "Costs differ by place, tastes differ."),
        ("The rule is a logit", "You meet it in Go 2, module 2.3."),
        ("No sudden flips", "Shares move smoothly as costs change."),
    ]),
    ("Discounting", "economy", "Value today = future amount ÷ (1 + r)^years.", [
        ("$100 in 100 years at 1.5%: $22.56", "At 3%: $5.20; at 5%: $0.76."),
        ("One number, thirtyfold change", "The chosen rate decides how much the future counts."),
        ("Used by cost-benefit models", "Process models use prices to choose technologies."),
    ]),
]

MM["1.5"] = [
    ("What a scenario is", "policy", "A consistent what-if story with numbers, not a forecast or a probability.", [
        ("Story + spreadsheet", "Like a choose-your-own-adventure book with numbers on every page."),
        ("Not a forecast", "It says what would follow if the assumptions held."),
        ("A set is not a list of odds", "Scenarios are not ranked by likelihood."),
    ]),
    ("A story and a number", "economy", "SSP = story about society; the number = forcing in 2100 in W/m².", [
        ("Five SSP stories", "Placed by how hard they make it to cut emissions and to adapt."),
        ("Number = W/m², not °C", "Inherited from the older RCPs; higher means more warming."),
        ("SSP2-4.5 ≈ 2.7 °C", "Middle of the road, 4.5 W/m² in 2100."),
    ]),
    ("The scenario matrix", "climate", "Stories in rows, forcing levels in columns.", [
        ("Five headline cells (AR6)", "SSP1-1.9, SSP1-2.6, SSP2-4.5, SSP3-7.0, SSP5-8.5."),
        ("Some cells cannot be reached", "SSP3's regional rivalry cannot reach the lowest forcing."),
        ("Above no-policy is not policy", "Forcing above a story's baseline is not a policy case."),
    ]),
    ("IPCC categories", "policy", "AR6 sorted 1,202 pathways into categories C1 to C8 by warming.", [
        ("C1: 1.5 °C, little overshoot", "Over 50% chance."),
        ("C3: below 2 °C; C8: above 4 °C", "Check wording against AR6 WGIII Box SPM.1."),
        ("CMIP7 (2026): seven scenarios", "Each from one IAM team; GCAM made the high one, H."),
    ]),
]

MM["1.6"] = [
    ("GCAM in a paragraph", "neutral", "Open-source model from PNNL/JGCRI: 32 regions, 300+ land units, 235 basins.", [
        ("32 regions, 235 basins", "Plus more than 300 land units."),
        ("2021 base year, 5-year steps", "Forward to 2100."),
        ("No foresight: recursive-dynamic", "Each step is solved on its own."),
    ]),
    ("An auction every period", "economy", "Prices of fuels, crops, land and water adjust until every market clears.", [
        ("Supply = demand everywhere", "All markets at once."),
        ("Technologies share by cost", "Cheaper wins more, not everything."),
        ("Emissions → Hector → °C", "The climate model returns temperature."),
    ]),
    ("Policy minus Reference", "policy", "The effect of a policy is the difference between two runs.", [
        ("Reference: no new policy", "A yardstick, not a forecast."),
        ("Same inputs plus one change", "Change only what you want to test."),
        ("Never read a run alone", "Results only mean something as differences."),
    ]),
    ("Toll or gate", "policy", "A carbon price fixes cost; an emissions limit fixes quantity: mirrors on one curve.", [
        ("Toll: fix price, find cut", "A $50 toll gives a 25% cut on the toy curve."),
        ("Gate: fix cut, find price", "A 60% cut needs $120."),
        ("Same cost curve", "Price = 2 × cut% in the toy example."),
    ]),
    ("What IAMs cannot tell", "neutral", "Findings are conditional: keep the model, question the inputs.", [
        ("Who pays and who gains", "Regions are large; households are averaged."),
        ("How people really behave", "Choices follow costs and calibration, not politics or habits."),
        ("Whether assumptions come true", "E.g. future costs, carbon removal later in the century."),
    ]),
]

# ------------------------------------------------------------------ Go 2
MM["2.1"] = [
    ("What it represents", "economy", "People and income, by region and period: assumptions, usually from an SSP.", [
        ("Inputs, not results", "In the standard setup population and GDP are chosen, not solved."),
        ("32 regions, 5-year steps", "From a 2021 base year to 2100."),
        ("Sets the scale of everything", "Every other module must serve this demand."),
    ]),
    ("Building population and GDP", "economy", "GDP = population × labour-force share × output per worker.", [
        ("Population: UN, then SSP", "Maddison and UN before 2015; the SSP database after."),
        ("Productivity grows at g", "Output per worker × (1 + g)^5 each step."),
        ("GDP from SSP (OECD model)", "Future GDP comes from the SSP database."),
    ]),
    ("Income drives demand", "energy", "GDP per person is the bridge to energy, food and water demand.", [
        ("D ∝ income^α × price^β", "Industry and transport service demand."),
        ("Floorspace: Gompertz curve", "Rises fast with income, then saturates."),
        ("Municipal water: elasticity 0.37", "Food and air-pollution controls also follow income."),
    ]),
    ("Kaya: splitting drivers", "climate", "CO2 = population × GDP/person × energy/GDP × CO2/energy.", [
        ("Ratios multiply", "Never add percentages."),
        ("Green road: 0.072", "1.10 × 5.70 × 0.132 × 0.087: emissions 7% of 2020."),
        ("Rocky road: 1.393", "1.52 × 2.22 × 0.53 × 0.79: a 39% rise."),
    ]),
    ("Macro module", "economy", "Since v7, KLEM can let energy and policy change GDP; v9.0 extends it to KLEAM.", [
        ("KLEM: capital, labour, energy, materials", "A nested CES production function."),
        ("Open-GDP mode", "A carbon policy changes GDP and consumption directly."),
        ("KLEAM adds agriculture", "Its own labour and capital (v9.0)."),
    ]),
]

MM["2.2"] = [
    ("What it represents", "economy", "GCAM finds prices so that supply equals demand in every market, every period.", [
        ("Market = a good in a place", "Energy carriers, crops and land, water by basin."),
        ("Agents submit bids", "Supply and demand sectors respond to trial prices."),
        ("Partial equilibrium", "Energy, land and water in detail; the wider economy via GDP."),
    ]),
    ("One market by hand", "economy", "Excess demand F(p) = demand − supply; solve F = 0.", [
        ("No tax: p = 100, q = 600", "1000 − 4p = 6p."),
        ("$50 tax: p = 127, q = 492", "1000 − 4p = 6p − 270."),
        ("Root finders find the sign change", "Bisection or Brent give the same answer."),
    ]),
    ("Many markets at once", "energy", "A carbon price on oil shifts electricity and biomass, which feeds back on oil.", [
        ("All prices found together", "A vector root finder is needed."),
        ("Toy: oil 9.04, elec 31.60, bio 5.25", "With a $50 carbon price."),
        ("Every gap below 2×10⁻¹⁰", "All excess demands cleared."),
    ]),
    ("GCAM's solver", "neutral", "Broyden's method in log prices, helped by bisection and a preconditioner.", [
        ("Broyden: B·δx = −F(x)", "A cheap secant approximation of the Jacobian."),
        ("A few hundred solved markets", "Each scaled to a common size."),
        ("Tolerance 0.001; check the log", "Example settings; max-model-calcs 2500."),
    ]),
    ("Recursive dynamics", "policy", "Agents decide with what they know now; the model then steps forward.", [
        ("No crystal ball", "Each 5-year period solved on its own."),
        ("Regrettable plants are possible", "A 2030 coal plant may be stranded by a 2040 policy."),
        ("Contrast: MESSAGEix optimises", "Chooses the whole century with perfect foresight (2.8)."),
    ]),
]

MM["2.3"] = [
    ("Not cheapest-takes-all", "energy", "A logit turns costs into smooth shares: cheaper wins more, never everything.", [
        ("No flip when costs cross", "Real markets never switch all at once."),
        ("Costs vary by site, investor", "And some preferences are unmeasured."),
        ("Smooth shares", "Small cost changes give small share changes."),
    ]),
    ("Relative-cost logit", "energy", "sᵢ = αᵢ cᵢ^γ ÷ Σ αⱼ cⱼ^γ, with γ < 0.", [
        ("γ = −4: 54 / 29 / 17%", "Coal $60, gas $70, solar $80, equal weights."),
        ("γ = −1: 38 / 33 / 29%", "Weak response to cost."),
        ("γ = −10: 79 / 17 / 4%", "Strong response: close to cheapest-takes-all."),
    ]),
    ("Absolute-cost logit", "energy", "Shares depend on cost differences, not ratios.", [
        ("sᵢ ∝ αᵢ exp(β cᵢ)", "GCAM derives β from the exponent you enter."),
        ("Copes with near-zero or negative costs", "Useful once subsidies and carbon prices enter."),
        ("Used for DAC, transport nests", "Direct air capture and passenger transport."),
    ]),
    ("Share weights", "economy", "Calibrated so the logit reproduces 2021 shares; future values are assumptions.", [
        ("α ∝ share ÷ c^γ", "Observed 30/50/20% gives weights 1 : 3.088 : 2.107."),
        ("Phase in new technologies", "Low at first, rising toward neutral."),
        ("A scenario lever, not a fact", "Report future share weights as assumptions."),
    ]),
    ("Nesting", "energy", "Sector → subsector → technology → cooling, each level with its own logit.", [
        ("γ = −3 between fuels", "Electricity subsectors in the reference example."),
        ("γ = −10 among coal technologies", "Close substitutes react strongly."),
        ("Kit: coal 48.2, gas 19.1, solar 32.6%", "Fossil nest at −6 inside, −3 outside."),
    ]),
]

MM["2.4"] = [
    ("Resources", "energy", "Fossil stocks sit on graded supply curves; renewables are annual flows.", [
        ("Graded curve: $3 → $12/GJ", "Toy price 3.6, 6.0, 11.0 at 200, 800, 1,400 EJ used."),
        ("Renewables: Q = Qmax·Pᵇ/(Pmidᵇ+Pᵇ)", "Half the maximum at the mid price."),
        ("Technical change lowers costs", "Extraction gets cheaper over time."),
    ]),
    ("Technology cost", "energy", "Cost = non-energy + fuel × coefficient + GHG price × emissions − by-products.", [
        ("Levelised capital + O&M", "Capex × CRF ÷ (CF × 8.76) + fixed and variable O&M."),
        ("Gas: 61.2 → 97.9 $/MWh", "From no carbon price to $100/t."),
        ("Solar: 45.4 $/MWh at any price", "Illustrative kit numbers."),
    ]),
    ("Value factor", "energy", "Wind and solar costs are divided by a value factor that falls with their share.", [
        ("PLCOE = LCOE ÷ VF", "Since v7.3, no backup pairing."),
        ("PV: 0.972 − 1.443 × share", "Then divided by 0.903; wind 0.91 − 1.2 × share."),
        ("From ReEDS (US); no storage", "May break down above about 75% VRE."),
    ]),
    ("Electricity, fuels, hydrogen", "energy", "Nested power with cooling; refining; 12 hydrogen routes; CCS and DAC.", [
        ("Fuel → technology → cooling", "Up to five cooling types."),
        ("Refining: oil, bio, CTL, GTL", "Up to 8 biomass technologies, some with CCS."),
        ("H2: 10 central + 2 forecourt", "From up to 7 primary sources."),
    ]),
    ("Vintages", "energy", "Plants built in one period keep running, so the fleet changes slowly.", [
        ("Profit shutdown", "Output falls as variable cost nears price."),
        ("S-curve lifetime", "Retirements spread over time."),
        ("Exogenous scalars", "E.g. a US coal vintage at 0.5 in 2021, 0 by 2040."),
    ]),
]

MM["2.5"] = [
    ("Services, not fuels", "energy", "Demand sectors produce services, then choose technologies and fuels.", [
        ("Floorspace, output, pkm, tkm", "The services GCAM models."),
        ("D ∝ income^α × price^β", "Service demand responds to both."),
        ("α 0.6, β −0.3: 100 → 151.6", "Doubling income; 134.2 if travel is 50% dearer."),
    ]),
    ("Buildings", "energy", "Floorspace follows income; heating and cooling follow degree-days.", [
        ("10 income deciles (v7.1)", "Residential demand is split by income."),
        ("Gompertz floorspace", "Rises with income and density, then saturates."),
        ("Degree-days link to climate", "Computed from gridded data by helios."),
    ]),
    ("Industry", "energy", "Steel, chemicals, aluminium, cement, fertiliser, food and more.", [
        ("Steel: BOF, EAF scrap, EAF DRI", "Three routes compete."),
        ("Fertiliser from crop output", "A direct farm-to-energy link."),
        ("Construction, mining, ag energy", "Also inside industry."),
    ]),
    ("Transport: money + time", "economy", "Technology cost per pkm, plus the value of travel time for modes.", [
        ("Pⱼ = (P_fuel·I + N) ÷ L", "Fuel intensity, non-fuel cost, load factor."),
        ("Time cost = W × V ÷ S", "Wage, time-value multiplier, speed."),
        ("Car share 3% → 61.7%", "As the wage rises from $2/h to $40/h (kit toy)."),
    ]),
]

MM["2.6"] = [
    ("What it represents", "land", "AgLU decides land use, crops, livestock and land carbon.", [
        ("Water-basin land units", "300+ in the text, 396 in the table."),
        ("Irrigated/rainfed × high/low", "Every crop has four management types."),
        ("Production can intensify", "When prices rise."),
    ]),
    ("Profit and land shares", "land", "Land is shared by a logit on profit per hectare.", [
        ("π = (price − cost) × yield", "Wheat $240/ha; energy grass $300/ha."),
        ("Shares 44% / 56%", "240 / 540 and 300 / 540."),
        ("Grass at $40: 29%; $90: 71%", "Shares follow the grass price."),
    ]),
    ("Bioenergy land", "energy", "Land = energy ÷ (yield × energy content).", [
        ("10 EJ → 55.6 Mha", "At 10 t/ha and 18 GJ/t."),
        ("100 EJ → 556 Mha", "Halve the yield: 1,111 Mha."),
        ("Cropland ≈ 1.5 billion ha", "Large targets compete with food."),
    ]),
    ("Land carbon", "climate", "LUC emissions = change in area × carbon density.", [
        ("Eₜ = AₜDₜ − Aₜ₋₁Dₜ₋₁", "Vegetation and soil separately."),
        ("Clearing fast, regrowth slow", "Forests mature over about 30 to 100 years."),
        ("Carbon price pays for stock", "Acts as a subsidy for holding carbon."),
    ]),
    ("Calibration and yields", "land", "Profit scalers match base-year land; yields grow by assumption.", [
        ("λ from base-year shares", "Invert the share equation."),
        ("FAO yield growth", "Scaled ±50% by SSP."),
        ("Exponents in input files", "Not on the documentation pages."),
    ]),
]

MM["2.7"] = [
    ("What it represents", "water", "Water balanced in 235 basins: withdrawals and consumption by sector.", [
        ("235 basins", "The water accounting units."),
        ("Agriculture by basin", "Other sectors by region, mapped to basins."),
        ("Withdrawal vs consumption", "Taken versus not returned."),
    ]),
    ("Six demand sectors", "water", "Irrigation, electricity, manufacturing, primary energy, livestock, municipal.", [
        ("Irrigation = coeff × crop output", "km³ per Mt."),
        ("Municipal: income^0.37, price^−0.33", "Per-capita demand."),
        ("Power: five cooling systems", "Chosen by a cost logit."),
    ]),
    ("Supply tiers and price", "water", "Renewable water, then groundwater, then desalination; a basin price clears.", [
        ("Accessible water minus EFR", "From Xanthos runoff and reservoir storage."),
        ("Groundwater, then desalination", "At rising cost."),
        ("Irrigation pays 5% of price", "IRR_PRICE_SUBSIDY_MULT."),
    ]),
    ("Cooling decides the tier", "energy", "Toy basin: cooling choice moves demand past the renewable limit.", [
        ("Dry-ish cooling: 48.6 km³", "Price stays at $0.01/m³."),
        ("Once-through: 66.0 km³", "Exceeds the 50 km³ renewable supply."),
        ("Price jumps to $0.05/m³", "Groundwater sets the price."),
    ]),
    ("Water–energy–land", "neutral", "Energy for water, water for energy, water for land.", [
        ("Desalination: 2.75 kWh/m³", "Reverse osmosis; thermal 58.3."),
        ("Energy production withdraws", "Seawater 95% of it in the Middle East."),
        ("Water cost in crop profit", "Shifts irrigated versus rainfed land."),
    ]),
]

MM["2.8"] = [
    ("Emissions", "climate", "Fuel CO2, process and LUC CO2, and non-CO2 gases with MAC curves.", [
        ("CO2 = fuel × carbon coefficient", "Plus cement, fugitive and land-use change."),
        ("Non-CO2: MAC curves", "Abatement responds to the carbon price (updated v8.9)."),
        ("Units: MtC/yr, Tg/yr", "Net CO2 = fossil + LUC."),
    ]),
    ("Hector inside GCAM", "climate", "Hector v3.2 turns emissions into ppm, forcing and temperature.", [
        ("One-way coupling", "No automatic climate impacts on yields or runoff."),
        ("F = 5.35 ln(C/C₀)", "CO2 forcing in W/m²."),
        ("Toy: 2.53 vs 1.52 °C", "Flat 40 Gt/yr versus net zero by 2050."),
    ]),
    ("Price, cap, target", "policy", "Fix the price, fix the emissions, or fix the climate goal.", [
        ("fixedTax: you set the price", "In 1990$ per tonne of carbon."),
        ("Constraint: GCAM finds price", "The shadow price of the cap."),
        ("Target finder: slow", "Searches the least-cost price path."),
    ]),
    ("Five feedback loops", "neutral", "One policy moves energy, land, water and emissions together.", [
        ("Bioenergy → land → food", "Energy crops raise food prices."),
        ("Carbon price → forests", "Land carbon subsidy expands forest."),
        ("Clean power → EVs, heat pumps", "Electricity demand rises; water drives cooling."),
    ]),
    ("Equilibrium vs optimisation", "economy", "GCAM clears markets period by period; MESSAGEix optimises the century.", [
        ("GCAM: no foresight", "Period-by-period equilibrium."),
        ("LP: cap's shadow price", "Plays the role of the carbon price."),
        ("Week 11 LP: about $22/t", "Coal 22.2, gas 50, solar 27.8 TWh."),
    ]),
]

# ------------------------------------------------------------------ Go 3
MM["3.1"] = [
    ("The pipeline", "neutral", "Source data → gcamdata → XML → configuration → solver → database → queries.", [
        ("gcamdata builds the XML", "An R package processes IEA, UC Davis, FAO, SSP data."),
        ("BaseX output database", "Read with ModelInterface, rgcam or gcamreader."),
        ("Release 9.1; docs describe v8.2", "Cite the exact version; units changed in v8.5."),
    ]),
    ("Markets, not optimisation", "economy", "Fₘ(p) = Dₘ(p) − Sₘ(p) = 0 for every market, solved by Broyden in log prices.", [
        ("Recursive-dynamic", "No one in GCAM knows a policy is coming."),
        ("Read main_log.txt", "A finished run is not necessarily a solved one."),
        ("Tolerance 0.001, 2,500 calcs", "Example settings; solution-tolerance ≥ Broyden ftol."),
    ]),
    ("Calibration", "policy", "Share-weights make every base year match observed energy use.", [
        ("Share-weights fit the data", "Whatever the costs say."),
        ("They absorb what costs miss", "Infrastructure, preferences, regulation, data error."),
        ("Future paths are assumptions", "Report them."),
    ]),
    ("Reproducibility", "neutral", "Be able to rebuild: version, inputs, configuration, analysis.", [
        ("Version: tag and commit", "Never edit the release in place."),
        ("Inputs and config in Git", "One configuration or batch file per scenario set."),
        ("Scripted analysis", "Every figure from code; no manual edits."),
    ]),
]

MM["3.2"] = [
    ("What is in the box", "energy", "Four final demands: passenger, freight, international aviation and shipping.", [
        ("trn_pass: price −1.25, income 1.0", "Per-capita; SSP1 income 0.8."),
        ("trn_freight: −0.65, 0.75", "Not per-capita."),
        ("Units: billion pkm (v8.5+)", "v8.2 used million pkm."),
    ]),
    ("The nesting tree", "energy", "Supplysectors → tranSubsectors (modes) → tranTechnologies (drivetrains).", [
        ("trn_pass → road → LDV → 4W", "Pass-through nodes hand the choice down."),
        ("Cars: Liquids, Hybrid, NG, BEV, FCEV", "Four size classes."),
        ("Walk 4.8 km/h, Cycle 15 km/h", "Non-motorised modes, no fuel."),
    ]),
    ("Step 1: cost per pkm", "economy", "Pⱼ = (P_fuel · Iⱼ + Nⱼ) ÷ Lⱼ.", [
        ("N: capital via CRF(10%, 10 y)", "Plus maintenance, insurance, tolls ÷ annual vkm."),
        ("Load factor 2.33, 14,000 vkm/yr", "Middle East compact car (UCD data)."),
        ("OTAQ_trn_data_EMF37.csv", "Holds most vehicle costs; edit it, not only UCD."),
    ]),
    ("Step 2: value of time", "economy", "Mode cost adds W × V ÷ S, with W = GDP per person ÷ 2,000 h.", [
        ("V: car 0.82, bus 0.808, air 1.244", "Time-value multipliers."),
        ("Only on passenger modes", "Never on freight or drivetrain choice."),
        ("GDP deflated to 1975$ (v8.5)", "Inside the code."),
    ]),
    ("Step 3: two logits", "energy", "Mode choice uses relative-cost logits; drivetrain choice absolute-cost.", [
        ("Modes: relative (ratios)", "The default when logit.type is empty."),
        ("Drivetrains: absolute (differences)", "Every tranSubsector, and the 4W sector."),
        ("Absolute copes with ≤ 0 costs", "Matters with subsidies and carbon prices."),
    ]),
    ("Step 4: how much travel", "economy", "Dₜ = Dₜ₋₁ (Y ratio)^α (P ratio)^β (N ratio).", [
        ("α = 1 for passengers", "Travel per person grows with income."),
        ("Price is the nest's average cost", "Passed up from below."),
        ("v8.8: H2 inputs renamed", "Fuel-cell share-weights cut from 1 to 0.5."),
    ]),
]

MM["3.3"] = [
    ("How it was built", "neutral", "Compiled 23 Oct 2026; DOIs checked; unconfirmed items marked [U].", [
        ("Journals, PNNL/OSTI, KAPSARC", "The search sources."),
        ("[U] = not confirmed", "DOI, pages or model list unchecked."),
        ("Summaries are a map", "Read the papers before citing."),
    ]),
    ("A: Foundations", "energy", "How GCAM transport was built.", [
        ("Kyle & Kim 2011", "Early LDV competition; EVs and H2 lower 2095 CO2."),
        ("Mishra et al. 2013", "The UC Davis transport database."),
        ("Calvin et al. 2019 (GMD)", "The paper to cite for structure."),
    ]),
    ("B: Comparisons", "policy", "Model comparisons and behavioural realism.", [
        ("Transport lags 10–30 years", "Pietzcker et al. 2014."),
        ("Cuts from intensity, fuel switch", "Edelenbosch et al. 2017."),
        ("Carbon price alone is not enough", "McCollum et al. 2018: preferences matter."),
    ]),
    ("C: Applications", "energy", "GCAM studies of modes, fuels and countries.", [
        ("Zero-emission transport by 2050", "Speizer et al. 2024, high case."),
        ("Hydrogen cuts costs up to 22%", "Wolfram et al. 2024."),
        ("BEV damages 2–3.5× lower", "Sadavarte et al. 2025."),
    ]),
    ("D: Saudi Arabia, downscaling", "policy", "GCAM-KSA studies and DSCALE.", [
        ("2060 CO2: 418 → 115 Mt", "No policy versus NZ2060 (Kamboj et al. 2024)."),
        ("Early action: −38 to −72% cost", "Apeaning et al. 2025."),
        ("DSCALE: 143 countries", "Sferra et al. 2026."),
    ]),
    ("Known, disputed, unknown", "climate", "Where the literature agrees, disagrees, or is silent.", [
        ("Known: BEVs cheapest for cars", "Freight and aviation hardest."),
        ("Disputed: mode shift, H2 vs biofuels", "And the speed of BEV uptake."),
        ("Unknown: fleets, Gulf hindcasts", "Explicit vehicle stocks; charging load."),
    ]),
]

MM["3.4"] = [
    ("Topic to question", "policy", "A research question names a decision, a metric and a comparison.", [
        ("Topic: 'EVs in Saudi Arabia'", "Not yet answerable."),
        ("Decision + metric + comparison", "E.g. ZEV standard vs equal-effort carbon price."),
        ("Separate policy from structure", "Test results against a different logit exponent."),
    ]),
    ("Scenario logic", "policy", "Background world, levers, policies: change one thing at a time.", [
        ("Background: SSP + current policy", "With the matching transport file."),
        ("Levers: BEV cost, share-weights", "Load factors, rail speed, new fuels."),
        ("Design matrix: 12 runs", "Reference, levers, policies, interactions, SSPs."),
    ]),
    ("Price or quantity?", "policy", "Carbon tax, emissions constraint or portfolio standard.", [
        ("Tax: price in, emissions out", "'What does $X buy?'"),
        ("Constraint: emissions in, price out", "Net-zero targets and budgets."),
        ("Match instruments on one dimension", "Equal emissions or equal price."),
    ]),
    ("Plan uncertainty", "neutral", "3–6 inputs with low, central, high values and a source.", [
        ("One-at-a-time", "Cheap; misses interactions."),
        ("Full factorial", "Clean, but explodes in size."),
        ("Latin hypercube", "Efficient for many inputs."),
    ]),
    ("Validity", "neutral", "Why should anyone believe it?", [
        ("Calibration check", "Base year matches IEA by construction."),
        ("Hindcast 2015 → 2024", "E.g. Saudi fuel-price reforms, EV sales."),
        ("Benchmark and face validity", "AR6 database; sector experts."),
    ]),
]

MM["3.5"] = [
    ("Add-on anatomy", "neutral", "An add-on repeats the path from <world> to the value it changes.", [
        ("Loads after the core file", "Later files update existing objects."),
        ("Names must match exactly", "A typo silently creates an unused object."),
        ("region → sector → mode → tech", "Names come from gcamdata mapping files."),
    ]),
    ("Lever 1: costs", "economy", "Non-fuel cost is an input-cost per vehicle-km.", [
        ("minicam-non-energy-input", "In $ per vehicle-km."),
        ("÷ load factor → $ per pkm", "Eq. 3.3."),
        ("Fuel: coefficient × market price", "minicam-energy-input."),
    ]),
    ("Lever 2: share-weights", "policy", "Where calibration and hidden assumptions live.", [
        ("Set in global-technology-database", "For future transport share-weights."),
        ("Interpolation rules override", "The default rule re-imposes its own path."),
        ("Add a fixed rule", "To make your value stick."),
    ]),
    ("Lever 3: service and speed", "economy", "Load factor, speed and elasticities change how people travel.", [
        ("Load factor divides per-vehicle", "Costs and intensities."),
        ("Speed sets time cost", "Faster modes look cheaper to richer travellers."),
        ("Elasticities set total travel", "Income and price."),
    ]),
    ("Lever 4: policies", "policy", "Carbon price, constraint, or a credit-market standard.", [
        ("fixedTax: a price path", "1990$ per tonne of carbon."),
        ("constraint: a solved price", "linked-ghg-policy for other gases."),
        ("ZEV standard = credit market", "Cars demand 0.3 credits; ZEVs supply 1."),
    ]),
    ("Batch runs", "neutral", "The scenario matrix as a file.", [
        ("ComponentSet = one dimension", "E.g. BEV cost."),
        ("FileSet = one level", "Lists its add-on files."),
        ("BatchMode = 1", "Point BatchFileName to the file."),
    ]),
    ("Go through gcamdata", "neutral", "Systematic changes: edit source tables and rebuild.", [
        ("OTAQ overrides UCD", "Editing UCD alone may change nothing."),
        ("User-modification chunk", "A clean record passed to the driver."),
        ("Check year column names", "'2030' vs X2030."),
    ]),
]

MM["3.6"] = [
    ("Step 1: extract", "neutral", "One script, every query, one tidy table.", [
        ("Never copy by hand", "From ModelInterface or elsewhere."),
        ("Main_queries.xml", "Service by mode, new-tech output, final energy."),
        ("Check levers took effect", "Query load factors and speeds."),
    ]),
    ("Step 2: compare", "policy", "Policy minus Reference: absolute, relative, per capita, cumulative.", [
        ("Toy: BEV-low 2050 = 26 Mt", "Versus 84 Mt in Reference."),
        ("Carbon price: 11 Mt by 2100", "Versus 142 Mt."),
        ("Fast wage raises car share", "Time value at work."),
    ]),
    ("Step 3: decompose", "climate", "LMDI splits a CO2 change into factors with no residual.", [
        ("CO2 = Σ A·S·I·F", "Activity, structure, intensity, carbon."),
        ("L(a,b) = (a−b)/(ln a − ln b)", "The logarithmic mean weight."),
        ("Effects add up exactly", "−38.65 Mt in the kit example."),
    ]),
    ("Step 4: stress-test", "neutral", "Tornado for one-at-a-time; scenario discovery for combinations.", [
        ("Tornado: BEV cost dominates", "Range 0.84 of BEV share."),
        ("Coverage and density", "Judge the box: 80% and 92% in the kit."),
        ("PRIM or classification tree", "Lab 13 uses rpart."),
    ]),
    ("Step 5: benchmark", "climate", "Compare with AR6 or CMIP7 for the same variables.", [
        ("IAMC variable names", "Final Energy|Transportation, etc."),
        ("Outside the range is allowed", "But explain why."),
        ("Filter by similar carbon price", "Lab 12 shows how."),
    ]),
]

MM["3.7"] = [
    ("A country region", "policy", "GCAM-KSA: Saudi Arabia as a 33rd region with national data.", [
        ("Add to iso_GCAM_regID.csv", "So gcamdata splits it from its parent."),
        ("Check UCD_ctry.csv mappings", "Transport parameters are by UCD region."),
        ("Re-check calibration", "Base-year energy must match national balances."),
    ]),
    ("Downscaling", "economy", "Split a regional path among countries; they must add back up.", [
        ("Convergence year", "Countries move from own trend to the regional pattern."),
        ("Harmonise to the total", "Rescale so countries sum to the region."),
        ("DSCALE: 143 countries", "Sferra et al. 2026; the course uses a simplification."),
    ]),
    ("No fleets in GCAM", "energy", "GCAM tracks service by technology, not vehicles.", [
        ("'Service output (new)' ≈ sales", "The closest proxy."),
        ("No counts or survival curves", "Nor second-hand markets."),
        ("Sales lead, fleet lags", "The gap is large and slow."),
    ]),
    ("Coupling", "neutral", "Soft links exchange numbers through files until models agree.", [
        ("Stock model: fleets", "Sales shares back as share-weights."),
        ("LEAP: national detail", "Electricity mix and demand corrections back."),
        ("Hourly model: charging peaks", "Grid and storage cost signals back."),
    ]),
]

MM["3.8"] = [
    ("Blind spots", "neutral", "What GCAM transport cannot see, and what you can do.", [
        ("No vehicle stock", "Use a sales proxy or couple a stock model."),
        ("One representative traveller", "Add disutility costs by consumer group."),
        ("Generic aviation and ship fuels", "Add a dedicated sector for SAF mandates."),
    ]),
    ("Ethics", "policy", "Whose future, whose cost?", [
        ("Reliance on carbon removal", "Report gross and net emissions."),
        ("Distribution", "A single consumer cannot show who pays."),
        ("Numbers read as forecasts", "Show ranges and state what the model cannot tell."),
    ]),
    ("Describing GCAM", "neutral", "Follow the JGCRI community guidelines.", [
        ("'GCAM v9.1 (tag gcam-v9.1)'", "Never just 'GCAM'."),
        ("List every modification", "Rename substantial variants, e.g. GCAM-KSA."),
        ("Cite docs DOI and repository", "Plus sector model papers."),
    ]),
    ("IAMC format", "climate", "Report in standard variables so results compare with AR6 and CMIP7.", [
        ("model, scenario, region, variable", "Then one column per year."),
        ("Energy Service|Transportation", "Passenger and Freight."),
        ("Convert carbon prices", "From 1990$/tC to US$2010/t CO2."),
    ]),
    ("Reproducible package", "neutral", "Archive everything needed to rebuild every figure.", [
        ("Version, add-ons, config", "Plus gcamdata chunks and queries."),
        ("Scripts and results table", "The database itself is optional."),
        ("README with run log", "Archive with a DOI, e.g. Zenodo."),
    ]),
]
