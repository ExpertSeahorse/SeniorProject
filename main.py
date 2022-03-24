"""
Make sure you install python 3.6+ and run:
    pip install dash
    pip install pandas
before trying to run.
"""

import os
import pandas
import plotly.subplots as sp
from dash import Dash, html, dcc

# import graphs and table building functions
import figures as figs

# Import csv files into memory
CSVs = {}
directory = 'data'
for filename in os.listdir(directory):
    CSVs[filename] = pandas.read_csv(os.path.join(directory, filename))

CSVDirectory = [
    [ CSVs["pan_allowed_traffic_stats_complete.csv"], CSVs["pan_blocked_traffic_stats_complete.csv"] ], # nts1
    [ CSVs['host_exploit_threat_stats_complete.csv'] ],                                                 # nts2
    [ CSVs['host_exploit_threat_stats_complete.csv'] ],                                                 # at
    [ CSVs['host_exploit_threat_stats_complete.csv'] ],                                                 # tns
    [  ],
    [  ], 
    [  ],
    [  ],
    [  ],
]

# Build each graph and table and return a single plotly object
# TODO: Fix annotation, move over to each graph
# TODO: stack bar graphs
def buildGraphs(row):
    left, right = figs.get()[row]
    fig = sp.make_subplots(
        rows=1, cols=2,
        row_heights=[0.6],
        specs=[
            [{"secondary_y": True},{"secondary_y": True}],
        ]
    )
    figlist, layout = left.build(*(CSVDirectory[2*row]))
    for i in range(len(figlist)):
        fig.add_trace(figlist[i], secondary_y=layout['secondary_y'][i], row=1, col=1)

    figlist, layout = right.build(*CSVDirectory[(2*row)+1])
    for i in range(len(figlist)):
        fig.add_trace(figlist[i], secondary_y=layout['secondary_y'][i], row=1, col=2)

    # return nts1.build(CSVs["pan_allowed_traffic_stats_complete.csv"], CSVs["pan_blocked_traffic_stats_complete.csv"])
    # return nts2.build(CSVs['host_exploit_threat_stats_complete.csv'])
    # return at.build(CSVs['host_exploit_threat_stats_complete.csv'])
    # return tns.build(CSVs['host_exploit_threat_stats_complete.csv'])

    return fig
    

app = Dash()   #initialising dash app
app.layout = html.Div(id = 'parent', children = [
    html.H1(id = 'H1', children = 'Raymond James Dashboard', style = {'textAlign':'center', 'marginTop':40,'marginBottom':40}),
    dcc.Graph(id = 'row1', figure = buildGraphs(0)),
    # dcc.Graph(id = 'row2', figure = buildGraphs(1))
])


if __name__ == '__main__': 
    app.run_server()