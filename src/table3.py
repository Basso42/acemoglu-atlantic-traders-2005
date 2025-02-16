import pandas as pd
import os 
import statsmodels.api as sm
import statsmodels.formula.api as smf

directory = os.getcwd()
data_path = directory[:directory.rfind('/')] + '/data'
figure_path = directory[:directory.rfind('/')] + '/figures'
print(f"data_path : {data_path}")
print(f"figure_path : {figure_path}")

df_country = pd.read_stata(data_path + "/REPLICATION-RoE-country-dataset-FINAL.dta")

def run_regression(formula, df, weight_col=None):
    if weight_col:
        model = smf.wls(formula, data=df, weights=df[weight_col]).fit()
    else:
        model = smf.ols(formula, data=df).fit()
    print(model.summary())
    return model

# Filtering dataset
base_filter = (df_country['asia'] != 1) & (df_country['date'] > 1200) & (df_country['date'] < 1850)
data_filtered = df_country[base_filter]

# Define regression formulas
base_formula = "gdppcmaddison ~ "
base_formula += " + ".join([f'westerneurope{i}' for i in [1600, 1700, 1750, 1800, 1850]]) + " + "
base_formula += " + ".join([f'country{i}' for i in range(1, 30)]) + " + "
base_formula += " + ".join([f'yr{i}' for i in [1000, 1100, 1200, 1300, 1400, 1500, 1600, 1700, 1750, 1800, 1850]])

# Running regressions
regressions = {}
regressions['col1'] = run_regression(base_formula, data_filtered, weight_col='totalpopulation')

data_filtered2 = df_country[(df_country['asia'] != 1) & (df_country['date'] < 1900)]
regressions['col2'] = run_regression(base_formula, data_filtered2, weight_col='totalpopulation')

# Including Atlantic traders
formula_atlantic = base_formula + " + " + " + ".join([f'atlantictrader{i}' for i in [1500, 1600, 1700, 1750, 1800, 1850]])
regressions['col3'] = run_regression(formula_atlantic, data_filtered, weight_col='totalpopulation')
regressions['col4'] = run_regression(formula_atlantic, data_filtered2, weight_col='totalpopulation')

# Unweighted regression
regressions['col5'] = run_regression(formula_atlantic, data_filtered)

# With Asia included
data_with_asia = df_country[(df_country['date'] > 1200) & (df_country['date'] < 1900)]
regressions['col6'] = run_regression(formula_atlantic, data_with_asia, weight_col='totalpopulation')

# Without Britain
data_no_britain = data_filtered[data_filtered['countryid'] != 7]
regressions['col7'] = run_regression(formula_atlantic, data_no_britain, weight_col='totalpopulation')

# Using coast-to-area trade variables
formula_coast = base_formula + " + " + " + ".join([f'coasttoarea{i}' for i in [1500, 1600, 1700, 1750, 1800, 1850]])
regressions['col8'] = run_regression(formula_coast, data_filtered, weight_col='totalpopulation')
regressions['col9'] = run_regression(formula_coast, data_filtered2, weight_col='totalpopulation')
regressions['col10'] = run_regression(formula_coast, data_filtered)

# Display results
for col, model in regressions.items():
    print(f"Results for {col}:")
    print(model.summary())
    print("\n" + "="*50 + "\n")
