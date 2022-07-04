import pandas as pd
from ta.trend import EMAIndicator, MACD
from ta.volume import OnBalanceVolumeIndicator

def calcula_indicadores(df:pd.DataFrame):
    df['SMA10'] = df['Close'].rolling(window=10, min_periods=1).mean()
    df['SMA50'] = df['Close'].rolling(window=50, min_periods=1).mean()
    # bandas de bollinger
    df['sma'] = df['Close'].rolling(30).mean()
    df['bb_superior'] = df['sma'] + ((df['Close'].rolling(30).std(ddof=0)) * 2)
    df['bb_inferior'] = df['sma'] - ((df['Close'].rolling(30).std(ddof=0)) * 2)
    # médias móveis exponencias
    df['ema10'] = EMAIndicator(close=df['Close'], window=10).ema_indicator()
    df['ema50'] = EMAIndicator(close=df['Close'], window=50).ema_indicator()
    # OBV
    df['obv'] = OnBalanceVolumeIndicator(close=df['Close'], volume=df['Volume']).on_balance_volume()
    # MACD
    df['macd_sinal'] = MACD(close=df['Close']).macd_signal()
    df['macd'] = MACD(close=df['Close']).macd()
    return df