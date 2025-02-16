"""
Allows to replicate table 1 (descriptive statistics) of the article
Multiply figures by 100 to get the article's rates
"""
import pandas as pd
import os

#path
directory = os.getcwd()
data_path = directory[:directory.rfind('/')] + '/data'
figure_path = directory[:directory.rfind('/')] + '/figures'
print(f"data_path : {data_path}")
print(f"figure_path : {figure_path}")

df = pd.read_stata(data_path + "/REPLICATION-RoE-country-dataset-FINAL.dta")

# years in the dataset
YEARS = [1300, 1400, 1500, 1600, 1700, 1800, 1850]

# Column 1: Whole Sample, Unweighted
for year in YEARS:
    print(f"Year {year}:", df.loc[df['date'] == year, 'sjurbanization'].describe())

# Column 2: Whole Sample, Weighted
for year in YEARS:
    weighted_mean = (df.loc[df['date'] == year, 'sjurbanization'] * df.loc[df['date'] == year, 'totalpopulation']).sum() / df.loc[df['date'] == year, 'totalpopulation'].sum()
    print(f"Year {year}, Weighted Mean: {weighted_mean}")

# Column 3: Atlantic Western Europe
for year in YEARS:
    subset = df[(df['date'] == year) & (df['westerneurope'] == 1) & (df['atlantictrader'] == 1)]
    weighted_mean = (subset['sjurbanization'] * subset['totalpopulation']).sum() / subset['totalpopulation'].sum()
    print(f"Year {year}, Atlantic Western Europe Weighted Mean: {weighted_mean}")

# Column 4: Non-Atlantic Western Europe
for year in YEARS:
    subset = df[(df['date'] == year) & (df['westerneurope'] == 1) & (df['atlantictrader'] == 0)]
    weighted_mean = (subset['sjurbanization'] * subset['totalpopulation']).sum() / subset['totalpopulation'].sum()
    print(f"Year {year}, Non-Atlantic Western Europe Weighted Mean: {weighted_mean}")

# Column 5: Eastern Europe
for year in YEARS:
    subset = df[(df['date'] == year) & (df['easterneurope'] == 1)]
    weighted_mean = (subset['sjurbanization'] * subset['totalpopulation']).sum() / subset['totalpopulation'].sum()
    print(f"Year {year}, Eastern Europe Weighted Mean: {weighted_mean}")

# Column 6: Asia
for year in YEARS[:-1]:  # No data for Asia in 1850
    subset = df[(df['date'] == year) & (df['asia'] == 1)]
    weighted_mean = (subset['sjurbanization'] * subset['totalpopulation']).sum() / subset['totalpopulation'].sum()
    print(f"Year {year}, Asia Weighted Mean: {weighted_mean}")

# GDP per capita calculations
GDP_YEARS = [1500, 1600, 1700, 1800, 1850]
for year in GDP_YEARS:
    print(f"Year {year}, GDP per capita:", df.loc[(df['date'] == year) & df['totalpopulation'].notna(), 'gdppcmaddison'].describe())

# Weighted GDP per capita
for year in GDP_YEARS:
    weighted_mean = (df.loc[df['date'] == year, 'gdppcmaddison'] * df.loc[df['date'] == year, 'totalpopulation']).sum() / df.loc[df['date'] == year, 'totalpopulation'].sum()
    print(f"Year {year}, Weighted GDP per capita: {weighted_mean}")

# Constraint on Executive
for year in YEARS:
    print(f"Year {year}, Constraint on Executive:", df.loc[(df['date'] == year) & df['totalpopulation'].notna(), 'sjcodeconsexec2'].describe())

# Atlantic Coast-to-Area
COAST_YEAR = 1500
print(f"Year {COAST_YEAR}, Atlantic Coast-to-Area:", df.loc[(df['totalpopulation'].notna()) & (df['date'] == COAST_YEAR), 'coasttoarea'].describe())
