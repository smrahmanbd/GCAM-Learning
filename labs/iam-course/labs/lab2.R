# Lab 2 (week 2): first plots and the Hector climate model
# Needs: data/co2_annual.csv (columns: year, ppm) and the hector package

library(tidyverse)

# ---- Part A: read a data file and draw a first chart ----
co2 <- read_csv("data/co2_annual.csv")
glimpse(co2)
head(co2)
max(co2$ppm)

ggplot(co2, aes(x = year, y = ppm)) +
  geom_line() +
  labs(y = "CO2 (ppm)")

# ---- Part B: run Hector for a low and a high emissions path ----
# install.packages("hector")   # run once
library(hector)

ini <- system.file("input/hector_ssp126.ini",
                   package = "hector")
low <- newcore(ini, name = "low")
run(low)
t_low <- fetchvars(low, 2000:2100,
                   GLOBAL_TAS())   # older Hector versions: GLOBAL_TEMP()

ini <- system.file("input/hector_ssp585.ini",
                   package = "hector")
high <- newcore(ini, name = "high")
run(high)
t_high <- fetchvars(high, 2000:2100,
                    GLOBAL_TAS())

temps <- bind_rows(t_low, t_high)
ggplot(temps, aes(year, value,
                  colour = scenario)) +
  geom_line()
