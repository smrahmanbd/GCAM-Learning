# Module 2.5 - Energy demand: service demand and mode choice with the cost of time (toy numbers)
service_demand <- function(base, income_ratio, price_ratio, inc_el = 0.6, price_el = -0.3)
  base * income_ratio^inc_el * price_ratio^price_el
cat("pkm if income doubles:", round(service_demand(100, 2, 1), 1), "; and 50% dearer:", round(service_demand(100, 2, 1.5), 1), "\n")
modes <- data.frame(mode = c("walk", "bus", "rail", "car"), money = c(0, 0.05, 0.12, 0.30), speed = c(5, 15, 30, 60))
for (wage in c(2, 10, 40)) {
  gc <- modes$money + 0.5 * wage / modes$speed       # value of time = half the wage
  sh <- gc^-3 / sum(gc^-3)
  cat(sprintf("wage %2d $/h: ", wage)); print(setNames(round(sh, 3), modes$mode))
}
