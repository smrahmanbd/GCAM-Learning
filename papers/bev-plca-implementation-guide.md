# Replicate the BEV pLCA study with Claude Code in VS Code: a beginner's guide

## What you will build

You will rebuild the method of [Šimaitis et al. (2025)](https://doi.org/10.1038/s43247-025-02447-2): a time-adjusted prospective LCA of passenger cars, run under future energy scenarios. Claude Code writes most of the code. Your job is to give clear instructions, read what it proposes, and check the numbers. No programming experience is assumed.

Pick the track that matches your access. Each one builds on the one before it.

| Track | What you do | What you need | Time |
| --- | --- | --- | --- |
| A · Teaching model | Run and extend `bev_plca_toy.py` from the course repo; reproduce the paper's figures in a simplified form | VS Code, Python, Claude Code | 2–3 hours |
| B · Full replication | Build the real pipeline: premise + TIAM-UCL scenarios, ecoinvent, carculator, brightway, Monte Carlo, Sobol | Track A, plus an ecoinvent licence and a premise scenario key | 3–6 days |
| C · GCAM variant | Swap TIAM-UCL for GCAM scenarios in premise and compare | Track B working | 1–2 days |

The study's chain, which Track B rebuilds:

1. **Scenario**: TIAM-UCL (or GCAM) says how electricity, diesel and hydrogen change, region by region, 2025–2050.
2. **premise**: rewrites the ecoinvent database to match that scenario for each year.
3. **carculator**: builds an inventory for each car (powertrain × size).
4. **brightway**: matches each car to the right scenario year and calculates g CO₂e per km.
5. **Time adjustment**: production in year 0, use in 5-year periods, end of life in the last year.
6. **Analysis**: 5,000 comparative Monte Carlo samples, then Sobol sensitivity.

If you are new to cars and LCA, first work through the course pages [Part 1: the basics](bev-plca-basics.html) and [Part 2: the paper, hands-on](bev-plca.html).

## Set up once (about 30 minutes)

You need four things on your computer: VS Code, Python, Git and the Claude Code extension.

1. **VS Code.** Install version 1.94 or newer from [code.visualstudio.com](https://code.visualstudio.com).
2. **Python through Miniconda.** Install [Miniconda](https://docs.conda.io/en/latest/miniconda.html). Conda keeps each project's packages separate, which matters because premise and brightway pin many versions. premise needs Python 3.12 or newer.
3. **Git.** Install it from [git-scm.com](https://git-scm.com), so you can clone the course repo and save versions of your work.
4. **Claude Code extension.** In VS Code, open Extensions (Ctrl+Shift+X / Cmd+Shift+X), search **Claude Code**, and install the one published by Anthropic. Sign in with a paid Claude plan (Pro, Max, Team or Enterprise) or a Claude Console account. Setup details are in the [Claude Code VS Code docs](https://code.claude.com/docs/en/ide-integrations).
5. **Get the course files.** In a terminal:

   ```bash
   git clone https://github.com/smrahmanbd/GCAM-Learning.git
   cd GCAM-Learning
   code .
   ```
6. **Open Claude.** Open any file, then click the **Spark** icon at the top right of the editor. You can also run "Claude Code: Open in New Tab" from the Command Palette (Ctrl+Shift+P).

Four controls you will use all the time:

- **@-mentions.** Type `@` and a file name to point Claude at a file, for example `@labs/papers/bev_plca_toy.py`. Select lines and press Alt+K (Option+K on Mac) to mention just those lines.
- **Plan mode.** Type `/plan` before a big task. Claude writes a plan for you to read and edit before it changes any files. Use it for every step marked *(plan first)* below.
- **Permission mode.** The indicator under the prompt box shows whether Claude asks before editing files or running commands. As a beginner, keep it on asking, and read each diff before you accept.
- **CLAUDE.md.** Run `/init` once in your project. Claude writes a `CLAUDE.md` file with notes about the project, and reads it at the start of every session. Add your own rules there, such as "Always use the conda environment `plca`".

**First message to send** (copy and paste):

```text
I am a beginner learning prospective LCA. Read @papers/bev-plca-study-guide.md and
@labs/papers/bev_plca_toy.py. Explain in plain language what the toy model does,
step by step, and which numbers in it are made up for teaching. Do not change any files.
```

## Track A: the teaching model, step by step

By the end of Track A you will have a small Python project that reproduces the logic of the paper's Figures 2, 3, 5 and 6, using made-up but realistic numbers. Send each prompt, read Claude's answer and diff, then go on.

**A1. Make a clean environment.**

```text
Create a conda environment called plca with Python 3.12, numpy, pandas, matplotlib,
jupyter and SALib. Give me the exact terminal commands, run them, and confirm the
environment works by importing each package.
```

**A2. Run the model and understand the output.**

```text
Run labs/papers/bev_plca_toy.py in the plca environment. For each of the six
exercises it prints, explain in two sentences what the numbers show and how they
compare with the paper (e.g. BEV 32-47% below HEV, breakeven 87k -> 51k km).
```

**A3. Start your own project folder** *(plan first)*.

```text
/plan Make a new folder my-plca/ with: src/model.py (copy the toy model's
functions), src/figures.py, notebooks/01_explore.ipynb, data/, results/ and a README.
Keep the parameters in data/params.json so I can edit them without touching code.
Add a tests/ folder with a test that the BEV footprint in China, <2 C, 200,000 km,
15 years equals the value the toy model prints.
```

**A4. Rebuild the paper's figures in simplified form.** Ask for one figure at a time:

```text
In src/figures.py write a function fig2_scatter() that runs the comparative Monte
Carlo (5,000 samples, the same inputs for every powertrain) and plots BEV (y) against
HEV (x), coloured by scenario, with a diagonal line and the scenario means marked.
Save it to results/fig2_bev_hev.png. Then show me the figure.
```

Then repeat with these, one prompt each:

- `fig3_contribution()`: stacked bars by life-cycle stage for the four cars, static LCA vs pLCA, China case.
- `fig5_breakeven()`: breakeven mileage against average grid intensity, one dot per region × scenario.
- `fig6_sobol()`: Sobol first-order and total-order indices with SALib, for the BEV-vs-HEV % difference.

**A5. Ask "why" questions.** These build understanding faster than code:

```text
In fig6, why does Lifetime have almost no influence? Change the model so that the
grid decarbonises much faster and rerun. Does Lifetime matter more now? Explain.
```

**A6. Save your work.**

```text
Commit everything in my-plca/ with a clear message. Do not push.
```

Checkpoint: your Fig. 2 cloud should sit mostly below the diagonal, and move further from it as the scenario gets more ambitious. If it doesn't, see the troubleshooting section.

## Track B: full replication, step by step

Track B rebuilds the real pipeline. Start from the authors' own code: the paper says the full code and data are in its **Supplementary Data 1** ZIP. Your goal is to run it, understand it, and then re-run it yourself.

**B0. Get access first (this can take a week).**

- [ ] An **ecoinvent** licence covering version 3.9.1 (cut-off system model). Universities often have one.
- [ ] A **premise scenario key**. The IAM scenario files in premise are encrypted; the [premise README](https://github.com/polca/premise) says to request a key by email from the developers.
- [ ] Download **Supplementary Data 1** from the [paper page](https://doi.org/10.1038/s43247-025-02447-2) and the TIAM-UCL coupling dataset from the [University of Bath archive](https://doi.org/10.15125/BATH-01431).
- [ ] At least 16 GB RAM and 100 GB free disk. Each prospective database is large.

**B1. Map the authors' code** *(plan first, no edits)*. Unzip each download into its own new folder, such as `external/supp1/`.

```text
/plan Read everything in @external/supp1/ without running or changing anything.
Draw me a map: which script does what, in what order, which package versions it
expects, which inputs it needs (ecoinvent path, premise key, scenario files) and what
it outputs. Mark each step as foreground, background, time adjustment, Monte Carlo or
Sobol, following the paper's Methods section.
```

**B2. Build the environment the authors used.** The paper used premise 2.1.1, ecoinvent 3.9.1 and brightway2. Newer premise defaults to Brightway 2.5, so match the authors' versions first.

```text
Create a separate conda environment called plca-full with the package versions the
authors' code expects (premise 2.1.1 with brightway2, carculator, SALib). If the
ZIP has no requirements file, propose pins and explain each one. Never install into
my base environment. Store the ecoinvent password and premise key in a .env file
and add .env to .gitignore.
```

**B3. Import ecoinvent into a brightway project.**

```text
Write scripts/01_import_ecoinvent.py that creates the brightway project "plca" and
imports ecoinvent 3.9.1 cut-off from the path in .env. Check that it worked by
printing the number of activities and the GWP100 of 1 kWh of low-voltage electricity
in China. Explain each step in comments a beginner can follow.
```

**B4. Generate the prospective databases with premise** *(plan first)*. Start small: one scenario, two years.

```text
/plan Write scripts/02_premise.py. First list the TIAM-UCL pathways available in my
premise version (do not guess their names). Then build databases for SSP2-RCP2.6 in
2025 and 2030 only, with the electricity, fuels, hydrogen, steel and cement
transformations, and write them to brightway. Print how long each step took.
```

When this works, extend to all four pathways (RCP6.0, 4.5, 2.6, 1.9) and 2025–2050 in 5-year steps: 24 databases. Run it overnight.

**B5. Build the foreground with carculator.**

```text
Write scripts/03_vehicles.py using carculator to create inventories for BEV, PHEV
(diesel, utility factor 0.47), HEV (diesel) and FCEV in the 7 size classes, for model
years 2020-2050. Separate production, use and end-of-life activities. Regionalise
the electricity, diesel and hydrogen inputs so each car can be linked to any of the
16 TIAM-UCL regions in any scenario database.
```

**B6. Write the time adjustment, the heart of the paper.**

```text
Write src/time_adjust.py with a function footprint(powertrain, size, region,
scenario, production_year, lifetime, km). Production and its upstream use the
production-year database. Use-phase km are split equally across 5-year periods, each
linked to that period's database. End of life uses the final year. Return g CO2e/km
and a breakdown by stage. Add a test showing that with "No scenario" every stage
uses the 2025 database.
```

**B7. Set up the impact method.** Use IPCC 2021 GWP100. The paper gives non-fossil CO₂ uptake a factor of −1 and its emission +1, so that BECCS shows as a removal.

```text
Create a copy of the IPCC 2021 GWP100 method in brightway where non-fossil CO2
uptake has characterisation factor -1 and non-fossil CO2 emissions +1. Show me which
flows changed, and check a BECCS electricity activity now gives a negative score.
```

**B8. Comparative Monte Carlo.** Test with 200 samples, then run 5,000.

```text
Write scripts/04_monte_carlo.py: sample size (7), region (16), km (100,000-300,000),
lifetime (10-20) and scenario (4). In each sample compute ALL four powertrains with the
SAME inputs. Save to results/mc.parquet. Use multiprocessing, cache LCA objects, and
print progress.
```

**B9. Sobol sensitivity with SALib.**

```text
Write scripts/05_sobol.py using SALib's Saltelli sampling. Treat categorical inputs as
uniform variables rounded to integers (e.g. scenario sampled from -0.5 to 4.5). Report
first-order and total-order indices for (a) each car's footprint and (b) the %
difference between each car and the HEV, as in the paper's Fig. 6.
```

## Track C: repeat it with GCAM scenarios

The paper stresses that different IAMs decarbonise at different speeds for the same climate target. The [premise README](https://github.com/polca/premise) lists **GCAM v8.2** among its supported models, so you can swap TIAM-UCL for GCAM and keep the rest of your Track B pipeline. That makes a good Go 3 research project.

Three things change when you switch:

- **Regions.** GCAM has 32 energy regions; TIAM-UCL has 16. Your regionalised car inventories and the region list in the Monte Carlo must follow GCAM's regions.
- **Pathways.** Use the GCAM pathways your premise version ships with. They may not line up one-to-one with SSP2-RCP6.0/4.5/2.6/1.9, so record which ones you pair.
- **Technology mix.** GCAM chooses technologies with logit shares, not least-cost optimisation. Expect a different mix of hydrogen routes and BECCS, which matters most for FCEVs.

**C1. Generate GCAM databases** *(plan first)*.

```text
/plan Copy scripts/02_premise.py to scripts/02_premise_gcam.py. List the GCAM
pathways available in my premise version, propose the closest match to each of the
paper's four scenarios, and explain any mismatch. Build 2025-2050 databases for those
pathways with names that start with "gcam_".
```

**C2. Make the pipeline model-agnostic.**

```text
Refactor src/time_adjust.py and scripts/04_monte_carlo.py so the IAM ("tiam-ucl" or
"gcam") is a setting in config.yaml, together with its region list and scenario
names. Keep every TIAM-UCL test passing.
```

**C3. Compare the two models.**

```text
Run the 5,000-sample comparative Monte Carlo with GCAM. Then make one figure and one
table comparing TIAM-UCL and GCAM for: mean BEV vs HEV gap by scenario, share of cases
where the BEV wins, average breakeven mileage, and the FCEV result in the 1.5 C case.
Write a 200-word summary of where the models agree and disagree, and why.
```

A question worth answering: does the FCEV's 1.5 °C win survive in GCAM, or was it driven by TIAM-UCL's BECCS hydrogen? For background on how GCAM represents transport, see course module 3.2, *Transport in GCAM*.

## Check your results, and fix common problems

A Track B replication is on track when your numbers land near the paper's. Small differences are normal: package versions and random sampling both move results a little.

| Check | Paper's value | Where in the paper |
| --- | --- | --- |
| BEV below HEV, share of cases | about 99% | Fig. 2a |
| Mean BEV vs HEV, no scenario | 219 vs 289 g CO₂e/km | Fig. 2a text |
| Mean BEV vs HEV, No climate action | 206 vs 302 g CO₂e/km | Fig. 2a text |
| Mean BEV vs HEV, 1.5 °C | 142 vs 270 g CO₂e/km | Fig. 2a text |
| BEV footprint drop, China case, static → pLCA | −31% | Fig. 3 |
| Production drop, 2025 → 2035 build | 21–25% | Fig. 3c |
| Average breakeven, no scenario → 1.5 °C | 87,000 → 51,000 km | Fig. 5 |
| FCEV vs BEV in 1.5 °C | FCEV 70% lower | Fig. 2c |

Copy the table above into a file called docs/checks.md, then ask Claude to check before you trust a number:

```text
Compare my results/mc.parquet with the paper's values in the table in
@docs/checks.md. For each one, say whether mine is within 10%, and if not, list the
three most likely causes in my code, with file and line.
```

| Problem | Likely cause | What to ask Claude |
| --- | --- | --- |
| `pip` conflicts or brightway errors on import | Mixed Brightway 2 and 2.5 packages | "Show me every installed bw2* and premise version and make them consistent with premise 2.1.1 on brightway2." |
| premise refuses to load scenarios | Missing or wrong scenario key | "Check that the key in .env is passed to premise, without printing the key." |
| Out of memory building databases | Too many scenario-years at once | "Build one database per run and write it to brightway before starting the next." |
| BEV barely changes between scenarios | Use phase linked to the production-year database | "Print which database each use period of a BEV links to." |
| FCEV shows no big drop in 1.5 °C | Biogenic CO₂ factors not changed | "Show the characterisation factors for non-fossil CO2 uptake in my method." |
| Monte Carlo takes days | A new LCA object built for every sample | "Profile one sample and reuse factorised LCA objects across samples." |
| Results jump between runs | No random seed | "Set and record a random seed for every sampling step." |

One rule: if a result surprises you, ask Claude to **explain** it before you ask it to **fix** it. Many surprises are correct, such as hydrogen footprints below zero in the 1.5 °C case.

## Prompt cheat sheet and good habits

Good prompts name the files, say what done looks like, and say what not to touch.

| When you want to… | Type something like |
| --- | --- |
| Understand code | "Explain @src/time_adjust.py line by line for a beginner. Don't change it." |
| Plan a big change | "/plan Add PHEV utility factor as a Monte Carlo input from 0.2 to 0.8." |
| Fix an error | Paste the full error, then: "Find the cause, explain it, then propose the smallest fix." |
| Check a number | "Recompute this value by hand in a few lines and compare it with the model's output." |
| Make a figure | "Plot X against Y, coloured by scenario, labelled axes with units, save to results/." |
| Learn the method | "Which part of the paper's Methods section does this function implement?" |
| Save progress | "Run the tests, then commit with a clear message. Don't push." |

Habits that save beginners hours:

1. **One step per prompt.** Finish and check A1 before A2.
2. **Read every diff** before accepting. Ask "why this line?" when unsure.
3. **Plan mode for anything touching more than one file.**
4. **Keep secrets out of code.** The ecoinvent password and premise key live in `.env`, never in a prompt or a commit.
5. **Commit after each working step**, so you can always go back.
6. **Write down decisions in CLAUDE.md**, such as versions, region lists and seeds, so every new session starts with them.
7. **Licences.** ecoinvent data cannot be shared publicly. Commit code and results, not the database.

## Sources

- Šimaitis, J. et al. (2025). [Battery electric vehicles show the lowest carbon footprints among passenger cars across 1.5–3.0 °C energy decarbonisation pathways](https://doi.org/10.1038/s43247-025-02447-2). Communications Earth & Environment 6, 476.
- [premise on GitHub](https://github.com/polca/premise): installation, ecoinvent licence, scenario key, supported IAMs including TIAM-UCL v4.1 and GCAM v8.2.
- [Use Claude Code in VS Code](https://code.claude.com/docs/en/ide-integrations): install, Spark icon, @-mentions, plan mode, permission modes.
- [TIAM-UCL coupling dataset](https://doi.org/10.15125/BATH-01431), University of Bath.
