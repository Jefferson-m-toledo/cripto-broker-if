import dash
from dash import Dash, dcc, html, Input, Output
import plotly.graph_objects as go
import pandas as pd
from helpers import encontra_objeto_banco, set_color, encontra_colecao, indicadores
from plotly.subplots import make_subplots
import dash_bootstrap_components as dbc

app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

moedas = encontra_colecao()
tempos= moedas.distinct('Tempo')
par = moedas.distinct('Par')

title = html.H1('Cripto Broker', style={'textAlign': 'center'})

themes_list = [
    "BOOTSTRAP",
    "CYBORG",
    "DARKLY"]

dropdown = dcc.Dropdown(
    id="themes",
    options=[{"label": str(i), "value": i} for i in themes_list],
    value="BOOTSTRAP",
    clearable=False,
)

moedas_drop = dcc.Dropdown(
                par,
                id='par',
                value='BTC_USDT'
            )
tempo_drop = dcc.Dropdown(
                tempos,
                id='tempo',
                value='1d'
            )

indicadores_drop = dcc.Dropdown(indicadores,
            id='indicadores')

grafico = dcc.Graph(id="graph")

app.layout = dbc.Container(
    title,
    dbc.Row(
        dbc.Col([dropdown, moedas_drop, tempo_drop, indicadores_drop] ,width=0.2),
        dbc.Col([grafico],width=0.8)
    )

)



