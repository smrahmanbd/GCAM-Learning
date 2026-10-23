# Lab 13 (week 13) SOLUTION: a GCAM ensemble and scenario discovery
# New R skill: batch runs; a classification tree with rpart
# Needs: data/ensemble_results.csv, prepared by the instructor from 36 GCAM
#        runs (see gcam-files/ensemble_batch.xml). One row per run:
#          run           the GCAM scenario name
#          solar_cost    "low" or "high"
#          ccs_storage   "low" or "high"   (how much CO2 storage is available)
#          ssp           "SSP1", "SSP2" or "SSP3"   (population and GDP)
#          carbon_price  "none", "low" or "high"
#          co2_2050      global CO2 emissions in 2050, GtCO2
#        These column names are this course's own choice.
#        rpart comes with R; no installation needed on most machines.
# This is the complete version: every gap is filled in.

library(tidyverse)
library(rpart)

# ---- Part A: no code. Read gcam-files/ensemble_batch.xml with the slides.

# ---- Part B: label the runs and fit a tree ----
ens <- read_csv("data/ensemble_results.csv") |>
  mutate(across(where(is.character), factor))   # rpart wants factors
glimpse(ens)
count(ens, solar_cost, ccs_storage, ssp, carbon_price)   # 36 rows, n = 1

# A run is "high" if its 2050 emissions are above a cut-off that you choose.
cut_off <- quantile(ens$co2_2050, 0.75)   # 0.75 marks the top quarter
ens <- ens |>
  mutate(high = factor(if_else(
    co2_2050 > cut_off, "high", "other")))
count(ens, high)

ggplot(ens, aes(co2_2050, fill = high)) +
  geom_histogram(bins = 12) +
  labs(x = "Global CO2 in 2050 (GtCO2)", y = "Number of runs")

# The tree looks for the input settings that best separate high from other.
# minsplit = 6 lets it split small groups; the default of 20 suits big data.
tree <- rpart(high ~ solar_cost + ccs_storage +
                ssp + carbon_price,
              data = ens, method = "class",
              minsplit = 6)

# ---- Part C: read the tree and check it ----
print(tree)                       # one line per node; * marks a leaf
plot(tree, margin = 0.1)
text(tree, use.n = TRUE, pretty = 0)   # pretty = 0 writes level names in full

ens <- ens |>
  mutate(pred = predict(tree, type = "class"))   # "class" gives labels
table(predicted = ens$pred, actual = ens$high)
mean(ens$pred == ens$high)        # share of runs the tree gets right
tree$variable.importance          # larger = more useful for the splits

# Worksheet 12: change the cut-off to 0.5 and fit the tree again.
# Does the first split stay the same?
