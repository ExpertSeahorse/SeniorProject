"""
SIEM graph data from the file 'allevents.stats.complete.csv'
"""

import pandas
import plotly.graph_objects as go


# csvs = []
# for filename in os.listdir(directory):
#     csvs.append(pandas.read_csv(filename))

# SIEM = pandas.read_csv(os.path.join(directory, 'allevents.stats.complete.csv'))
# print(SIEM)

def build(allStats):
    #sum_event = SIEM.groupby('date').sum()
    # print(sum_event)
    o= allStats.groupby(['date'], as_index=False)['count'].sum()
    #print(o)
    # fig = go.Figure([
    fig = go.Scatter(
        x = o['date'], 
        y = o['count'],
        #SIEM.groupby(['date'], as_index=False)['count'].sum(), 
        mode="lines",
        line = dict(color = 'SteelBlue', width = 4),
        name = 'SIEM'
    )
    # ])
    layout = {
        'title': 'All Splunk Events',
        'xaxis_title': 'Dates',
        'yaxis_title': 'Count',
        'showlegend': True,
        'newshape_line_dash': 'dot'
    }
    # fig.update_layout(
    #     title = 'All Splunk Events',
    #     xaxis_title = 'Dates',
    #     yaxis_title = 'Count',
    #     showlegend=True,
    #     newshape_line_dash='dot'
    # )
    return [fig], layout