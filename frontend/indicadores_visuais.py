import pandas as pd
from indicadores import calcula_medias_moveis

def gera_visuais(df: pd.DataFrame):
    # grafico geral
    candlestick_set = {
        'x': df['Data'],
        'open': df['Open'],
        'high':  df['High'],
        'low': df['Low'],
        'close': df['Close']
    }
    # médias móveis
    sma1 = {
        'x': df['Data'],
        'open': df['Open'],
        'high': df['High'],
        'low': df['Low'],
        'close': df['Close']
    }
    return (candlestick_set)

