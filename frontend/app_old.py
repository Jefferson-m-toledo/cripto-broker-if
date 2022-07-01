from dash import Dash, dcc, html, Input, Output
import plotly.graph_objects as go
import pandas as pd
from object import encontra_objeto_banco


app = Dash(__name__)




app.layout = html.Div([
    html.H2('PB Cripto Broker', style={'textAlign': 'center'}),
    dcc.Checklist(
        id='toggle-rangeslider',
        options=[{'label': 'slider',
                  'value': 'slider'}],
        value=['slider']
    ),
    dcc.Graph(id="graph"),
])


@app.callback(
    Output("graph", "figure"),
    Input("toggle-rangeslider", "value"))
def display_candlestick(value):
    df = encontra_objeto_banco(index='AAVE_USDT_1d')

    fig = go.Figure(data=[go.Candlestick(
        x=df['Data'],
        open=df['Open'],
        high=df['High'],
        low=df['Low'],
        close=df['Close']
    )])

    fig.update_layout(
        xaxis_rangeslider_visible='slider' in value
    )

    return fig


app.run_server(debug=True)