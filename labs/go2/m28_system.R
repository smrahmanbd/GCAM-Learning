# Module 2.8 (B) - A tiny one-region power-and-land toy IAM (illustrative only)
years <- seq(2025, 2100, 5)
cost0 <- c(coal = 60, gas = 70, solar = 80, bio_ccs = 110); ef <- c(0.9, 0.4, 0, -0.8); decline <- c(0, 0, 0.015, 0.005)
bio_land <- function(gen) gen * 3.6 / 0.35 / 180          # Mha
step <- function(t, cp, demand) {
  mix <- function(adder) { c <- cost0 * (1 - decline)^t + ef * cp; c[4] <- c[4] + adder; x <- pmax(c, 5)^-6; x / sum(x) }
  a <- uniroot(function(a) a - 0.08 * bio_land(demand * mix(a)[4]), c(0, 1e4))$root   # land market
  mix(a)
}
run <- function(prices) {
  cum <- 0; out <- data.frame()
  for (i in seq_along(years)) {
    t <- years[i] - 2025; demand <- 30000 * 1.02^t; s <- step(t, prices[i], demand); gen <- demand * s
    co2 <- sum(gen * ef) / 1000; cum <- cum + 5 * co2
    out <- rbind(out, data.frame(year = years[i], co2 = co2, solar = s[3], bio_land = bio_land(gen[4]), dT = 0.45 * cum / 1000))
  }
  out
}
ref <- run(rep(0, length(years))); tax <- run(25 * 1.05^(years - 2025))
i50 <- which(years == 2050); target <- 0.5 * ref$co2[1]
p0 <- uniroot(function(p) run(p * 1.05^(years - 2025))$co2[i50] - target, c(0.01, 5000))$root
cap <- run(p0 * 1.05^(years - 2025))
for (nm in c("Reference", "Carbon price", "Cap")) {
  r <- list(Reference = ref, "Carbon price" = tax, Cap = cap)[[nm]]
  cat(sprintf("%-13s 2050 CO2 %6.2f Gt, solar %.2f, bio land %6.1f Mha | warming added by 2100 %.2f C\n", nm, r$co2[i50], r$solar[i50], r$bio_land[i50], tail(r$dT, 1)))
}
cat(sprintf("Cap met by a price starting at %.1f $/t in 2025, growing 5%%/yr\n", p0))
