# read_transport.R - pull the kit's transport queries with rgcam, or load the synthetic sample data,
# and save tidy CSVs (same output as read_transport.py).
#
# Usage:  Rscript read_transport.R sample
#         Rscript read_transport.R db /path/to/gcam/output database_basexdb
# Needs for db: rgcam (remotes::install_github("JGCRI/rgcam")) and Java.
# rgcam API (rgcam vignette): localDBConn(dbPath, dbFile); addScenario(conn, proj, scenario, queryFile);
#   getQuery(proj, title). rgcam names the year column "year". The db path has NOT been run against
#   a real database; the sample path is tested.
suppressMessages({library(dplyr); library(readr)})
args <- commandArgs(trailingOnly = TRUE); mode <- if (length(args)) args[1] else "sample"
here <- tryCatch(dirname(normalizePath(sub("--file=", "", grep("--file=", commandArgs(), value = TRUE)))), error = function(e) ".")
qfile <- file.path(here, "..", "queries", "transport_queries.xml")
want <- c(service_by_mode = "transport service output by mode",
          energy_by_mode_fuel = "transport final energy by mode and fuel",
          co2_transport = "CO2 emissions by sector (excluding resource production)")
sample_files <- c(service_by_mode = "transport_service_output_by_mode.csv",
                  energy_by_mode_fuel = "transport_final_energy_by_mode_and_fuel.csv",
                  co2_transport = "CO2_emissions_by_sector.csv")
tidy <- function(df) {
  df <- rename_with(df, ~ c(Year = "year", Units = "units", input = "fuel")[.x] %||% .x)
  if ("sector" %in% names(df) && !"mode" %in% names(df)) df <- filter(df, startsWith(sector, "trn_"))
  df
}
`%||%` <- function(a, b) ifelse(is.na(a), b, a)
if (mode == "sample") {
  data <- lapply(sample_files, function(f) tidy(read_csv(file.path(here, "sample_data", f), show_col_types = FALSE)))
} else {
  library(rgcam)
  conn <- localDBConn(args[2], ifelse(length(args) >= 3, args[3], "database_basexdb"))
  prj_file <- file.path(here, "out", "transport.dat"); dir.create(dirname(prj_file), showWarnings = FALSE)
  scen <- listScenariosInDB(conn)$name
  for (s in scen) prj <- addScenario(conn, prj_file, s, qfile)
  data <- lapply(want, function(t) tidy(getQuery(prj, t)))
}
dir.create(file.path(here, "out"), showWarnings = FALSE)
for (k in names(data)) {
  p <- file.path(here, "out", paste0(k, "_R.csv")); write_csv(data[[k]], p)
  cat(sprintf("%-22s %5d rows, %d scenarios -> %s\n", k, nrow(data[[k]]), length(unique(data[[k]]$scenario)), p))
}
