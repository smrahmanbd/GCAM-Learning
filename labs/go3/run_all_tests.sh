#!/usr/bin/env bash
# run_all_tests.sh - re-run every script in the kit that can run without GCAM, in order.
# Needs: Python 3 with numpy, pandas, matplotlib, scikit-learn; R with dplyr, readr, rpart.
set -e
cd "$(dirname "$0")"
echo "== toy model (Python, then R) and agreement check"
python3 toy/gcam_transport_toy.py > /dev/null
Rscript toy/gcam_transport_toy.R > /dev/null
python3 - <<'PY'
import pandas as pd
a = pd.read_csv("toy/toy_results.csv"); b = pd.read_csv("toy/toy_results_R.csv")
n = a.select_dtypes("number").columns
d = float((a[n] - b[n]).abs().max().max()); print(f"Python vs R toy results: max difference {d}")
assert d < 1e-6
PY
echo "== synthetic sample data"; python3 analysis/make_sample_data.py
echo "== read (sample mode)"; python3 analysis/read_transport.py --sample; Rscript analysis/read_transport.R sample
echo "== LMDI"; python3 analysis/decompose_lmdi.py | tail -2; Rscript analysis/decompose_lmdi.R | tail -1
echo "== figures"; python3 analysis/plot_transport.py
echo "== scenario discovery"; python3 analysis/scenario_discovery.py | tail -4; Rscript analysis/scenario_discovery.R | tail -1
echo "== downscaling"; python3 downscale/downscale_demo.py > downscale/downscale_log.txt; head -1 downscale/downscale_log.txt
echo "== XML well-formedness and scale_from_base test"
python3 - <<'PY'
import glob, xml.dom.minidom
for f in sorted(glob.glob("xml/*.xml") + glob.glob("config/*.xml") + glob.glob("queries/*.xml")):
    xml.dom.minidom.parse(f)
print("all XML files well-formed")
PY
python3 xml/scale_from_base.py --base xml/tests/base_transport_sample.xml --region "Middle East" \
  --sector trn_pass_road_LDV_4W --subsector Car --tech BEV --field input-cost --factor 0.7 \
  --from-year 2030 --out xml/tests/out_cost.xml | tail -1
echo "ALL TESTS PASSED"
