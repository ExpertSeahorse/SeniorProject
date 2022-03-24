"""
c. “Allowed” Threats represented as a table using host_exploit_threat_stats_complete.csv
"""
import pandas
import plotly.graph_objects as go
import plotly.subplots as sp
import numpy as np
def build(threat_stats):
    # Sum all counts for a given month
    sum_action = threat_stats.groupby(['time', 'Action'], as_index=False, dropna=False)['count'].sum()
    # print(sum_action)

    # Move all required columns into a single DF and calculate any derived information
    cols = pandas.DataFrame()
    cols["date"] = sum_action['time']

    cols["allowed"] = sum_action[sum_action['Action']=="Blocked"]['count']
    cols["blocked"] = sum_action[sum_action['Action']!="Blocked"]['count']

    data = {"date":[], "allowed":[], "blocked":[], "prcnt_block":[], "total":[]}
    for _, group in cols.groupby('date'):
        vals = group.values
        data['date'].append(vals[0][0])
        data['allowed'].append(vals[0][1])
        data['blocked'].append(vals[1][2])
        data['prcnt_block'].append((int)(vals[1][2]/(vals[0][1]+vals[1][2]) * 100))
        data['total'].append(vals[1][2]+vals[0][1])
    cols = pandas.DataFrame(data)
    # print(cols)
    
    # fig = go.Figure(data=[go.Table(
    fig = go.Table(
        header=dict(
            values=["Date", "Total", "Allowed","Blocked","Block Rate Percentage"],
            fill_color='paleturquoise',
            align='left'
        ),
        cells=dict(
            values=[data['date'],data['total'],data['allowed'],data['blocked'],data['prcnt_block']],
            fill_color='lavender',
            align='left'
        )
    )
    # ])

    layout = {
        'width':500, 'height':400
    }
    # fig.update_layout(width=500, height=400)
    # fig.show()
    return [fig], layout

if __name__ == "__main__":
    build(pandas.read_csv(r"C:\Users\dtfel\OneDrive\Documents\School\Senior Project\SeniorProject\data\host_exploit_threat_stats_complete.csv"))