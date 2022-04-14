from get_stock_data import get_stock_data
from transform_to_csv import transform_to_csv
import os
import dash
from dash import dcc
from dash import html
import pandas as pd
import plotly.graph_objs as go

from dash.dependencies import Input, Output

"""
link: https://github.com/plotly/simple-example-chart-apps/tree/master/dash-timeseriesplot
"""

get_stock_data()
transform_to_csv()

app = dash.Dash(__name__)
server = app.server
app.config.suppress_callback_exceptions = True
data_folder = "./data/"

df = pd.read_csv(data_folder + 'all_stocks.csv')
df['Date'] = pd.to_datetime(df.Date, infer_datetime_format=True)

if 'DYNO' in os.environ:
    app_name = os.environ['DASH_APP_NAME']
else:
    app_name = 'dash-timeseriesplot'

app.layout = html.Div([html.H1("Stock Prices", style={'textAlign': 'center'}),
    dcc.Dropdown(id='my-dropdown',options=[{'label': 'Amazon', 'value': 'AMZN'},{'label': 'Google', 'value': 'GOOGL'},{'label': 'Facebook', 'value': 'FB'},{'label': 'Netflix', 'value': 'NFLX'}],
        multi=True,value=['AMZN'],style={"display": "block","margin-left": "auto","margin-right": "auto","width": "60%"}),
    dcc.Graph(id='my-graph')
], className="container")


@app.callback(Output('my-graph', 'figure'),
              [Input('my-dropdown', 'value')])
def update_graph(selected_dropdown_value):
    dropdown = {"AMZN": "Amazon","GOOGL": "Google","FB": "Facebook","NFLX": "Netflix"}
    trace1 = []
    trace2 = []
    for stock in selected_dropdown_value:
        trace1.append(go.Scatter(x=df[df["Stock"] == stock]["Date"],y=df[df["Stock"] == stock]["Open"],mode='lines',
            opacity=0.7,name=f'Open {dropdown[stock]}',textposition='bottom center'))
        trace2.append(go.Scatter(x=df[df["Stock"] == stock]["Date"],y=df[df["Stock"] == stock]["Close"],mode='lines',
            opacity=0.6,name=f'Close {dropdown[stock]}',textposition='bottom center'))
    traces = [trace1, trace2]
    data = [val for sublist in traces for val in sublist]
    figure = {'data': data,
        'layout': go.Layout(colorway=['#fcbe32', '#004e66', '#fcbe32', '#6f2108', '#274c5e', '#dae9f4','#fdc23e', '#ff7761'],
            height=600,title=f"Opening and Closing Prices for {', '.join(str(dropdown[i]) for i in selected_dropdown_value)} Over Time",
            xaxis={"title":"Date",
                   'rangeselector': {'buttons': list([{'count': 1, 'label': '1M', 'step': 'month', 'stepmode': 'backward'},
                                                      {'count': 6, 'label': '6M', 'step': 'month', 'stepmode': 'backward'},
                                                      {'step': 'all'}])},
                   'rangeslider': {'visible': True}, 'type': 'date'},yaxis={"title":"Price (USD)"})}
    return figure

@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname is None or pathname.replace(app_name, '').strip('/') == '':
        return main.layout
    else:
        return code.layout

if __name__ == '__main__':
    app.run_server(debug=False)
