import pandas as pd
import pymongo
from pymongo import MongoClient
from os import listdir
from os.path import isfile, join
import datetime
import re
from indicadores_back import calcula_indicadores
from ta.trend import EMAIndicator, MACD
from ta.volume import OnBalanceVolumeIndicator
import gridfs
import itertools


def zip_with_scalar(lista, elemento1, elemento2):
    return list(zip(lista, itertools.repeat(elemento1), itertools.repeat(elemento2)))


def convert_binance_time(time):
    """
    Converte tempo da binance para datatime.
    :param time:
    :return:
    """
    return datetime.datetime.fromtimestamp(time / 1000)


def find_time(s):
    """Encontra tempo gráfico
    """
    result = re.search('T-(.*).json', s)
    return result.group(1)


def find_pair(diretorio, time, s):
    """Encontra tempo gráfico
    """
    result = re.search(f'{diretorio}/(.*)-{time}.json', s)
    return result.group(1)


def carrega_dados_mongo(diretorio: str):
    """
    Carrega dados no Mongodb
    :param diretorio: diretório para o qual foram extraídos dados
    :return:
    """
    # conexão com mongo
    client = MongoClient("mongodb://localhost:27017/")
    # cria database
    db = client["cripto"]
    # cria coleção
    moedas = db["moedas"]
    # lista de arquivos
    files = [diretorio + "/" + f for f in listdir(diretorio) if isfile(join(diretorio, f))]
    for file in files:
        df = pd.read_json(file)
        if df.shape[1] == 6:
            # nomeia colunas
            df.columns = ['Data', 'Open', 'High', 'Low', 'Close', 'Volume']
            # converte coluna de data
            df['Data'] = df['Data'].apply(convert_binance_time)
            # calcula HML
            df['HML'] = df['High'] - df['Low']
            # indicadores
            df = calcula_indicadores(df)
            # transforma dados para dicionário
            df_dict = df.to_dict("records")
            tempo_grafico = find_time(file)
            par = find_pair(diretorio, tempo_grafico, file)
            # insert no banco
            data_insert = {
                "Candles": df_dict,
                "Tempo": tempo_grafico,
                "Par": par,
                "_id": par + '_' + tempo_grafico
            }

            if tempo_grafico != '5m':
                moedas.insert_one(data_insert)

def carrega_dados_mongo_collection(diretorio: str):
    """
    Carrega dados no Mongodb
    :param diretorio: diretório para o qual foram extraídos dados
    :return:
    """
    # conexão com mongo
    client = MongoClient("mongodb://localhost:27017/")
    # cria database
    db = client["cripto_documents"]
    # cria coleção
    moedas = db["moedas"]
    # lista de arquivos
    files = [diretorio + "/" + f for f in listdir(diretorio) if isfile(join(diretorio, f))]
    for file in files:

        df = pd.read_json(file)
        if df.shape[1] == 6:
            tempo_grafico = find_time(file)
            if tempo_grafico != '5m':
                # nomeia colunas
                df.columns = ['Datetime', 'Open', 'High', 'Low', 'Close', 'Volume']
                # converte coluna de data
                df['Data'] = df['Datetime'].apply(convert_binance_time)
                # calcula HML
                df['HML'] = df['High'] - df['Low']
                # indicadores
                df = calcula_indicadores(df)

                par = find_pair(diretorio, tempo_grafico, file)
                # cria dicionário a partir dataframe
                df_list = df.to_dict("record")
                df_insert = [{
                             "Candle": element[0],
                              "Pares": element[1],
                              "Tempo": element[2]} for element in zip_with_scalar(df_list,
                                                                                  {'par':par.split('_'),
                                                                                   'inicio':df['Data'].min()},
                                                                                   {'tempo':tempo_grafico})]
                # insere dados no mongo
                moedas.insert_many(df_insert)

# def carrega_dados_mongo_collection(diretorio: str):
#     """
#     Carrega dados no Mongodb
#     :param diretorio: diretório para o qual foram extraídos dados
#     :return:
#     """
#     # conexão com mongo
#     client = MongoClient("mongodb://localhost:27017/")
#     # cria database
#     db = client["cripto_documents"]
#     # cria coleção
#     moedas = db["moedas"]
#     # lista de arquivos
#     files = [diretorio + "/" + f for f in listdir(diretorio) if isfile(join(diretorio, f))]
#     for file in files:
#
#         df = pd.read_json(file)
#         if df.shape[1] == 6:
#             tempo_grafico = find_time(file)
#             if tempo_grafico != '5m':
#
#                 # nomeia colunas
#                 df.columns = ['Datetime', 'Open', 'High', 'Low', 'Close', 'Volume']
#                 # converte coluna de data
#                 df['Data'] = df['Datetime'].apply(convert_binance_time)
#                 # calcula HML
#                 df['HML'] = df['High'] - df['Low']
#                 # indicadores
#                 df = calcula_indicadores(df)
#
#                 par = find_pair(diretorio, tempo_grafico, file)
#                 # insert no banco
#
#                 df_list = df.to_dict("record")
#                 df_insert = [{"Candle": element[0],
#                               "Par": element[1],
#                               "Tempo": element[2]} for element in zip_with_scalar(df_list, par, tempo_grafico)]
#                 moedas.insert_many(df_insert)
