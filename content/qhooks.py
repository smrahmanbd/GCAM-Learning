"""Intuition and memory hooks for the question bank, in the same order as qbank.Q within each module.
Each entry: (intuition: why the answer makes sense, hook: a vivid image to remember it by).
Also PALACE: one memory-palace walk per go, one station per module."""

H = {}

H["1.1"] = [
    ("One question, many linked parts: change one and the rest must follow.", "Picture a giant mobile over a baby's cot: economy, energy, land, water, air. Tap one piece and every piece swings."),
    ("'Integrated' is about the parts; 'assessment' is about the purpose.", "A chef (integrated: all ingredients in one pot) cooking for a judge (assessment: someone must decide)."),
    ("You choose the dials; the model reports what follows. No dials, no answer.", "A vending machine labelled WHAT IF: you insert assumptions as coins and a consistent world drops out. It never predicts which coin you will insert."),
    ("Separate guesses can each look fine yet contradict each other; one system cannot.", "Six witnesses telling six stories versus one CCTV tape. The model is the tape: every scene agrees."),
    ("Emissions are just energy times how dirty each unit is.", "600 coal sacks, each leaking a 0.06 puff of smoke: 36 puffs. Swap to half-dirty sacks and the smoke halves."),
    ("If a reasonable person could pick another value, it was a choice, not a result.", "Two modellers arguing over a price tag stuck on a solar panel: if they can argue about the tag, it is an input."),
    ("Outputs are what the model is built to calculate from everything else.", "A printer spitting out pages titled MIX, PRICES, LAND, CO2, TEMPERATURE."),
    ("Weigh costs now against damages later, and pick the best balance.", "A see-saw with a pile of cash (cutting cost) on one side and a melting thermometer (damage) on the other. DICE rolls to find the balance."),
    ("Fix the goal first, then search for the cheapest way to reach it.", "A satnav: you type the destination (the goal) and it finds the cheapest route through power plants, cars and fields."),
    ("Models of the future cannot be checked against the future, only against logic and assumptions.", "A beautiful cake under glass labelled 2100, with a sign: DO NOT TASTE. You can only read the recipe."),
]

H["1.2"] = [
    ("Each link causes the next: more gas, thicker blanket, more trapped heat, warmer planet.", "A smokestack pumping into a balloon (concentration) that thickens a blanket (forcing) over a sweating Earth (temperature)."),
    ("CO2 lingers for centuries, so it piles up like savings in a bank.", "A piggy bank that only accepts coins and never lets them out: warming tracks the total inside."),
    ("Warming rises almost in a straight line with total CO2 emitted.", "A ruler where every 1,000 Gt mark is stamped with a small 0.45 °C flame."),
    ("Straight line: double the CO2, double the extra warming.", "Two 1,000 Gt sacks on the scale, two 0.45 flames: about 0.9 °C."),
    ("A stricter goal leaves a smaller budget.", "Two bank cards: 1.5 °C card holds 500, the 2 °C card holds 1,150. The stricter card is the poorer one."),
    ("Budget divided by spending rate gives the time it lasts.", "500 euros in your wallet, spending 40 a year: the wallet is empty in 12 and a half years."),
    ("A falling line spends half as fast on average, so it lasts twice as long.", "A triangle-shaped slice of cake: same 500 crumbs, but eaten more slowly, it lasts 25 years."),
    ("Inflow, slow outflow, and a limit before it spills.", "A bathtub with the tap wide open, the plughole clogged with hair, and the rim marked 1.5 °C."),
    ("Any inflow still raises the level; only shutting the tap stops the rise.", "Turning the tap from gushing to dribbling still overfills the clogged tub. Only closing it stops the water rising."),
    ("GCAM handles people and markets; it hands the physics to a small climate model.", "GCAM passes a bag of emissions over the wall to Hector, a little climate robot who hands back a thermometer."),
]

