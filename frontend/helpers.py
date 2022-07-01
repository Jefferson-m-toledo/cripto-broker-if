from pymongo import MongoClient
import pandas as pd
from indicadores import *


def encontra_objeto_banco(index: str):
    # conexão com mongo
    client = MongoClient("mongodb://localhost:27017/")
    # cria database
    db = client["cripto"]
    # cria coleção
    moedas = db["moedas"]
    # ler dados do banco
    data_from_db = moedas.find_one({"_id": index})
    # cria dataframe pandas
    df = pd.DataFrame(data_from_db["Candles"])
    return df


def encontra_colecao():
    # conexão com mongo
    client = MongoClient("mongodb://localhost:27017/")
    # cria database
    db = client["cripto"]
    # cria coleção
    moedas = db["moedas"]
    return moedas


def set_color(x):
    if x<0:
        return "red"
    else:
        return "green"



indicadores = ['Média Móvel Simpes',
               'Média móvel exponencial',
               'On-Balance Volume - OBV',
                'Bandas de Bollinger',
                'Relative Strength Index - IFR',
                'MACD'
               ]

