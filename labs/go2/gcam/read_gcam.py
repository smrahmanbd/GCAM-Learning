"""Go 2 - pull the handbook's GCAM results into pandas with gcamreader.

NOT RUN AGAINST A LIVE GCAM DATABASE. Written to the gcamreader API as documented
(gcamreader 1.5.0, Python >= 3.11, needs Java): LocalDBConn, parse_batch_query, runQuery.
Install:  pip install gcamreader
Usage:    python read_gcam.py /path/to/gcam/output database_basexdb
"""
import sys
import gcamreader

db_dir = sys.argv[1] if len(sys.argv) > 1 else "../gcam/output"     # folder that holds the database
db_name = sys.argv[2] if len(sys.argv) > 2 else "database_basexdb"

conn = gcamreader.LocalDBConn(db_dir, db_name)
queries = gcamreader.parse_batch_query("go2_queries.xml")             # the 8 course queries
print("queries in file:", [q.title for q in queries])

wanted = {  # handbook module -> query title
    "2.1 / 2.8": "CO2 emissions by region",
    "2.4": "elec gen by subsector",
    "2.4 / 2.5": "primary energy consumption by region (direct equivalent)",
    "2.8": "global mean temperature",
    "2.8 ": "CO2 prices",
    "2.6": "aggregated land allocation",
    "2.7": "water withdrawals by region",
    "2.7 ": "water withdrawals by basin",
}
for module, title in wanted.items():
    q = next((q for q in queries if q.title == title), None)
    if q is None:
        print("missing query:", title); continue
    df = conn.runQuery(q)                     # optional: scenarios=["Reference", "CarbonPrice"]
    out = title.replace(" ", "_").replace("(", "").replace(")", "") + ".csv"
    df.to_csv(out, index=False)
    print(f"module {module.strip():<9} {title:<58} -> {out} ({len(df)} rows)")
