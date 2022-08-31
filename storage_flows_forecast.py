# Forecasting net storage flows
# # integrating Linear Regression ML ouput (relationship between explanatory and response variables) with SARIMA model (degree days, explanatory variable, forecasting)

import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from europe_gas_storage import df
from forecast_dd_SARIMA import temp_df_merged, szn_dd
from establish_ML_model_linReg import predictions, X_dd, storage_flow_df


# slope and intercept of line of best fit
slope = (predictions[2] - predictions[1]) / (X_dd[2] - X_dd[1])
intercept = predictions[1] - (slope * X_dd[1])
print('slope: ', slope)
print('intercept: ', intercept)


# merge storage_flow_df with szn_dd
fcast_dd_flow = pd.merge(storage_flow_df, szn_dd.reset_index(), how='outer', left_on='gasDayStart', right_on='index')
fcast_dd_flow = fcast_dd_flow.drop(['gasDayStart'], axis=1)
fcast_dd_flow = fcast_dd_flow.set_index('index')
fcast_dd_flow[130:145]

## Forecast Storage Flow
# interpolate linear regression output with forecasted degree days to get forecasted storage flows
fcast_dd_flow['storage flow forecast'] = fcast_dd_flow['forecast'] * slope + intercept

# chart actual vs. modeled storage flows
plt.figure(figsize=(12,8))
plt.plot(fcast_dd_flow.index, fcast_dd_flow['net storage flow'], label='actual')
plt.plot(fcast_dd_flow.index, fcast_dd_flow['storage flow forecast'], label='model')
plt.title('Net EU gas storage flows')
plt.ylabel('net storage flows (GWh/month)')
plt.legend()
plt.show()


## Create df with metrics needed to forecast Storage Levels (abs and rel)
# pull relevant cols from original df
gas_storage = df[['gasDayStart', 'gasInStorage', 'workingGasVolume']].set_index('gasDayStart')
# get monthly storage levels and capacity - last day of month value
gas_storage = gas_storage.groupby([gas_storage.index.year, gas_storage.index.month]).tail(1)

# merge historic gas storage
fcast_gas_storage = gas_storage.join(fcast_dd_flow, how='outer')
# drop rows where storage flow forecast is NaN (current date is included in the merged df - need index of just EoM)
fcast_gas_storage = fcast_gas_storage.dropna(subset=['storage flow forecast'])


# create empty column
fcast_gas_storage['gasInStorage forecast'] = np.nan
# start forecast by adding most recent historic value to forecasted numbers
fcast_gas_storage['gasInStorage forecast'].iloc[len(storage_flow_df)-2] = (fcast_gas_storage['gasInStorage'].iloc[len(storage_flow_df)-2])
# remaining forecast uses prior month's 'gasInStorage forecast' and adds current month 'storage flow forecast'
for i in range(len(storage_flow_df)-1, len(fcast_gas_storage)):
    fcast_gas_storage['gasInStorage forecast'].iloc[i] = (
        fcast_gas_storage['gasInStorage forecast'].iloc[i-1] + 
        fcast_gas_storage['storage flow forecast'].iloc[i] /
        1000)

# chart history and forecast
plt.plot(fcast_gas_storage['gasInStorage'], label='actual')
plt.plot(fcast_gas_storage['gasInStorage forecast'], label='model')
plt.title('Forecasted EU Gas storage (TWh)')
plt.legend()
plt.show()



### Seasonality Chart: % of gas storage full
# fill NaNs of workingGasVolume rows with latest value
fcast_gas_storage['workingGasVolume'] = fcast_gas_storage['workingGasVolume'].fillna(method='ffill')
# add pct full columns - history and forecast
fcast_gas_storage['pct full hist'] = fcast_gas_storage['gasInStorage'] / fcast_gas_storage['workingGasVolume']
fcast_gas_storage['pct full fcast'] = fcast_gas_storage['gasInStorage forecast'] / fcast_gas_storage['workingGasVolume']
fcast_gas_storage['pct full'] = fcast_gas_storage['pct full hist'].fillna(fcast_gas_storage['pct full fcast'])

# columns to get latest 10 years - used for sumary stats in pivot table
last_ten_years = slice(df['year'].iat[-1] - 9, df['year'].iat[-1])
# create month and year columns to pivot on
fcast_gas_storage['month'] = fcast_gas_storage.index.month 
fcast_gas_storage['year'] = fcast_gas_storage.index.year

# set up pivot table
pivot_fcast = pd.pivot_table(fcast_gas_storage, values='pct full', index=['month'], columns=['year'], aggfunc=np.sum)
# add summary statistics columns
pivot_fcast['max'] = pivot_fcast.loc[:, last_ten_years].max(axis=1)
pivot_fcast['min'] = pivot_fcast.loc[:, last_ten_years].min(axis=1)
pivot_fcast['10 year avg'] = pivot_fcast.loc[:, last_ten_years].mean(axis=1)



import plotly.graph_objects as go
from plotly.offline import plot
# establish figure, list of figure colors
fcast_eu_fig = go.Figure()
colors = ['#17becf','#e377c2','#ff7f0e','#2ca02c','darkblue','firebrick']
# build traces for 3 summary stats, fixing params to visualize max vs. min range band
# room for improvement: list month-day on x axis vs. currently showing day of year
fcast_eu_fig.add_trace(
    go.Scatter(
        x=pivot_fcast.index,
        y=pivot_fcast['max'],
        fill=None,
        mode=None,
        line_color='lightgray',
        showlegend=False
        ))
fcast_eu_fig.add_trace(
    go.Scatter(
        x=pivot_fcast.index,
        y=pivot_fcast['min'],
        fill='tonexty',
        mode=None,
        line_color='lightgray',
        showlegend=False))
fcast_eu_fig.add_trace(
    go.Scatter(x=pivot_fcast.index,
    y=pivot_fcast['10 year avg'],
    name='10 year avg',
    line=dict(color='black', width=4, dash='dot')))
# build traces for each
for i in range(-6, -3):
    fcast_eu_fig.add_trace(
        go.Scatter(
            x=pivot_fcast.index, 
            y=pivot_fcast.iloc[:,i], 
            name=pivot_fcast.columns[i], 
            line=dict(color=colors[i + 8], 
            width=4
            )))
# update layout, add title and axis labels
fcast_eu_fig.update_layout(
    title='EU gas storage 10yr range - pct full - forecast begins ' + str(gas_storage.index[-1].month) + '-' + str(gas_storage.index[-1].year),
    xaxis_title='month',
    yaxis_title='pct. of storage filled',
    template='plotly_white')
plot(fcast_eu_fig)