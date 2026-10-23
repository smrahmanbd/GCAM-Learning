"""Module 2.8 (part A) - From emissions to warming with a tiny climate model.

GCAM passes its emissions to Hector, a simple climate model (GCAM v8.2 docs, 'Climate').
This toy does the same chain with two textbook pieces:
  carbon cycle: an impulse response (Joos et al. 2013, used in IPCC AR5) turns CO2 emissions into ppm;
  energy balance: forcing F = 5.35 ln(C/C0) W/m2 drives a two-layer ocean model.
Parameters are rounded textbook values; this is not Hector. Run:  python m28a_climate.py
"""
import numpy as np

a = np.array([0.2173, 0.2240, 0.2824, 0.2763]); tau = np.array([np.inf, 394.4, 36.54, 4.304])
GT_PER_PPM = 7.8                                   # Gt CO2 per ppm of atmospheric CO2
lam, C_up, C_deep, gamma = 1.3, 8.0, 100.0, 0.7     # W/m2/K, W yr/m2/K, W yr/m2/K, W/m2/K

def climate(emis, c_start=410.0, T0=1.1, Td0=0.3):
    boxes, conc, temp, T, Td = np.zeros(4), [], [], T0, Td0
    for e in emis:                                 # one value per year, Gt CO2
        decay = np.where(np.isinf(tau), 1.0, np.exp(-1 / tau))
        boxes = boxes * decay + a * e / GT_PER_PPM
        C = c_start + boxes.sum()
        F = 5.35 * np.log(C / 278.0)
        T, Td = T + (F - lam * T - gamma * (T - Td)) / C_up, Td + gamma * (T - Td) / C_deep
        conc.append(C); temp.append(T)
    return np.array(conc), np.array(temp)

yrs = np.arange(2021, 2101)
paths = {"Flat at 40 Gt": np.full(len(yrs), 40.0),
         "Net zero 2050": np.clip(40 * (1 - (yrs - 2020) / 30), 0, None)}
for name, e in paths.items():
    C, T = climate(e)
    cum = e.sum()
    print(f"{name:<14} cumulative {cum:6.0f} Gt -> CO2 {C[-1]:5.0f} ppm, warming 2100 {T[-1]:.2f} C "
          f"(TCRE rule of thumb: +{0.45 * cum / 1000:.2f} C)")
