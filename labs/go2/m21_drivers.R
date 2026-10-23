# Module 2.1 - Socioeconomic drivers: population, GDP and the Kaya identity (toy numbers)
years <- seq(2020, 2100, by = 5); t <- years - 2020
population <- function(p0, pmax, rate) pmax / (1 + (pmax / p0 - 1) * exp(-rate * t))   # billion
income <- function(y0, growth) y0 * (1 + growth)^t                                     # thousand $ per person

stories <- list(
  "Green road" = list(pop = population(7.8, 8.6, 0.05), inc = income(11, 0.022), ei = -0.025, ci = -0.030),
  "Rocky road" = list(pop = population(7.8, 12.5, 0.03), inc = income(11, 0.010), ei = -0.008, ci = -0.003))

par(mfrow = c(1, 3))
res <- list()
for (nm in names(stories)) {
  s <- stories[[nm]]
  gdp <- s$pop * s$inc                       # trillion $
  e_gdp <- 6.0 * (1 + s$ei)^t                # MJ per $
  c_e <- 0.065 * (1 + s$ci)^t                # kg CO2 per MJ
  co2 <- gdp * e_gdp * c_e                   # Gt CO2
  r <- c(pop = s$pop[17] / s$pop[1], income = s$inc[17] / s$inc[1], e_gdp = e_gdp[17] / e_gdp[1], c_e = c_e[17] / c_e[1])
  cat(nm, ": ratios 2100/2020 =", round(r, 3), " product =", round(prod(r), 3), " CO2 ratio =", round(co2[17] / co2[1], 3), "\n")
  res[[nm]] <- data.frame(year = years, pop = s$pop, gdp = gdp, co2 = co2)
}
for (v in c("pop", "gdp", "co2")) {
  plot(years, res[[1]][[v]], type = "l", lwd = 2, ylim = range(sapply(res, `[[`, v)), xlab = "Year", ylab = v, main = v)
  lines(years, res[[2]][[v]], lwd = 2, lty = 2)
  legend("topleft", names(res), lty = 1:2, bty = "n")
}
