# Lab 14 (week 14) SOLUTION: project clinic - polishing charts and tables
# New R skill: titles and labels with units, a fixed scenario order and
#              colours, theme and text size, ggsave, a table with kable
# Needs: output/gcam_course.dat with the query "CO2 emissions by region".
#        The example uses the course scenarios and the region Japan:
#        replace them with your team's scenarios and region.
# This is the complete version: every gap is filled in.

library(tidyverse)
library(rgcam)

prj <- loadProject("output/gcam_course.dat")

# ---- Part A: one order, one set of colours, clear labels ----
# Define these once at the top (or in R/style.R) and use them in every figure.
scen_order <- c("Reference", "CheapSolar",
                "CarbonPrice", "NetZero")
scen_cols <- c(Reference   = "#5E6E73",
               CheapSolar  = "#E69F00",
               CarbonPrice = "#0072B2",
               NetZero     = "#009E73")

co2 <- getQuery(prj, "CO2 emissions by region") |>
  filter(region == "Japan", year >= 2020) |>      # replace with your region
  mutate(mt = value * 44 / 12)                    # MTC to MtCO2: check Units

co2 <- co2 |>
  mutate(scenario = factor(scenario,
                           levels = scen_order))         # the order vector

p <- ggplot(co2,
       aes(year, mt, colour = scenario)) +
  geom_line(linewidth = 1) +
  scale_colour_manual(values = scen_cols) +
  labs(title = "Write your main finding here, as one short sentence",                             # your finding in one line
       x = NULL,
       y = "CO2 emissions (MtCO2 per year)",
       colour = NULL,
       caption = "Source: own GCAM runs. CO2 from energy and industry.") +
  theme_minimal(base_size = 14)
p

# ---- Part B: save the figure and make a summary table ----
# Fix the size in the code so the figure looks the same on every computer.
ggsave("output/fig1_co2.png", plot = p,
       width = 16, height = 10,
       units = "cm", dpi = 300)                   # 300 is print quality

tab <- co2 |>
  filter(year %in% c(2030, 2050)) |>
  select(scenario, year, mt) |>
  pivot_wider(names_from = year,
              values_from = mt)
tab

# In your R Markdown report, put this in a chunk:
knitr::kable(tab, digits = 0,
  caption = "CO2 emissions, MtCO2 per year")