H["1.3"] = [
    ("Energy is a means; the service is the end.", "Nobody hugs a kilowatt-hour. They hug a warm radiator."),
    ("Primary is raw from nature; final is what you buy at the meter or pump.", "A lump of coal in a mine (primary) versus a socket in your wall (final)."),
    ("Losses multiply along the chain.", "100 coal lumps go into a leaky pipe: 40 come out as electricity, 36 reach the house."),
    ("Saving at the end saves even more at the start, because losses are avoided too.", "Switch off one bulb and nearly three lumps of coal jump back into the mine."),
    ("Four factors that multiply back to CO2 because the units cancel.", "A four-carriage train: people, wealth, energy appetite, smokiness. The train's smoke is the product of all four carriages."),
    ("An identity is bookkeeping, not a theory; it sorts the drivers.", "A sorting hat for emissions: it never guesses, it only files each change into one of four drawers."),
    ("How many and how rich is about society; how efficiently and how cleanly is about technology.", "Two people carriages at the front of the train, two engine carriages at the back."),
    ("Multiply ratios: growth and cleanup nearly cancel.", "Avalon's scale: 1.2 and 1.5 on one pan, 0.7 and 0.8 on the other. The needle barely moves: 1.008."),
    ("Ratios multiply; adding percentages ignores how they compound.", "A calculator with its plus key taped over and a sign: Kaya multiplies."),
    ("Every step is costed, so a better wall can compete with a new power plant.", "An insulation roll and a solar panel standing in the same price queue."),
]

H["1.4"] = [
    ("Price rises when goods run short and falls when they pile up.", "Tomatoes at a closing market: a mountain unsold means price slashed; an empty stall means price up next week."),
    ("Set demand equal to supply and solve.", "1000 apples wanted minus 4 per euro, 6 offered per euro: they meet at 100 euros and 600 apples."),
    ("A carbon price is a toll proportional to how much each option pollutes.", "A toll booth that charges each lorry by the size of its exhaust cloud."),
    ("Dirtier options get a bigger surcharge.", "Coal's price tag grows 45, gas's only 20: coal 105, gas 90."),
    ("Break-even is where the extra charge closes the cost gap.", "Gas starts 10 behind coal but gains 0.5 per euro of carbon price: 20 euros to catch up."),
    ("Solar has no surcharge, so the carbon price only has to close a 10 gap at 0.4 per euro.", "Gas climbing 0.4 steps per euro to reach solar's fixed 80: 25 steps."),
    ("Real choices are spread out because places and people differ.", "A food court: the cheapest stall has the longest queue, but every stall still has customers."),
    ("Divide by growth for every year of waiting.", "A coin shrinking a little each year it waits in the future."),
    ("Three percent a year over a century shrinks value about twentyfold.", "A 100 dollar note fading in a time machine to a 5 dollar note by 2126."),
    ("Small changes in the rate compound into huge changes over a century.", "Three telescopes looking at the same 100 dollars in 2126: one sees 22, one 5, one less than a dollar."),
]

H["1.5"] = [
    ("Scenarios explore; they do not predict or rank.", "A choose-your-own-adventure book with a spreadsheet on every page and no odds printed on any ending."),
    ("Stories about society, ranked by how hard they make mitigation and adaptation.", "Five roads on a map, each a different landscape: green, middle, walls, gated mansions, fossil motorway."),
    ("Story first, then the physics number.", "A book title (SSP2, the middle road) with a page number (4.5 W/m²) on the spine."),
    ("Watts per square metre is forcing, not degrees.", "A heater rated 4.5 watts on each square metre of Earth: it warms things by about 2.7 °C, not 4.5."),
    ("Each story sets how easy cutting and adapting are.", "SSP1 a cycling city, SSP3 a walled fortress, SSP5 a motorway with petrol pumps."),
    ("A spread from very low to very high forcing.", "A five-step staircase: 1.9, 2.6, 4.5, 7.0, 8.5."),
    ("Some worlds cannot reach the lowest forcing.", "SSP3's fortress door is too small for the 1.9 key: the cell stays empty."),
    ("Sort by the warming outcome, from best to worst.", "Eight lockers, C1 to C8, getting hotter left to right."),
    ("C3 is the 'likely below 2 °C' locker.", "Locker three holds a thermometer that stays under 2 two times out of three."),
    ("New climate-model generation, one scenario per modelling team.", "Seven new cards dealt in 2026; GCAM drew the high card, H."),
]

