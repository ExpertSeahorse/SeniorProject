"""
pip install dash
pip install pandas
"""
"""
JUST A QUICK DEMO I SPUN UP WITH A SIMPLE TUTORIAL
"""
import dash
import dash_html_components as html
import dash_core_components as dcc
import plotly.graph_objects as go
import plotly.express as px


app = dash.Dash()   #initialising dash app
df = px.data.stocks() #reading stock price dataset 
print(df)
def stock_prices():
    # Function for creating line chart showing Google stock prices over time 
    fig = go.Figure([
        go.Scatter(
            x = df['date'], 
            y = df['GOOG'], 
            line = dict(color = 'firebrick', width = 4),
            name = 'Google'
        ),
        go.Scatter(
            x = df['date'],
            y = df['AAPL'],
            line = dict(color="fuchsia", width=4),
            name = "Apple"
        ),
        go.Bar(

            x = df['date'],
            y = df['AMZN'],
            marker_color="indigo",
            name="Amazon"
        ),
        go.Bar(

            x = df['date'],
            y = df['FB'],
            marker_color="cyan",
            name="Facebook"
        )
    ])
    fig.update_layout(title = 'Prices over time',
                      xaxis_title = 'Dates',
                      yaxis_title = 'Prices',
                      barmode='stack'
                      )
    return fig  

 
app.layout = html.Div(id = 'parent', children = [
    html.H1(id = 'H1', children = 'Example website', style = {'textAlign':'center', 'marginTop':40,'marginBottom':40}),
    dcc.Graph(id = 'line_plot', figure = stock_prices())    
])


if __name__ == '__main__': 
    app.run_server()