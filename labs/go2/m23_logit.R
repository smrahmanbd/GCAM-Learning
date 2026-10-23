# Module 2.3 - Choice: the logit (relative-cost form as in GCAM's economic choice docs)
relative_logit <- function(costs, g, w = rep(1, length(costs))) { x <- w * costs^g; x / sum(x) }
absolute_logit <- function(costs, b, w = rep(1, length(costs))) { x <- w * exp(b * costs); x / sum(x) }
costs <- c(coal = 60, gas = 70, solar = 80)
for (g in c(-1, -4, -10)) { cat("exponent", g, ": "); print(round(relative_logit(costs, g), 3)) }
# Calibrate share weights so the base year reproduces observed shares
observed <- c(0.30, 0.50, 0.20); g <- -4
w <- observed / costs^g; w <- w / w[1]
cat("share weights:", round(w, 3), " -> shares:", round(relative_logit(costs, g, w), 3), "\n")
# Two-level nest: fossil (coal, gas) vs solar
fossil <- relative_logit(c(60, 70), -6); fossil_cost <- sum(c(60, 70) * fossil)
top <- relative_logit(c(fossil_cost, 80), -3)
cat(sprintf("nested: coal %.3f, gas %.3f, solar %.3f\n", top[1] * fossil[1], top[1] * fossil[2], top[2]))