H["1.6"] = [
    ("A US national laboratory publishes it openly.", "A lab door on the Pacific coast standing wide open with a FREE sign."),
    ("Different questions need different maps: economy, land, water.", "Three overlapping maps: 32 country jigsaw pieces, 300 land patches, 235 river basins."),
    ("Start where data exist, then step forward.", "A staircase starting on a 2021 landing, steps every five years to 2100."),
    ("Each step is decided without knowing the next.", "A hiker in fog who can see only the five-year step in front."),
    ("All prices adjust together until every market clears.", "An auctioneer shouting prices for oil, wheat, water and land at once until every hand is down."),
    ("The difference isolates the effect of the one change.", "Twin worlds, identical except one has a carbon price: the gap between them is the policy's footprint."),
    ("A baseline to compare against, not a prediction.", "A ruler laid on the table, not a crystal ball."),
    ("Fix the price, or fix the amount; the other follows.", "A toll booth (price fixed, traffic varies) versus a gate with a counter (traffic fixed, price rises until it fits)."),
    ("On the same straight curve, price and cut move in step.", "A seesaw marked price = 2 × cut: 50 lifts 25, 60 needs 120."),
    ("Big averages hide people, politics and uncertain futures.", "A map with three fog patches: who pays, how people behave, whether assumptions come true."),
]

H["2.1"] = [
    ("They set the stage; the model plays on it.", "Stagehands placing population and income props before the actors (energy, land, water) walk on."),
    ("Output equals workers times what each produces.", "A factory gate counting heads, then weighing what each worker carries out."),
    ("Five years of compounding per model step.", "A worker's toolbox growing 2% a year, five times: 50 becomes 55."),
    ("History from historians, the future from scenario databases.", "A bookshelf: old Maddison and UN volumes on the left, SSP folders on the right."),
    ("Income per person drives every kind of demand.", "A bridge from a wallet to houses, cars, factories, fridges and taps."),
    ("Demand moves with income, price and population, each with its own power.", "Three dials: the wallet dial (α), the price-tag dial (β) and the headcount dial."),
    ("Houses grow with income, then saturate.", "A house inflating like a balloon as its owner gets richer, then stopping at the garden fence."),
    ("Multiply the four ratios.", "A green road where a rich population drives clean cars: 7% of today's smoke."),
    ("Let energy costs feed back on GDP.", "A pipe from the power station back into the economy's engine room."),
    ("KLEAM adds a farm to the factory.", "A tractor parked next to the KLEM machine: A for agriculture."),
]

H["2.2"] = [
    ("Only energy, land and water markets are solved; the rest is given.", "A spotlight on three market stalls; the rest of the economy sits in the dark."),
    ("The gap the solver must close.", "Excess demand is the queue left standing when the shop shuts."),
    ("A tax shifts supply; price rises until the gap closes.", "A €50 sticker on every supply crate pushes the price from 100 to 127."),
    ("Prices push on each other, so they must be found together.", "A web of strings: pull the oil string and electricity and biomass jiggle."),
    ("A Newton-like step reusing an approximate slope.", "A climber who remembers roughly how steep each slope was instead of measuring again every step."),
    ("Bad starts need a nudge before the clever method works.", "A bisection knife cutting the search in half, and a preconditioner pushing the car to start it."),
    ("Logs keep prices positive and markets comparable.", "Markets weighed on a log scale so a water basin and an oil field fit on the same balance."),
    ("Close enough to bang the hammer, within a budget of tries.", "An auctioneer allowed 2,500 shouts per period, stopping when gaps are under 0.1%."),
    ("No foresight means no anticipation of future policy.", "A coal plant built in 2030, then struck by a 2040 policy lightning bolt."),
    ("Optimisers see the whole century at once.", "A chess player who sees all 90 moves ahead, versus GCAM playing one move at a time."),
]

