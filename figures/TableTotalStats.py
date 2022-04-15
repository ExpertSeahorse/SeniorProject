"""
SIEM graph and table data from the file 'allevents.stats.complete.csv'
"""
import plotly.graph_objects as go

def build(SIEM):
    o= SIEM.groupby(['date'], as_index=False)['count'].sum()
    fig = go.Table(
        header=dict(
            values=["Date","Count"],
            fill_color='lightskyblue',
            align='center'
        ),
        cells=dict(
            values=[o['date'],o['count']],
            fill_color='lavender',
            align='center'
        )       
    )
    layout = {
        'width':500, 'height':400, 'title': "Total SIEM Stats"
    }
    return [fig], layout
