# Establishing Appropriate ML Model - Linear Regression

import pandas as pd
import seaborn as sns
from europe_gas_storage import df
import matplotlib.pyplot as plt
from scipy.stats import pearsonr


# Remember goal is to forecast EU gas storage levels
# Need to identify the most relevant independent variable(s) driving storage flows
    # then establish optimal model based on results
# it is known that weather is a large impact of severity of gas flows
    # first let's visualize and quantify this assumption


# Downloaded daily degree days of Cologne, Germany (EDDK) weather station given lack of aggregate data availability for the EU

## Read csv and Prep DataFrame
# read csv
temp_df = pd.read_csv('tas_timeseries_monthly_cru_1901-2021_DEU.csv', skiprows=2)
# melt into long format (unpivot csv)
temp_df = temp_df.melt(id_vars=['Unnamed: 0'])
# rename cols
temp_df.columns = ['year', 'month', 'temperature']
# convert month to number
month_conv = {'Jan':1, 'Feb':2, 'Mar':3, 'Apr':4, 'May':5, 'Jun':6, 'Jul':7, 'Aug':8, 'Sep':9, 'Oct':10, 'Nov':11, 'Dec':12}
temp_df['month'] = temp_df['month'].map(month_conv)
# combine cols to form date, sort by date
temp_df['date'] = pd.to_datetime(temp_df[['year', 'month']].assign(day=1))
temp_df = temp_df.sort_values(by='date')
# convert temperature to F
temp_df['temperature'] = temp_df['temperature'] * (9/5) + 32
# add column to get degree days, with base 65 degrees
temp_df['degree_days'] = temp_df['temperature'] - 65


## Prep to merge relevant columns of multiple DataFrames

# create DataFrame of gasDayStart and storage flow from europe_gas_storage.py
storage_flow_df = df[['gasDayStart', 'net storage flow']]
# sum flows by month
storage_flow_df = storage_flow_df.set_index('gasDayStart').resample('MS').sum().reset_index()
# merge df_storage_flow with dd on date
temp_df_merged = pd.merge(temp_df, storage_flow_df, how='inner', left_on='date', right_on='gasDayStart')
# show only relevant data for analysis: drop columns and set date as index
temp_df_merged = temp_df_merged.drop(['year', 'month', 'temperature', 'gasDayStart'], axis=1).set_index('date')


## Visualize and Quantify Potential Correlation

# plot EU net gas storage flows vs. degree days overtime
sns.lineplot(x='date', y='net storage flow', data=temp_df_merged)
plt.xticks(rotation=45)
ax2 = plt.twinx()
sns.lineplot(x='date', y='degree_days', color='r', data=temp_df_merged, ax=ax2)
plt.show()

# scatterplot of net storage flows vs. degree days
sns.scatterplot(x='degree_days', y='net storage flow', data=temp_df_merged)
plt.xlabel('Daily Degree Days')
plt.ylabel('Net EU Gas Storage Flows (GWh/d)')
plt.show()

# visuals show that the lower the degree days (colder) the more gas is drawn from storage

# using Pearson correlation to quantify strength of relationship between two continuous variables 
print("Association between Daily Degree Days and Net EU Gas Storage Flows:")
print(pearsonr(temp_df_merged['degree_days'], temp_df_merged['net storage flow']))

# TAKEAWAY
    # strong correlation between the variables exists
    # the association between degree days and net storage flows is statistically significant



### Linear Regression to find line of best fit
# remember: trying to forecast storage levels (gasInStorage)
    # first need a good estimator
    # based on strong correlation, using degree days could be a good predictor for storage flows - Linear Regression could work here

# creating feature and target arrays
X_dd = temp_df_merged['degree_days'].values
y = temp_df_merged['net storage flow'].values
print(X_dd.shape, y.shape)

# reshape to make array 2D for scikitlearn compatibility
X_dd = X_dd.reshape(-1, 1)

from sklearn.linear_model import LinearRegression
# instantiate regression model
reg = LinearRegression()
reg.fit(X_dd, y)
# predict storage flows using X_dd (y-axis for line of best fit)
predictions = reg.predict(X_dd)
# scatter plot plus reg line
plt.scatter(X_dd, y)
plt.plot(X_dd, predictions, color='r', label='line of best fit')
plt.legend()
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
    # degree days explain 84% of the variance in storage flows

from sklearn.metrics import mean_squared_error
rmse = mean_squared_error(y, predictions, squared=False) # False to return sqrt of MSE
print('RMSE: {}'.format(rmse))
# model has average error of storage flows of 40,850 GWH/mo

# based on correlation, p-value, R^2 and RMSE output, Linear Regression will be an appropriate model to predict storage levels