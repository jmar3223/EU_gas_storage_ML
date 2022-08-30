# Forecasting degree days using SARIMA

# now that we:
    # concluded the statistical significance degree days has on storage flows
    # and through Linear Regression established a line of best fit that can be used to predict storage flows,
# we will now forecast degree days in order to predict future gas storage levels

import pandas as pd
import seaborn as sns
from establish_ML_model_linReg import temp_df_merged
import matplotlib.pyplot as plt
from statsmodels.tsa.seasonal import seasonal_decompose
import statsmodels.api as sm
from pandas.tseries.offsets import DateOffset


### Reviewing seasonality to determine usage of SARIMA model
# chart degree days over time
sns.lineplot(x='date', y='degree_days', data=temp_df_merged)
plt.xticks(rotation=45)
plt.show()

# Isolate and Analyze Trend, potential Seasonality, and Noise in degree days data
szn_dd = pd.DataFrame().assign(degree_days=temp_df_merged['degree_days'])
decompose_output = seasonal_decompose(szn_dd, model='additive', period=12)
decompose_output.plot()
plt.show()

# TREND:
    # no apparent trend in degree days
# SEASONALITY
    # is apparent in dataset, and statistically confirmed in new_establish_ML_model_linReg.py
# RESIDUAL
    # what's left over after stripping out seasonality and trend
    # shows statistical noise, shows randomness and/or periodic anomalies


### SARIMA modelling
import statsmodels.api as sm
sarima = sm.tsa.statespace.SARIMAX(szn_dd['degree_days'], order=(1,1,1), seasonal_order=(1,1,1,12))
results = sarima.fit()
szn_dd['forecast'] = results.predict(start=120, end=132, dynamic=False)
szn_dd[['degree_days', 'forecast']].plot(figsize=(12,8))
plt.show()

# create NaN df of future dates and concat to original df to use for forecasting
from pandas.tseries.offsets import DateOffset
pred_date = [szn_dd.index[-1] + DateOffset(months=x) for x in range(0,36)]
pred_date=pd.DataFrame(index=pred_date[1:], columns=szn_dd.columns)
szn_dd = pd.concat([szn_dd, pred_date])

# plot model - prediction vs. actual and forecast
szn_dd['forecast'] = results.predict(start=0, end=190)
plt.plot(szn_dd['degree_days'], label='actual')
plt.plot(szn_dd['forecast'], label='model')
plt.axvspan(temp_df_merged.index[-1], szn_dd.index[-1], alpha=0.5, color='lightgrey')
plt.title('Degree Days - Actual vs. Model')
plt.legend()
plt.show()

# model returns forecasted values similar to history, making us confident in the model's preditive ability
# now that degree days has been forecasted, time to feed it into the Linear Regression model (in establish_ML_model_linReg.py) to estimate net storage flows