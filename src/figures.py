"""
Reproduces figure 1a and 1b of the article
"""


import pandas as pd
import os
import matplotlib.pyplot as plt 


directory = os.getcwd()
data_path = directory[:directory.rfind('/')] + '/data'
figure_path = directory[:directory.rfind('/')] + '/figures'
print(f"data_path : {data_path}")
print(f"figure_path : {figure_path}")


df = pd.read_stata(data_path + "/REPLICATION-RoE-country-dataset-FINAL.dta")


## Fig 1a

# years in the dataset
YEARS = [1300, 1400, 1500, 1600, 1700, 1750, 1800, 1850]

results_year_western = []
results_year_eastern = []
results_year_asia = []

# Column 3: Western Europe
for year in YEARS:

    #western
    subset = df[(df['date'] == year) & (df['westerneurope'] == 1)]
    weighted_mean = (subset['sjurbanization'] * subset['totalpopulation']).sum() / subset['totalpopulation'].sum()
    results_year_western.append(weighted_mean*100)

    #eastern
    subset = df[(df['date'] == year) & (df['easterneurope'] == 1)]
    weighted_mean = (subset['sjurbanization'] * subset['totalpopulation']).sum() / subset['totalpopulation'].sum()
    results_year_eastern.append(weighted_mean*100)

    #asia
    subset = df[(df['date'] == year) & (df['asia'] == 1)]
    weighted_mean = (subset['sjurbanization'] * subset['totalpopulation']).sum() / subset['totalpopulation'].sum()
    results_year_asia.append(weighted_mean*100)


plt.plot(YEARS, results_year_western, linestyle='-', marker='o', label='Western Europe')
plt.plot(YEARS, results_year_eastern, linestyle='-', marker='o', label='Eastern Europe')
plt.plot(YEARS, results_year_asia, linestyle='-', marker='o', label='Asia')



plt.xticks(YEARS)
plt.ylabel('Urbanization rate')
plt.xlabel('Years')
plt.legend()
plt.title('Urbanization rates (%), weighted by population, 1300–1850')
plt.grid()
plt.tight_layout()
plt.savefig(figure_path + '/urb_rate_west-east-asia.pdf',dpi=200)
plt.show()
plt.close()


#Fig 1b

# years in the dataset
results_year_atlantic = []
results_year_west_not_atlantic = []
results_year_eastern = []

for year in YEARS:

    subset = df[(df['date'] == year) & (df['westerneurope'] == 1) & (df['atlantictrader'] == 1)]
    weighted_mean = (subset['sjurbanization'] * subset['totalpopulation']).sum() / subset['totalpopulation'].sum()
    results_year_atlantic.append(weighted_mean*100)

    #eastern
    subset = df[(df['date'] == year) & (df['westerneurope'] == 1) & (df['atlantictrader'] == 0)]
    weighted_mean = (subset['sjurbanization'] * subset['totalpopulation']).sum() / subset['totalpopulation'].sum()
    results_year_west_not_atlantic.append(weighted_mean*100)

    #asia
    subset = df[(df['date'] == year) & (df['easterneurope'] == 1)]
    weighted_mean = (subset['sjurbanization'] * subset['totalpopulation']).sum() / subset['totalpopulation'].sum()
    results_year_eastern.append(weighted_mean*100)


plt.plot(YEARS, results_year_atlantic, linestyle='-', marker='o', label='Atlantic Traders')
plt.plot(YEARS, results_year_west_not_atlantic, linestyle='-', marker='o', label='Western Europe not Atlantic Traders')
plt.plot(YEARS, results_year_eastern, linestyle='-', marker='o', label='Eastern Europe')



plt.xticks(YEARS)
plt.ylabel('Urbanization rate')
plt.xlabel('Years')
plt.legend()
plt.title('Urbanization rates (%), weighted by population, 1300–1850')
plt.grid()
plt.tight_layout()
plt.savefig(figure_path + '/urb_rate_atl-west-east.pdf', dpi=200)
plt.show()