H["2.3"] = [
    ("Real buyers differ, so shares change smoothly.", "A dimmer switch instead of an on-off switch for each technology."),
    ("Cost raised to a negative power, normalised.", "Each option's cost shrunk by a magnifying glass of power γ, then cut into a pie."),
    ("Cheaper wins more, not all.", "Pie of 54, 29, 17: coal biggest, solar smallest slice."),
    ("Bigger exponent, harsher competition.", "A volume knob on cost differences: at −1 a whisper, at −10 a shout."),
    ("Differences, not ratios.", "A ruler measuring the gap between price tags instead of a ratio scale."),
    ("Exponentials do not break at zero or negative costs.", "A subsidised technology with a negative price tag still gets a sensible share."),
    ("Calibrated to the past, assumed for the future.", "A tailor's adjustment pinned on the suit so it fits 2021; the future pins are guesses."),
    ("Invert the logit to find the weights.", "Working backwards from the pie you saw to the hidden preferences that cut it."),
    ("Trees of choices with tighter competition inside nests.", "Russian dolls: sector, subsector, technology, cooling, each doll with its own logit."),
    ("Close substitutes react strongly; different fuels less.", "Coal plants elbowing each other hard (−10) inside a room; fuels negotiating politely (−3) in the hall."),
]

H["2.4"] = [
    ("Cheap deposits first; dearer as you dig deeper.", "A staircase of coal grades, each step more expensive."),
    ("More price, more supply, but never above the maximum.", "A wind turbine's output rising like an S toward a ceiling labelled Qmax."),
    ("Everything that makes a unit of output costs money, minus by-products.", "A receipt: non-energy cost, fuel, carbon charge, minus a refund for by-products."),
    ("Spread capital over hours of output.", "A power plant's price tag sliced thinly over every hour it runs."),
    ("Carbon raises gas, not solar.", "Gas price climbing a ladder of carbon; solar sitting still at 45."),
    ("More of the same intermittent power is worth less.", "The tenth solar panel at noon gets paid less than the first: a value factor sinking as the share grows."),
    ("Linear fall with share.", "A slide from 0.97 down by 1.44 per unit of share: at 30%, about 0.54."),
    ("Derived from US data; storage missing.", "A US-made ruler that bends beyond 75%, with no battery in the toolbox."),
    ("Many ways to make hydrogen.", "Ten big factories and two corner shops selling hydrogen."),
    ("Old plants keep running, so change is slow.", "A car park full of cars from different years; only new arrivals change the mix quickly."),
]

H["2.5"] = [
    ("Model the service, then the fuel.", "A warm living room ordered first; the boiler and fuel chosen afterwards."),
    ("Income raises demand by a power, price lowers it.", "A wallet doubling sends passenger-km to 152; a 50% fare rise pulls it back to 134."),
    ("Income groups behave differently.", "Ten apartments stacked by income, each with different floorspace."),
    ("Cold and heat drive heating and cooling.", "A thermometer stuck to the wall counting degree-days."),
    ("Three ways to make steel.", "A blast furnace, an arc furnace eating scrap, an arc furnace eating sponge iron."),
    ("Crops need fertiliser, which needs energy.", "A wheat field plugged into a power socket through a fertiliser bag."),
    ("Divide vehicle costs by passengers.", "A taxi fare split among the passengers inside."),
    ("Richer travellers value time, so fast modes win.", "A banker running past the bus stop to a car."),
    ("Percent response per percent change.", "Two springs: one stretched by income, one squeezed by price."),
    ("Costs flow through technology choice.", "Cheap electricity pouring into heat pumps and EVs through a funnel."),
]

H["2.6"] = [
    ("Land, food and land carbon in one module.", "A farmer, a cow and a forest sharing one map."),
    ("Four ways to farm each crop.", "Each field split into four: wet and dry, careful and casual."),
    ("Profit per hectare drives land choice.", "A field sign: (price − cost) × yield."),
    ("Higher profit, bigger share.", "Grass earning 300 beats wheat earning 240: 56% to 44%."),
    ("Land is energy divided by what one hectare yields in energy.", "A field sign: yield × energy content. Bigger yield, fewer fields."),
    ("10 t/ha × 18 GJ/t = 180 GJ per hectare; 10 EJ needs 55.6 million of them.", "Hay bales stacked to fill 10 EJ cover a country the size of France."),
    ("Bioenergy needs huge areas.", "100 EJ of energy crops covering a third of the world's cropland."),
    ("Change in carbon stock is the emission.", "A forest's carbon bank account: today minus yesterday."),
    ("Clearing is instant, regrowth is slow.", "An axe falls in one second; the sapling takes a century."),
    ("Carbon price pays land for holding carbon.", "A forest receiving a rent cheque for every tonne of carbon it holds."),
]

