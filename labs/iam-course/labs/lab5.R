# Lab 5 (week 5): running DICE many times
# Needs: R/dice.R, the course's teaching version of DICE. It must define
#   run_dice(discount = ..., damage = ...)
# returning a data frame with columns
#   year, output, emissions, temperature, carbon_price
# dice.R is NOT included here; the instructor supplies it.

library(tidyverse)
source("R/dice.R")

# ---- Part A: run DICE once and look inside the result ----
base <- run_dice()
glimpse(base)

ggplot(base, aes(year, temperature)) +
  geom_line()

ggplot(base, aes(year, carbon_price)) +
  geom_line()

# ---- Part B: vary one assumption and compare the runs ----
rates <- c(0.005, 0.015, 0.03)

one_run <- function(r) {
  run_dice(discount = r) |>
    mutate(rate = r)
}
runs <- map(rates, one_run) |>
  list_rbind()

ggplot(runs, aes(year, carbon_price)) +
  geom_line() +
  facet_wrap(~ rate)

# Step 5: repeat for the damage setting, keeping the discount rate
# at its default. Choose values around the default set in dice.R.
