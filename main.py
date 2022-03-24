"""
Make sure you install python 3.6+ and run:
    pip install dash
    pip install pandas
before trying to run.
"""

import os

import dash
from dash import html
from dash import dcc
import pandas

# import graphs and table building functions
import figures.NetworkTrafficStats as nts1
import figures.NetworkThreatStats as nts2
import figures.AllowedThreats as at
import figures.TotalNetworkStats as tns
import figures.HostExploitDetectionStats as heds
import figures.SplunkIndexStats as sis

# Import csv files into memory
CSVs = {}
directory = 'data'
for filename in os.listdir(directory):
    CSVs[filename] = pandas.read_csv(os.path.join(directory, filename))

# Build each graph and table and return a single plotly object
def buildGraphs():
    # return nts1.build(CSVs["pan_allowed_traffic_stats_complete.csv"], CSVs["pan_blocked_traffic_stats_complete.csv"])
    # return nts2.build(CSVs['host_exploit_threat_stats_complete.csv'])
    # return at.build(CSVs['host_exploit_threat_stats_complete.csv'])
    return tns.build(CSVs['host_exploit_threat_stats_complete.csv'])
    

app = dash.Dash()   #initialising dash app
app.layout = html.Div(id = 'parent', children = [
    html.H1(id = 'H1', children = 'Raymond James Dashboard', style = {'textAlign':'center', 'marginTop':40,'marginBottom':40}),
    dcc.Graph(id = 'plot', figure = buildGraphs())    
])


if __name__ == '__main__': 
    app.run_server()