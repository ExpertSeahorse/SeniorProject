import pandas
import plotly.graph_objects as go
import plotly.subplots as sp
def build(host_exploit):

    # Sum all counts for a given month
    HostAlertEvents = host_exploit.groupby(['time', 'EventName'], as_index=False, dropna=False)['count'].sum()

    # HostAlertEvents
    colsHostAlerts = pandas.DataFrame()
    colsHostAlerts["date"] = HostAlertEvents['time']
    colsHostAlerts["Events"] = HostAlertEvents[HostAlertEvents['EventName']!="null"]['count']
    
    data = {"date":[], "hostAlerts":[]}
    for _, group in colsHostAlerts.groupby('date'): # HostAlertEvents
        vals = group.values
        data['date'].append(vals[0][0])
        i = 0
        while(True):
            try:
                data['hostAlerts'].append(vals[i][1])
                i += 1
            except:
                break
                
    # Create all subplots for the first graph
    figlist = [
        go.Scatter(
            name="Quarantined Count",
            x=data['date'],
            y=data['hostAlerts'],
            marker_color="SkyBlue"
        )
    ]

    # Add quarantined trendline
    quarantined = host_exploit.groupby(['time', 'Status'], as_index=False, dropna=False)['count'].count()
    total = host_exploit.groupby(['time'], as_index=False)['count'].count()
    # print(quarantined[quarantined['time']=='2021-07'])
    # print(total)

    # Make table for graph
    cols = pandas.DataFrame()
    cols["time"] = quarantined['time']
    cols["quart"] = quarantined[quarantined['Status']=="Quarantined"]['count']
    cols = cols.dropna()
    cols = cols.merge(right=total, on="time")
    cols['avg'] = cols["quart"].expanding().mean()
    cols['avg2'] = cols["quart"]/cols['count']
    # print(cols)

    figlist = [
        go.Scatter(
            name="Quarantined Count",
            x=cols['time'],
            y=cols['quart'],
            marker_color="SkyBlue"
        )
    ]

    figlist.append(go.Scatter(
        name="Avg Quarantined",
        x=cols['time'],
        y=cols['avg'],
        marker_color="Chartreuse"
    ))

    layout= {
        'title': 'Host Threat Quarantined Stats',
        'xaxis_title': 'Dates',
        'yaxis_title': 'Count',
    }

    return figlist, layout