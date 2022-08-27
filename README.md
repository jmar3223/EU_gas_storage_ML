# Analyzing EU Gas Storage Data

## Project Description
- Requests data through API provided by Gas Infrastructure Europe (GIE) from Aggregate Gas Storage Inventory (AGSI)
- Charts the seasonal percentage of EU's gas volumes in storage, updated daily
- Chart includes the 10-year min, max, average, and the most recent 5 year storage trend
- Storage capacity based on the region's total available underground storage facilities

Room for improvement:
- Enhance chart's x-axis by listing month-day, rather than the current day of year

To do:
- Forecast projected gas storage:
    - Establish optimal ML model
    - Feed model historic HDD, CDD, other demand variables
    - Feed model historic injection rate (supply)
    - Increase weight of injection rate variable to coincide with most recent supply trends  


## Sources
- Gas storage data for the EU, its member states, and the UK: https://agsi.gie.eu/
- Data definitions: https://agsi.gie.eu/data-definition
- See API Key Registration to get access to API docs


## API Key Registration
- API key redacted from code to prevent potential misuse (line 14 in europe_gas_storage.py)
- Register for free to get AGSI API docs and API key: https://agsi.gie.eu/account