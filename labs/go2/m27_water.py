"""Module 2.7 - Water: a basin supply curve and water for power cooling.

Supply comes first from cheap renewable water, then groundwater, then desalination,
so the water price climbs as withdrawals grow (GCAM v8.2 docs, 'Water Supply'). Toy numbers.
Run:  python m27_water.py
"""
renewable_cap, ground_cap = 50.0, 30.0           # km3 per year available in each tier
cost = {"renewable": 0.01, "groundwater": 0.05, "desalination": 0.8}   # $ per m3

def water_price(withdrawal):
    if withdrawal <= renewable_cap: return cost["renewable"]
    if withdrawal <= renewable_cap + ground_cap: return cost["groundwater"]
    return cost["desalination"]

def withdrawals(irrigation, municipal, power_twh, litres_per_kwh=2.0):
    power = power_twh * 1e9 * litres_per_kwh / 1e12      # km3 (1 km3 = 1e12 litres)
    return irrigation + municipal + power

for twh, lpk in ((100, 2.0), (300, 2.0), (300, 60.0)):   # dry cooling vs once-through cooling
    w = withdrawals(40, 8, twh, lpk)
    print(f"{twh} TWh at {lpk:>4} L/kWh: withdrawals {w:6.1f} km3 -> water price ${water_price(w)}/m3")
