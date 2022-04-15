"""
SIEM graph data from the file 'allevents.stats.complete.csv'
"""

import plotly.graph_objects as go


def build(allStats):
    o= allStats.groupby(['date'], as_index=False)['count'].sum()
    fig = go.Scatter(
        x = o['date'], 
        y = o['count'],
        mode="lines",
        line = dict(color = 'SteelBlue', width = 4),
        name = 'SIEM'
    )
    layout = {
        'title': 'All Splunk Events',
        'xaxis_title': 'Dates',
        'yaxis_title': 'Count',
        'showlegend': True,
        'newshape_line_dash': 'dot'
    }
    return [fig], layout