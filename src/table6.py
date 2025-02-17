"""
Replicating Table 6= Regressions where dependent variable is constraint on the executive (from Polity IV dataset)
"""
import pandas as pd
import os 
import statsmodels.api as sm
import statsmodels.formula.api as smf

from utils import weighted_regression

directory = os.getcwd()
data_path = directory[:directory.rfind('/')] + '/data'
figure_path = directory[:directory.rfind('/')] + '/figures'
print(f"data_path : {data_path}")
print(f"figure_path : {figure_path}")

df_country = pd.read_stata(data_path + "/REPLICATION-RoE-country-dataset-FINAL.dta")

# variables
western_vars = [f'westerneurope{year}' for year in [1600, 1700, 1750, 1800, 1850]]
protestant_vars = [f'protestant{year}' for year in [1600, 1700, 1750, 1800, 1850]]
roman_vars = [f'romanempire{year}' for year in [1600, 1700, 1750, 1800, 1850]]
latitude_vars = [f'latitude{year}' for year in [1600, 1700, 1750, 1800, 1850]]
atlantic_vars = [f'atlantictrader{year}' for year in [1500, 1600, 1700, 1750, 1800, 1850]]
country_vars = [f'country{i}' for i in range(1, 30)]
year_vars = [f'yr{i}' for i in [1000, 1100, 1200, 1300, 1400, 1500, 1600, 1700, 1750, 1800, 1850]]
trade_vars = ["logsept2002atradexatlantictrader", "logsept2002atradexcoasttoarea"]

#filters
base_filter = (df_country["date"] > 1200)

#regression formulas
formulas = {
    "Column 1": "sjcodeconsexec2 ~ " + " + ".join(western_vars + country_vars + year_vars),
    "Column 2": "sjcodeconsexec2 ~ " + " + ".join(western_vars + atlantic_vars + country_vars + year_vars),
    "Column 3": "sjcodeconsexec2 ~ " + " + ".join(western_vars + country_vars + year_vars + ["logsept2002atradexatlantictrader"]),
    "Column 4": "sjcodeconsexec2 ~ " + " + ".join(western_vars + country_vars + year_vars + ["logsept2002atradexatlantictrader"] + protestant_vars),
    "Column 5": "sjcodeconsexec2 ~ " + " + ".join(western_vars + country_vars + year_vars + ["logsept2002atradexatlantictrader", "warsperyear"]),
    "Column 6": "sjcodeconsexec2 ~ " + " + ".join(western_vars + country_vars + year_vars + ["logsept2002atradexatlantictrader"] + roman_vars),
    "Column 7": "sjcodeconsexec2 ~ " + " + ".join(western_vars + country_vars + year_vars + ["logsept2002atradexatlantictrader"] + latitude_vars),
    "Column 8": "sjcodeconsexec2 ~ " + " + ".join(western_vars + country_vars + year_vars + ["coasttoarea1500", "coasttoarea1600", "coasttoarea1700", "coasttoarea1750", "coasttoarea1800", "coasttoarea1850"]),
    "Column 9": "sjcodeconsexec2 ~ " + " + ".join(western_vars + country_vars + year_vars + ["logsept2002atradexcoasttoarea"])
}

#regressions
regressions = {}
for col, formula in formulas.items():
    regressions[col] = weighted_regression(formula, df_country[base_filter], "totalpopulation")

#results
for col, model in regressions.items():
    print(f"Results for {col}:")
    print(model.summary())
    print("\n" + "="*50 + "\n")

