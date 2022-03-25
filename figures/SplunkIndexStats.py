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
    data = pandas.DataFrame()
    data["date"] = sum_action['date']
    data["index"] = sum_action['index']
    data["count"] = sum_action['count']

    # data = {"date":[], "index":[], "count":[]}
    # for _, group in cols.groupby('date'):
    #     vals = group.values
    #     # print(vals)
    #     data['date'].append(vals[0][0])
    #     data['index'].append(vals[0][1])
    #     data['count'].append(vals[0][2])
    # cols = pandas.DataFrame(data)
    # print(cols)
    
    # fig = go.Figure(data=[go.Table(
    fig = go.Table(
        header=dict(
            values=["Date", "Index", "Count"],
            fill_color='lightskyblue',
            align='center'
        ),
        cells=dict(
            values=[data['date'],data['index'],data['count']],
            fill_color='lavender',
            align='center'
        )
    )
    # ])

    layout = {
        'width':500, 'height':400, 'title': "Stats per SIEM index"
    }
    # fig.update_layout(width=500, height=400)
    # fig.show()
    return [fig], layout