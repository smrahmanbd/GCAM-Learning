# Lab 1 (week 1): install R, run a first script
# Part A of this lab is done in the browser: en-roads.climateinteractive.org

# install once; load in every script
install.packages("tidyverse")
library(tidyverse)

# CO2 in the air, parts per million
co2 <- c(before = 280, today = 420)

co2["today"] - co2["before"]   # expect 140
co2["today"] / co2["before"]   # expect 1.5