H["2.7"] = [
    ("Rivers, not countries, set water limits.", "235 bathtubs, one per river basin."),
    ("Withdrawal is borrowed; consumption is not returned.", "A borrowed cup: what you drink is consumption; what you pour back is not."),
    ("Six users of water.", "Six taps on one pipe: farm, power plant, factory, mine, cow, home."),
    ("Richer cities use more, dearer water less.", "A city tap opening with wealth and closing with price."),
    ("Cheapest water first, then dearer tiers.", "Three wells: river, deep groundwater, then a desalination plant on the coast."),
    ("Farmers pay a small share.", "A farmer's water bill stamped 5%."),
    ("Total demand within renewable supply keeps the price low.", "48.6 litres poured into a 50-litre jug: no overflow, price stays one cent."),
    ("Thirsty cooling tips the basin into groundwater.", "Once-through cooling spills the jug: price jumps to five cents."),
    ("Thermal desalination is twenty times hungrier.", "A small battery for reverse osmosis versus a huge furnace for thermal."),
    ("Water, energy and land need each other.", "A three-legged stool: water, energy, land."),
]

H["2.8"] = [
    ("Carbon in fuel ends up in the air.", "Every litre of fuel stamped with its carbon weight."),
    ("Cheap cuts happen first as the price rises.", "A staircase of abatement: each carbon price unlocks another step."),
    ("Emissions go to Hector, but climate does not come back.", "A one-way door from GCAM to Hector."),
    ("Forcing grows with the log of concentration.", "Each doubling adds the same 3.7 W blanket."),
    ("Doubling CO2 adds about 3.7 W/m².", "A double blanket weighing 3.7 kilos."),
    ("Price, quantity or outcome.", "Three dials: fixed price, fixed cap, fixed temperature."),
    ("Prices are per tonne of carbon in old dollars.", "A 1990 banknote taped to a tonne of black carbon, not CO2."),
    ("One change ripples through the whole system.", "A stone in a pond: rings through land, food, water, power."),
    ("The cap's shadow price is the marginal cost.", "A shadow cast by the cap, shaped like a price tag."),
    ("The LP picks the cheapest mix under a cap.", "Coal 22, gas 50, solar 28 on a scale at $22 a tonne."),
]

H["3.1"] = [
    ("Data become XML, XML becomes results.", "A factory line: raw data → gcamdata → XML → solver → database → queries."),
    ("Docs lag code.", "A manual for version 8.2 lying next to a version 9.1 machine."),
    ("Calibrate to history, then project.", "Six photographs on the wall: 1975 to 2021."),
    ("Bigger units, older dollars.", "A ruler switching from millions to billions, a 1975 banknote."),
    ("Finished is not solved.", "A race car crossing the line with a flat tyre: check the log."),
    ("Tolerance must not be tighter than the inner solver.", "Two sieves: the outer one cannot be finer than the inner."),
    ("Share-weights hide everything costs miss.", "A secret drawer behind each technology full of unmodelled reasons."),
    ("Version, inputs, config, scripts.", "Four boxes on a shelf, each labelled: rebuild me."),
]

H["3.2"] = [
    ("Four demands: people, goods, flights, ships.", "Four doors: a commuter, a lorry, a plane, a ship."),
    ("Travel grows with income, falls with price.", "A suitcase that grows with your salary."),
    ("A nesting tree from service down to vehicle.", "Russian dolls: travel, road, light vehicles, cars, engines."),
    ("Divide vehicle cost by passengers.", "A taxi fare split by 2.33 riders."),
    ("Capital annualised then spread by distance.", "A car's price spread over ten years and 14,000 km a year."),
    ("OTAQ overrides UCD.", "Two rulebooks: OTAQ on top, UCD underneath."),
    ("Wage from GDP over 2,000 hours.", "A clock with 2,000 hours and a salary slip."),
    ("Planes cost more time per hour.", "A bus 0.81, a car 0.82, a plane 1.24: waiting at the airport costs more."),
    ("Time cost only for passengers.", "A stopwatch on passenger seats, none on freight."),
    ("Modes compare ratios; drivetrains compare differences.", "A ratio ruler for modes, a difference ruler for engines."),
    ("Time cost = wage × multiplier ÷ speed.", "A €10 wage, a slow bus at 22 km/h: 37 cents a kilometre."),
    ("Hydrogen renamed, fuel cells less favoured.", "A hydrogen tank relabelled, with half its share-weight sticker torn off."),
]

