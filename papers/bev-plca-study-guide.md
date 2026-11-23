# Study guide: cars across 1.5–3 °C futures

**Paper:** Šimaitis, J., Lupton, R., Vagg, C., Butnar, I., Sacchi, R. & Allen, S. (2025). *Battery electric vehicles show the lowest carbon footprints among passenger cars across 1.5–3.0 °C energy decarbonisation pathways.* Communications Earth & Environment 6, 476. <https://doi.org/10.1038/s43247-025-02447-2> (open access, CC BY 4.0)

**Companions:** [Part 1: the basics (interactive)](bev-plca-basics.html) · [Part 2: the paper, hands-on](bev-plca.html) · [slides](../downloads/papers/BEV-pLCA-Simaitis2025-slides.pptx) · [toy model](../labs/papers/bev_plca_toy.py) · [implementation guide](bev-plca-implementation-guide.md)

---

## 1. The paper in three sentences

1. A car is built in year 0 and then driven for 10–20 years, but most life cycle assessments (LCAs) use **year-0 energy data for every stage**.
2. The authors use a **time-adjusted prospective LCA**: each 5-year period of driving gets the electricity, diesel and hydrogen mix from one of **four TIAM-UCL scenarios** (3.0 °C down to 1.5 °C).
3. Across **5,000 comparisons**, **battery electric vehicles (BEVs)** had the lowest footprint in almost every case, **32% (3 °C) to 47% (1.5 °C) below hybrids**, because electricity decarbonises faster than diesel or hydrogen.

## 2. Build-up: the ideas you need, in order

| Step | Idea | One-line meaning |
|--|---------|------------------------------|
| 1 | **Powertrain** | What moves the car: engine (ICEV), engine + small battery (HEV), plug-in battery + engine (PHEV), battery only (BEV), fuel cell + hydrogen (FCEV). |
| 2 | **Energy carrier** | Electricity, diesel or hydrogen. Each can be made in clean or dirty ways. |
| 3 | **Carbon intensity** | CO₂e per unit of energy: kg/kWh for electricity, kg/L for diesel, kg/kg for H₂. |
| 4 | **LCA** | Add up emissions from materials, manufacturing, use and end of life (*cradle to grave*). |
| 5 | **Functional unit** | What you compare: **g CO₂e per km** over the car's life. |
| 6 | **CO₂e / GWP100** | Other gases converted to CO₂ using 100-year global warming potentials (IPCC 2021). |
| 7 | **IAM scenario** | A model's picture of how the energy system changes under a climate target. |
| 8 | **Prospective LCA (pLCA)** | An LCA that uses future data from scenarios. |
| 9 | **Time adjustment** | Each life stage uses the data for *when* it happens. |
| 10 | **Comparative Monte Carlo** | Random input combinations, with every car worked out under the *same* inputs. |
| 11 | **Breakeven mileage** | Lifetime km at which a BEV's whole-life footprint drops below a hybrid's. |
| 12 | **Sobol index** | The share of the spread in a result caused by one input. |

## 3. The core equation (with a worked example)

**Footprint (g/km) = (production + end of life) ÷ lifetime km + average over use years of (energy per km × carbon intensity that year)**

*Example:* a BEV uses 0.20 kWh/km. The grid is 0.60, 0.45 and 0.30 kg CO₂e/kWh in three equal 5-year periods.

- Typical LCA: 0.20 × 0.60 = **120 g/km** for charging.
- Time-adjusted: 0.20 × (0.60 + 0.45 + 0.30)/3 = 0.20 × 0.45 = **90 g/km**, which is 25% less.

Add production: a 15 t BEV driven 200,000 km is 15,000,000 g ÷ 200,000 = **75 g/km**. As the grid gets cleaner, **production becomes the hotspot**.

## 4. Method at a glance

- **Background:** TIAM-UCL scenarios → **premise** → modified **ecoinvent 3.9.1** (electricity, diesel, hydrogen, steel, cement…).
- **Foreground:** **carculator** vehicle inventories (4 powertrains × 7 sizes; WLTP cycle; NMC-811 battery; diesel for combustion cars).
- **Matching and time adjustment:** **brightway2**. Production in year 0, use split into 5-year periods with equal km, end of life in the last year.
- **Impact method:** IPCC 2021 GWP100, with biogenic CO₂ counted as −1/+1 so that carbon-negative technologies (BECCS) appear.
- **Experiment:** 5,000 comparative Monte Carlo samples (size, 16 regions, 100–300k km, 10–20 years, scenario). Sobol sensitivity analysis with SALib.
- **End of life:** cut-off approach. Battery recycling credits are shown separately and not subtracted.

