# Module 2.4 - Energy supply: levelised cost, resource supply curve, learning (toy numbers)
crf <- function(r, n) r * (1 + r)^n / ((1 + r)^n - 1)
lcoe <- function(capex, fom, cf, fuel_price = 0, eff = 1, ef = 0, carbon = 0, r = 0.07, n = 30) {
  mwh <- cf * 8.76
  (capex * crf(r, n) + fom) / mwh + fuel_price * 3.6 / eff + ef * 3.6 / eff * carbon
}
for (cp in c(0, 50, 100))
  cat(sprintf("carbon %3d: gas %5.1f, solar %5.1f $/MWh\n", cp,
      lcoe(1000, 25, 0.55, 6, 0.55, 0.0561, cp), lcoe(900, 15, 0.22)))
grades <- data.frame(q = c(0, 500, 1000, 1500), cost = c(3, 4.5, 7, 12))
resource_price <- function(cum) approx(grades$q, grades$cost, xout = cum, rule = 2)$y
cat("resource price at 200, 800, 1400 EJ:", resource_price(c(200, 800, 1400)), "\n")
cat("solar capex after 3 doublings at 20%:", 900 * (1 - 0.20)^3, "$/kW\n")
