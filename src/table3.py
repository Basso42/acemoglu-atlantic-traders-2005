"Outputs third table with gdp from Maddison (2001) as the dependent variable"

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

df_country = pd.read_stata(data_path + "/REPLICATION-RoE-country-dataset-FINAL.dta")

# Filter conditions
base_filter = (df_country["asia"] != 1) & (df_country["date"] > 1200) & (df_country["date"] < 1850)
base_filter_extended = (df_country["asia"] != 1) & (df_country["date"] > 1200) & (df_country["date"] < 1900)

# List of independent variables
western_vars = ["westerneurope1600", "westerneurope1700", "westerneurope1750", "westerneurope1800", "westerneurope1850"]
country_vars = [f"country{i}" for i in range(1, 30)]
year_vars = [f'yr{i}' for i in [1000, 1100, 1200, 1300, 1400, 1500, 1600, 1700, 1750, 1800, 1850]]

regressions = {}

"""
Panel A: flexible specification - MATCHING RESULTS
"""
# Column 1: Weighted Regression
formula_1 = "loggdppcmaddison ~ " + " + ".join(western_vars + country_vars + year_vars)
regressions["Column 1"] = weighted_regression(formula_1, df_country[base_filter], "totalpopulation")

# Column 2: Weighted Regression to 1900
regressions["Column 2"] = weighted_regression(formula_1, df_country[base_filter_extended], "totalpopulation")

# Column 3: Atlantic Trader Excluding Ireland/Belgium
atlantic_vars = ["atlantictrader1600", "atlantictrader1700", "atlantictrader1750", "atlantictrader1800", "atlantictrader1850"]
formula_3 = formula_1 + " + " + " + ".join(atlantic_vars)
regressions["Column 3"] = weighted_regression(formula_3, df_country[base_filter], "totalpopulation")

# Column 4: Atlantic Trader to 1900
regressions["Column 4"] = weighted_regression(formula_3, df_country[base_filter_extended], "totalpopulation")

# Column 5: Unweighted Regression
regressions["Column 5"] = unweighted_regression(formula_3, df_country[base_filter & df_country["totalpopulation"].notna()])

# Column 6: With Asia
regressions["Column 6"] = weighted_regression(formula_3, df_country[(df_country["date"] > 1200) & (df_country["date"] < 1850)], "totalpopulation")

# Column 7: Without Britain
regressions["Column 7"] = weighted_regression(formula_3, df_country[base_filter & (df_country["countryid"] != 7)], "totalpopulation")


"""
Panel B: structured specification
"""

trade_vars = ["logsept2002atradexatlantictrader", "logsept2002atradexcoasttoarea"]

# Define filters
base_filter = (df_country["asia"] != 1) & (df_country["date"] > 1200) & (df_country["date"] < 1900)
base_filter_extended = (df_country["asia"] != 1) & (df_country["date"] < 1900)

# Define regression formulas
formula_1 = "loggdppcmaddison ~ " + " + ".join(western_vars + country_vars + year_vars)
formula_trade = formula_1 + " + " + trade_vars[0]
formula_trade_coast = formula_1 + " + " + trade_vars[1]

# regressions
regressions = {
    "Panel B Column 1": weighted_regression(formula_1, df_country[base_filter], "totalpopulation"),
    "Panel B Column 2": weighted_regression(formula_1, df_country[base_filter_extended], "totalpopulation"),
    "Panel B Column 3": weighted_regression(formula_trade, df_country[base_filter & (df_country["date"] < 1850)], "totalpopulation"),
    "Panel B Column 4": weighted_regression(formula_trade, df_country[base_filter_extended], "totalpopulation"),
    "Panel B Column 5": unweighted_regression(formula_trade, df_country[base_filter & (df_country["date"] < 1850) & df_country["totalpopulation"].notna()]),
    "Panel B Column 6": weighted_regression(formula_trade, df_country[(df_country["date"] > 1200) & (df_country["date"] < 1850)], "totalpopulation"),
    "Panel B Column 7": weighted_regression(formula_trade, df_country[base_filter & (df_country["date"] < 1850) & (df_country["countryid"] != 7)], "totalpopulation"),
    "Panel B Column 8": weighted_regression(formula_trade_coast, df_country[base_filter & (df_country["date"] < 1850)], "totalpopulation"),
    "Panel B Column 9": weighted_regression(formula_trade_coast, df_country[base_filter_extended], "totalpopulation"),
    "Panel B Column 10": unweighted_regression(formula_trade_coast, df_country[base_filter & (df_country["date"] < 1850) & df_country["totalpopulation"].notna()]),
}

# Display results
for col, model in regressions.items():
    print(f"Results for {col}:")
    print(model.summary())
    print("\n" + "="*50 + "\n")