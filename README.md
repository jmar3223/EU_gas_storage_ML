# Analyzing and Forecasting EU Natural Gas Storage Levels

## Project Description
- Requests data through API credentials from Aggregate Gas Storage Inventory (AGSI), provided by Gas Infrastructure Europe (GIE)
- Charts the seasonal percentage of EU's gas volumes in storage, updated daily
    - Includes the 10-year min, max, average, and the most recent 5 year storage trend
- Storage capacity based on the region's total available underground storage facilities
- Forecasts and charts EU gas storage levels based on established models:
    - Supervised ML model Linear Regression to confirm statistical relationship strength between variables
    - SARIMA model to forecast degree days

Room for improvement:
- Enhance x-axis of historic EU gas storage utilization seasonality chart by charting month-day
- Run a multiple Linear Regression model to return potentially higher R^2 to forecast storage flows
	- potential features to add: daily production, net imports
- Run grid search on SARIMA model to find optimal hyperparameters

To do:
- Upload .ipynb files to display code output (charts, statistics, summaries etc.)
- Conduct gas storage scenario analysis based on:
    - historic min and max degree days
    - potential supply disruptions (primarily Nordstream 1 flow levels)


## EU Gas Storage Forecasting Methodology
1. Choosing the ML model
- Confirmed the association between degree days and net storage flows is statistically significant
- Established the Linear Regression ML method to forecast storage flows based on degree days
    - The Supervised Learning category is chosen given the structured and labeled dataset
    - Under the Supervised Learning umbrella, the Regression Model subcategory is chosen given the expected continuous data output
- We conclude The Linear Regression method is an accurate model to run after assessing the model's performance
- A line of best fit is found by running OLS between degree days and net gas storage flows
    - a significant R^2 and reasonable RMSE allows us to proceed with the forecasting

2. Choosing the time series forecasting model
- Confirmed the statistical significance of the response vs. explanatory variable
- Run time series seasonal decomposition of explanatory variable Degree Days to guage potential trend and seasonality
- Establish the SARIMA model given the data's inherent seasonal nature

3. Forecasting gas storage levels
- Interpolate the SARIMA model's output (forecasted degree days) with the optimized Linear Regression equation to forecast net gas storage flows
- Add monthly forecasted net gas storage flows to prior month's value
- Append historic (monthly) gas storage data with forecasted data


## Model Limitations (list not exhaustive)
- Gas storage forecast does not take into account any supply variables
    - Though the R^2 of the demand variable (degree days) returned 84%, supply uncertainties could reduce the relationship's statistical strength in the future
- SARIMA model hyperparameters not yet optimized
- Degree Days data based on German weather history through December 2021
    - Lack of available data on a continental-aggregated level


## Sources
- Gas storage data for the EU, its member states, and the UK: https://agsi.gie.eu/
- Data definitions: https://agsi.gie.eu/data-definition
- See API Key Registration to get access to AGSI's API docs
- Degree Days derived from historic temperature data, retrieved from https://climateknowledgeportal.worldbank.org/download-data


## AGSI API Key Registration
- API key redacted from script to prevent potential misuse
- Register to get AGSI API docs and API key: https://agsi.gie.eu/account