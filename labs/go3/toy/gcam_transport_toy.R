# gcam_transport_toy.R -- R twin of gcam_transport_toy.py (same structure, same numbers).
#
# A stand-alone passenger-transport model that mimics GCAM 9.1's transport structure:
#   nests trn_pass -> road -> trn_pass_road -> LDV -> trn_pass_road_LDV -> 4W -> Car;
#   relative-cost logit among modes (trn_pass -2, trn_pass_road -4, trn_pass_road_LDV -4; A54.sector.csv),
#   absolute-cost logit among technologies (Car -8, 2W and 3W -8, Bus -3, Passenger Rail -1,
#   Domestic Aviation -6; A54.tranSubsector_logit_revised.csv);
#   cost per pkm = (non-fuel $/vkm + fuel price x intensity) / load factor (tran_technology.cpp);
#   time value = GDP per capita / 2000 h x time-value-multiplier / speed (tran_subsector.cpp 175-214);
#   demand elasticities income 1.0, price -1.25 (A54.demand.csv);
#   share-weights calibrated to the 2020 base year (calibrate_share_weight_visitor.cpp).
# See the header of gcam_transport_toy.py for sources, units and simplifications.
# Numbers are illustrative (2005$). Run: Rscript gcam_transport_toy.R

YEARS <- seq(2020, 2100, 5); BASE <- 2020

interp <- function(points, year) {           # points: named numeric vector, names = years
  ys <- as.numeric(names(points)); v <- unname(points); o <- order(ys); ys <- ys[o]; v <- v[o]
  if (year <= ys[1]) return(v[1]); if (year >= ys[length(ys)]) return(v[length(v)])
  approx(ys, v, xout = year)$y
}
pts <- function(...) { x <- c(...); x }      # pts(`2020` = 1, `2050` = 2)

EF <- c("refined liquids enduse" = 19.6 * 44 / 12 / 1000, "delivered gas" = 14.2 * 44 / 12 / 1000,
        "elect_td_trn" = 0, "H2 LDV" = 0, "H2 MHDV" = 0)

SCENARIOS <- list(
  "Reference"    = list(),
  "BEV-low"      = list(bev_cost_mult = 0.70),
  "Carbon-price" = list(carbon = TRUE),
  "Fast-wage"    = list(gdp_growth = 0.03),
  "LF-up"        = list(car_lf_2050 = 2.60))

opt <- function(sc, key, default) if (is.null(sc[[key]])) default else sc[[key]]

fuel_price <- function(fuel, year, sc) {
  base <- switch(fuel,
    "refined liquids enduse" = interp(pts(`2020` = 15, `2050` = 18), year),
    "delivered gas" = 8, "elect_td_trn" = 30,
    "H2 LDV" = interp(pts(`2020` = 45, `2050` = 30), year),
    "H2 MHDV" = interp(pts(`2020` = 40, `2050` = 28), year))
  if (isTRUE(sc$carbon) && year >= 2025) base <- base + EF[[fuel]] * 50 * 1.05^(year - 2025)
  base
}
gdp_pc <- function(year, sc) 18 * (1 + opt(sc, "gdp_growth", 0.02))^(year - BASE)
population <- function(year) 260 + 140 * (1 - exp(-0.025 * (year - BASE)))

