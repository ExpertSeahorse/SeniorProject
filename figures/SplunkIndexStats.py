"""
g. Stats for month/qtr/year per Splunk index represented as a table 
    using allevents.stats.complete.csv
fix: is not displaying all the indexes
"""

import pandas
import plotly.graph_objects as go

def build(splunk_stats):
    # Sum all counts for a given month
    sum_action = splunk_stats.groupby(['date', 'index'], as_index=False, dropna=False)['count'].sum()

    # Move all required columns into a single DF and calculate any derived information
    data = pandas.DataFrame()
    data["date"] = sum_action['date']
    data["index"] = sum_action['index']
    data["count"] = sum_action['count']
    data.sort_values(by=['date', 'count'], inplace=True, ascending=[True, False])

    # Create Table
    fig = go.Table(
        header=dict(
            values=["Date", "Index", "Count"]),
        cells=dict(
            values=[data['date'],data['index'],data['count']]
        )
    )

    layout = {
        'title': "Stats per SIEM index"
    }
    return [fig], layout