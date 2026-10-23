"""read_transport.py - pull the kit's transport queries from a GCAM output database (gcamreader),
or load the synthetic sample data, and save tidy CSVs for the other analysis scripts.

Usage
  python read_transport.py --sample                       # no GCAM needed (synthetic data)
  python read_transport.py --db /path/to/gcam/output --dbname database_basexdb
Needs for --db: pip install gcamreader (1.5.0, Python >= 3.11) and Java on the PATH.
API used (gcamreader README): LocalDBConn(dbpath, dbfile), parse_batch_query(file), conn.runQuery(q).
Filtering queries by q.title is an assumption about the Query object; if it fails, print dir(q).
The --db path has NOT been run against a real database; the --sample path is tested.
Output: analysis/out/{service_by_mode, energy_by_mode_fuel, co2_transport}.csv with columns
  scenario, region, [sector, mode, fuel], year, value, units
"""
import argparse, os
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
QFILE = os.path.join(HERE, "..", "queries", "transport_queries.xml")
WANT = {"service_by_mode": "transport service output by mode",
        "energy_by_mode_fuel": "transport final energy by mode and fuel",
        "co2_transport": "CO2 emissions by sector (excluding resource production)"}
SAMPLE = {"service_by_mode": "transport_service_output_by_mode.csv",
          "energy_by_mode_fuel": "transport_final_energy_by_mode_and_fuel.csv",
          "co2_transport": "CO2_emissions_by_sector.csv"}


def tidy(df):
    df = df.rename(columns={"Year": "year", "Units": "units", "input": "fuel"})
    if "sector" in df and "mode" not in df:   # CO2 query: keep transport sectors only
        df = df[df["sector"].str.startswith("trn_")]
    return df


def from_db(db, dbname):
    import gcamreader
    conn = gcamreader.LocalDBConn(db, dbname)
    queries = gcamreader.parse_batch_query(QFILE)
    out = {}
    for key, title in WANT.items():
        q = [x for x in queries if getattr(x, "title", None) == title]
        if not q:
            raise SystemExit(f"query '{title}' not found in {QFILE}")
        out[key] = tidy(conn.runQuery(q[0]))
    return out


def from_sample():
    return {k: tidy(pd.read_csv(os.path.join(HERE, "sample_data", f))) for k, f in SAMPLE.items()}


def main():
    ap = argparse.ArgumentParser()
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--sample", action="store_true")
    g.add_argument("--db")
    ap.add_argument("--dbname", default="database_basexdb")
    a = ap.parse_args()
    data = from_sample() if a.sample else from_db(a.db, a.dbname)
    os.makedirs(os.path.join(HERE, "out"), exist_ok=True)
    for k, df in data.items():
        p = os.path.join(HERE, "out", f"{k}.csv"); df.to_csv(p, index=False)
        print(f"{k:<22} {len(df):>5} rows, scenarios {sorted(df.scenario.unique())} -> {p}")


if __name__ == "__main__":
    main()
