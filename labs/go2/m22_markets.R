# Module 2.2 - Markets, equilibrium and solving (toy numbers)
# Part A: one market (lab 4). Part B: three linked markets solved together.
excess <- function(p, tax) (1000 - 4 * p) - 6 * (p - 0.9 * tax)
for (tax in c(0, 50)) {
  p <- uniroot(excess, c(0, 500), tax = tax)$root
  cat(sprintf("One market, tax %2d: price %6.1f, quantity %6.1f\n", tax, p, 1000 - 4 * p))
}

excess3 <- function(p, carbon = 0) {
  oil <- p[1]; elec <- p[2]; bio <- p[3]; oc <- oil + 0.07 * carbon
  d <- c(100 * (oc / 10)^-0.6 * (elec / 30)^0.3, 80 * (elec / 30)^-0.5 * (oc / 10)^0.3, 20 * (bio / 5)^-0.8 * (oc / 10)^0.5)
  s <- c(100 * (oil / 10)^1.2, 80 * (elec / 30) * (bio / 5)^-0.2, 20 * (bio / 5)^1.5)
  d - s
}
# A tiny Newton solver in log-prices (GCAM uses Broyden's method, a cheaper cousin of Newton).
solve_markets <- function(carbon, p = c(8, 25, 6), iters = 50) {
  x <- log(p)
  f <- function(x) excess3(exp(x), carbon) / c(100, 80, 20)
  for (i in 1:iters) {
    fx <- f(x)
    if (max(abs(fx)) < 1e-10) break
    J <- sapply(1:3, function(j) { h <- 1e-6; xh <- x; xh[j] <- xh[j] + h; (f(xh) - fx) / h })
    x <- x - solve(J, fx)
  }
  list(price = exp(x), iterations = i, max_excess = max(abs(excess3(exp(x), carbon))))
}
for (cp in c(0, 50)) {
  s <- solve_markets(cp)
  cat(sprintf("Three markets, carbon %2d: oil %.2f, electricity %.2f, biomass %.2f (%d iterations, max excess %.1e)\n",
              cp, s$price[1], s$price[2], s$price[3], s$iterations, s$max_excess))
}
