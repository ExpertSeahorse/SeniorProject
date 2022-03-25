import pandas
import plotly.graph_objects as go
import plotly.subplots as sp
import numpy as np
def build(threat_stats):
    # Sum all counts for a given month
    sum_action = threat_stats.groupby(['time', 'Action'], as_index=False, dropna=False)['count'].sum()
    # print(sum_action)

    # sum_block = pan_block.groupby('date', as_index=False).sum()

    # Move all required columns into a single DF and calculate any derived information
    cols = pandas.DataFrame()
    cols["date"] = sum_action['time']

    cols["allow_ct"] = sum_action[sum_action['Action']=="Blocked"]['count']
    cols["block_ct"] = sum_action[sum_action['Action']!="Blocked"]['count']

    data = {"date":[], "allow_ct":[], "block_ct":[]}
    for _, group in cols.groupby('date'):
        vals = group.values
        data['date'].append(vals[0][0])
        data['allow_ct'].append(vals[0][1])
        data['block_ct'].append(vals[1][2])
    cols = pandas.DataFrame(data)
    
    cols["prcnt_block"] = cols['block_ct']/(cols['allow_ct']+cols['block_ct'])
    # print(cols)

    # Create all subplots for the first graph
    figlist = [
        go.Bar(
            name="Action=Allowed",
            x=cols['date'],
            y=cols['allow_ct'],
            marker_color="SkyBlue"
        ),
        go.Bar(
            name="Action=Blocked",
            x=cols['date'],
            y=cols['block_ct'],
            marker_color="SteelBlue"
        ),
        go.Scatter(
            name="Percent Blocked",
            x=cols['date'],
            y=cols["prcnt_block"],
            marker_color="CornflowerBlue"
        )
    ]
    
    layout = {
        'title': 'Network Traffic Stats​',
        'xaxis_title': 'Dates',
        'yaxis_title': 'Count',
        'secondary_y': [False, False, True]
    }
    # Overlap all the subplots onto one plot
    # fig = sp.make_subplots(specs=[[{"secondary_y": True}]])
    # fig.add_trace(figlist[0], secondary_y=False)
    # fig.add_trace(figlist[1], secondary_y=False)
    # fig.add_trace(figlist[2], secondary_y=True)
    
    # # Apply formatting
    # fig.update_layout(
    #     title = 'Network Traffic Stats​',
    #     xaxis_title = 'Dates',
    #     yaxis_title = 'Count',
    #     barmode='stack'
    # )
    # return fig
    return figlist, layout

# if __name__ == "__main__":
#     build(pandas.read_csv(r"C:\Users\dtfel\OneDrive\Documents\School\Senior Project\SeniorProject\data\host_exploit_threat_stats_complete.csv"))