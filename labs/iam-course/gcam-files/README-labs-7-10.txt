gcam-files: small non-R files for the GCAM labs (labs 7 to 10)
================================================================

Every file here was written from the GCAM documentation and from the
gcam-core repository at tag gcam-v9.1 (checked October 2026). None of them
has been run. Check each one against the GCAM release installed for the
course before the lab that uses it.

course_queries.xml                    labs 7-10  query file read by rgcam
lab8_cheapsolar_config_snippet.xml    lab 8      two edits for the CheapSolar run
carbon_price_global.xml               lab 10     add-on file: one global CO2 price
lab10_carbonprice_config_snippet.xml  lab 10     two edits for the CarbonPrice run
lab10_netzero_config_snippet.xml      lab 10     instructor only: the NetZero run

Paths the lab scripts assume (change them at the top of each script):
  ~/gcam          your own GCAM workspace: exe, input, output
  ~/gcamdata      your own copy of input/gcamdata with its drake cache built
  db_dir          folder with the instructor's database_basexdb
