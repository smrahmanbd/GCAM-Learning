# Research proposal template: a GCAM transport study

Fill every section in one to three sentences, then keep this file in the project repository and
update it when the design changes. Two pages maximum.

## 1. Question
- **Policy or science question (one sentence):**
  _e.g. What does a light-duty zero-emission standard achieve in the Middle East by 2050, compared with a carbon price of equal cost?_
- **Who will use the answer, and for what decision?**
- **Why GCAM** (what the question needs that a sector-only model cannot give: fuel-price feedback, electricity and hydrogen supply, land and bioenergy, other regions)?
- **What GCAM cannot answer here** (no vehicle stock or sales in units, no explicit charging infrastructure, generic regional data unless overridden, aviation and shipping liquids not distinct).

## 2. Model and version
- GCAM release: `gcam-v9.1` (or later) — tag and commit hash: ______
- Region(s) studied: ______ (public GCAM 9.1 has 32 energy-economy regions; Saudi Arabia is part of "Middle East" unless you use GCAM-KSA)
- Modifications to the public model (list each file and why). If substantial, name the model "GCAM-<institution>" (GCAM community guidelines).
- Unit conventions checked: transport costs 1975$/vkm and intensities EJ per billion vkm (v8.5+); carbon prices 1990$/tC; CO2 constraints MtC.

## 3. Scenario design (see scenario_design_matrix.csv)
| Dimension | Values | Implemented by |
| --- | --- | --- |
| Socioeconomics | e.g. SSP2 (reference), SSP1 and SSP3 as sensitivity | configuration_ssp.xml / batch files |
| Technology | Reference; BEV cost -30%; ... | xml/trn_bev_cost_low.xml ... |
| Behaviour | Reference; load factor +20% ... | xml/trn_loadfactor_up.xml |
| Policy | None; carbon tax; net-zero constraint; ZEV standard | xml/policy_*.xml |

- Number of runs: ______ (dimensions multiply; check run time and disk space).
- Which comparison answers the question (e.g. policy run minus its own reference, same assumptions otherwise)?

## 4. Indicators
- Primary: ______ (e.g. direct transport CO2 2050 in MtCO2; ZEV share of car pkm)
- Secondary: final energy by fuel; service by mode; electricity and hydrogen demand; carbon price; cost of transport services.
- Queries used: `queries/transport_queries.xml` (titles listed in its header).

## 5. Uncertainty plan
- Which inputs are uncertain, and ranges with sources (table).
- Method: one-at-a-time sensitivity / ensemble (n = __) / scenario discovery on the ensemble (analysis/scenario_discovery.py).
- What result would change the policy conclusion?

## 6. Validation and checks
- Base year: compare calibrated 2021 transport energy with IEA balances for the region.
- Recent trend: compare 2025 model years with observed EV sales / fuel use where available.
- Solver: every period solved; log checked for warnings.
- Sanity: decomposition (analysis/decompose_lmdi.py) explains the CO2 change with sensible signs.

## 7. Outputs and timeline
- Figures and tables (list), report sections, code and data release plan (repository + DOI).
- Weeks 1–2 design and setup · 3–4 runs · 5 analysis · 6 write-up and presentation.
