"""Module 2.1 - Socioeconomic drivers: population, GDP and the Kaya identity.

Toy numbers only. Two invented storylines, 'Green road' and 'Rocky road', loosely
in the spirit of SSP1 and SSP3. Run:  python m21_drivers.py
"""
import numpy as np
import matplotlib.pyplot as plt

years = np.arange(2020, 2101, 5)
t = years - 2020

# 1. Population: grows, then levels off (logistic curve). Units: billion people.
def population(p0, pmax, rate):
    return pmax / (1 + (pmax / p0 - 1) * np.exp(-rate * t))

# 2. Income per person grows at a constant rate. Units: thousand $ per person.
def income(y0, growth):
    return y0 * (1 + growth) ** t

stories = {
    "Green road": dict(pop=population(7.8, 8.6, 0.05), inc=income(11, 0.022), ei=-0.025, ci=-0.030),
    "Rocky road": dict(pop=population(7.8, 12.5, 0.03), inc=income(11, 0.010), ei=-0.008, ci=-0.003),
}

fig, ax = plt.subplots(1, 3, figsize=(13, 4))
for name, s in stories.items():
    gdp = s["pop"] * s["inc"]                       # trillion $
    energy_per_gdp = 6.0 * (1 + s["ei"]) ** t       # MJ per $
    co2_per_energy = 0.065 * (1 + s["ci"]) ** t     # kg CO2 per MJ
    co2 = gdp * energy_per_gdp * co2_per_energy     # Gt CO2 (trillion$ x MJ/$ x kg/MJ = 1e12 kg = Gt)
    ax[0].plot(years, s["pop"], label=name)
    ax[1].plot(years, gdp, label=name)
    ax[2].plot(years, co2, label=name)
    # Kaya check: ratios multiply to the CO2 ratio
    r = [s["pop"][-1] / s["pop"][0], s["inc"][-1] / s["inc"][0],
         energy_per_gdp[-1] / energy_per_gdp[0], co2_per_energy[-1] / co2_per_energy[0]]
    print(f"{name}: factor ratios 2100/2020 = {np.round(r, 3)}, product = {np.prod(r):.3f}, "
          f"CO2 ratio = {co2[-1] / co2[0]:.3f}")

for a, title in zip(ax, ["Population (billion)", "GDP (trillion $)", "CO2 (Gt per year)"]):
    a.set_title(title); a.set_xlabel("Year"); a.legend()
plt.tight_layout(); plt.savefig("m21_drivers.png", dpi=120)
print("Saved m21_drivers.png")
