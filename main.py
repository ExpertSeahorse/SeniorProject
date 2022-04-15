"""
Make sure you install python 3.6+ and run:
    pip install dash
    pip install pandas
before trying to run.
"""

import os
import math
from datetime import datetime
import pandas
import plotly.subplots as sp
from dash import Dash, html, dcc
from dash.dependencies import Input, Output

# import graphs and table building functions
import figures as figs

FYs = []
QTRs = []
MONs = []
CSVs = {}
directory = 'data'
for filename in os.listdir(directory):
    # Import csv files into Pandas DataFrames
    csv = pandas.read_csv(os.path.join(directory, filename))
    CSVs[filename] = csv
    
    # Generate list of FYs, QTRs, and MONs
    if 'time' in csv.columns:
        dates = csv.time.unique()
    elif 'date' in csv.columns:
        dates = csv.date.unique()
    else:
        print("no 'date' or 'time' column to get dates")
        
    for d in dates:
        date = datetime.strptime(d, "%Y-%m")
        
        # Determine if year is already in years
        if date.strftime("%y") not in FYs:
            FYs.append(date.strftime("%y"))
        date.strftime('%m') 

        # Determine if quarter is already in quarters
        yr = date.strftime("%y")
        mo = date.strftime("%m")
        qnum = math.ceil(int(mo)/3)
        if qnum == 4:
            qnum = 1
        else:
            qnum += 1
        qtr = 'Y' + yr + 'Q' + str(qnum)
        if qtr not in QTRs:
            QTRs.append(qtr)

        # Determine if month is already in months
        if d not in MONs:
            MONs.append(d)

# Organize which CSVs will be needed for which visuals
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
def buildGraphs(row, types):
    # Build Subplot Frame
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
        subplot_titles=("Left", "Right"),
        row_heights=[0.6],
        specs=[specs]
    )

    # Fill each cell with a graph or table
    title_replace = {}
    for i in range(2):
        figlist = None,
        layout = None

        # build left and right visuals
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
            # Plot the figures in the figlist
            for j in range(len(figlist)):
                if layout.get('secondary_y'):
                    fig.add_trace(figlist[j], secondary_y=layout['secondary_y'][j], row=1, col=(1+i))
                else:
                    fig.add_trace(figlist[j], row=1, col=(1+i))
                
                # Add any formatting
                if layout.get('xaxis_title'):
                    fig.update_xaxes(title_text=layout['xaxis_title'], tickangle=45, row=1, col=1+i)
                if layout.get('yaxis_title'):
                    fig.update_yaxes(title_text=layout['yaxis_title'], row=1, col=1+i)
                if layout.get('y2axis_title'):
                    fig.update_yaxes(title_text=layout['y2axis_title'], tickformat=".0%", row=1, col=1+i, secondary_y=True)
                if layout.get('width'):
                    fig.update_layout
                if layout.get('height'):
                    fig.update_layout
    
    # Adjust the layout of the fig
    fig.update_layout(
        barmode='stack',
    )

    # Replace all placeholder titles with real ones
    # https://stackoverflow.com/questions/63220009/how-do-i-set-each-plotly-subplot-title-during-graph-creation-loop
    fig.for_each_annotation(lambda a: a.update(text = title_replace[a.text]))
    return fig


def buildDropdowns():
    fy = html.Div(id="fydiv", children=[
        dcc.Dropdown(sorted(FYs), placeholder="Select a Fiscal Year", id="fy")
    ], style={'padding': 10, 'flex': 1})

    qtr = html.Div(id="qtrdiv", children=[
        dcc.Dropdown(sorted(QTRs), placeholder="Select a Quarter", id="qtr")
    ], style={'padding': 10, 'flex': 1})

    mon = html.Div(id="modiv", children=[
        dcc.Dropdown(sorted(MONs), placeholder="Select a Month", id="mo")
    ], style={'padding': 10, 'flex': 1})

    return html.Div(id="dates", children=[
        fy, qtr, mon
    ], style={'display': 'flex', 'flex-direction': 'row'})


