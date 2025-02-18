"Outputs second table with country level urbanization as the dependent variable"

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


def run_regression(data, formula, weight_col=None):
    """
    Runs a regression with optional weighting.
    """
    if weight_col:
        model = smf.wls(formula, data=data, weights=data[weight_col]).fit()
    else:
        model = smf.ols(formula, data=data).fit()
    return model


# Filters
base_filter = (df_country['asia'] != 1) & (df_country['date'] > 1200) & (df_country['date'] < 1900)
data_filtered = df_country[base_filter]

"""
Panel A: flexible specification - MATCHING RESULTS
"""

# formulas
base_formula = "sjurbanization ~ westerneurope1600 + westerneurope1700 + westerneurope1750 + westerneurope1800 + westerneurope1850 + "
base_formula += " + ".join([f'country{i}' for i in range(1, 30)]) + " + "
base_formula += " + ".join([f'yr{i}' for i in [1000, 1100, 1200, 1300, 1400, 1500, 1600, 1700, 1750, 1800, 1850]])

# Running regressions
regressions = {}
regressions['col1'] = run_regression(data_filtered, base_formula, weight_col='totalpopulation')
data_filtered2 = df_country[(df_country['asia'] != 1) & (df_country['date'] < 1900)]
regressions['col2'] = run_regression(data_filtered2, base_formula, weight_col='totalpopulation')

# Including Atlantic traders
formula_atlantic = base_formula + " + atlantictrader1500 + atlantictrader1600 + atlantictrader1700 + atlantictrader1750 + atlantictrader1800 + atlantictrader1850"
regressions['col3'] = run_regression(data_filtered, formula_atlantic, weight_col='totalpopulation')
regressions['col4'] = run_regression(data_filtered2, formula_atlantic, weight_col='totalpopulation')

# Unweighted regression
regressions['col5'] = run_regression(data_filtered, formula_atlantic)

# With Asia included
data_with_asia = df_country[(df_country['date'] > 1200) & (df_country['date'] < 1900)]
regressions['col6'] = run_regression(data_with_asia, formula_atlantic, weight_col='totalpopulation')

# Without Britain
data_no_britain = data_filtered[data_filtered['countryid'] != 7]
regressions['col7'] = run_regression(data_no_britain, formula_atlantic, weight_col='totalpopulation')

# coast-to-area trade variables
formula_coast = base_formula + " + coasttoarea1500 + coasttoarea1600 + coasttoarea1700 + coasttoarea1750 + coasttoarea1800 + coasttoarea1850"
regressions['col8'] = run_regression(data_filtered, formula_coast, weight_col='totalpopulation')
regressions['col9'] = run_regression(data_filtered2, formula_coast, weight_col='totalpopulation')
regressions['col10'] = run_regression(data_filtered, formula_coast)

# results
for col, model in regressions.items():
    print(f"Results for {col}:")
    print(model.summary())
    print("\n" + "="*50 + "\n")


"""
Panel B: structured specification - MATCHING RESULTS
"""
# variables
western_vars = [f'westerneurope{year}' for year in [1600, 1700, 1750, 1800, 1850]]
country_vars = [f'country{i}' for i in range(1, 30)]
year_vars = [f'yr{i}' for i in [1000, 1100, 1200, 1300, 1400, 1500, 1600, 1700, 1750, 1800, 1850]]
trade_vars = ["logsept2002atradexatlantictrader", "logsept2002atradexcoasttoarea"]

# filters
base_filter = (df_country["asia"] != 1) & (df_country["date"] > 1200) & (df_country["date"] < 1900)
base_filter_extended = (df_country["asia"] != 1) & (df_country["date"] < 1900)

# regression formulas
formula_1 = "sjurbanization ~ " + " + ".join(western_vars + country_vars + year_vars)
formula_trade = formula_1 + " + " + trade_vars[0]
formula_trade_coast = formula_1 + " + " + trade_vars[1]

# regressions
regressions = {
    "Column 1": weighted_regression(formula_1, df_country[base_filter], "totalpopulation"),
    "Column 2": weighted_regression(formula_1, df_country[base_filter_extended], "totalpopulation"),
    "Column 3": weighted_regression(formula_trade, df_country[base_filter], "totalpopulation"),
    "Column 4": weighted_regression(formula_trade, df_country[base_filter_extended], "totalpopulation"),
    "Column 5": unweighted_regression(formula_trade, df_country[base_filter & df_country["totalpopulation"].notna()]),
    "Column 6": weighted_regression(formula_trade, df_country[(df_country["date"] > 1200) & (df_country["date"] < 1900)], "totalpopulation"),
    "Column 7": weighted_regression(formula_trade, df_country[base_filter & (df_country["countryid"] != 7)], "totalpopulation"),
    "Column 8": weighted_regression(formula_trade_coast, df_country[base_filter], "totalpopulation"),
    "Column 9": weighted_regression(formula_trade_coast, df_country[base_filter_extended], "totalpopulation"),
    "Column 10": unweighted_regression(formula_trade_coast, df_country[base_filter & df_country["totalpopulation"].notna()]),
}

# results
for col, model in regressions.items():
    print(f"Results for {col}:")
    print(model.summary())
    print("\n" + "="*50 + "\n")

