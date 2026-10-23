# Lab 9 (week 9): map land and water results; first look inside gcamdata
# Needs: output/gcam_course.dat from labs 7 and 8, the rmap package, and
#        your own copy of gcamdata on the course server (~/gcamdata).
# Hand in: Worksheet 8 as a knitted R Markdown report.
#
# SOLUTION: the two gaps of labs/lab9.R are filled in.

library(tidyverse)
library(rgcam)

# ---- Part A: map cropland by region ----
prj <- loadProject("output/gcam_course.dat")
crops <- prj |>
  getQuery("aggregated land allocation") |>
  filter(scenario == "Reference", year == 2050,
         landleaf == "crops") |>
  group_by(region) |>
  summarise(value = sum(value)) |>
  mutate(subRegion =
           str_replace_all(region, "-", "_"))
rmap::map(crops, shape = rmap::mapGCAMReg32,
          save = FALSE)

# ---- Part B: map water withdrawals by basin ----
basin <- prj |>
  getQuery("water withdrawals by basin") |>
  filter(scenario == "Reference", year == 2050) |>
  mutate(subRegion = str_remove(
    basin, "_water withdrawals")) |>
  group_by(subRegion) |>
  summarise(value = sum(value)) |>
  left_join(rmap::mapping_gcambasins,
            by = "subRegion") |>
  select(subRegion = subRegionMap, value)
rmap::map(basin, shape = rmap::mapGCAMBasins,
          save = FALSE)

# ---- Part C: a first look inside gcamdata ----
gcamdata_dir <- path.expand("~/gcamdata")
devtools::load_all(gcamdata_dir)
chunks <- find_chunks()
count(chunks, module)
inputs_of("module_energy_L223.electricity")
outputs_of(
  "module_energy_elec_tech_scenarios_xml")
cf <- read_csv(file.path(gcamdata_dir,
  "inst/extdata/energy",
  "A23.globaltech_capacity_factor.csv"),
  comment = "#")
filter(cf, subsector == "solar")
