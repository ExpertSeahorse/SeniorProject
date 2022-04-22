"""
    Table Total stats for month/qtr/FY SIEM/Network Traffic and Threats/Host Alerts (takes up two columns)
"""
import pandas
import numpy as np
import math, statistics
import plotly.graph_objects as go


def constrainTable(df, fy) -> pandas.DataFrame:
    """Return only the rows in the year from the dataframe"""
    try:
        lfy = str(int(fy)-1)
        pattern = f'20{fy}-0[1-9]|20{lfy}-1[0-2]'
        return df[df['time'].str.contains(pattern)]
    except KeyError:
        return df[df['date'].str.contains(pattern)]


def build(fiscal_years, threat_stats, pan, allEvents):
    # Consolidate all tables around month and required columns
    grouped_dfs = [
        pan.groupby(['date'], as_index=False, dropna=False)['count'].sum(),                           # NetworkTraffic
        threat_stats.groupby(['time', 'Action'], as_index=False, dropna=False)['count'].sum(),                  # NetworkThreats
        allEvents.groupby(['date'], as_index=False, dropna=False)['count'].sum(),                               # SIEM_Events
        threat_stats.groupby(['time', 'Action', 'Status'], as_index=False, dropna=False)['count'].sum(),        # HostAlertEvents
    ]   

    # initialize data dict
    data = {"Type": [
        "Blocked Network Traffic",  # blocked only
        "Network Threats",          # allowed or blocked
        "SIEM Events",              # total, all index's
        "Host Alerts"               # action=blocked or status=quarantined
    ]}
    data['20'+str(fiscal_years[0])+" Total"] = (len(data["Type"]))*[np.nan]     # No growth for first year
    for i in range(1, len(fiscal_years)):
        fy = fiscal_years[i]
        data['20'+str(fy)+" Total"] = (len(data["Type"]))*[np.nan]
        data['20'+str(fy)+" Growth"] = (len(data["Type"]))*[np.nan]

    data.pop('20'+str(fiscal_years[i])+" Growth")
    data['20'+str(fiscal_years[i])+" Projected Growth"] = (len(data["Type"]))*[np.nan]
    data['Annualized Growth'] = (len(data["Type"]))*[np.nan]


    growths = [[], [], [], []]
    for j, fy in enumerate(fiscal_years):
        # Get all totals for the year
        for i, raw_df in enumerate(grouped_dfs):
            df = constrainTable(raw_df, fy)
            if not df.empty:
                if i == 0:
                    data['20'+str(fy)+" Total"][i] = df['count'].sum()
                elif i == 1:
                    data['20'+str(fy)+" Total"][i] = df['count'].sum()
                elif i == 2:
                    data['20'+str(fy)+" Total"][i] = df['count'].sum()
                elif i == 3:
                    quart = df.loc[df['Status']=='Quarantined', 'count'].sum()
                    block = df.loc[df['Action']=='Blocked', 'count'].sum()
                    data['20'+str(fy)+" Total"][i] = int(quart) + int(block)

        # Get all Growth amounts
        if 0 < j and j < len(fiscal_years)-1:
            for i in range(len(grouped_dfs)):
                present = data['20'+str(fy)+" Total"][i]
                past = data['20'+str(int(fy)-1)+" Total"][i]
                if past != 0:
                    growth = (present - past) / past
                    growths[i].append(growth)
                    data['20'+str(fy)+" Growth"][i] = growth
    
    # Get projected growth
    for i, row in enumerate(growths):            
        if len(row) != 0:
            data['20'+str(fy)+" Projected Growth"][i] = statistics.mean(row)
        else:
            data['20'+str(fy)+" Projected Growth"][i] = np.nan

    # Get annualized growth params
    max_year = max(list(map(int, fiscal_years))) 
    CAGRs = []
    for _ in range(len(grouped_dfs)):
        CAGRs.append([np.nan, np.nan, 0])
    for i, raw_df in enumerate(grouped_dfs):
        for j, fy in enumerate(fiscal_years):
            if str(fy) == str(max_year):
                continue
            
            amnt = data['20'+str(fy)+" Total"][i]
            if amnt != np.nan:
                CAGRs[i][1] = amnt
                if math.isnan(CAGRs[i][0]):
                    CAGRs[i][0] = amnt
                else:
                    CAGRs[i][2] += 1
    
    # Calculate the CAGR
    for i, row in enumerate(CAGRs):
        if row[2] > 0:
            cagr = ( (row[1]/row[0])**(1/row[2]) ) - 1
            data['Annualized Growth'][i] = cagr      
        
    # Consolidate all data into a dataframe
    cols = pandas.DataFrame(data)

    # Convert all decimals to percentages
    values = []
    for col in cols.transpose().values.tolist():
        if type(col[0]) == str:
            values.append(col)
            continue
        values.append(list(map(
            lambda x: "{0:.2f}%".format(x * 100) if abs(float(x)) < 1 else str(x), col
        )))

    fig = go.Table(
        header=dict(values=list(cols.columns)),
        cells=dict(values=values)
    )
    layout = {
        "title": "Table For All Totals"
    }

    return [fig], layout