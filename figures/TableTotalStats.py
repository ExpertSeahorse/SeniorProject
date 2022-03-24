"""
SIEM graph and table data from the file 'allevents.stats.complete.csv'
"""

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

# SIEM = pandas.read_csv(os.path.join(directory, 'allevents.stats.complete.csv'))
# print(SIEM)
def build(SIEM):
    o= SIEM.groupby(['date'], as_index=False)['count'].sum()
    # fig = go.Figure([
    fig = go.Table(
        header=dict(
            values=["date","count"],
            fill_color='paleturquoise',
            align='center'
        ),
        cells=dict(
            values=[o['date'],o['count']],
            fill_color='lavender',
            align='center'
        )       
    )
    # ])
    layout = {
        'width':500, 'height':400
    }
    # fig.update_layout(width=500, height=400)
    # fig.show()
    return [fig], layout


# app = dash.Dash()   #initialising dash app
# app.layout = html.Div(id = 'parent', children = [
#     html.H1(id = 'H1', children = 'Raymond Jeff Dashboard', style = {'textAlign':'center', 'marginTop':40,'marginBottom':40}),
#     dcc.Graph( figure = buildGraphs())    
# ])


# if __name__ == '__main__': 
#     app.run_server()