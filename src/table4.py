"""
Replicates table 4
"""

import pandas as pd
import os 
import statsmodels.api as sm
import statsmodels.formula.api as smf

from utils import weighted_regression, unweighted_regression

directory = os.getcwd()
data_path = directory[:directory.rfind('/')] + '/data'
figure_path = directory[:directory.rfind('/')] + '/figures'
print(f"data_path : {data_path}")
print(f"figure_path : {figure_path}")

# load data
df_country = pd.read_stata(data_path + "/REPLICATION-RoE-country-dataset-FINAL.dta")


# define regressors
western_vars = [f'westerneurope{year}' for year in [1600, 1700, 1750, 1800, 1850]]
protestant_vars = [f'protestant{year}' for year in [1600, 1700, 1750, 1800, 1850]]
roman_vars = [f'romanempire{year}' for year in [1600, 1700, 1750, 1800, 1850]]
latitude_vars = [f'latitude{year}' for year in [1600, 1700, 1750, 1800, 1850]]
country_vars = [f'country{i}' for i in range(1, 30)]
year_vars = [f'yr{i}' for i in [1000, 1100, 1200, 1300, 1400, 1500, 1600, 1700, 1750, 1800, 1850]]
trade_vars = ["logsept2002atradexatlantictrader", "logsept2002atradexcoasttoarea"]

# Define filters
base_filter = (df_country["asia"] != 1) & (df_country["date"] > 1200)
base_filter_extended = (df_country["asia"] != 1) & (df_country["date"] > 1200) & (df_country["date"] < 1850)

# Define regression formulas
formulas = {
    "Structured Column 1": "sjurbanization ~ " + " + ".join(western_vars + protestant_vars + year_vars + country_vars + [trade_vars[0]]),
    "Structured Column 2 (Wars)": "sjurbanization ~ " + " + ".join(western_vars + year_vars + country_vars + [trade_vars[0], "warsperyear"]),
    "Structured Column 3 (Roman Heritage)": "sjurbanization ~ " + " + ".join(western_vars + year_vars + roman_vars + country_vars + [trade_vars[0]]),
    "Structured Column 4 (Latitude)": "sjurbanization ~ " + " + ".join(western_vars + year_vars + latitude_vars + country_vars + [trade_vars[0]]),
    "Structured Column 5": "loggdppcmaddison ~ " + " + ".join(western_vars + protestant_vars + year_vars + country_vars + [trade_vars[0]]),
    "Structured Column 6 (GDP Wars)": "loggdppcmaddison ~ " + " + ".join(western_vars + protestant_vars + year_vars + country_vars + [trade_vars[0], "warsperyear"]),
    "Structured Column 7 (GDP Roman Heritage)": "loggdppcmaddison ~ " + " + ".join(western_vars + year_vars + roman_vars + country_vars + [trade_vars[0]]),
    "Structured Column 8 (GDP Latitude)": "loggdppcmaddison ~ " + " + ".join(western_vars + year_vars + latitude_vars + country_vars + [trade_vars[0]])
}


# regressions
regressions = {}
for col, formula in formulas.items():
    regressions[col] = weighted_regression(formula, df_country[base_filter_extended if "loggdppcmaddison" in formula else base_filter], "totalpopulation")

#For coastline columns
formulas.update({
    "Coastline Column 1": "sjurbanization ~ " + " + ".join(western_vars + protestant_vars + year_vars + country_vars + [trade_vars[1]]),
    "Coastline Column 2 (Wars)": "sjurbanization ~ " + " + ".join(western_vars + year_vars + country_vars + [trade_vars[1], "warsperyear"]),
    "Coastline Column 3 (Roman Heritage)": "sjurbanization ~ " + " + ".join(western_vars + year_vars + roman_vars + country_vars + [trade_vars[1]]),
    "Coastline Column 4 (Latitude)": "sjurbanization ~ " + " + ".join(western_vars + year_vars + latitude_vars + country_vars + [trade_vars[1]]),
    "Coastline Column 5": "loggdppcmaddison ~ " + " + ".join(western_vars + protestant_vars + year_vars + country_vars + [trade_vars[1]]),
    "Coastline Column 6 (GDP Wars)": "loggdppcmaddison ~ " + " + ".join(western_vars + year_vars + country_vars + [trade_vars[1], "warsperyear"]),
    "Coastline Column 7 (GDP Roman Heritage)": "loggdppcmaddison ~ " + " + ".join(western_vars + year_vars + roman_vars + country_vars + [trade_vars[1]]),
    "Coastline Column 8 (GDP Latitude)": "loggdppcmaddison ~ " + " + ".join(western_vars + year_vars + latitude_vars + country_vars + [trade_vars[1]])
})

# Run regressions
for col, formula in formulas.items():
    regressions[col] = weighted_regression(formula, df_country[base_filter_extended if "loggdppcmaddison" in formula else base_filter], "totalpopulation")

#results
for col, model in regressions.items():
    print(f"Results for {col}:\n")
    print(model.summary())
    print("\n" + "="*50 + "\n")
