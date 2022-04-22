"""
Make sure you install python 3.6+ and run:
    pip install dash
    pip install pandas
before trying to run.
"""

from email import header
import os
import math, sys
from datetime import datetime
import pandas
import plotly.subplots as sp
from dash import Dash, html, dcc
from dash.dependencies import Input, Output

# import graphs and table building functions
import figures
from figures import TableForAllTotals

# Create Table and Graph themes
import plotly.graph_objects as go
import plotly.io as pio
lightmode = go.layout.Template()
lightmode.data.table = [go.Table(
    header={'fill_color': 'lightskyblue', 'align': 'center'},
    cells={'align': 'center'}
)]
pio.templates['mylight'] = lightmode
darkmode = go.layout.Template()
darkmode.data.table = [go.Table(
    header={'fill_color': 'SteelBlue', 'align': 'center'},
    cells={'align': 'center'}
)]
pio.templates['mydark'] = darkmode

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
        
        # Determine if year is already in years, or if next FY has arrived
        if date.strftime("%y") not in FYs:
            FYs.append(date.strftime("%y"))
        if int(date.strftime("%m")) in [10, 11, 12] and str(int(date.strftime("%y"))+1) not in FYs:
            FYs.append(str(int(date.strftime("%y"))+1))

        # Determine if quarter is already in quarters
        yr = date.strftime("%y")
        mo = date.strftime("%m")
        qnum = math.ceil(int(mo)/3)
        if qnum == 4:
            qnum = 1
            yr = str(int(yr)+1)
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
    [ CSVs['host_exploit_threat_stats_complete.csv'] ]
]

# Build each graph and table and return a single plotly object
def buildGraphs(row, types, ret='div'):
    # Get figlists and layouts for row
    fig_bases = figures.get()[row]

    # Fill each cell with a graph or table
    rowid = 'row'+str(row)
    figs = [None, None]
    children = [None, None]
    for i in range(2):
        if fig_bases[i] is not None:
            figlist, layout = fig_bases[i].build(*(CSVDirectory[(2*row)+i]))
            specs = {"type": types[i]}
            if types[i] == 'xy':
                specs['secondary_y'] = True

            fig = sp.make_subplots(
                specs=[[specs]]
            )
            fig.update_layout(
                barmode='stack',
                # template="plotly_dark+mydark"
                template="plotly+mylight"
            )   

            # Plot the figures from the figlist
            for j in range(len(figlist)):
                if layout.get('secondary_y'):
                    fig.add_trace(figlist[j], secondary_y=layout['secondary_y'][j])
                else:
                    fig.add_trace(figlist[j])
                
                # Add any formatting
                fig.update_layout(title_text=layout['title'])
                if layout.get('xaxis_title'):
                    fig.update_xaxes(title_text=layout['xaxis_title'], tickangle=45)
                if layout.get('yaxis_title'):
                    fig.update_yaxes(title_text=layout['yaxis_title'])
                if layout.get('y2axis_title'):
                    fig.update_yaxes(title_text=layout['y2axis_title'], tickformat=".0%", secondary_y=True, automargin=True)
                    fig.update_layout(legend={"x" : 1.05, "y" : 1})
                
            figs[i] = fig
            children[i] = html.Div(id=rowid+str(i), children=[
                dcc.Graph(id=rowid+str(i)+'g', figure=fig, responsive=True)
            ], style={'padding': 20, 'flex': 1})
        else:
            children[i] = html.Div(id=rowid+str(i), style={'padding': 20, 'flex': 1, 'width': '49%'})
    if ret == 'div':
        return html.Div(id=rowid, children=children, style={'display': 'flex', 'flex-direction': 'row', 'min-height': 300})
    else:
        return figs


def buildDropdowns():
    fy = html.Div(id="fydiv", children=[
        dcc.Dropdown(sorted(FYs, reverse=True), placeholder="Select a Fiscal Year", id="fy")
    ], style={'padding': 10, 'flex': 1})

    qtr = html.Div(id="qtrdiv", children=[
        dcc.Dropdown(sorted(QTRs, reverse=True), placeholder="Select a Quarter", id="qtr")
    ], style={'padding': 10, 'flex': 1})

    mon = html.Div(id="modiv", children=[
        dcc.Dropdown(sorted(MONs, reverse=True), placeholder="Select a Month", id="mo")
    ], style={'padding': 10, 'flex': 1})

    return html.Div(id="dates", children=[
        fy, qtr, mon
    ], style={'display': 'flex', 'flex-direction': 'row'})


def serve_layout():
    """Serving Dash the layout as a function makes it reload the graphs after each reload of the webpage, instead of after each reboot of the WSGI server"""
    return html.Div(id = 'parent', children = [
        buildDropdowns(),
        html.H1(id = 'H1', children = 'Raymond James Dashboard', style = {'textAlign':'center', 'marginTop':40,'marginBottom':40}),
        buildGraphs(0, ['xy','xy']),
        buildGraphs(1, ['table','table']),
        buildGraphs(2, ['xy','table']),
        buildGraphs(3, ['table', 'xy']),
        buildGraphs(4, ['xy', 'xy']),
        html.Div(id='bigtablediv', children=[
            dcc.Graph(id="bigtable", figure=TableForAllTotals.build(
                FYs, 
                CSVs['host_exploit_threat_stats_complete.csv'], 
                CSVs["pan_blocked_traffic_stats_complete.csv"], 
                CSVs['allevents.stats.complete.csv']
            ), responsive=True, style={'flex': 1})
        ], style={'display': 'flex', 'flex-direction': 'row'})
    ])
import dash_bootstrap_components as dbc

app = Dash(external_stylesheets=[dbc.themes.DARKLY])   #initialize dash app
app.layout = serve_layout

# # Update all the visuals according to the values in the dropdowns
@app.callback(
    Output(component_id='row00g', component_property='figure'),
    Output(component_id='row01g', component_property='figure'),
    Output(component_id='row10g', component_property='figure'),
    Output(component_id='row11g', component_property='figure'),
    Output(component_id='row20g', component_property='figure'),
    Output(component_id='row21g', component_property='figure'),
    Output(component_id='row30g', component_property='figure'),
    # Output(component_id='row31g', component_property='figure'),   # unused
    Output(component_id='row40g', component_property='figure'),
    Output(component_id='row41g', component_property='figure'),   
    Input (component_id="fy", component_property='value'),
    Input (component_id="qtr", component_property='value'),
    Input (component_id="mo", component_property='value'),
    prevent_initial_call=True
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
        [ filtered_CSVs['host_exploit_threat_stats_complete.csv'] ],
    ]

    ret = []
    ret += buildGraphs(0, ['xy','xy'], 'fig')
    ret += buildGraphs(1, ['table','table'], 'fig')
    ret += buildGraphs(2, ['xy','table'], 'fig')
    ret += buildGraphs(3, ['table', 'xy'], 'fig')
    ret += buildGraphs(4, ['xy', 'xy'], 'fig')
    ret = list(filter(None, ret))
    return ret


if __name__ == '__main__': 
    app.run_server()
