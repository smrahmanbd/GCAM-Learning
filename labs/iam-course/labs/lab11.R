# Lab 11 (week 11): a three-technology power system as a linear program
# New R skill: lpSolve - objective, constraints, reading shadow prices
# Needs: install.packages("lpSolve") once. No data files.
# Gaps: three places are marked with three underscores. Replace each
#   with your own code before you run that line. The hint is in the comment.
#
# Illustrative numbers (not data for any real country):
#   technology   cost $/MWh   emissions tCO2/MWh   limit TWh
#   coal             60             0.9                60
#   gas              70             0.4                50
#   solar            80             0.0                30
#   demand: 100 TWh
# Units: $/MWh x TWh = million $.   tCO2/MWh x TWh = MtCO2.

library(lpSolve)

# ---- Part A: the cheapest mix that meets demand ----
# Decision variables: TWh from coal, gas and solar (always in this order).
# lpSolve assumes every variable is zero or more.
cost <- c(60, 70, 80)             # objective: cost per unit, coal, gas, solar

# One row per constraint, one column per technology.
A <- rbind(demand = c(1, 1, 1),   # coal + gas + solar = demand
           coal   = c(1, 0, 0),   # coal  <= its limit
           gas    = c(0, 1, 0),   # gas   <= its limit
           solar  = c(0, 0, 1))   # solar <= its limit
dir <- c("=", "<=", "<=", "<=")
rhs <- c(___, 60, 50, 30)         # GAP 1: demand in TWh

base <- lp("min", cost, A, dir, rhs,
           compute.sens = TRUE)   # compute.sens = TRUE asks for the duals

base$status     # 0 = success, 2 = no feasible solution
base$solution   # TWh of coal, gas, solar
base$objval     # total cost, million $

# ---- Part B: add a cap on emissions ----
emis <- c(0.9, 0.4, 0)            # tCO2 per MWh: coal, gas, solar
sum(emis * base$solution)         # MtCO2 without a cap

A2   <- rbind(A, co2 = ___)       # GAP 2: the new row is the emissions vector
dir2 <- c(dir, "<=")
rhs2 <- c(rhs, ___)               # GAP 3: the cap, 40 MtCO2

capped <- lp("min", cost, A2, dir2, rhs2,
             compute.sens = TRUE)
capped$status
capped$solution
capped$objval
sum(emis * capped$solution)       # should equal the cap

# ---- Part C: read the duals (shadow prices) ----
# duals holds one number per constraint, in the order of the rows of the
# constraint matrix, and then one number per variable (technology).
# Each number is the change in total cost when that constraint's
# right-hand side goes up by one unit.
base$duals      # 4 constraints, then 3 technologies
capped$duals    # 5 constraints, then 3 technologies

# The same numbers with labels:
tech <- c("coal", "gas", "solar")
setNames(base$duals,   c(rownames(A),  paste0("var_", tech)))
setNames(capped$duals, c(rownames(A2), paste0("var_", tech)))

# Check one dual yourself: loosen the cap by 1 Mt and solve again.
rhs3 <- rhs2
rhs3[5] <- rhs2[5] + 1
looser <- lp("min", cost, A2, dir2, rhs3)
looser$objval - capped$objval     # compare with capped$duals[5]

# Worksheet 10: try a cap of 37 Mt. Look at $status before anything else.
