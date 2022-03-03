"""
Make sure you install python 3.6+ and run:
    pip install dash
    pip install pandas
before trying to run.
"""

from msilib import sequence
import os

import dash
from dash import html
from dash import dcc
import plotly.graph_objects as go
import plotly.express as px
import pandas
import numpy as np

directory = 'data'

# csvs = []
# for filename in os.listdir(directory):
#     csvs.append(pandas.read_csv(filename))

pan_allow = pandas.read_csv(os.path.join(directory, 'pan_allowed_traffic_stats_complete.csv'))
# print(pan_allow)
pan_block = pandas.read_csv(os.path.join(directory, 'pan_blocked_traffic_stats_complete.csv'))

def buildGraphs():
    # sum_allow = pan_allow.groupby('date', as_index=False).sum()
    # print(sum_allow)
    # sum_block = pan_block.groupby('date', as_index=False).sum()
    fig = go.Figure([
        go.Bar(
            name="Action=Allowed",
            x=pan_allow['date'],
            y=pan_allow['count'],
            marker_color="SkyBlue"
        ),
        go.Bar(
            name="Action=Blocked",
            x=pan_block['date'],
            y=pan_block['count'],
            marker_color="SteelBlue"
        )
    ])
    fig.update_layout(
        title = 'Network Traffic Stats​',
        xaxis_title = 'Dates',
        yaxis_title = 'Count',
        barmode='stack'
    )
    return fig
    

app = dash.Dash()   #initialising dash app
app.layout = html.Div(id = 'parent', children = [
    html.H1(id = 'H1', children = 'Raymond James Dashboard', style = {'textAlign':'center', 'marginTop':40,'marginBottom':40}),
    dcc.Graph(id = 'line_plot', figure = buildGraphs())    
])


if __name__ == '__main__': 
    app.run_server()