# Lab 6 (week 6): reading AR6 scenarios
# Needs: data/ar6_world.csv (columns: Model, Scenario, Region, Variable,
#        Unit, then one column per year) and
#        data/ar6_meta.csv  (columns: Model, Scenario, Category)

library(tidyverse)
ar6 <- read_csv("data/ar6_world.csv")

# ---- Part A: reshape from wide to long ----
long <- ar6 |>
  filter(Variable == "Emissions|CO2") |>
  pivot_longer(
    matches("^[0-9]{4}$"),
    names_to = "year",
    values_to = "mt"
  ) |>
  mutate(year = as.integer(year),
         gt = mt / 1000)
# long <- drop_na(long, mt)   # if missing years cause trouble

# ---- Part B: join the categories and plot ----
meta <- read_csv("data/ar6_meta.csv")

both <- long |>
  left_join(meta,
    by = c("Model", "Scenario")) |>
  filter(Category %in% c("C1", "C3", "C7")) |>
  mutate(run = paste(Model, Scenario))

ggplot(both, aes(year, gt, group = run)) +
  geom_line(alpha = 0.2) +
  facet_wrap(~ Category)

# Then: File > New File > R Markdown. Paste this code into chunks,
# add a sentence under each chart, and press Knit.
