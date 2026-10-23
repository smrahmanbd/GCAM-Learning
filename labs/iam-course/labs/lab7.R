# Lab 7 (week 7): run the reference scenario and pull results into R
# Needs: your GCAM workspace on the course server (~/gcam),
#        the instructor's database folder (db_dir below),
#        gcam-files/course_queries.xml, and the rgcam package.
# Hand in: Worksheet 6 as a knitted R Markdown report.

# ---- Part A: start your own reference run (Terminal tab, not R) ----
# Type these four lines in the RStudio Terminal tab. They are shell
# commands, so they are written here as comments.
#
#   cd ~/gcam/exe
#   cp configuration_ref.xml configuration.xml
#   nohup ./gcam.exe -C configuration.xml &
#   tail -n 3 logs/main_log.txt
#
# The run carries on after the lab. It is finished when the last lines of
# exe/logs/main_log.txt include "Model run completed."

# ---- Part B: connect to the database and run the queries ----
library(tidyverse)
library(rgcam)
db_dir <- "/course/gcam/output"  # from instructor
conn <- localDBConn(db_dir, "database_basexdb")
listScenariosInDB(conn)

dir.create("output", showWarnings = FALSE)
prj <- addScenario(conn, "output/gcam_course.dat",
  "Reference", "gcam-files/course_queries.xml")
listScenarios(prj)
listQueries(prj)

# ---- Part C: get one query, plot it, save the project ----
co2 <- getQuery(prj, "CO2 emissions by region")
glimpse(co2)
japan <- filter(co2, region == "Japan")  # replace with your region
ggplot(japan, aes(year, value)) +
  geom_line() +
  labs(y = japan$Units[1])

elec <- getQuery(prj, "elec gen by subsector") |>
  filter(region == "Japan")
ggplot(elec, aes(year, value, fill = subsector)) +
  geom_col()
saveProject(prj)

# Next time you do not need the database or the queries again:
# prj <- loadProject("output/gcam_course.dat")
