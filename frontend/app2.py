from dash import Dash, dcc, html, Input, Output
import plotly.graph_objects as go
import pandas as pd
from helpers import encontra_objeto_banco, set_color, encontra_colecao, indicadores
from plotly.subplots import make_subplots
import dash_bootstrap_components as dbc
from dash_bootstrap_templates import ThemeChangerAIO, template_from_url



app = Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

# CYBORG, DARKLY, SLATE, BOOTSTRAP

themes_list = [
    "BOOTSTRAP",
    "CYBORG",
    "DARKLY",
]

moedas = encontra_colecao()
tempos= moedas.distinct('Tempo')
par = moedas.distinct('Par')

app.layout = html.Div([
    html.H2('Cripto Broker', style={'textAlign': 'center'}),
    html.Div(dcc.Dropdown(
    id="themes",
    options=[{"label": str(i), "value": i} for i in themes_list],
    value="BOOTSTRAP",
    clearable=False,
)),
    html.Br(),
    html.Div([
        html.Div([
        html.Br(),
        html.Br(),html.Br(),
html.Br(),
        html.Div(["Tempo gráfico",
            dcc.Dropdown(
                tempos,
                id='tempo',
                value='1d'
            )
            ]),
        html.Br(),
        html.Div(["Par de moedas:",
            dcc.Dropdown(
                par,
                id='par',
                value='BTC_USDT'
            )
        ]),
        html.Br(),
            html.Div(['Indicador: ',
                dcc.Dropdown(
                    indicadores,
                    id='indicadores')
                ]

            )
        ], style={'width': '15%',  'padding': '0.5em','display': 'inline-block', 'float': 'left'}),
        html.Div([
            dcc.Graph(id="graph")
        ],style={'width': '80%', 'display': 'inline-block', 'padding':'0.5em'}),
    ])


,html.Div(id="blank_output")])

# app.clientside_callback(
#     """
#     function(theme) {
#         var stylesheet = document.querySelector('link[rel=stylesheet][href^="https://stackpath"]')
#         var name = theme.toLowerCase()
#         if (name === 'bootstrap') {
#             var link = 'https://stackpath.bootstrapcdn.com/bootstrap/4.5.0/css/bootstrap.min.css'
#           } else {
#             var link = "https://stackpath.bootstrapcdn.com/bootswatch/4.5.0/" + name + "/bootstrap.min.css"
#         }
#         stylesheet.href = link
#     }
#     """,
#     Output("blank_output", "children"),
#     Input("themes", "value"),
# )

@app.callback(
    Output("graph", "figure"),
    Input("themes", "value"),
    Input("tempo", "value"),
    Input("par", "value"),
    Input("indicadores", "value")
)
def display_candlestick(themes,tempo,par, indicadores):
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
        xaxis_rangeslider_visible= True,
        template = template_from_url(themes)
    )

    return fig


app.run_server(debug=True)