## 5. Numbers worth remembering

| What | Value |
|------------|-------------|
| BEV below HEV, share of cases | ~99% (all cases except a few in dirty-grid regions at low km) |
| Mean BEV vs HEV, typical LCA | 219 vs 289 g/km (−24%) |
| Mean BEV vs HEV, 3 °C | 206 vs 302 g/km (−32%) |
| Mean BEV vs HEV, 1.5 °C | 142 vs 270 g/km (−47%) |
| BEV vs PHEV | 20–31% lower (typical LCA: 15%) |
| BEV vs FCEV (not 1.5 °C) | 14–19% lower; BEV lower in 88–96% of cases |
| FCEV vs BEV (1.5 °C) | FCEV 70% lower, thanks to BECCS hydrogen |
| China case, BEV, typical → pLCA | −31% (other cars −3 to −19%) |
| Breakeven mileage (avg) | 87k (typical) → 70k → 64k → 63k → 51k km (1.5 °C) |
| Avg grid intensity behind those | 0.381 → 0.343 → 0.278 → 0.258 → 0.191 kg CO₂e/kWh |
| Production decarbonisation 2025 → 2035 | 21–25% |
| PHEV electric share assumed | 47% (the utility factor) |

## 6. Why each car behaves as it does

- **BEV:** high production footprint (battery), but use-phase emissions follow the grid, which cleans up in every scenario.
- **HEV:** exhaust CO₂ dominates. Biodiesel cleans up diesel *supply* (−41% in China), but the HEV footprint falls only about 11%.
- **PHEV:** in between, and sensitive to driver behaviour. If drivers rarely charge, it approaches (or exceeds) an HEV, so it is *high-risk*.
- **FCEV:** hydrogen is fossil-based for years, so gains are small, *except* in 1.5 °C, where carbon-negative BECCS hydrogen makes it the best (an unrealistic assumption for now).

## 7. Limitations to discuss

Coarse regions (Estonia and Norway hidden inside averages) · yearly time steps (no hourly charging) · BECCS realism · PHEV utility factor · carbon only (no metals, acidification) · one battery chemistry · diesel used instead of petrol (more optimistic for combustion cars).

## 8. Link to GCAM (this course)

TIAM-UCL is a cost-optimisation IAM. GCAM is a market-equilibrium IAM with logit choice. The pLCA chain is model-agnostic, and **premise also reads GCAM v8.2 scenarios**. A Go 3 project could repeat this comparison with GCAM scenarios and check whether the conclusions hold (see modules 1.5, 3.2, 3.6 and 3.9).

## 9. Self-test (answers below)

1. Why does a typical LCA overstate a BEV's footprint?
2. What is the functional unit?
3. A hybrid uses 6 L/100 km of diesel. What is the exhaust CO₂ in g/km?
4. Why do HEVs benefit least from ambitious scenarios?
5. In which scenario do FCEVs beat BEVs, and why should we be cautious?
6. What makes a Monte Carlo "comparative"?
7. Which two inputs matter most for the *difference* between BEV and HEV?
8. Name two limitations of the study.

<details><summary>Answers</summary>

1. It uses the 2025 grid for all 10–20 years of driving, but the grid gets cleaner.
2. 1 km driven over the vehicle's lifetime (g CO₂e/km).
3. 0.06 L/km × 2.68 kg/L = 0.161 kg = **161 g/km**.
4. Most of their footprint is fossil exhaust CO₂, which cleaner diesel supply hardly reduces.
5. 1.5 °C, because of carbon-negative BECCS hydrogen, which has low technology readiness.
6. All powertrains in one sample share the same inputs (size, region, km, lifetime, scenario).
7. Region and future scenario.
8. Any two from section 7.

</details>

## 10. Glossary

**BECCS:** bioenergy with carbon capture and storage; removes CO₂ from the air. **Brightway:** open-source Python LCA framework. **carculator:** Python model that builds car life cycle inventories. **ecoinvent:** commercial life cycle inventory database. **IAM:** integrated assessment model. **NDC:** nationally determined contribution (a country's climate pledge). **premise:** Python tool that rewrites ecoinvent using IAM scenarios. **RCP:** representative concentration pathway (W/m² of extra heating in 2100). **SSP2:** "middle of the road" socioeconomic storyline. **TIAM-UCL:** the TIMES Integrated Assessment Model at University College London. **Utility factor:** a PHEV's share of km driven on electricity. **WLTP:** standard test driving cycle.

---
*Independent teaching material. Numbers in sections 1, 4, 5 and 6 are from the paper; the worked example in section 3 is illustrative.*
