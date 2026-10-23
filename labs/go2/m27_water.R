# Module 2.7 - Water: basin supply tiers and water for power cooling (toy numbers)
water_price <- function(w, renewable = 50, ground = 30)
  if (w <= renewable) 0.01 else if (w <= renewable + ground) 0.05 else 0.8      # $ per m3
withdrawals <- function(irrigation, municipal, power_twh, l_per_kwh = 2) irrigation + municipal + power_twh * 1e9 * l_per_kwh / 1e12
for (x in list(c(100, 2), c(300, 2), c(300, 60))) {
  w <- withdrawals(40, 8, x[1], x[2])
  cat(sprintf("%d TWh at %g L/kWh: %.1f km3 -> $%g per m3\n", x[1], x[2], w, water_price(w)))
}
