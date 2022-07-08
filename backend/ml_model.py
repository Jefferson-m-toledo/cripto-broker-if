from pymongo import MongoClient
import pandas as pd
import tensorflow as tf
import datetime
import matplotlib.pyplot as plt
import numpy as np

def windowed_dataset(series, window_size, batch_size, shuffle_buffer):
    dataset = tf.data.Dataset.from_tensor_slices(series)
    dataset = dataset.window(window_size + 1, shift=1, drop_remainder=True)
    dataset = dataset.flat_map(lambda window: window.batch(window_size + 1))
    dataset = dataset.shuffle(shuffle_buffer).map(lambda window: (window[:-1], window[-1]))
    dataset = dataset.batch(batch_size).prefetch(1)
    return dataset

def treina_modelo_nn():
    client = MongoClient("mongodb://localhost:27017/")
    # cria database
    db = client["cripto"]
    # cria coleção
    moedas = db["moedas"]

    data_from_db = moedas.find_one({"_id": 'BTC_USDT_1h'})

    df = pd.DataFrame(data_from_db["Candles"])

    df['Mean'] = df['Close'].mean()
    df['Predict'] = df['Close'] / df['Mean']
    series = df["Predict"].to_numpy()
    split = 80
    split_time = int(len(series) * split / 100)
    # time = df['time'].to_numpy()
    time = np.array(range(0, df.shape[0]))
    time_train = time[:split_time]
    x_train = series[:split_time]
    time_valid = time[split_time:]
    x_valid = series[split_time:]
    #df.insert(0, 'time', range(0, df.shape[0]))
    window_size = 20
    batch_size = 32
    shuffle_buffer_size = 1000

    dataset = windowed_dataset(x_train, window_size, batch_size, shuffle_buffer_size)

    model = tf.keras.models.Sequential([
        tf.keras.layers.Dense(10, input_shape=[window_size], activation="relu"),
        tf.keras.layers.Dense(10, activation="relu"),
        tf.keras.layers.Dense(1)
    ])
    model.compile(loss='mse',
                  metrics=[tf.keras.metrics.RootMeanSquaredError()], optimizer='adam')
    model.fit(dataset, epochs=50, verbose=0)