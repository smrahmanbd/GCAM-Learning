# Lab 12 SOLUTION, helper file. Copy to R/gcam_helpers.R
# Used by labs/lab12.R through source("R/gcam_helpers.R").
# Needs library(tidyverse) and library(rgcam) to be loaded by the main script.

# Global CO2 for one GCAM scenario, in GtCO2 per year.
# GCAM reports this query in million tonnes of carbon (look at the Units
# column): x 44/12 gives MtCO2, / 1000 gives GtCO2.
get_co2 <- function(prj, scen) {
  getQuery(prj, "CO2 emissions by region", scenarios = scen) |>
    group_by(scenario, year) |>
    summarise(gt = sum(value) * 44 / 12 / 1000, .groups = "drop")
}
