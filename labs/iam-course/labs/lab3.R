# Lab 3 (week 3): Kaya decomposition with dplyr
# Needs: data/kaya_data.csv (columns: country, year, pop, gdp, energy, co2)

library(tidyverse)
kaya <- read_csv("data/kaya_data.csv")

# ---- Part A: pick a country and compute its Kaya factors ----
mine <- kaya |>
  filter(country == "Japan") |>          # replace Japan with your country
  select(year, pop, gdp, energy, co2) |>
  mutate(
    income   = gdp / pop,
    e_intens = energy / gdp,
    c_intens = co2 / energy
  )

# ---- Part B: which factor drove the change? ----
change <- mine |>
  arrange(year) |>
  summarise(
    pop      = last(pop) / first(pop),
    income   = last(income) / first(income),
    e_intens = last(e_intens) / first(e_intens),
    c_intens = last(c_intens) / first(c_intens),
    co2      = last(co2) / first(co2)
  )
change

# Check: the four factor ratios multiply to the CO2 ratio
change$pop * change$income * change$e_intens * change$c_intens
change$co2

# Step 4: three countries at once
kaya |>
  filter(country %in% c("Japan", "India", "Brazil")) |>
  select(country, year, pop, gdp, energy, co2) |>
  mutate(
    income   = gdp / pop,
    e_intens = energy / gdp,
    c_intens = co2 / energy
  ) |>
  arrange(year) |>
  group_by(country) |>
  summarise(
    pop      = last(pop) / first(pop),
    income   = last(income) / first(income),
    e_intens = last(e_intens) / first(e_intens),
    c_intens = last(c_intens) / first(c_intens),
    co2      = last(co2) / first(co2)
  )