tech <- function(fuel, nf, mj, lf, sw = NULL) list(fuel = fuel, nf = nf, mj = mj, lf = lf, sw = sw)
techs <- function(year, sc) {
  car_lf <- interp(c(`2020` = 2.33, `2050` = opt(sc, "car_lf_2050", 2.00)), year)
  bev_mult <- if (year >= 2030) opt(sc, "bev_cost_mult", 1.0) else 1.0
  list(
    "Car" = list(
      "Liquids" = tech("refined liquids enduse", interp(pts(`2020` = .6345, `2030` = .6747, `2050` = .7652), year),
                       interp(pts(`2020` = 3.322, `2030` = 3.101, `2050` = 2.718), year), car_lf),
      "Hybrid Liquids" = tech("refined liquids enduse", interp(pts(`2020` = .6629, `2030` = .7081, `2050` = .7872), year),
                       interp(pts(`2020` = 2.581, `2030` = 2.454, `2050` = 2.226), year), car_lf),
      "NG" = tech("delivered gas", interp(pts(`2020` = .6599, `2030` = .7017, `2050` = .7958), year),
                  interp(pts(`2020` = 3.355, `2030` = 3.132, `2050` = 2.745), year), car_lf),
      "BEV" = tech("elect_td_trn", bev_mult * interp(pts(`2020` = .7407, `2030` = .6894, `2050` = .7652), year),
                   interp(pts(`2020` = 1.026, `2030` = 1.019, `2050` = 1.005), year), car_lf,
                   pts(`2020` = 0, `2025` = 0, `2030` = 1)),
      "FCEV" = tech("H2 LDV", interp(pts(`2020` = .8050, `2030` = .7280, `2050` = .7799), year),
                    interp(pts(`2020` = 1.572, `2030` = 1.518, `2050` = 1.418), year), car_lf,
                    pts(`2020` = 0, `2030` = 0, `2050` = 0.5))),
    "Bus" = list(
      "Liquids" = tech("refined liquids enduse", 1.6319, interp(pts(`2020` = 7.908, `2050` = 7.884), year), 25),
      "NG" = tech("delivered gas", 1.7609, interp(pts(`2020` = 7.908, `2050` = 7.884), year), 25),
      "BEV" = tech("elect_td_trn", interp(pts(`2020` = 2.00, `2050` = 1.70), year), 3.0, 25,
                   pts(`2020` = 0, `2025` = 0, `2050` = 1))),
    "2W and 3W" = list(
      "Liquids" = tech("refined liquids enduse", 0.12, 1.0, 1.3),
      "BEV" = tech("elect_td_trn", interp(pts(`2020` = 0.14, `2050` = 0.11), year), 0.30, 1.3,
                   pts(`2020` = 0, `2025` = 0, `2030` = 1))),
    "Passenger Rail" = list("Electric" = tech("elect_td_trn", 16.005, 53.197, 1152)),
    "Domestic Aviation" = list("Liquids" = tech("refined liquids enduse", 13.77,
                               interp(pts(`2020` = 366.5, `2050` = 310.6), year),
                               interp(pts(`2020` = 148.8, `2050` = 161.6), year))))
}

TECH_EXP <- c("Car" = -8, "Bus" = -3, "2W and 3W" = -8, "Passenger Rail" = -1, "Domestic Aviation" = -6)
MODES <- list(
  "Walk" = list(vott = 1.066, add = 1, speed = function(y) 4.8),
  "Cycle" = list(vott = 1.066, add = 1, speed = function(y) 15),
  "Passenger Rail" = list(vott = 0.80, add = 1, speed = function(y) 42),
  "Domestic Aviation" = list(vott = 1.244, add = 1, speed = function(y) 197),
  "Bus" = list(vott = 0.808, add = 1, speed = function(y) interp(pts(`2020` = 22, `2050` = 24, `2100` = 25), y)),
  "2W and 3W" = list(vott = 0.82, add = 1, speed = function(y) 30),
  "4W" = list(vott = 0.82, add = 1, speed = function(y) interp(pts(`2020` = 35, `2050` = 40, `2100` = 42), y)))
NEST <- list(
  "trn_pass_road_LDV" = list(g = -4, kids = c("2W and 3W", "4W")),
  "trn_pass_road" = list(g = -4, kids = c("Bus", "LDV")),
  "trn_pass" = list(g = -2, kids = c("Walk", "Cycle", "Passenger Rail", "Domestic Aviation", "road")))
