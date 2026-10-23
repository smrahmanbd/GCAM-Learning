# scenario_discovery.R - classification tree (rpart) on the ensemble table, as in course lab 13.
# Same data and "high" definition as scenario_discovery.py (top quarter of 2050 CO2).
# Run: Rscript scenario_discovery.R
suppressMessages({library(rpart); library(readr)})
here <- tryCatch(dirname(normalizePath(sub("--file=", "", grep("--file=", commandArgs(), value = TRUE)))), error = function(e) ".")
df <- read_csv(file.path(here, "sample_data", "ensemble.csv"), show_col_types = FALSE)
thr <- quantile(df$co2_2050_mtco2, 0.75, type = 7)
df$high <- factor(df$co2_2050_mtco2 > thr, levels = c(FALSE, TRUE), labels = c("not_high", "high"))
cat(sprintf("%d runs; 'high' = 2050 CO2 above %.1f Mt: %d runs\n\n", nrow(df), thr, sum(df$high == "high")))
fit <- rpart(high ~ bev_cost_mult + car_lf_2050 + gdp_growth + carbon_start_usd_tco2, data = df,
             method = "class", control = rpart.control(maxdepth = 3, minbucket = 10, cp = 0.01))
print(fit)
cat("\nVariable importance:\n"); print(round(fit$variable.importance / sum(fit$variable.importance), 2))
# Coverage and density of the leaf that holds most high runs
leaf <- fit$where; tab <- table(leaf, df$high)
best <- rownames(tab)[which.max(tab[, "high"])]
inleaf <- leaf == as.integer(best)
cov <- sum(df$high[inleaf] == "high") / sum(df$high == "high"); den <- mean(df$high[inleaf] == "high")
cat(sprintf("\nLeaf with most high runs: coverage %.2f, density %.2f\n", cov, den))
