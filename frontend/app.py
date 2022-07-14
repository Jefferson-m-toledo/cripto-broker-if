from dash import Dash, dcc, html, Input, Output
from helpers import encontra_objeto_banco, set_color, encontra_colecao, indicadores
from plotly.subplots import make_subplots
import dash_bootstrap_components as dbc
from dash_bootstrap_templates import load_figure_template
from indicadores_visuais import *


app = Dash(external_stylesheets=[dbc.themes.SLATE])
# CYBORG, DARKLY, SLATE, BOOTSTRAP


moedas = encontra_colecao()
tempos = moedas.distinct('Tempo')
par = moedas.distinct('Par')

templates = [
    "bootstrap",
    "darkly",
    "slate"
]

load_figure_template(templates)

app.layout = html.Div([
    html.H2('Crypto Broker', style={'textAlign': 'center'}),
    html.Br(),
    html.Div([
        html.Div([
            html.Div(["Tema",
                      dcc.Dropdown(templates, id='theme', value='slate', clearable=False)]),
            html.Br(),
            html.Br(), html.Br(),
            html.Br(),
            html.Div(["Tempo gráfico",
                      dcc.Dropdown(
                          tempos,
                          id='tempo',
                          value='1d',
                          clearable=False
                      )
                      ]),
            html.Br(),
            html.Div(["Par de moedas:",
                      dcc.Dropdown(
                          par,
                          id='par',
                          value='BTC_USDT',
                          clearable=False
                      )
                      ]),
            html.Br(),
            html.Div(['Indicador: ',
                      dcc.Dropdown(
                          indicadores,
                          id='indicadores',
                          value=None)
                      ]

                     )
        ], style={'width': '15%', 'padding': '0.5em', 'display': 'inline-block', 'float': 'left'}),
        html.Div([
            dcc.Graph(id="graph")
        ], style={'width': '80%', 'display': 'inline-block', 'padding': '0.5em'}),
    ])

])


@app.callback(
    Output("graph", "figure"),
    Input("theme", "value"),
    Input("tempo", "value"),
    Input("par", "value"),
    Input("indicadores", "value")
)
def display_candlestick(theme, tempo, par, indicadores):
    df = encontra_objeto_banco(index=f'{par}_{tempo}')
    media = df['Close'].mean()
    fig = make_subplots(rows=2, cols=1, shared_xaxes=True,
                        vertical_spacing=0.3, subplot_titles=(f'Preço (valor médio no período: {media:0.2f})',
                                                              'Volume' if indicadores not in ('MACD','Relative Strength Index - IFR') else ''),
                        row_width=[0.2, 0.9])

    # adiciona candles
    fig.add_trace(trace_candles(df), row=1, col=1)
    # adiciona volume
    if indicadores != 'MACD' and indicadores != 'Relative Strength Index - IFR':
        fig.add_trace(trace_volume(df),row=2, col=1 )
    # adiciona médias móveis simples
    if indicadores == 'Média Móvel Simples':
        fig.add_trace(trace_sma10(df))
        fig.add_trace(trace_sma50(df))
    # adiciona bandas de bollinger
    elif indicadores == 'Bandas de Bollinger':
        fig.add_trace(trace_bb(df)[0])
        fig.add_trace(trace_bb(df)[1])
        fig.add_trace(trace_bb(df)[2])
    # adiciona hml
    elif indicadores == 'HML':
        fig.add_trace(trace_hml(df))
    # adiciona ema
    elif indicadores == 'Média móvel exponencial':
        fig.add_trace(trace_ema10(df))
        fig.add_trace(trace_ema50(df))
    # adiciona obv
    elif indicadores == 'On-Balance Volume - OBV':
        fig.add_trace(trace_obv(df), row=2, col=1)
    # Adiciona MACD
    elif indicadores == 'MACD':
        fig.add_trace(trace_macd(df)[0], row=2, col=1)
        fig.add_trace(trace_macd(df)[1], row=2, col=1)
    # RSI
    elif indicadores == 'Relative Strength Index - IFR':
        fig.add_trace(trace_rsi(df), row=2, col=1)
        fig.add_hrect(
            y0=60, y1=100, line_width=0,
            fillcolor="blue", opacity=0.3, row=2, col=1)

    # fig.add_trace(go.Bar(x=df['Data'],
    #                      y=df['Volume'],
    #                      showlegend=False,
    #                      marker=dict(color=list(map(set_color, df['Close'] - df['Open'])))
    #                      )
    #               , row=2, col=1)

    # fig.update(layout_xaxis_rangeslider_visible=False)
    fig.update_layout(
        xaxis_rangeslider_visible=True,
        template=theme
    )

    return fig


app.run_server(debug=True)
