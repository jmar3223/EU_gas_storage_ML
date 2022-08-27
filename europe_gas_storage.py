# Daily EU gas storage, injection, withdrawal starting 01/01/2011

import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import datetime as dt
import requests
import plotly.graph_objects as go
from plotly.offline import plot


url = 'https://agsi.gie.eu/api?'
api = 'xxxxxxxxxx'
headers = {'x-key': api}

# params for url
query_dict = {
    'continent': 'eu',
 #   'country': 'de',
 #   'from': '2022-08-24',
 #   'to': '2022-01-01',
    'size': 300
}

# request data first to pull total number of pages (data['last_page']) during loop iteration
response = requests.get(url, params=query_dict, headers=headers)
data = response.json()


### Iterate over as many pages as params (query_dict) pulls, unless pages > 55
gas = []

for page in range(1, data['last_page']+1):
    # break if last page > 55
    if data['last_page'] > 55:
        print('---increase size param, limit range, or specify a date range to avoid API blacklist---')
        break
    
    print('----')
    last_page = page + 1

    url = f'https://agsi.gie.eu/api?&page={page}'
    response = requests.get(url, params=query_dict, headers=headers)
    print('total pages is', data['last_page'], 'currently requesting page', last_page - 1, 'and url: ', response.url)
    data = response.json()

    # append next page of data to list
    gas.extend(data['data'])



### Create and Clean DataFrame

df = pd.DataFrame(gas).sort_values(by='gasDayStart')
# drop unecessary columns
df = df.drop(['url', 'consumption', 'consumptionFull', 'info'], axis=1)
# convert all columns in cols from object to numeric
cols = df.columns.drop(['name', 'code', 'gasDayStart', 'status'])
df[cols] = df[cols].apply(pd.to_numeric)
# convert date to datetime type
df['gasDayStart'] = df['gasDayStart'].astype('datetime64[ns]')
# add net storage flow column
df['net storage flow'] = df['injection'] - df['withdrawal']
# add year and month-day columns for charting and analysis
df['year'] = df['gasDayStart'].dt.year
df['month_day'] = df['gasDayStart'].dt.strftime('%m-%d')



### Seasonality Chart: % of gas storage full

# columns to get latest 10 years - used for sumary stats in pivot table
last_ten_years = slice(df['year'].iat[-1] - 9, df['year'].iat[-1])

# set up pivot table
pivot_full = pd.pivot_table(df, values='full', index=['month_day'], columns=['year'], aggfunc=np.sum)
# drop leap year
pivot_full = pivot_full.drop(pivot_full.index[59])
# add summary statistics columns
pivot_full['max'] = pivot_full.loc[:, last_ten_years].max(axis=1)
pivot_full['min'] = pivot_full.loc[:, last_ten_years].min(axis=1)
pivot_full['10 year avg'] = pivot_full.loc[:, last_ten_years].mean(axis=1)





# establish figure, list of figure colors
full_eu_fig = go.Figure()
colors = ['#17becf','#e377c2','#ff7f0e','#2ca02c','darkblue','firebrick']
# build traces for 3 summary stats, fixing params to visualize max vs. min range band
# room for improvement: list month-day on x axis vs. currently showing day of year
full_eu_fig.add_trace(
    go.Scatter(
        x=np.arange(1,366),
        y=pivot_full['max'],
        fill=None,
        mode=None,
        line_color='lightgray',
        showlegend=False
        ))
full_eu_fig.add_trace(
    go.Scatter(
        x=np.arange(1,366),
        y=pivot_full['min'],
        fill='tonexty',
        mode=None,
        line_color='lightgray',
        showlegend=False))
full_eu_fig.add_trace(
    go.Scatter(x=np.arange(1,366),
    y=pivot_full['10 year avg'],
    name='10 year avg',
    line=dict(color='black', width=4, dash='dot')))
# build traces for each of past 5 years
for i in range(-8, -3):
    full_eu_fig.add_trace(
        go.Scatter(
            x=np.arange(1,366), 
            y=pivot_full.iloc[:,i], 
            name=pivot_full.columns[i], 
            line=dict(color=colors[i + 8], 
            width=4
            )))
# update layout, add axis labels
full_eu_fig.update_layout(
    title='EU gas storage - pct full as of: '+ data['gas_day'],
    xaxis_title='day of year',
    yaxis_title='pct. of storage filled',
    template='plotly_white')
plot(full_eu_fig)