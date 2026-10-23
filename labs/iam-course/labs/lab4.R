# Lab 4 (week 4): a toy energy market
# No data file. All numbers are illustrative.
# base = cost in $/MWh, ef = tonnes of CO2 per MWh, tax = $ per tonne of CO2

# ---- Part A: a cost function and a loop over carbon taxes ----
cost <- function(base, ef, tax) {
  if (tax < 0) stop("tax is negative")
  base + ef * tax
}
cost(60, 0.9, 50)   # coal at a tax of 50: expect 105

for (tax in c(0, 22, 30, 50)) {
  costs <- c(coal  = cost(60, 0.9, tax),
             gas   = cost(70, 0.4, tax),
             solar = cost(80, 0, tax))
  print(names(which.min(costs)))   # expect coal, gas, solar, solar
}

# ---- Part B: the market price with and without the tax ----
demand <- function(p) 1000 - 4 * p
supply <- function(p, tax) {
  6 * (p - 0.9 * tax)
}
gap <- function(p, tax) {
  demand(p) - supply(p, tax)
}

p0 <- uniroot(gap, c(0, 500), tax = 0)$root    # expect about 100
p50 <- uniroot(gap, c(0, 500), tax = 50)$root  # expect about 127
demand(c(p0, p50))                             # expect about 600 and 492
