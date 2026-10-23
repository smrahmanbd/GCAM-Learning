# Lab 12 (week 12) SOLUTION: compare your GCAM run with AR6 scenarios
# New R skill: organising a reproducible analysis - folders, sourced
#              scripts, Git basics
# Needs: output/gcam_course.dat (your rgcam project file; it must hold the
#          query "CO2 emissions by region" for ALL regions),
#        data/ar6_world.csv and data/ar6_meta.csv (from lab 6)
# This is the complete version: every gap is filled in.

library(tidyverse)
library(rgcam)

# ---- Part A: the two functions now live in the R folder ----
# R/ar6_helpers.R   defines to_long(ar6, variable)   (solutions/lab12_ar6_helpers.R)
# R/gcam_helpers.R  defines get_co2(prj, scen)       (solutions/lab12_gcam_helpers.R)
source("R/ar6_helpers.R")
source("R/gcam_helpers.R")

# ---- Part B: your run beside other models' runs ----
prj  <- loadProject("output/gcam_course.dat")
listScenarios(prj)
listQueries(prj)                 # is "CO2 emissions by region" in the list?
gcam <- get_co2(prj, "CarbonPrice") |>
  filter(year >= 2020)

ar6  <- read_csv("data/ar6_world.csv")
meta <- read_csv("data/ar6_meta.csv")

# Match the scope. The GCAM query counts CO2 from energy and industry and
# leaves out land-use change, so use the AR6 variable with the same scope.
# The GCAM line is the sum of all regions, to match Region "World".
co2_var <- "Emissions|CO2|Energy and Industrial Processes"

# AR6 scenarios with a 2050 carbon price close to yours.
# Look at the Unit column of Price|Carbon first. Your instructor gives you
# the 2050 price of your CarbonPrice run in that unit. Choose a band
# around it, for example from half to double.
similar <- to_long(ar6, "Price|Carbon") |>
  filter(year == 2050, value > 50, value < 200)   # EXAMPLE band only: set it around your own price
nrow(similar)                    # aim for 20 to 100 scenarios

ar6_co2 <- to_long(ar6, co2_var) |>
  semi_join(similar, by = c("Model", "Scenario")) |>  # keep matching rows
  filter(year >= 2020) |>
  mutate(run = paste(Model, Scenario))

ggplot() +
  geom_line(aes(year, value / 1000, group = run),
            data = ar6_co2, alpha = 0.2) +
  geom_line(aes(year, gt), data = gcam,
            colour = "#B84A14", linewidth = 1.5) +
  labs(x = NULL, y = "CO2 from energy and industry (GtCO2 per year)",
       title = "My GCAM run (orange) and AR6 scenarios with a similar 2050 carbon price")

# Which warming categories do the similar-price scenarios fall in?
similar |>
  left_join(meta, by = c("Model", "Scenario")) |>
  count(Category)

# Spread of AR6 results in 2050, to compare with your run:
ar6_co2 |>
  filter(year == 2050) |>
  summarise(low = min(value) / 1000, median = median(value) / 1000,
            high = max(value) / 1000)
filter(gcam, year == 2050)

# ---- Part C: Git (type these in the Terminal pane, not the Console) ----
# git config --global user.name "Your Name"         (once per computer)
# git config --global user.email you@example.org    (once per computer)
# git init
# Copy gcam-files/gitignore_lab12.txt to the project folder as .gitignore
# git status
# git add .gitignore R labs
# git commit -m "write your own message here"
# git log --oneline