CHILD_SECTOR <- c("road" = "trn_pass_road", "LDV" = "trn_pass_road_LDV")
BASE_PKM <- list("Walk" = 70, "Cycle" = 25, "Passenger Rail" = 6, "Domestic Aviation" = 55,
                 "Bus" = c("Liquids" = 157, "NG" = 3), "2W and 3W" = c("Liquids" = 45),
                 "Car" = c("Liquids" = 1120, "Hybrid Liquids" = 20, "NG" = 10))

rel_shares <- function(prices, sws, g) { w <- ifelse(sws > 0, sws * prices^g, 0); w / sum(w) }
abs_shares <- function(costs, sws, beta, p0) { w <- ifelse(sws > 0, sws * exp(beta * costs / p0), 0); w / sum(w) }
base_out <- function(k) {
  if (k == "road") return(base_out("Bus") + base_out("LDV"))
  if (k == "LDV") return(base_out("2W and 3W") + base_out("4W"))
  if (k == "4W") return(sum(BASE_PKM[["Car"]]))
  sum(BASE_PKM[[k]])
}

run <- function(name, sc) {
  cal <- list(); rows <- list(); D_prev <- NA; P_prev <- NA
  add <- function(year, var, item, value, unit)
    rows[[length(rows) + 1]] <<- data.frame(scenario = name, year = year, variable = var, item = item, value = value, unit = unit)
  for (year in YEARS) {
    Tt <- techs(year, sc); wage <- gdp_pc(year, sc) * 1000 / (40 * 50)
    tech_share <- list(); mode_money <- c()
    for (mode in names(Tt)) {
      tt <- Tt[[mode]]
      costs <- sapply(tt, function(v) (v$nf + fuel_price(v$fuel, year, sc) * v$mj / 1000) / v$lf)
      if (year == BASE) {
        b <- BASE_PKM[[mode]]; if (is.null(names(b))) names(b) <- names(tt)[1]
        calk <- sapply(names(tt), function(k) if (k %in% names(b)) b[[k]] else 0)
        tot <- sum(calk); p0 <- max(costs[calk > 0]); anchor <- names(which.max(calk))
        sws <- sapply(names(tt), function(k) if (calk[[k]] > 0)
          (calk[[k]] / tot) / (calk[[anchor]] / tot) * exp(TECH_EXP[[mode]] / p0 * (costs[[anchor]] - costs[[k]])) else 0)
        cal[[mode]] <- list(p0 = p0, sw = sws)
      }
      sws <- sapply(names(tt), function(k) if (!is.null(tt[[k]]$sw) && cal[[mode]]$sw[[k]] == 0) interp(tt[[k]]$sw, year) else cal[[mode]]$sw[[k]])
      sh <- abs_shares(costs, sws, TECH_EXP[[mode]], cal[[mode]]$p0)
      tech_share[[mode]] <- sh; mode_money[mode] <- sum(sh * costs)
    }
    mode_money["Walk"] <- 0; mode_money["Cycle"] <- 0; mode_money["4W"] <- mode_money[["Car"]]
    mode_price <- function(m) { md <- MODES[[m]]; mode_money[[m]] + if (md$add == 1) wage * md$vott / md$speed(year) else 0 }
    sector_price <- c(); mode_sh <- list()
    for (sector in names(NEST)) {
      g <- NEST[[sector]]$g; kids <- NEST[[sector]]$kids
      prices <- sapply(kids, function(k) if (k %in% names(CHILD_SECTOR)) sector_price[[CHILD_SECTOR[[k]]]] else mode_price(k))
      if (year == BASE) {
        outs <- sapply(kids, base_out); anchor <- names(which.max(outs))
        cal[[sector]] <- (outs / outs[[anchor]]) * (prices[[anchor]] / prices)^g
      }
      sh <- rel_shares(prices, cal[[sector]], g); mode_sh[[sector]] <- sh
      sector_price[sector] <- sum(sh * prices)
    }
    P <- sector_price[["trn_pass"]]
    if (year == BASE) D <- sum(sapply(BASE_PKM, sum)) else
      D <- D_prev * (gdp_pc(year, sc) / gdp_pc(year - 5, sc))^1.0 * (P / P_prev)^-1.25 * population(year) / population(year - 5)
    D_prev <- D; P_prev <- P
    top <- mode_sh[["trn_pass"]]; road <- mode_sh[["trn_pass_road"]]; ldv <- mode_sh[["trn_pass_road_LDV"]]
    mode_pkm <- c("Walk" = D * top[["Walk"]], "Cycle" = D * top[["Cycle"]], "Passenger Rail" = D * top[["Passenger Rail"]],
                  "Domestic Aviation" = D * top[["Domestic Aviation"]], "Bus" = D * top[["road"]] * road[["Bus"]],
                  "2W and 3W" = D * top[["road"]] * road[["LDV"]] * ldv[["2W and 3W"]],
                  "Car" = D * top[["road"]] * road[["LDV"]] * ldv[["4W"]])
    energy <- c(); co2 <- 0
    for (m in names(mode_pkm)) {
      pk <- mode_pkm[[m]]
      add(year, "service output by mode", m, pk, "billion pkm"); add(year, "mode share", m, pk / D, "fraction")
      if (m %in% names(Tt)) for (k in names(tech_share[[m]])) {
        v <- Tt[[m]][[k]]; s <- tech_share[[m]][[k]]
        ej <- pk * s / v$lf * v$mj / 1000
        energy[v$fuel] <- (if (v$fuel %in% names(energy)) energy[[v$fuel]] else 0) + ej
        co2 <- co2 + ej * 1e3 * EF[[v$fuel]]
        add(year, "tech share", paste0(m, "|", k), s, "fraction")
      }
    }
    add(year, "service output", "trn_pass", D, "billion pkm"); add(year, "service price", "trn_pass", P, "2005$/pkm")
    for (f in sort(names(energy))) add(year, "final energy by fuel", f, energy[[f]], "EJ")
    add(year, "CO2 (direct)", "trn_pass", co2, "MtCO2")
  }
  do.call(rbind, rows)
}

