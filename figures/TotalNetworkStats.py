"""
c. “Allowed” Threats represented as a table using host_exploit_threat_stats_complete.csv
"""
import pandas
import plotly.graph_objects as go

def build(threat_stats):
    # Sum all counts for a given month
    sum_action = threat_stats.groupby(['time', 'Action'], as_index=False, dropna=False)['count'].sum()

    # Sort data into correct columns
    cols = pandas.DataFrame()
    cols["date"] = sum_action['time']
    cols["allowed"] = sum_action[sum_action['Action']=="Blocked"]['count']
    cols["blocked"] = sum_action[sum_action['Action']!="Blocked"]['count']

    # Merge rows and calculate derived information
    data = {"date":[], "allowed":[], "blocked":[], "prcnt_block":[], "total":[]}
    for _, group in cols.groupby('date'):
        vals = group.values
        data['date'].append(vals[0][0])
        data['allowed'].append(vals[0][1])
        data['blocked'].append(vals[1][2])
        data['prcnt_block'].append((int)(vals[1][2]/(vals[0][1]+vals[1][2]) * 100))
        data['total'].append(vals[1][2]+vals[0][1])
    cols = pandas.DataFrame(data)
    
    # Generate table
    fig = go.Table(
        header=dict(
            values=[
                "Date", 
                "Total", 
                "Allowed",
                "Blocked",
                "Block Rate Percentage"
            ],
            fill_color='lightskyblue',
            align='center'
        ),
        cells=dict(
            values=[
                data['date'],
                data['total'],
                data['allowed'],
                data['blocked'],
                data['prcnt_block']
            ],
            fill_color='lavender',
            align='center'
        )
    )

    layout = {
        'width':500, 'height':400, 'title': "Total Network Stats"
    }
    return [fig], layout