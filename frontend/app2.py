from dash import Dash, dcc, html, Input, Output
import plotly.graph_objects as go
import pandas as pd
from helpers import encontra_objeto_banco, set_color, encontra_colecao, indicadores
from plotly.subplots import make_subplots
import dash_bootstrap_components as dbc


app = Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

moedas = encontra_colecao()
tempos= moedas.distinct('Tempo')
par = moedas.distinct('Par')

app.layout = html.Div([
    html.H2('Cripto Broker', style={'textAlign': 'center'}),

    html.Div(
    [
        html.Div(["Tempo gráfico",
            dcc.Dropdown(
                tempos,
                id='tempo',
                value='1d'
            )
            ], style={'width': '20%', 'display': 'inline-block', 'padding':'0.5em'}),
        html.Div(["Par de moedas:",
            dcc.Dropdown(
                par,
                id='par',
                value='BTC_USDT'
            )
        ], style={'width': '20%', 'display': 'inline-block', 'float':'left', 'padding':'0.5em'})

        ]
    ),
    html.Div([

        html.Div(
        dcc.Graph(id="graph")
        ,style={'width': '80%', 'display': 'inline-block', 'padding':'0.5em'}),
        html.Div(
            dcc.Dropdown(
                indicadores,
                id='indicadores')
        ,style={'width': '15%', 'display': 'inline-block', 'float':'left','padding':'0.5em'}
        )

        ]
    )
])



@app.callback(
    Output("graph", "figure"),
    Input("tempo", "value"),
    Input("par", "value"),
)
def display_candlestick(tempo,par):
    df = encontra_objeto_banco(index=f'{par}_{tempo}')
    fig = make_subplots(rows=2, cols=1, shared_xaxes=True,
                        vertical_spacing=0.3, subplot_titles=('Preço', 'Volume'),
                        row_width=[0.2, 0.9])

    fig.add_trace(go.Candlestick(
        x=df['Data'],
        open=df['Open'],
        high=df['High'],
        low=df['Low'],
        close=df['Close']
    )  )

    fig.add_trace(go.Bar(x=df['Data'],
                         y=df['Volume'],
                         showlegend=False,
                         marker = dict(color=list(map(set_color, df['Close'] - df['Open'])))
                         )
                  , row=2, col=1)

    #fig.update(layout_xaxis_rangeslider_visible=False)
    fig.update_layout(
        xaxis_rangeslider_visible= True
    )

    return fig


app.run_server(debug=True)