H["3.3"] = [
    ("Four strands of literature.", "Four library shelves: foundations, comparisons, applications, Saudi."),
    ("Cite the model paper for structure.", "Calvin 2019 on the reference shelf."),
    ("Transport is slow to decarbonise.", "A transport snail trailing 10–30 years behind power."),
    ("Prices alone are not enough.", "A carbon price pushing a car that stays put because of preferences."),
    ("Aviation is the expensive residual.", "A plane needing $1,300 a tonne to go clean."),
    ("Saudi transport CO2 range.", "A 418 to 115 slide."),
    ("Known, disputed, unknown.", "Three traffic lights: green known, amber disputed, red unknown."),
    ("Check unconfirmed references.", "A [U] stamp meaning unverified: check before citing."),
]

H["3.4"] = [
    ("Decision, metric, comparison.", "A question with three hooks: what to decide, how to measure, against what."),
    ("Sharpen a topic into a testable question.", "A pencil sharpener turning 'EVs in Saudi Arabia' into a point."),
    ("World, levers, policies.", "A stage (world), dials (levers), rules (policies)."),
    ("One change at a time.", "A science experiment with only one dial turned."),
    ("Compare like with like.", "Two runners on the same track: same emissions or same price."),
    ("Assumptions are not policies.", "A cheaper battery is luck, not law."),
    ("Three sampling designs.", "One dial at a time, every combination, or a smart scatter."),
    ("Four checks for credibility.", "Four witnesses: history, hindcast, other models, experts."),
]

H["3.5"] = [
    ("Add-ons patch only what changes.", "A sticky note on one page of the big model book."),
    ("Typos create ghosts.", "A misspelt name creating an empty ghost object."),
    ("Costs per vehicle-km.", "A meter ticking per vehicle-kilometre."),
    ("Interpolation rules override your values.", "A rule-keeper erasing your future share-weights."),
    ("Levers that change how people travel.", "Three knobs: load factor, speed, elasticity."),
    ("Constraint solves the price.", "A cap that becomes a market with a hidden price."),
    ("Mandates become credit markets.", "Petrol cars paying 0.3 credits; ZEVs earning 1."),
    ("No cars, only kilometres.", "A road full of kilometres but no counted cars."),
    ("Batch files make matrices.", "A matrix of folders, each a scenario."),
    ("Systematic changes belong in data.", "Editing the recipe book, not each dish."),
]

H["3.6"] = [
    ("Script once, rebuild forever.", "A recipe card instead of a handwritten note."),
    ("New-vintage output is the sales proxy.", "A shop window showing only new cars."),
    ("Check levers took effect.", "A mechanic checking the tyres after inflating them."),
    ("Report in many ways.", "Four lenses: absolute, relative, per person, cumulative."),
    ("Four factors multiply to CO2.", "Activity, structure, intensity, carbon: four gears."),
    ("No residual.", "A pie cut into slices that add up exactly."),
    ("Log mean weights.", "A scale balancing two values on a log beam."),
    ("Effects add to the total.", "26.88 + 3.77 − 28.49 − 40.81 = −38.65."),
    ("Bars show sensitivity.", "A tornado: the widest band is the input that matters most."),
    ("Coverage and density.", "A net catching high runs: how many caught, how pure the catch."),
]

H["3.7"] = [
    ("Saudi Arabia is in the Middle East region.", "A Saudi flag folded inside a Middle East map."),
    ("GCAM-KSA splits it out.", "A 33rd jigsaw piece cut out of the Middle East."),
    ("Add the country, check mappings, override data, recalibrate.", "Four steps on a ladder to a new region."),
    ("Countries must sum to the region.", "Pieces of a pie that must still make the whole pie."),
    ("Blend own trend and regional pattern.", "Two rivers merging by a convergence year."),
    ("DSCALE downscales to 143 countries.", "A pie cut into 143 slices."),
    ("No fleet in GCAM.", "A parking lot with no counted cars."),
    ("Models pass numbers back and forth.", "Two models passing notes until they agree."),
]

