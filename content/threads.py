"""Concept threads: the same idea met three times, once per go, each time deeper.
Each stop: (module id, what you learn at this depth, a recall question, its answer).
Module pages show every thread that passes through them, with a retrieval question from the earlier go."""

THREADS = [
    dict(id="markets", name="Markets and prices", icon="market", sys="economy", stops=[
        ("1.4", "Prices balance supply and demand; a carbon price shifts who wins.", "What does a price do in a market?", "It moves until the amount supplied equals the amount demanded."),
        ("2.2", "Many linked markets clear at once; GCAM's solver adjusts all prices together.", "How does GCAM clear many markets in a period?", "Its solver (Broyden's method) adjusts all prices until excess demand is below tolerance everywhere."),
        ("3.1", "Check the solver log for unsolved markets before trusting a run.", "Name one thing to check before trusting a GCAM run.", "That every market solved: no unsolved markets in the log.")]),
    dict(id="choice", name="Choice and the logit", icon="dice", sys="energy", stops=[
        ("1.4", "Real models share the market: cheaper options win more, not all.", "Why don't models give the whole market to the cheapest option?", "Because costs and preferences vary, so shares are spread by relative cost."),
        ("2.3", "Relative- and absolute-cost logits, share weights and nesting.", "What do share weights do in a logit?", "They calibrate the logit to reproduce base-year shares, capturing non-cost preferences."),
        ("3.2", "Transport modes compete on generalised cost with absolute-cost logits; share weights are a research lever.", "Which logit form does GCAM use inside passenger modes?", "Absolute-cost logits on generalised cost (money plus value of time).")]),
    dict(id="climate", name="Cumulative emissions and warming", icon="thermo", sys="climate", stops=[
        ("1.2", "Warming follows the running total of CO2: about 0.45 °C per 1,000 Gt.", "What drives long-term warming: this year's emissions or the running total?", "The running total (cumulative CO2)."),
        ("2.8", "Hector turns GCAM's emissions into concentrations, forcing and temperature each period.", "Which model inside GCAM computes temperature?", "Hector, a simple climate model."),
        ("3.4", "A climate target can be imposed as a constraint; plan which climate outcome your study reports.", "How can a climate goal be imposed in GCAM?", "As an emissions or climate constraint, solved as a market with a shadow price.")]),
    dict(id="drivers", name="Drivers and decomposition", icon="people", sys="economy", stops=[
        ("1.3", "Kaya: CO2 = people × income × energy per $ × CO2 per energy.", "Name the four Kaya factors.", "Population, GDP per person, energy per unit of GDP, CO2 per unit of energy."),
        ("2.1", "Population and GDP come from the SSPs and drive every demand.", "Where do GCAM's population and GDP come from?", "From the Shared Socioeconomic Pathways (SSPs)."),
        ("3.6", "LMDI splits a change in transport CO2 into activity, structure, intensity and carbon effects that add up exactly.", "What does an LMDI decomposition give you?", "Additive effects of each driver that sum exactly to the total change.")]),
    dict(id="scenarios", name="Scenarios", icon="map", sys="policy", stops=[
        ("1.5", "A scenario pairs a story (SSP) with a forcing level (RCP).", "In SSP2-4.5, what is 4.5?", "Radiative forcing of 4.5 W/m² in 2100."),
        ("2.1", "SSP choices set the socioeconomic inputs of a GCAM run.", "What changes in GCAM when you switch SSP?", "Population, GDP and related assumptions that drive demands."),
        ("3.4", "Design a scenario matrix: Reference, levers, policies and an uncertainty plan.", "What are the rows and columns of a scenario design matrix?", "Typically levers (assumptions) by policies, each cell one run.")]),
    dict(id="policy", name="Price or cap", icon="scale", sys="policy", stops=[
        ("1.6", "A toll or a gate: a carbon price and an emissions cap are mirrors.", "How are a carbon price and a cap related?", "A cap is met by the carbon price that delivers it; a price gives some quantity of cuts."),
        ("2.8", "Caps are solved as extra markets whose prices are shadow prices.", "How does GCAM solve an emissions constraint?", "As a market for the constraint; its price is the shadow (carbon) price."),
        ("3.5", "Write policy add-on XML: carbon tax, net-zero constraint, ZEV standard.", "How would you build a ZEV standard in GCAM?", "As a credit market (portfolio-standard style) in add-on XML.")]),
    dict(id="feedbacks", name="Stocks, flows and feedbacks", icon="loop", sys="climate", stops=[
        ("1.7", "Stocks change by inflow minus outflow; loops reinforce or balance.", "Why does CO2 keep rising after emissions start to fall?", "Because inflow still exceeds outflow (sinks)."),
        ("2.8", "Five feedback loops run through GCAM's whole system.", "Give one feedback loop that runs through GCAM.", "For example: bioenergy demand → land competition → food prices → land use → emissions."),
        ("3.7", "Coupling GCAM with other models adds feedbacks it does not have.", "Why couple GCAM with another model?", "To add detail or feedbacks GCAM lacks, such as fleets, grids or climate impacts.")]),
    dict(id="costs", name="Costs of cutting", icon="coin", sys="energy", stops=[
        ("1.8", "A MAC curve: cheapest cuts first, up to the carbon price.", "What does a carbon price buy on a MAC curve?", "Every option whose cost per tonne is below the price."),
        ("2.4", "Technology costs, resource curves and the value factor set what each option costs in GCAM.", "Why do wind and solar get less valuable as their share rises in GCAM?", "The value factor falls with share, raising their effective cost."),
        ("3.5", "Cost add-ons (for example cheaper batteries) are a core transport lever.", "How do you test cheaper battery-electric vehicles in GCAM?", "With an add-on XML that scales BEV costs, loaded after the base files.")]),
    dict(id="nexus", name="Water, land and energy", icon="drop", sys="water", stops=[
        ("1.9", "The nexus: irrigation, cooling and bioenergy tie the systems together.", "Name two links in the water–energy–food nexus.", "Irrigation, cooling water, bioenergy land."),
        ("2.7", "235 basins, six demand sectors, three supply tiers and a water price.", "What are GCAM's three water supply tiers?", "Renewable water, non-renewable groundwater, desalination."),
        ("3.7", "Electrified transport shifts demand to power and cooling water; go finer with downscaling.", "Why can transport electrification affect water?", "More power demand means more cooling water at thermal plants.")]),
    dict(id="uncertainty", name="Uncertainty", icon="dice", sys="climate", stops=[
        ("1.10", "Parameter, structural and scenario uncertainty; ensembles give a range.", "Name the three kinds of uncertainty.", "Parameter, structural and scenario."),
        ("2.1", "Socioeconomic ranges across SSPs widen every result downstream.", "Why do SSP choices widen results?", "They change population and GDP, which drive all demands."),
        ("3.6", "Stress-test with sensitivity analysis and scenario discovery.", "What does scenario discovery find?", "Which combinations of inputs lead to an outcome of interest.")]),
    dict(id="families", name="Kinds of model", icon="layers", sys="neutral", stops=[
        ("1.1", "Two families: cost–benefit (DICE) and process-based (GCAM, MESSAGEix).", "What question does a cost–benefit model answer?", "How much to cut, by weighing abatement costs against damages."),
        ("2.8", "Equilibrium versus optimisation: GCAM clears markets rather than optimising.", "Does GCAM optimise or clear markets?", "It clears markets period by period (equilibrium), without intertemporal optimisation."),
        ("3.9", "Seven models side by side: foresight, scope and solution method.", "Name a perfect-foresight IAM and a recursive one.", "Perfect foresight: MESSAGEix, REMIND or WITCH. Recursive: GCAM, IMAGE or AIM-Hub.")]),
    dict(id="transport", name="Transport", icon="car", sys="energy", stops=[
        ("1.3", "People want services (travel), not energy.", "Is passenger travel demand measured in energy or service?", "In service: passenger-kilometres."),
        ("2.5", "Transport costs money plus time; richer travellers value time more.", "What two parts make up the generalised cost of travel?", "Money cost plus the value of travel time."),
        ("3.2", "The full transport nest: modes, size classes, technologies, load factors.", "How is cost per passenger-km computed for a vehicle?", "Vehicle cost per km divided by the load factor (passengers per vehicle).")]),
    dict(id="time", name="Time and foresight", icon="clock", sys="economy", stops=[
        ("1.4", "Discounting weighs the future: a dollar later is worth less today.", "What does a higher discount rate do to future damages?", "It shrinks their present value."),
        ("2.2", "Recursive dynamics: GCAM has no crystal ball.", "Does GCAM know future prices when it solves 2030?", "No; it solves each period with that period's information."),
        ("3.9", "Foresight models act early; carbon prices rise at the discount rate.", "What is the Hotelling rule for carbon prices?", "On a least-cost path under a budget, the price rises at the discount rate.")]),
]
