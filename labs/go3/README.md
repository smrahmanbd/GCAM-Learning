# Go 3 transport research kit (GCAM 9.1)

Companion kit to the Go 3 handbook *Research with GCAM: a transport case*. It gives you everything
around a GCAM transport study except GCAM itself: a stand-alone toy model of GCAM's passenger
transport structure, add-on XML templates for technology, behaviour and policy scenarios, a
configuration snippet and batch file, a query file, analysis scripts in Python and R, a
downscaling demo, and research templates.

**Targets:** gcam-core tag `gcam-v9.1` (released 2 June 2026). Element names, sector and technology
names, units and query titles were checked against that tag's source, input CSVs, ModelInterface
headers and `output/queries/Main_queries.xml` (file and line references are in each file's header).
The online documentation describes v8.2; where code and docs differ, the kit follows the code.

## Contents

| Path | What it is | Status |
| --- | --- | --- |
| `toy/gcam_transport_toy.py`, `toy/gcam_transport_toy.R` | Passenger transport toy model with GCAM's nesting, logit types and exponents, generalised cost with value of time, service demand elasticities and share-weight calibration. Five scenarios: Reference, BEV-low, Carbon-price, Fast-wage, LF-up. Writes `toy_results.csv` / `toy_results_R.csv` | Tested; Python and R agree exactly |
| `xml/trn_bev_cost_low.xml` | BEV car non-fuel cost -30% from 2030 (one region) | Template, not run in GCAM |
| `xml/trn_loadfactor_up.xml` | Car load factor +20% by 2050 | Template, not run |
| `xml/trn_zev_shareweights.xml` | Faster BEV/FCEV acceptance via global share-weights and an interpolation rule | Template, not run |
| `xml/trn_freight_truck_efficiency.xml` | Heavy diesel truck intensity -25% by 2050 | Template, not run |
| `xml/policy_carbon_tax.xml` | Regional CO2 tax, 25 $/tC (1990$) in 2025 +5%/yr | Template, not run |
| `xml/policy_co2_constraint_netzero.xml` | Regional CO2 cap falling linearly to zero in 2060 (MtC) | Template, not run |
| `xml/policy_zev_standard.xml` | ZEV standard as a credit market (RES policy), 10% to 70% of car pkm 2030-2050 | Template, not run; unit handling to test |
| `xml/scale_from_base.py` | Writes add-on XML by scaling values in **your** gcamdata-built base file (costs, load factors, intensities) | Tested on `xml/tests/base_transport_sample.xml` (synthetic) |
| `config/configuration_transport_snippet.xml` | Where the add-ons go in a copy of `exe/configuration_ref.xml` | Not run |
| `config/batch_transport.xml` | 4 technology x 3 policy batch matrix (12 runs) | Not run |
| `queries/transport_queries.xml` | 13 transport and CO2 queries copied unchanged from `Main_queries.xml` (line numbers in header) | Well-formed; not run against a database |
| `analysis/make_sample_data.py` | Builds SYNTHETIC GCAM-shaped CSVs and a 300-run ensemble from the toy | Tested |
| `analysis/read_transport.py` / `.R` | gcamreader / rgcam readers with a `--sample` / `sample` mode | Sample mode tested; database mode not run |
| `analysis/decompose_lmdi.py` / `.R` | LMDI-I decomposition of CO2 into activity, structure, intensity and carbon effects | Tested; Python and R agree |
| `analysis/plot_transport.py` | Mode shares, CO2 paths, fuel mix, LMDI waterfalls | Tested |
| `analysis/scenario_discovery.py` / `.R` | Classification tree (scikit-learn / rpart) and a PRIM-style box with coverage and density | Tested; same splits in both |
| `downscale/downscale_demo.py` | Region-to-country downscaling: proportional vs intensity convergence + harmonisation (DSCALE-inspired) on invented countries | Tested |
| `templates/research_proposal.md`, `scenario_design_matrix.csv`, `reporting_checklist.md` | Proposal outline, 12-scenario design matrix, reporting and reproducibility checklist (GCAM community guidelines, IAMC variables) | — |
| `run_all_tests.sh` | Re-runs everything that runs without GCAM | Passes |

## Quick start (no GCAM needed)

```bash
./run_all_tests.sh            # or run the steps one by one:
python3 toy/gcam_transport_toy.py
python3 analysis/make_sample_data.py
python3 analysis/read_transport.py --sample
python3 analysis/decompose_lmdi.py
python3 analysis/plot_transport.py
python3 analysis/scenario_discovery.py
python3 downscale/downscale_demo.py
```
Python 3.11+ with numpy, pandas, matplotlib, scikit-learn. R 4.x with dplyr, readr, rpart.

## Using the kit with GCAM 9.1

1. Build the input XML with gcamdata (or use the release package's `input/gcamdata/xml`).
2. Make add-ons from your own base file, so units match:
   `python3 xml/scale_from_base.py --base <gcam>/input/gcamdata/xml/transportation_UCD_CORE.xml --region "Middle East" --sector trn_pass_road_LDV_4W --subsector Car --tech BEV --field input-cost --factor 0.70 --from-year 2030 --out trn_bev_cost_low.xml`
   The numbers inside the shipped `xml/trn_*.xml` files are placeholders that show structure only.
3. Copy the add-ons to `<gcam>/input/user/`, copy `exe/configuration_ref.xml`, and paste the lines from
   `config/configuration_transport_snippet.xml` after the transportation entry. Or run the matrix with
   `config/batch_transport.xml` (set `BatchFileName` and `BatchMode` = 1).
4. Run GCAM, check that every period solved, then read results:
   `python3 analysis/read_transport.py --db <gcam>/output --dbname database_basexdb`
   (or `Rscript analysis/read_transport.R db <gcam>/output database_basexdb`), then the decomposition,
   plots and, for an ensemble, scenario discovery on your own run table.

## Things that trip people up

- **Units changed in v8.5:** transport output in billion pkm/tkm, costs 1975$/vkm, intensities EJ per
  billion vkm. v8.2 files and older papers use 1990$ and BTU/vkm. Never copy numbers across versions.
- **Hydrogen inputs were renamed in v8.8:** `H2 LDV`, `H2 MHDV`, `LH2`.
- **Where costs come from:** for most modes `OTAQ_trn_data_EMF37.csv` overrides `UCD_trn_data_CORE.csv`
  in gcamdata. Edit the file that actually feeds the XML.
- **Logit types:** modes compete with a relative-cost logit (sector level); technologies inside a mode
  with an absolute-cost logit (`A54.tranSubsector_logit_revised.csv`); `trn_pass_road_LDV_4W` is
  absolute-cost (`A54.sector.csv`). The documentation's choice page says relative for passenger
  transport; the input files say otherwise.
- **Share-weights are assumptions.** Changing them is not a model result; say so in the paper.
- **No vehicle stock:** "service output by tech (new)" (new vintages) is the closest thing to sales shares.
- **Carbon prices are 1990$ per tonne of carbon;** constraints are MtC.
- **Saudi Arabia** is inside "Middle East" in the public release. GCAM-KSA (KAPSARC) splits it out but
  is not part of gcam-core.

## About the toy model

It mimics GCAM's structure, not its numbers. Illustrative inputs are rounded from the Middle East rows of
`UCD_trn_data_CORE.csv` and `OTAQ_trn_data_EMF37.csv` or invented (base-year activity, fuel prices).
There is no vintaging, no solver feedback on fuel prices, no freight. Because there is no vintaging, BEV
uptake jumps when its share-weight switches on in 2030 (2025-2030 drop in CO2 in every scenario);
real GCAM spreads this over vehicle lifetimes. Reference results (from `toy_results.csv`):

| year | pkm (bn) | car % | BEV % of car | CO2 (Mt) |
| --- | --- | --- | --- | --- |
| 2020 | 1511 | 76.1 | 0.0 | 133 |
| 2050 | 2236 | 78.7 | 46.5 | 84 |
| 2100 | 3523 | 89.1 | 46.5 | 142 |

## Unverified (test before relying on it)

- Nothing in `xml/` or `config/` has been run in GCAM.
- `trn_zev_shareweights.xml`: whether the `fixed` interpolation rule replaces the base rule or adds to it.
- `policy_zev_standard.xml`: a credit input on a tranTechnology is per vehicle-km while secondary output
  is per passenger-km; the file scales the coefficient by an assumed load factor. Check that the
  resulting ZEV share of pkm equals the target.
- `batch_transport.xml`: empty FileSets used to mean "no add-on".
- `read_transport.py`: selecting queries by `q.title` on gcamreader's query objects.
- A transport-only carbon price (renamed CO2 object or `ctax-input`) is not provided because it is untested.
- IAMC variable names in the checklist follow the AR6 template convention; check the current common definitions.
