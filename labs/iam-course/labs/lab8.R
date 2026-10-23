# Lab 8 (week 8): change a technology cost and compare with the reference
# Needs: output/gcam_course.dat from lab 7, the instructor's database
#        (now with the CheapSolar scenario), gcam-files/course_queries.xml,
#        gcam-files/lab8_cheapsolar_config_snippet.xml, rgcam and rchart.
# Hand in: Worksheet 7 as a knitted R Markdown report.

# ---- Part A: build and start the CheapSolar run (Terminal tab, not R) ----
#
#   cd ~/gcam/exe
#   tail -n 3 logs/main_log.txt
#   cp configuration_ref.xml config_cheapsolar.xml
#   # edit config_cheapsolar.xml (two changes), then:
#   nohup ./gcam.exe -C config_cheapsolar.xml &
#
# The two changes are shown in gcam-files/lab8_cheapsolar_config_snippet.xml:
#   1. add solar_adv.xml as the last input file, before the solver line
#   2. change scenarioName from Reference to CheapSolar

# ---- Part B: add CheapSolar and take differences from Reference ----
library(tidyverse)
library(rgcam)
db_dir <- "/course/gcam/output"  # from instructor
conn <- localDBConn(db_dir, "database_basexdb")

prj <- loadProject("output/gcam_course.dat")
prj <- addScenario(conn, prj, "CheapSolar",
  "gcam-files/course_queries.xml")
elec <- getQuery(prj, "elec gen by subsector") |>
  filter(region == "Japan")              # replace with your region
ref <- elec |>
  filter(scenario == "Reference") |>
  select(subsector, year, ref = value)
dif <- elec |>
  filter(scenario == "CheapSolar") |>
  left_join(ref, by = c("subsector", "year")) |>
  mutate(change = value - ref)
# If left_join warns about a many-to-many match, add up elec first:
# elec <- elec |> group_by(scenario, region, subsector, year) |>
#   summarise(value = sum(value), .groups = "drop")

# ---- Part C: plot the differences, then let rchart do it ----
ggplot(dif, aes(year, change, fill = subsector)) +
  geom_col()
library(rchart)
rc <- elec |>
  select(scenario, region, year, value,
         class = subsector) |>
  mutate(param = "Electricity")
charts <- chart(rc, scenRef = "Reference",
                save = FALSE)
names(charts)
charts$chart_class
charts$chart_class_diff_absolute
