"""
g. Stats for month/qtr/year per Splunk index represented as a table 
    using allevents.stats.complete.csv
fix: is not displaying all the indexes
"""

import pandas
import plotly.graph_objects as go
import plotly.subplots as sp
import numpy as np

def build(splunk_stats):
    # Sum all counts for a given month
    sum_action = splunk_stats.groupby(['date', 'index'], as_index=False, dropna=False)['count'].sum()
    # print(sum_action)

    # Move all required columns into a single DF and calculate any derived information
    cols = pandas.DataFrame()
    cols["date"] = sum_action['date']
    cols["index"] = sum_action['index']
    cols["count"] = sum_action['count']

    data = {"date":[], "index":[], "count":[]}
    for _, group in cols.groupby('date'):
        vals = group.values
        data['date'].append(vals[0][0])
        data['index'].append(vals[0][1])
        data['count'].append(vals[0][2])
    cols = pandas.DataFrame(data)
    
    # fig = go.Figure(data=[go.Table(
    fig = go.Table(
        header=dict(
            values=["Date", "Index", "Count"],
            fill_color='lightskyblue',
            align='left'
        ),
        cells=dict(
            values=[data['date'],data['index'],data['count']],
            fill_color='lavender',
            align='left'
        )
    )
    # ])

    layout = {
        'width':500, 'height':400
    }
    # fig.update_layout(width=500, height=400)
    # fig.show()
    return [fig], layout