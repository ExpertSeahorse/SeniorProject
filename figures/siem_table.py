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

SIEM = pandas.read_csv(os.path.join(directory, 'allevents.stats.complete.csv'))
# print(SIEM)

def buildGraphs():
   
    fig = go.Figure([
        go.Table(
               header=dict(
                values=["date","index","count"],
                fill_color='paleturquoise',
                align='center'),
            cells=dict(values=[SIEM[i].tolist() for i in SIEM.columns[0:]],
                fill_color='lavender',
                align='center')       
        )
    ])
    return fig