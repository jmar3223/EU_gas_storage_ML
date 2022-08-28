# Establishing Appropriate ML Model - Linear Regression

import pandas as pd
import seaborn as sns
import europe_gas_storage
from europe_gas_storage import df
import matplotlib.pyplot as plt
from statsmodels.tsa.seasonal import seasonal_decompose
from scipy.stats import pearsonr


# Remember goal is to forecast EU gas storage levels
# Need to identify the most relevant independent variable(s) driving storage flows
    # then establish optimal model based on results
# it is known that weather is a large impact of severity of gas flows
    # first let's visualize and quantify this assumption


# Downloaded daily degree days of Cologne, Germany (EDDK) weather station given lack of aggregate data availability for the EU

## Read csv and Prep DataFrame
# read csv
dd = pd.read_csv('EDDK_DD_65F.csv')
# rename columns
dd.columns = ['date', 'HDD', 'CDD']
# start at beginning of csv dataset
dd = dd.iloc[6:]
# convert from object types
dd['date'] = dd['date'].astype('datetime64[ns]')
dd_cols = dd.columns.drop('date')
dd[dd_cols] = dd[dd_cols].apply(pd.to_numeric, axis=1)
# new column for ease of analysis - shows net degree days
dd['degree_days'] = dd['CDD'] - dd['HDD']


## Prep to merge relevant columns of multiple DataFrames

# create DataFrame of gasDayStart and storage flow from europe_gas_storage.py
df_storage_flow = df[['gasDayStart', 'net storage flow']]
# merge df_storage_flow with dd on date
dd_merged = pd.merge(dd, df_storage_flow, how='inner', left_on='date', right_on='gasDayStart')
# show only relevant data for analysis: drop columns and set date as index
dd_merged = dd_merged.drop(['HDD', 'CDD', 'gasDayStart'], axis=1).set_index('date')


## Visualize and Quantify Potential Correlation

# plot EU net gas storage flows vs. degree days overtime
sns.lineplot(x='date', y='net storage flow', data=dd_merged)
plt.xticks(rotation=45)
ax2 = plt.twinx()
sns.lineplot(x='date', y='degree_days', color='r', data=dd_merged, ax=ax2)
plt.show()

# scatterplot of net storage flows vs. degree days
sns.scatterplot(x='degree_days', y='net storage flow', data=dd_merged)
plt.xlabel('Daily Degree Days')
plt.ylabel('Net EU Gas Storage Flows (GWh/d)')
plt.show()

# visuals show that the lower the degree days (colder) the more gas is drawn from storage

# using Pearson correlation to quantify strength of relationship between two continuous variables 
print("Association between Daily Degree Days and Net EU Gas Storage Flows:")
print(pearsonr(dd_merged['degree_days'], dd_merged['net storage flow']))

# TAKEAWAY
    # strong correlation between the variables exists
    # the association between degree days and net storage flows is statistically significant



### Linear Regression to find line of best fit
# remember: trying to forecast storage levels (gasInStorage)
    # first need a good estimator
    # based on strong correlation, using degree days could be a good predictor for storage flows - Linear Regression could work here

# creating feature and target arrays
X_dd = dd_merged['degree_days'].values
y = dd_merged['net storage flow'].values
print(X_dd.shape, y.shape)

# reshape to make array 2D for scikitlearn compatibility
X_dd = X_dd.reshape(-1, 1)

from sklearn.linear_model import LinearRegression
# instantiate regression model
reg = LinearRegression()
reg.fit(X_dd, y)
# predict storage flows using X_dd
predictions = reg.predict(X_dd)
# scatter plot plus reg line
plt.scatter(X_dd, y)
plt.plot(X_dd, predictions, color='r')
plt.xlabel('Daily Degree Days')
plt.ylabel('Net EU Gas Storage Flows (GWh/d)')
plt.show()

# show slope and intercept of line of best fit
a = (predictions[2] - predictions[1]) / (X_dd[2] - X_dd[1])
b = predictions[1] - (a * X_dd[1])
print('slope: ', a)
print('intercept: ', b)


## Assessing regression model performance
r_squared = reg.score(X_dd, y)
print('R^2: {}'.format(r_squared))
# degree days explain 67% of the variance in storage flows

from sklearn.metrics import mean_squared_error
rmse = mean_squared_error(y, predictions, squared=False) # False to return sqrt of MSE
print('RMSE: {}'.format(rmse))
# model has average error of storage flows of 2,200 GWH/d

# based on correlation, p-value, R^2 and RMSE output, Linear Regression will be an appropriate model to predict storage levels