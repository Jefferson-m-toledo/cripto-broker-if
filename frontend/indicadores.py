import pandas as pd


def moving_average(df: pd.DataFrame, periods: int):
    df[f'avg_{periods}'] = df['Close'].rolling(window=20, min_periods=1).mean()
    return df[f'avg_{periods}']


def calcula_medias_moveis(df: pd.DataFrame):
    avg_20 = moving_average(df, periods=20)
    df['avg_20'] = avg_20

    avg_50 = moving_average(df, periods=50)
    df['avg_20'] = avg_50

    avg_100 = moving_average(df, periods=100)
    df['avg_20'] = avg_100

    return df