H["3.8"] = [
    ("Know what the model cannot see.", "Three blindfolds: no fleet, one traveller, generic fuels."),
    ("Freight has no time value.", "A lorry with no clock."),
    ("Removal is not reduction.", "Two ledgers: gross and net."),
    ("A single consumer hides distribution.", "One average person standing in for everyone."),
    ("State the exact version.", "A label: GCAM v9.1, not just GCAM."),
    ("Rename heavily modified models.", "A new name tag: GCAM-KSA."),
    ("Standard columns for comparability.", "A spreadsheet with the same column names everyone uses."),
    ("Convert carbon prices.", "A 1990 tonne of carbon turned into a 2010 tonne of CO2."),
    ("Archive everything needed to rebuild.", "A time capsule with every file and a README."),
]

PALACE = {
    1: {"place": "Your home",
        "intro": "Walk through your own home, front door to garden. In each room, picture the strange scene and let it remind you of the module's core idea.",
        "stations": [
            ("1.1", "Front door", "A baby's mobile hanging in the doorway: economy, energy, land, water and air dangle from it. You brush one and every piece swings. Integrated means everything moves together."),
            ("1.2", "Bathroom", "The bathtub overflows with smoke instead of water. The tap gushes 40 Gt a year, the plug is clogged, and the rim is marked 1.5 °C. Only shutting the tap stops it rising."),
            ("1.3", "Kitchen", "A four-carriage toy train runs across the counter: people, wealth, energy appetite, smoke. A calculator has its plus key taped over. Kaya multiplies."),
            ("1.4", "Dining room", "A market stall on the table, tomatoes with a toll booth charging each by its smoke. A coin shrinks every year it waits on the plate."),
            ("1.5", "Living room", "A choose-your-own-adventure book on the sofa. Each chapter is an SSP road, and the page number is the forcing in watts, not degrees."),
            ("1.6", "Garden", "An auctioneer on a five-year staircase shouts prices for oil, wheat and water. Twin gardens grow side by side; the gap between them is the policy's footprint."),
        ]},
    2: {"place": "A city market",
        "intro": "Walk through a busy market square, stall by stall. Each stall is one GCAM component with its own odd scene.",
        "stations": [
            ("2.1", "Gate", "Stagehands carry population and income props through the gate before the market opens."),
            ("2.2", "Auction podium", "An auctioneer allowed 2,500 shouts per period bangs the hammer when every gap is below 0.1%."),
            ("2.3", "Food court", "Every stall has a queue; the cheapest the longest. Russian dolls on the counters show nested choices."),
            ("2.4", "Power stall", "A staircase of coal grades and a sinking solar value-factor slide."),
            ("2.5", "Travel kiosk", "A banker runs past the bus stop to a car: richer travellers value time."),
            ("2.6", "Farmers' corner", "Wheat and energy grass fight for fields; a forest receives a rent cheque for its carbon."),
            ("2.7", "Water fountain", "Six taps on one pipe; once-through cooling spills the jug and the price jumps."),
            ("2.8", "Town hall", "Three dials (price, cap, temperature) and a stone dropped in a pond ripples through every stall."),
        ]},
    3: {"place": "A research institute",
        "intro": "Walk through a research institute, floor by floor, as you would through a transport study.",
        "stations": [
            ("3.1", "Server room", "A factory line from raw data to XML to results, with a race car crossing the line on a flat tyre."),
            ("3.2", "Transport lab", "Russian dolls of travel; a taxi fare split by 2.33 riders and a stopwatch on passenger seats."),
            ("3.3", "Library", "Four shelves, with a transport snail crawling 10–30 years behind."),
            ("3.4", "Seminar room", "A pencil sharpener turning 'EVs in Saudi Arabia' into a sharp question."),
            ("3.5", "Workshop", "Sticky notes on the model book; a misspelt name spawning a ghost."),
            ("3.6", "Analysis room", "A pie cut into slices that add up exactly, and a tornado chart on the wall."),
            ("3.7", "Map room", "A 33rd jigsaw piece, a pie cut into 143 slices, and two models passing notes."),
            ("3.8", "Press room", "Three blindfolds, a time capsule, and a label reading GCAM v9.1."),
        ]},
}
