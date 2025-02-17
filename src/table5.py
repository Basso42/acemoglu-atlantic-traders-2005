"""
Need fixing to get proper absorption in the regression - results
"""
import pandas as pd
import os 
import statsmodels.api as sm
import statsmodels.formula.api as smf
from linearmodels.iv import absorbing

directory = os.getcwd()
data_path = directory[:directory.rfind('/')] + '/data'
figure_path = directory[:directory.rfind('/')] + '/figures'
print(f"data_path : {data_path}")
print(f"figure_path : {figure_path}")

# Load data
df_city = pd.read_stata(data_path + "/REPLICATION-RoE-city-dataset-FINAL.dta")

# Define regressors
western_vars = [f'westerneurope{year}' for year in [1600, 1700, 1750, 1800, 1850]]
atlantic_ports = [f'atlanticport{year}' for year in [1500, 1600, 1700, 1750, 1800, 1850]]
broad_atlantic_ports = [f'broadatlanticport{year}' for year in [1500, 1600, 1700, 1750, 1800, 1850]]
year_vars = [f'yr{i}' for i in [1400, 1500, 1600, 1700, 1750, 1800, 1850]]
trade_vars = ["logsept2002atlantictradexatport", "logsept2002atlantictxbroadatport"]
med_ports = [f'medport{year}' for year in [1500, 1600, 1700, 1750, 1800, 1850]]

# Define filters
city_filter = (df_city["year"] > 1200) & (df_city["year"] < 1900) & (df_city["asia"] != 1) & (df_city["nonmissing13001850"] == 8)

# Convert absorbing variable to categorical
df_city["cityid"] = df_city["cityid"].astype("category")
df_city["countryid"] = df_city["countryid"].astype("category")
df_city["year"] = df_city["year"].astype("category")
df_city["countryid_year"] = df_city["countryid"].astype(str) + "_" + df_city["year"].astype(str)
df_city["countryid_year"] = df_city["countryid_year"].astype("category")

# Here we try to replicate the effect of the areg command in Stata
def absorbing_regression(endog_var, exog_vars, data, weight_col, absorb_col):
    exog = sm.tools.tools.add_constant(data[exog_vars])
    endog = data[endog_var]
    absorb = data[[absorb_col]]  # Ensure absorb is a DataFrame
    weights = data[weight_col] if weight_col in data.columns else None
    
    # Apply clustering at the absorbed fixed effects level (cityid)
    model = absorbing.AbsorbingLS(endog, exog, absorb=absorb, weights=weights, drop_absorbed=True)
    return model.fit(cov_type='clustered', clusters=data["cityid"], debiased=True)

# regressions
city_formulas = {
    "City Column 1 Panel A": ("logu", western_vars + year_vars + atlantic_ports, "cityid"),
    "City Column 1 Panel B": ("logu", western_vars + year_vars + [trade_vars[0]], "cityid"),
    "City Column 2 Panel A": ("logu", western_vars + year_vars + atlantic_ports, "cityid"),
    "City Column 2 Panel B": ("logu", western_vars + year_vars + [trade_vars[0]], "cityid"),
    "City Column 3 Panel A": ("logu", western_vars + year_vars + broad_atlantic_ports, "cityid"),
    "City Column 3 Panel B": ("logu", [trade_vars[1]] + western_vars + year_vars, "cityid"),
    "City Column 4 Panel A": ("logu", western_vars + year_vars + broad_atlantic_ports, "cityid"),
    "City Column 4 Panel B": ("logu", [trade_vars[1]] + western_vars + year_vars, "cityid"),
    "City Column 5 Panel A": ("logu", western_vars + year_vars + atlantic_ports, "cityid"),
    "City Column 5 Panel B": ("logu", western_vars + year_vars + [trade_vars[0]], "cityid"),
    "City Column 6 Panel A": ("logu", western_vars + year_vars + atlantic_ports, "countryid_year"),
    "City Column 6 Panel B": ("logu", western_vars + year_vars + [trade_vars[0]], "countryid_year"),
    "City Column 7 Panel A": ("logu", western_vars + year_vars + atlantic_ports + ["asia1500", "asia1600", "asia1700", "asia1750", "asia1800", "asia1850"], "cityid"),
    "City Column 7 Panel B": ("logu", western_vars + year_vars + [trade_vars[0]] + ["asia1500", "asia1600", "asia1700", "asia1750", "asia1800", "asia1850"], "cityid"),
    "City Column 8 Panel A": ("logu", western_vars + year_vars + atlantic_ports + med_ports, "cityid"),
    "City Column 8 Panel B": ("logu", western_vars + year_vars + med_ports + [trade_vars[0]], "cityid"),
}

# fun regressions using absorbing fixed effects
city_regressions = {}
for col, (endog_var, exog_vars, absorb_col) in city_formulas.items():
    city_regressions[col] = absorbing_regression(endog_var, exog_vars, df_city[city_filter], "u", absorb_col)

# results
for col, model in city_regressions.items():
    print(f"Results for {col}:\n")
    print(model.summary)
    print("\n" + "="*50 + "\n")
