# decompose_lmdi.R - LMDI-I additive decomposition of passenger-transport CO2 (same method and
# output as decompose_lmdi.py; see that file's header for the equations and references).
# Input: out/service_by_mode_R.csv and out/energy_by_mode_fuel_R.csv from read_transport.R.
# Run: Rscript decompose_lmdi.R
suppressMessages({library(dplyr); library(readr)})
here <- tryCatch(dirname(normalizePath(sub("--file=", "", grep("--file=", commandArgs(), value = TRUE)))), error = function(e) ".")
EF <- c("refined liquids enduse" = 19.6 * 44 / 12 / 1000, "delivered gas" = 14.2 * 44 / 12 / 1000)   # tCO2/GJ
EPS <- 1e-12
L <- function(a, b) { a <- max(a, EPS); b <- max(b, EPS); if (abs(a - b) < 1e-15) a else (a - b) / (log(a) - log(b)) }
svc <- read_csv(file.path(here, "out", "service_by_mode_R.csv"), show_col_types = FALSE)
en  <- read_csv(file.path(here, "out", "energy_by_mode_fuel_R.csv"), show_col_types = FALSE)

factors <- function(sc, yr) {
  s <- svc %>% filter(scenario == sc, year == yr) %>% group_by(mode) %>% summarise(pkm = sum(value), .groups = "drop")
  e <- en %>% filter(scenario == sc, year == yr) %>%
    mutate(co2 = value * 1e3 * ifelse(fuel %in% names(EF), EF[fuel], 0)) %>%
    group_by(mode) %>% summarise(ej = sum(value), co2 = sum(co2), .groups = "drop")
  A <- sum(s$pkm)
  inner_join(e, s, by = "mode") %>% mutate(A = A, S = pkm / A, I = ej / pkm, C = ifelse(ej > 0, co2 / ej, 0))
}
lmdi <- function(f0, f1) {
  m <- full_join(f0, f1, by = "mode", suffix = c("0", "1"))
  eff <- c(activity = 0, structure = 0, intensity = 0, carbon = 0)
  for (i in seq_len(nrow(m))) {
    r <- m[i, ]; c0 <- ifelse(is.na(r$co20), 0, r$co20); c1 <- ifelse(is.na(r$co21), 0, r$co21)
    if (c0 <= 0 && c1 <= 0) next
    w <- L(c1, c0)
    for (k in c(activity = "A", structure = "S", intensity = "I", carbon = "C")) {
      x0 <- r[[paste0(k, "0")]]; x1 <- r[[paste0(k, "1")]]
      eff[names(which(c(activity = "A", structure = "S", intensity = "I", carbon = "C") == k))] <-
        eff[names(which(c(activity = "A", structure = "S", intensity = "I", carbon = "C") == k))] + w * log(max(x1, EPS) / max(x0, EPS))
    }
  }
  t0 <- sum(f0$co2); t1 <- sum(f1$co2)
  c(eff, co2_start = t0, co2_end = t1, change = t1 - t0, residual = t1 - t0 - sum(eff))
}
scens <- sort(unique(svc$scenario)); res <- list()
for (sc in scens) res[[paste0(sc, ": 2020 -> 2050")]] <- lmdi(factors(sc, 2020), factors(sc, 2050))
for (sc in setdiff(scens, "Reference")) res[[paste0("2050: Reference -> ", sc)]] <- lmdi(factors("Reference", 2050), factors(sc, 2050))
out <- bind_cols(comparison = names(res), as_tibble(do.call(rbind, res)))
print(as.data.frame(mutate(out, across(where(is.numeric), ~ round(.x, 2)))), row.names = FALSE)
cat(sprintf("\nlargest |residual| = %.2e Mt\n", max(abs(out$residual))))
write_csv(out, file.path(here, "out", "lmdi_results_R.csv"))
