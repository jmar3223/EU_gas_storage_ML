# Analyzing EU Gas Storage Data

## Project Description
- Requests data through API credentials from Aggregate Gas Storage Inventory (AGSI), provided by Gas Infrastructure Europe (GIE)
- Charts the seasonal percentage of EU's gas volumes in storage, updated daily
- Chart includes the 10-year min, max, average, and the most recent 5 year storage trend
- Storage capacity based on the region's total available underground storage facilities
- Will use Linear Regression + a time series forecasting model to forecast EU gas storage levels

Room for improvement:
- Enhance x-axis of the EU gas storage utilization seasonality chart by charting month-day, rather than the current day of year
- Request and automate degree days .csv dataretrival from degreedays.net
- Run multiple Linear Regression model to return potentially higher R^2 to forecast storage flows
	- potential features to add: daily production, net imports

To do:
- Forecast projected gas storage:
    - Forecast degree days as a time series likely using the SARIMA prediction model
    - Use line of best fit established from scikit-learn's LinearRegression fitting to predict net storage flows
    - Feed model historic injection rate (supply)
    - Increase weight of injection rate variable to coincide with most recent supply trends
- Build new seasonality chart and anlysis to visualize and discuss findings, limitations, etc.
- upload .ipynb files to display code output


## Storage Forecasting Methodology
- Confirmed the association between degree days and net storage flows is statistically significant
- Established the Linear Regression ML method as a likely candidate to forecast storage flows as a result
    - The Supervised Learning category is chosen given the structured and labeled dataset
    - Under the Supervised Learning umbrella, the Regression Model subcategory is chosen given the expected continuous data output
- We conclude The Linear Regression method is an accurate model to run after assessing the model's performance
- A line of best fit is found by running OLS between degree days and net gas storage flows
    - a significant R^2 and reasonable RMSE allows us to proceed with the forecasting


## Sources
- Gas storage data for the EU, its member states, and the UK: https://agsi.gie.eu/
- Data definitions: https://agsi.gie.eu/data-definition
- See API Key Registration to get access to API docs


## API Key Registration
- API key redacted from code to prevent potential misuse
- Register to get AGSI API docs and API key: https://agsi.gie.eu/account