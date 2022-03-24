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
def buildGraphs(row, types):
    left, right = figs.get()[row]
    specs = [
        {"type": types[0]}, {"type": types[1]}
    ]
    if types[0] == 'xy':
        specs[0]['secondary_y'] = True
    if types[1] == 'xy':
        specs[1]['secondary_y'] = True
        
    fig = sp.make_subplots(
        rows=1, cols=2,
        row_heights=[0.6],
        specs=[specs]
    )
    for i in range(2):
        if i % 2 == 0:
            figlist, layout = left.build(*(CSVDirectory[2*row]))
        else:
            print((2*row)+1)
            figlist, layout = right.build(*(CSVDirectory[(2*row)+1]))

        for j in range(len(figlist)):
            if layout.get('secondary_y'):
                fig.add_trace(figlist[j], secondary_y=layout['secondary_y'][j], row=1, col=(1+i))
            else:
                fig.add_trace(figlist[j], row=1, col=(1+i))

    # return nts1.build(CSVs["pan_allowed_traffic_stats_complete.csv"], CSVs["pan_blocked_traffic_stats_complete.csv"])
    # return nts2.build(CSVs['host_exploit_threat_stats_complete.csv'])
    # return at.build(CSVs['host_exploit_threat_stats_complete.csv'])
    # return tns.build(CSVs['host_exploit_threat_stats_complete.csv'])

    return fig
    

app = Dash()   #initialising dash app
# graphs = []
# for i in range(len(figs.get())):
#     graphs.append(dcc.Graph(id=f"row{i}", figure=buildGraphs(i)))

app.layout = html.Div(id = 'parent', children = [
    html.H1(id = 'H1', children = 'Raymond James Dashboard', style = {'textAlign':'center', 'marginTop':40,'marginBottom':40}),
    # *graphs
    dcc.Graph(id = 'row1', figure = buildGraphs(0, ['xy','xy'])),
    dcc.Graph(id = 'row2', figure = buildGraphs(1, ['table','table'])),
    # dcc.Graph(id = 'row3', figure = buildGraphs(2)),
    # dcc.Graph(id = 'row4', figure = buildGraphs(3)),
    # dcc.Graph(id = 'row5', figure = buildGraphs(4)),
    # dcc.Graph(id = 'row6', figure = buildGraphs(5)),
    # dcc.Graph(id = 'row7', figure = buildGraphs(6))
])


if __name__ == '__main__': 
    app.run_server()