args <- commandArgs(trailingOnly = FALSE)
here <- dirname(normalizePath(sub("--file=", "", args[grep("--file=", args)][1])))
res <- do.call(rbind, lapply(names(SCENARIOS), function(n) run(n, SCENARIOS[[n]])))
res$value <- signif(res$value, 6)
write.csv(res, file.path(here, "toy_results_R.csv"), row.names = FALSE)
g <- function(sn, y, v, i) { x <- res$value[res$scenario == sn & res$year == y & res$variable == v & res$item == i]; if (length(x)) x else 0 }
cat(sprintf("%-13s%5s%9s%7s%6s%6s%6s%8s%9s%7s%7s%8s\n", "scenario", "year", "pkm(bn)", "car%", "bus%", "rail%", "air%", "BEV%car", "FCEV%car", "liqEJ", "elecEJ", "CO2 Mt"))
for (sn in names(SCENARIOS)) for (y in c(2020, 2030, 2050, 2075, 2100))
  cat(sprintf("%-13s%5d%9.0f%7.1f%6.1f%6.1f%6.1f%8.1f%9.1f%7.2f%7.2f%8.0f\n", sn, y, g(sn, y, "service output", "trn_pass"),
      100 * g(sn, y, "mode share", "Car"), 100 * g(sn, y, "mode share", "Bus"), 100 * g(sn, y, "mode share", "Passenger Rail"),
      100 * g(sn, y, "mode share", "Domestic Aviation"), 100 * g(sn, y, "tech share", "Car|BEV"), 100 * g(sn, y, "tech share", "Car|FCEV"),
      g(sn, y, "final energy by fuel", "refined liquids enduse"), g(sn, y, "final energy by fuel", "elect_td_trn"), g(sn, y, "CO2 (direct)", "trn_pass")))
cat("\nWrote", file.path(here, "toy_results_R.csv"), "\n")
