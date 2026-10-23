# Reporting checklist for a GCAM transport study

Tick every line before submitting a report, thesis chapter or paper.

## A. Model description (GCAM community guidelines, https://jgcri.github.io/gcam-doc/community-guide.html)
- [ ] GCAM version stated ("GCAM v9.1"), with the public repository and the DOI of that release cited.
- [ ] Documentation cited (the guidelines suggest "JGCRI, 2025. GCAM Documentation (Version 8.2)" with its Zenodo DOI; note that the docs describe v8.2 while the release used is 9.x).
- [ ] Standard introductory description of GCAM used, with links to the documentation.
- [ ] Every change from the public model listed (file, element, old and new value, reason). Substantial changes: model renamed "GCAM-<institution>" and the change stated in the opening paragraph.
- [ ] GCAM team members invited as co-authors where their expertise is used (guidelines); questions on data or results raised on GCAM GitHub Discussions.

## B. Transport-specific transparency
- [ ] Nesting and logit exponents used (default from A54.sector.csv and A54.tranSubsector_logit_revised.csv, or changed).
- [ ] Source of vehicle costs and intensities named (OTAQ_trn_data_EMF37.csv overrides UCD_trn_data_CORE.csv for most modes in 9.1).
- [ ] Units stated: pkm/tkm in billions, costs 1975$/vkm, intensities EJ per billion vkm, carbon prices 1990$/tC (converted for the reader, e.g. to 2024$/tCO2, with the deflator named).
- [ ] Share-weight changes reported as assumptions, with the reason.
- [ ] Statement that GCAM has no vehicle stock: "sales shares" are new-vintage output shares.
- [ ] Value-of-time settings (time-value multipliers, speeds, wage definition) if mode shift matters to the result.

## C. Results reporting (IAMC-style variable names)
Report regional results in the IAMC template format (model, scenario, region, variable, unit, years) so they can be compared with other models. Names below follow the IAMC/AR6 template convention; check them against the current IAMC common definitions (https://github.com/IAMconsortium/common-definitions) before submission.
| Variable | Unit | GCAM source query |
| --- | --- | --- |
| Final Energy\|Transportation | EJ/yr | transport final energy by fuel (sum) |
| Final Energy\|Transportation\|Liquids | EJ/yr | ... fuel = refined liquids enduse |
| Final Energy\|Transportation\|Electricity | EJ/yr | ... fuel = elect_td_trn |
| Final Energy\|Transportation\|Hydrogen | EJ/yr | ... fuel = H2 LDV, H2 MHDV, LH2 |
| Final Energy\|Transportation\|Gases | EJ/yr | ... fuel = delivered gas |
| Energy Service\|Transportation\|Passenger | bn pkm/yr | transport service output by service |
| Energy Service\|Transportation\|Freight | bn tkm/yr | transport service output by service |
| Emissions\|CO2\|Energy\|Demand\|Transportation | Mt CO2/yr | CO2 emissions by sector (x 44/12 from MTC) |
| Price\|Carbon | US$2010/t CO2 | CO2 market price (convert from 1990$/tC) |

## D. Reproducibility
- [ ] Repository with: configuration files, every add-on XML, batch file, query file, analysis scripts, a README with run order.
- [ ] gcamdata changes as user-modification chunks or a documented diff, plus the commit hash of gcam-core.
- [ ] Output database not committed (too large); instead the queried CSVs and the scripts that make every figure.
- [ ] Each figure regenerates from one command; random seeds fixed for ensembles.
- [ ] Solver log checked: all periods solved; warnings listed.
- [ ] Data licences respected (e.g. IEA data terms) and stated.

## E. Interpretation
- [ ] Results compared with at least one other source (another model, AR6 database, national plan).
- [ ] Limits stated: no stock turnover by vehicle count, regional data generality, behavioural realism, aviation/shipping fuels.
- [ ] Uncertainty shown (ranges, ensemble or sensitivity), not single lines only.
