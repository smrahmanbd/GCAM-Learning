# Module 2.8 (A) - Emissions to warming: impulse-response carbon cycle + two-layer energy balance.
# Rounded textbook parameters (Joos et al. 2013 impulse response); this is not Hector.
a <- c(0.2173, 0.2240, 0.2824, 0.2763); tau <- c(Inf, 394.4, 36.54, 4.304)
climate <- function(emis, c0 = 410, T0 = 1.1, Td0 = 0.3, lam = 1.3, Cu = 8, Cd = 100, g = 0.7) {
  boxes <- rep(0, 4); out <- data.frame(); T <- T0; Td <- Td0
  decay <- ifelse(is.infinite(tau), 1, exp(-1 / tau))
  for (e in emis) {
    boxes <- boxes * decay + a * e / 7.8
    C <- c0 + sum(boxes); F <- 5.35 * log(C / 278)
    Tn <- T + (F - lam * T - g * (T - Td)) / Cu; Td <- Td + g * (T - Td) / Cd; T <- Tn
    out <- rbind(out, data.frame(C = C, T = T))
  }
  out
}
yrs <- 2021:2100
paths <- list("Flat at 40 Gt" = rep(40, length(yrs)), "Net zero 2050" = pmax(40 * (1 - (yrs - 2020) / 30), 0))
for (nm in names(paths)) {
  r <- climate(paths[[nm]]); cum <- sum(paths[[nm]])
  cat(sprintf("%-14s cumulative %5.0f Gt -> %4.0f ppm, warming 2100 %.2f C (TCRE: +%.2f C)\n", nm, cum, tail(r$C, 1), tail(r$T, 1), 0.45 * cum / 1000))
}
