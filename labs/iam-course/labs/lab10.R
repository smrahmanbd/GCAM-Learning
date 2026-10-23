# Lab 10 (week 10): a carbon price, a net-zero scenario, and one changed
#                   assumption in gcamdata
# Needs: output/gcam_course.dat from labs 7 to 9, the instructor's database
#        (now with CarbonPrice and NetZero), gcam-files/course_queries.xml,
#        gcam-files/carbon_price_global.xml,
#        gcam-files/lab10_carbonprice_config_snippet.xml,
#        and your own copy of gcamdata (~/gcamdata) with its cache built.
# Hand in: Worksheet 9 as a knitted R Markdown report.
#
# Gaps are written ___ with a hint in the comment beside them.
# This script has three gaps.

# ---- Part A: build and start the CarbonPrice run (Terminal tab, not R) ----
#
#   cd ~/gcam/exe
#   cp configuration_ref.xml config_carbonprice.xml
#   # edit config_carbonprice.xml (two changes), then:
#   nohup ./gcam.exe -C config_carbonprice.xml &
#   tail -n 3 logs/main_log.txt
#
# The two changes are shown in
# gcam-files/lab10_carbonprice_config_snippet.xml:
#   1. add carbon_price_global.xml as the last input file (full path)
#   2. change scenarioName from Reference to CarbonPrice

# ---- Part B: compare the policy scenarios with the reference ----
# Run Part B in the iam-course project.
library(tidyverse)
library(rgcam)
db_dir <- "/course/gcam/output"  # from instructor
conn <- localDBConn(db_dir, "database_basexdb")

prj <- loadProject("output/gcam_course.dat")
for (s in c("CarbonPrice", "___")) {  # 2nd policy
  prj <- addScenario(conn, prj, s,
    "gcam-files/course_queries.xml")
}
# Hint: the second policy scenario is the one the instructor ran with an
# emissions limit. See listScenariosInDB(conn) for its exact name.
co2 <- getQuery(prj, "CO2 emissions by region") |>
  group_by(scenario, year) |>
  summarise(value = sum(value), .groups = "drop")
ggplot(co2, aes(year, value, colour = scenario)) +
  geom_line()
temp <- getQuery(prj, "___")  # a query title
# Hint: one query in listQueries(prj) returns the global mean temperature.
getQuery(prj, "CO2 prices") |> distinct(market)

# Plot temperature the same way as emissions:
ggplot(temp, aes(year, value, colour = scenario)) +
  geom_line()
# And the carbon price in each market:
price <- getQuery(prj, "CO2 prices")
ggplot(price, aes(year, value, colour = scenario)) +
  geom_line() +
  facet_wrap(~ market)

# ---- Part C: change one assumption in gcamdata and rebuild ----
# Run Part C in your gcamdata project, not in iam-course:
# File > Open Project, then choose ~/gcamdata/gcamdata.Rproj.
# Do NOT edit R/constants.R: gcamdata then clears its whole cache and
# rebuilds everything, which takes far longer than the lab.
library(tidyverse)
devtools::load_all(".")
obj <- "L223.GlobalIntTechCapFac_elec"
before <- drake::readd(obj, character_only = TRUE)
file.edit(file.path("inst/extdata/energy",
  "A23.globaltech_capacity_factor.csv"))
# change the PV value for 2050, save, then:
devtools::load_all(".")
driver_drake()
after <- drake::readd(obj, character_only = TRUE)
filter(after, subsector.name == "solar",
       year == ___)  # the year you edited
# Hint: you changed the number in one year column of the PV row.
# Compare with the old value:
# filter(before, subsector.name == "solar", year == 2050)
