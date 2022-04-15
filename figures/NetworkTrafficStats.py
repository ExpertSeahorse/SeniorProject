import pandas
import plotly.graph_objects as go
import plotly.subplots as sp
def build(pan_allow, pan_block):
    # Sum all counts for a given month
    sum_allow = pan_allow.groupby('date', as_index=False).sum()
    sum_block = pan_block.groupby('date', as_index=False).sum()

    # Move all required columns into a single DF and calculate any derived information
    cols = pandas.DataFrame()
    cols["date"] = sum_allow['date']
    cols["allow_ct"] = sum_allow['count']
    cols["block_ct"] = sum_block['count']
    cols["prcnt_block"] = cols['block_ct']/(cols['allow_ct']+cols['block_ct'])
    cols["trnd_block"] = cols['prcnt_block'].expanding().mean()

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
        ),
        go.Scatter(
            name="Avg Blocked",
            x=cols['date'],
            y=cols["trnd_block"],
            marker_color="Chartreuse"
        )
    ]
    layout = {
        'title': 'Network Traffic Stats​',
        'xaxis_title': 'Dates',
        'yaxis_title': 'Count',
        'y2axis_title': 'Percent',
        'secondary_y': [False, False, True, True]
    }
    # # Overlap all the subplots onto one plot
    # fig = sp.make_subplots(specs=[[{"secondary_y": True}]])
    # fig.add_trace(figlist[0], secondary_y=False)
    # fig.add_trace(figlist[1], secondary_y=False)
    # fig.add_trace(figlist[2], secondary_y=True)
    # fig.add_trace(figlist[3], secondary_y=True)
    
    # # Apply formatting
    # fig.update_layout(
    #     title = 'Network Traffic Stats​',
    #     xaxis_title = 'Dates',
    #     yaxis_title = 'Count',
    #     barmode='stack'
    # )
    return figlist, layout