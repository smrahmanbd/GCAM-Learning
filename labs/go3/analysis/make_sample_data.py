"""make_sample_data.py - build SYNTHETIC sample data so every analysis script runs without GCAM.

Everything here comes from the kit's toy model (toy/gcam_transport_toy.py), reshaped to look like
GCAM query output read with gcamreader (columns: Units, scenario, region, <axes>, Year, value).
Region is labelled "Middle East (toy)". These are NOT GCAM results.

Writes analysis/sample_data/:
  transport_service_output_by_mode.csv       (query "transport service output by mode")
  transport_final_energy_by_mode_and_fuel.csv (query "transport final energy by mode and fuel")
  CO2_emissions_by_sector.csv                  (query "CO2 emissions by sector ...", transport rows)
  ensemble.csv                                 (300 toy runs for scenario discovery)
Run: python analysis/make_sample_data.py
"""
import csv, os, random, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "toy"))
import gcam_transport_toy as toy  # noqa: E402

OUT = os.path.join(HERE, "sample_data")
os.makedirs(OUT, exist_ok=True)
REGION = "Middle East (toy)"
SECTOR = {"Walk": "trn_pass", "Cycle": "trn_pass", "Passenger Rail": "trn_pass", "Domestic Aviation": "trn_pass",
          "Bus": "trn_pass_road", "2W and 3W": "trn_pass_road_LDV", "Car": "trn_pass_road_LDV_4W"}


def detail(name, sc):
    """Re-run the toy and rebuild energy by mode and fuel from its rows and technology table."""
    rows = toy.run(name, sc)
    get = {(r[1], r[2], r[3]): r[4] for r in rows}
    svc, en = [], []
    for y in toy.YEARS:
        T = toy.techs(y, sc)
        for m in SECTOR:
            pk = get[(y, "service output by mode", m)]
            svc.append(["billion pass-km", name, REGION, SECTOR[m], m, y, round(pk, 6)])
            if m in T:
                byfuel = {}
                for k, v in T[m].items():
                    s = get.get((y, "tech share", f"{m}|{k}"), 0.0)
                    byfuel[v["fuel"]] = byfuel.get(v["fuel"], 0.0) + pk * s / v["lf"] * v["mj"] / 1000
                for f, e in byfuel.items():
                    en.append(["EJ", name, REGION, SECTOR[m], m, f, y, round(e, 8)])
    return rows, svc, en


svc_all, en_all, co2_all = [], [], []
for name, sc in toy.SCENARIOS.items():
    rows, svc, en = detail(name, sc)
    svc_all += svc; en_all += en
    for y in toy.YEARS:
        # direct CO2 = EJ x 1e3 (PJ = million GJ) x tCO2/GJ = MtCO2; GCAM reports MTC (divide by 44/12)
        mtco2 = sum(r[7] * 1e3 * toy.EF[r[5]] for r in en if r[6] == y)
        co2_all.append(["MTC", name, REGION, "trn_pass", y, round(mtco2 / (44 / 12), 6)])


def write(fname, header, rows):
    with open(os.path.join(OUT, fname), "w", newline="") as fh:
        w = csv.writer(fh); w.writerow(header); w.writerows(rows)
    print(f"wrote {fname}: {len(rows)} rows")


write("transport_service_output_by_mode.csv", ["Units", "scenario", "region", "sector", "mode", "Year", "value"], svc_all)
write("transport_final_energy_by_mode_and_fuel.csv", ["Units", "scenario", "region", "sector", "mode", "input", "Year", "value"], en_all)
write("CO2_emissions_by_sector.csv", ["Units", "scenario", "region", "sector", "Year", "value"], co2_all)

# ---- ensemble for scenario discovery: 300 toy runs, uniform sampling (seeded) ----
random.seed(2026)
ens = []
for i in range(300):
    x = dict(bev_cost_mult=random.uniform(0.5, 1.1), car_lf_2050=random.uniform(1.6, 2.6),
             gdp_growth=random.uniform(0.01, 0.035), carbon_start=random.uniform(0, 150))
    sc = dict(x, carbon=x["carbon_start"] > 0)
    rows = toy.run(f"run{i:03d}", sc)
    get = {(r[1], r[2], r[3]): r[4] for r in rows}
    ens.append([f"run{i:03d}", round(x["bev_cost_mult"], 4), round(x["car_lf_2050"], 4), round(x["gdp_growth"], 5),
                round(x["carbon_start"], 2), round(get[(2050, "CO2 (direct)", "trn_pass")], 3),
                round(get[(2050, "tech share", "Car|BEV")], 4)])
write("ensemble.csv", ["run", "bev_cost_mult", "car_lf_2050", "gdp_growth", "carbon_start_usd_tco2",
                       "co2_2050_mtco2", "bev_share_car_2050"], ens)