def serve_layout():
    """Serving Dash the layout as a function makes it reload the graphs after each reload of the webpage, instead of after each reboot of the WSGI server"""
    return html.Div(id = 'parent', children = [
        buildDropdowns(),
        html.H1(id = 'H1', children = 'Raymond James Dashboard', style = {'textAlign':'center', 'marginTop':40,'marginBottom':40}),
        dcc.Graph(id = 'row1', figure = buildGraphs(0, ['xy','xy'])),
        dcc.Graph(id = 'row2', figure = buildGraphs(1, ['table','table'])),
        dcc.Graph(id = 'row3', figure = buildGraphs(2, ['xy','table'])),
        dcc.Graph(id = 'row4', figure = buildGraphs(3, ['table', 'xy'])),
        dcc.Graph(id = 'row5', figure = buildGraphs(4, ['xy', 'xy'])),
        # TODO: make a 2 col graph obj, maybe dont build table as a subplot ==> in specs of subplot, use rowspan=2
        # dcc.Graph(id = 'row6', figure = buildGraphs(5, [])),
    ])

app = Dash()   #initialize dash app
app.layout = serve_layout

# Update all the visuals according to the values in the dropdowns
@app.callback(
    Output(component_id='row1', component_property='figure'),
    Output(component_id='row2', component_property='figure'),
    Output(component_id='row3', component_property='figure'),
    Output(component_id='row4', component_property='figure'),
    Output(component_id='row5', component_property='figure'),
    Input (component_id="fy", component_property='value'),
    Input (component_id="qtr", component_property='value'),
    Input (component_id="mo", component_property='value'),
)
def update_graphs(fy, qtr, mo):
    """Update graph values with dropdown filters"""
    filtered_CSVs = {}
    if fy:
        for name, df in CSVs.items():
            try:
                lfy = str(int(fy)-1)
                pattern = f'20{fy}-0[1-9]|20{lfy}-1[0-2]'
                # NOTE: we only have host exploit data for calander year 2021, so that is all that shows up when FY21 is selected
                filtered_CSVs[name] = df[df['time'].str.contains(pattern)]
            except KeyError:
                filtered_CSVs[name] = df[df['date'].str.contains(pattern)]

    elif qtr:
        for name, df in CSVs.items():
            # qtr = Y21Q1
            yr = qtr[1:3]
            ly = str(int(yr)-1)
            if qtr[4] == '1':
                pattern = f'20{ly}-1[0-2]'
            else:
                pattern = f'20{yr}-0['
                if qtr[4] == '2':
                    pattern += '1-3]'
                elif qtr[4] == '3':
                    pattern += '4-6]'
                elif qtr[4] == '4':
                    pattern += '7-9]'
            try:
                filtered_CSVs[name] = df[df['time'].str.contains(pattern)]
            except KeyError:
                filtered_CSVs[name] = df[df['date'].str.contains(pattern)]
    elif mo:
        for name, df in CSVs.items():
            try:
                filtered_CSVs[name] = df[df['time'].str.contains(str(mo))]
            except KeyError:
                filtered_CSVs[name] = df[df['date'].str.contains(str(mo))]
    else:
        filtered_CSVs = CSVs

    global CSVDirectory
    CSVDirectory = [
        [ filtered_CSVs["pan_allowed_traffic_stats_complete.csv"], filtered_CSVs["pan_blocked_traffic_stats_complete.csv"] ], # Network Traffic Stats
        [ filtered_CSVs['host_exploit_threat_stats_complete.csv'] ],                                                 # Network Threat Stats
        [ filtered_CSVs['host_exploit_threat_stats_complete.csv'] ],                                                 # Table Top count
        [ filtered_CSVs['host_exploit_threat_stats_complete.csv'] ],                                                 # Total network stats
        [ filtered_CSVs['allevents.stats.complete.csv'] ],                                                           # All Splunk Events
        [ filtered_CSVs['allevents.stats.complete.csv'] ],                                                           # Table Total stats for Splunk
        [ filtered_CSVs['allevents.stats.complete.csv'] ],                                                           # Stats per SIEM index
        [ filtered_CSVs['host_exploit_threat_stats_complete.csv'] ],                                                 # Host Exploit Detection Stats
        [ filtered_CSVs['host_exploit_threat_stats_complete.csv'] ],                                                 # Host Threat Quarantined Stats
        [  ],
    ]

    return (
        buildGraphs(0, ['xy','xy']),
        buildGraphs(1, ['table','table']),
        buildGraphs(2, ['xy','table']),
        buildGraphs(3, ['table', 'xy']),
        buildGraphs(4, ['xy', 'xy'])
    )

if __name__ == '__main__': 
    app.run_server()
