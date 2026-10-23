"""scale_from_base.py - write a GCAM transport add-on XML by scaling values in YOUR base file.

Why: GCAM input values (costs, load factors, intensities) differ by region, version and unit
convention (v8.5+ uses 1975$/vkm and EJ per billion vkm). Copying numbers from papers or other
versions is the commonest error. This script reads the transportation XML that gcamdata built
for you and multiplies the chosen values, so units are always consistent.

Fields (element names from gcam-v9.1 ModelInterface_headers.txt):
  input-cost   StubTranTechCost       period/minicam-non-energy-input[name=non-energy]/input-cost
  loadFactor   StubTranTechLoadFactor period/loadFactor
  coefficient  StubTranTechCoef       period/minicam-energy-input[name=INPUT]/coefficient (+market-name)

Examples (Python 3, no extra packages):
  python scale_from_base.py --base transportation_UCD_CORE.xml --region "Middle East" \
      --sector trn_pass_road_LDV_4W --subsector Car --tech BEV --field input-cost \
      --factor 0.70 --from-year 2030 --out trn_bev_cost_low.xml
  python scale_from_base.py --base transportation_UCD_CORE.xml --region "Middle East" \
      --sector trn_pass_road_LDV_4W --subsector Car --tech ALL --field loadFactor \
      --ramp 2025:1.0,2050:1.2 --out trn_loadfactor_up.xml
  python scale_from_base.py --base transportation_UCD_CORE.xml --region "Middle East" \
      --sector trn_freight_road --subsector "Heavy truck" --tech Liquids --field coefficient \
      --input "refined liquids enduse" --ramp 2025:1.0,2050:0.75 --out trn_freight_truck_efficiency.xml
Tested on: tests/base_transport_sample.xml (a synthetic file with the same structure). Not tested
on a real gcamdata output file - check the printed table against your base file.
"""
import argparse
import sys
import xml.etree.ElementTree as ET


def ramp_factor(ramp, year):
    pts = sorted((int(a), float(b)) for a, b in (p.split(":") for p in ramp.split(",")))
    if year <= pts[0][0]:
        return pts[0][1]
    if year >= pts[-1][0]:
        return pts[-1][1]
    for (y0, f0), (y1, f1) in zip(pts, pts[1:]):
        if y0 <= year <= y1:
            return f0 + (f1 - f0) * (year - y0) / (y1 - y0)


def find_value(period, field, input_name):
    if field == "loadFactor":
        return period.find("loadFactor"), None
    if field == "input-cost":
        for n in period.findall("minicam-non-energy-input"):
            if n.get("name") == "non-energy":
                return n.find("input-cost"), None
        return None, None
    for n in period.findall("minicam-energy-input"):
        if n.get("name") == input_name:
            return n.find("coefficient"), n.find("market-name")
    return None, None


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--base", required=True)
    ap.add_argument("--region", required=True)
    ap.add_argument("--sector", required=True)
    ap.add_argument("--subsector", required=True)
    ap.add_argument("--tech", required=True, help="technology name, or ALL")
    ap.add_argument("--field", required=True, choices=["input-cost", "loadFactor", "coefficient"])
    ap.add_argument("--input", default=None, help="energy input name (field coefficient)")
    ap.add_argument("--factor", type=float, default=None, help="constant multiplier")
    ap.add_argument("--ramp", default=None, help="year:multiplier pairs, linear between, flat outside")
    ap.add_argument("--from-year", type=int, default=2025, help="first model year to change")
    ap.add_argument("--out", required=True)
    a = ap.parse_args(argv)
    if (a.factor is None) == (a.ramp is None):
        ap.error("give exactly one of --factor or --ramp")
    if a.field == "coefficient" and not a.input:
        ap.error("--input is required for --field coefficient")

    root = ET.parse(a.base).getroot()
    out_root = ET.Element("scenario"); w = ET.SubElement(out_root, "world")
    r_out = ET.SubElement(w, "region", name=a.region)
    s_out = ET.SubElement(r_out, "supplysector", name=a.sector)
    ss_out = ET.SubElement(s_out, "tranSubsector", name=a.subsector)
    rows = 0
    print(f"{'technology':<16}{'year':>6}{'base':>12}{'x':>7}{'new':>12}")
    for reg in root.iter("region"):
        if reg.get("name") != a.region:
            continue
        for sec in reg.findall("supplysector"):
            if sec.get("name") != a.sector:
                continue
            for sub in sec.findall("tranSubsector"):
                if sub.get("name") != a.subsector:
                    continue
                for tech in sub.findall("stub-technology"):
                    if a.tech != "ALL" and tech.get("name") != a.tech:
                        continue
                    t_out = None
                    for per in tech.findall("period"):
                        y = int(per.get("year"))
                        if y < a.from_year:
                            continue
                        el, mkt = find_value(per, a.field, a.input)
                        if el is None or el.text is None:
                            continue
                        f = a.factor if a.factor is not None else ramp_factor(a.ramp, y)
                        base = float(el.text); new = base * f
                        if t_out is None:
                            t_out = ET.SubElement(ss_out, "stub-technology", name=tech.get("name"))
                        p = ET.SubElement(t_out, "period", year=str(y))
                        if a.field == "loadFactor":
                            ET.SubElement(p, "loadFactor").text = f"{new:.6g}"
                        elif a.field == "input-cost":
                            n = ET.SubElement(p, "minicam-non-energy-input", name="non-energy")
                            ET.SubElement(n, "input-cost").text = f"{new:.6g}"
                        else:
                            n = ET.SubElement(p, "minicam-energy-input", name=a.input)
                            ET.SubElement(n, "coefficient").text = f"{new:.6g}"
                            ET.SubElement(n, "market-name").text = mkt.text if mkt is not None else a.region
                        rows += 1
                        print(f"{tech.get('name'):<16}{y:>6}{base:>12.6g}{f:>7.3f}{new:>12.6g}")
    if rows == 0:
        sys.exit("No matching values found: check region/sector/subsector/tech/field names against the base file.")
    ET.indent(out_root)
    header = (f"<!-- Generated by scale_from_base.py from {a.base}: field {a.field}, "
              f"{'factor ' + str(a.factor) if a.factor is not None else 'ramp ' + a.ramp}, from {a.from_year}. "
              f"Load AFTER the transportation file in ScenarioComponents. -->\n")
    with open(a.out, "w", encoding="utf-8") as fh:
        fh.write('<?xml version="1.0" encoding="UTF-8"?>\n' + header + ET.tostring(out_root, encoding="unicode") + "\n")
    print(f"wrote {rows} values to {a.out}")


if __name__ == "__main__":
    main()
