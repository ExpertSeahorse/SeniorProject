"""
c. “Allowed” Threats represented as a table using host_exploit_threat_stats_complete.csv
"""
import pandas
import plotly.graph_objects as go

def build(threat_stats):
    # Sum all counts for a given month
    sum_action = threat_stats.groupby(['time', 'Action'], as_index=False, dropna=False)['count'].sum()

    # Move all required columns into a single DF and calculate any derived information
    cols = pandas.DataFrame()
    cols["date"] = sum_action['time']
    cols["allowed"] = sum_action[sum_action['Action']=="Blocked"]['count']

    # Merge the two tables
    data = {"date":[], "allowed":[]}
    for _, group in cols.groupby('date'):
        vals = group.values
        data['date'].append(vals[0][0])
        data['allowed'].append(vals[0][1])
    cols = pandas.DataFrame(data)
    
    # Generate the table
    fig = go.Table(
        header=dict(
            values=["Date","Allowed Threats"],
            fill_color='lightskyblue',
            align='center'
        ),
        cells=dict(
            values=[data['date'],data['allowed']],
            fill_color='lavender',
            align='center'
        )
    )

    layout = {
        'title': "Allowed Threats"
    }
    return [fig], layout