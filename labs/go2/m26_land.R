# Module 2.6 - Land, food and bioenergy (toy numbers, week 9 example)
profit <- function(price, cost, yield_t) (price - cost) * yield_t
land_shares <- function(p, exponent = 1) { p <- pmax(p, 1e-9); p^exponent / sum(p^exponent) }
for (gp in c(40, 60, 90)) {
  pr <- c(wheat = profit(200, 120, 3), grass = profit(gp, 30, 10))
  cat(sprintf("grass $%d/t: profits %s -> shares %s\n", gp, paste(pr, collapse = "/"), paste(round(land_shares(pr), 3), collapse = "/")))
}
for (x in list(c(10, 10), c(100, 10), c(100, 5)))
  cat(sprintf("%3d EJ at %2d t/ha -> %6.1f million ha\n", x[1], x[2], x[1] * 1e9 / (x[2] * 18) / 1e6))
