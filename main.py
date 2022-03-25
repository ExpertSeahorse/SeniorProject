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
    [ CSVs["pan_allowed_traffic_stats_complete.csv"], CSVs["pan_blocked_traffic_stats_complete.csv"] ], # Network Traffic Stats
    [ CSVs['host_exploit_threat_stats_complete.csv'] ],                                                 # Network Threat Stats
    [ CSVs['host_exploit_threat_stats_complete.csv'] ],                                                 # Table Top count
    [ CSVs['host_exploit_threat_stats_complete.csv'] ],                                                 # Total network stats
    [ CSVs['allevents.stats.complete.csv'] ],                                                           # All Splunk Events
    [ CSVs['allevents.stats.complete.csv'] ],                                                           # Table Total stats for Splunk
    [ CSVs['allevents.stats.complete.csv'] ],                                                           # Stats per SIEM index
    [ CSVs['host_exploit_threat_stats_complete.csv'] ],                                                 # Host Exploit Detection Stats
    [ CSVs['host_exploit_threat_stats_complete.csv'] ],                                                 # Host Threat Quarantined Stats
    [  ],
]

# Build each graph and table and return a single plotly object
# TODO: Fix annotation, move over to each graph
# TODO: stack bar graphs
def buildGraphs(row, types):
    # Build Subplot Frame
    left, right = figs.get()[row]
    specs = [
        {"type": types[0]}, {"type": types[1]}
    ]
    if types[0] == 'xy':
        specs[0]['secondary_y'] = True
        # specs[0]['barmode'] = 'stack'
    if types[1] == 'xy':
        specs[1]['secondary_y'] = True
        # specs[1][
    
    fig = sp.make_subplots(
        rows=1, cols=2,
        subplot_titles=("Left", "Right"),
        row_heights=[0.6],
        specs=[specs]
    )

    # Fill each cell with a graph or table
    title_replace = {}
    for i in range(2):
        figlist = None,
        layout = None
        if i % 2 == 0:
            if left is not None:
                figlist, layout = left.build(*(CSVDirectory[2*row]))
                title_replace["Left"] = layout['title']
            else:
                title_replace["Left"]= ""
        else:
            if right is not None:
                figlist, layout = right.build(*(CSVDirectory[(2*row)+1]))
                title_replace["Right"]= layout['title']
            else:
                title_replace["Right"]= ""

        if figlist is not None and layout is not None:
            for j in range(len(figlist)):
                if layout.get('secondary_y'):
                    fig.add_trace(figlist[j], secondary_y=layout['secondary_y'][j], row=1, col=(1+i))
                else:
                    fig.add_trace(figlist[j], row=1, col=(1+i))
                
                # fig.update_layout(title_text=layout['title'], row=1, col=(1+i))
                # fig.update
    
    # Adjust the layout of the fig
    fig.update_layout(
        barmode='stack'
    )

    # Replace all placeholder titles with real ones
    # https://stackoverflow.com/questions/63220009/how-do-i-set-each-plotly-subplot-title-during-graph-creation-loop
    fig.for_each_annotation(lambda a: a.update(text = title_replace[a.text]))
    return fig
    

app = Dash()   #initialize dash app
app.layout = html.Div(id = 'parent', children = [
    html.H1(id = 'H1', children = 'Raymond James Dashboard', style = {'textAlign':'center', 'marginTop':40,'marginBottom':40}),
    # *graphs
    dcc.Graph(id = 'row1', figure = buildGraphs(0, ['xy','xy'])),
    dcc.Graph(id = 'row2', figure = buildGraphs(1, ['table','table'])),
    dcc.Graph(id = 'row3', figure = buildGraphs(2, ['xy','table'])),
    dcc.Graph(id = 'row4', figure = buildGraphs(3, ['table', 'xy'])),
    dcc.Graph(id = 'row5', figure = buildGraphs(4, ['xy', 'xy'])),
    # TODO: make a 2 col graph obj, maybe dont use build graphs
    # dcc.Graph(id = 'row6', figure = buildGraphs(5, [])),
])


if __name__ == '__main__': 
    app.run_server()