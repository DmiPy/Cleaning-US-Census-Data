import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import glob
import seaborn as sns

states = glob.glob("states*.csv")

df_list = []

for state in states:
    data = pd.read_csv(state)
    df_list.append(data)

us_census = pd.concat(df_list)

us_census = us_census.drop_duplicates()

us_census.Income = us_census.Income.str[1:]
us_census.Income = us_census.Income.str.replace(",","")
us_census.Income = pd.to_numeric(us_census.Income)

us_census.GenderPop = us_census.GenderPop.str.split("_")
us_census["Men"] = us_census.GenderPop.str.get(0)
us_census.Men = us_census.Men.str[:-1]
us_census.Men = pd.to_numeric(us_census.Men)
us_census["Women"] = us_census.GenderPop.str.get(1)
us_census.Women = us_census.Women.str[:-1]
us_census.Women = pd.to_numeric(us_census.Women)
us_census.drop("GenderPop", axis=1, inplace=True)

us_census = us_census.fillna(
    value={"Women": us_census.TotalPop - us_census.Men})

plt.scatter(us_census.Women, us_census.Income)
plt.xlabel("Women population")
plt.ylabel("Income")
plt.show()
plt.close()

races = ["Hispanic", "White", "Black", "Native", "Asian", "Pacific"]

for race in races:
    us_census[race] = us_census[race].str[:-1]
    us_census[race] = pd.to_numeric(us_census[race])

us_census = us_census.fillna(value={"Pacific": us_census.Pacific.mean()})

fig, axes = plt.subplots(nrows=2, ncols=3, figsize=(12, 8))
for i, race in enumerate(races):
    rows = i // 3
    cols = i % 3
    ax = axes[rows, cols]
    sns.histplot(data=us_census[race], ax=ax)
plt.tight_layout()
plt.show()
plt.close()
