import pandas as pd
from indicadores import calcula_medias_moveis
import plotly.graph_objects as go


def trace_candles(df: pd.DataFrame):
    candles = go.Candlestick(
        x=df['Data'],
        open=df['Open'],
        high=df['High'],
        low=df['Low'],
        close=df['Close'],
        name=None
    )
    return candles

def trace_sma10(df: pd.DataFrame):
    trace10 = go.Scatter(x=df['Data'],
                         y=df['SMA10'],
                         mode='lines',
                         name='Média Móvel Simples 10 períodos',
                         line={'color':'blue','width': 1})

    return trace10

def trace_sma50(df: pd.DataFrame):
    trace50 = go.Scatter(x=df['Data'],
                         y=df['SMA50'],
                         mode='lines',
                         name='Média Móvel Simples 50 períodos',
                         line={'color':'yellow','width': 1})

    return trace50

def trace_bb(df: pd.DataFrame):
    bb_sma = go.Scatter(x=df['Data'],
                             y=df['sma'],
                             mode='lines',
                             name=None,
                             line={'color': 'gray', 'width': 0.7})
    bb_superior = go.Scatter(x=df['Data'],
                         y=df['bb_superior'],
                         mode='lines',
                         name=None,
                         line={'color':'gray','width': 0.7})
    bb_inferior = go.Scatter(x=df['Data'],
                             y=df['bb_inferior'],
                             mode='lines',
                             name=None,
                             line={'color': 'gray', 'width': 0.7})

    return bb_sma, bb_inferior, bb_superior

def trace_hml(df:pd.DataFrame):
    hml = go.Scatter(x=df['Data'],
                             y=df['HML'],
                             mode='lines',
                             name=None,
                             line={'color': 'blue', 'width': 1})
    return hml
