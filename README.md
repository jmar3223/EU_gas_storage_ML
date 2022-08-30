# Analyzing EU Gas Storage Data

## Project Description
- Requests data through API credentials from Aggregate Gas Storage Inventory (AGSI), provided by Gas Infrastructure Europe (GIE)
- Charts the seasonal percentage of EU's gas volumes in storage, updated daily
- Chart includes the 10-year min, max, average, and the most recent 5 year storage trend
- Storage capacity based on the region's total available underground storage facilities
- Will use Linear Regression + a time series forecasting model to forecast EU gas storage levels

Room for improvement:
- Enhance x-axis of the EU gas storage utilization seasonality chart by charting month-day, rather than the current day of year
- Run multiple Linear Regression model to return potentially higher R^2 to forecast storage flows
	- potential features to add: daily production, net imports
- Run grid search on SARIMA model to find optimal hyperparameters

To do:
- Forecast projected gas storage:
    - Use line of best fit established from scikit-learn's LinearRegression fitting to predict net storage flows
    - Feed model historic injection rate (supply)
    - Increase weight of injection rate variable to coincide with most recent supply trends
- Build new seasonality chart and analysis to visualize and discuss findings, limitations, etc.
- upload .ipynb files to display code output
- Conduct gas storage scenario analysis based on historic min and max degree days


## Storage Forecasting Methodology
- Confirmed the association between degree days and net storage flows is statistically significant
- Established the Linear Regression ML method to forecast storage flows based on degree days
    - The Supervised Learning category is chosen given the structured and labeled dataset
    - Under the Supervised Learning umbrella, the Regression Model subcategory is chosen given the expected continuous data output
- We conclude The Linear Regression method is an accurate model to run after assessing the model's performance
- A line of best fit is found by running OLS between degree days and net gas storage flows
    - a significant R^2 and reasonable RMSE allows us to proceed with the forecasting
- Degree days is forecasted using the SARIMA model given its seasonal nature


## Sources
- Gas storage data for the EU, its member states, and the UK: https://agsi.gie.eu/
- Data definitions: https://agsi.gie.eu/data-definition
- See API Key Registration to get access to API docs


## API Key Registration
- API key redacted from code to prevent potential misuse
- Register to get AGSI API docs and API key: https://agsi.gie.eu/account