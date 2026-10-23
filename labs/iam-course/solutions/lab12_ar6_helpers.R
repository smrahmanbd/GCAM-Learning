# Lab 12 SOLUTION, helper file. Copy to R/ar6_helpers.R
# Used by labs/lab12.R through source("R/ar6_helpers.R").
# Needs library(tidyverse) to be loaded by the main script.

# One AR6 variable in long form: one row per model, scenario and year.
to_long <- function(ar6, variable) {
  ar6 |>
    filter(Variable == variable) |>          # use the function's argument
    pivot_longer(matches("^[0-9]{4}$"),
      names_to = "year", values_to = "value") |>
    mutate(year = as.integer(year)) |>
    drop_na(value)
}
