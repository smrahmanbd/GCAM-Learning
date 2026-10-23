# Go 2 - pull the handbook's GCAM results into R with rgcam.
# NOT RUN AGAINST A LIVE GCAM DATABASE. Written to the rgcam API as documented
# (localDBConn, addScenario, listQueries, getQuery). Same pattern as labs 7 to 10.
# Install: remotes::install_github('JGCRI/rgcam')
library(rgcam)

db_dir  <- "/course/gcam/output"          # folder holding database_basexdb (from your instructor)
conn    <- localDBConn(db_dir, "database_basexdb")
print(listScenariosInDB(conn))

prj <- addScenario(conn, "go2_project.dat", "Reference", "go2_queries.xml")
# Add a policy run to the same project file to compare, e.g.:
# prj <- addScenario(conn, prj, "CarbonPrice", "go2_queries.xml")
print(listQueries(prj))

titles <- c("CO2 emissions by region", "elec gen by subsector",
            "primary energy consumption by region (direct equivalent)",
            "global mean temperature", "CO2 prices", "aggregated land allocation",
            "water withdrawals by region", "water withdrawals by basin")
for (q in titles) {
  df <- getQuery(prj, q)
  write.csv(df, paste0(gsub("[ ()]", "_", q), ".csv"), row.names = FALSE)
  cat(sprintf("%-58s %6d rows\n", q, nrow(df)))
}
