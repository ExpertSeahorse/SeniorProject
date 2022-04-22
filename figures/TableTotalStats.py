"""
SIEM graph and table data from the file 'allevents.stats.complete.csv'
"""
import plotly.graph_objects as go

def build(SIEM):
    o= SIEM.groupby(['date'], as_index=False)['count'].sum()
    fig = go.Table(
        header=dict(
            values=["Date","Count"],
        ),
        cells=dict(
            values=[o['date'],o['count']],
        )       
    )
    layout = {
        'title': "Total SIEM Stats"
    }
    return [fig], layout
