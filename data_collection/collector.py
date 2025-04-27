import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import ccxt
import pickle




# 1. Загрузка данных
pairs = ['XLM/USDT', 'SOL/USDT', 'ONDO/USDT', 'ETC/USDT',
         'BNB/USDT', 'ADA/USDT','XRP/USDT', 'TRX/USDT',
         'SUI/USDT']


def load_all_pairs(pairs, timeframe, limit):
    """Загружает данные для всех пар и возвращает словарь DataFrame"""
    exchange = ccxt.bybit()
    data = {}
    for pair in pairs:
        try:
            data[pair] = load_pair_data(exchange, pair, timeframe, limit)
        except Exception as e:
            print(f"Ошибка загрузки {pair}: {str(e)}")
    print('Загружены данные со всех пар')
    return data


def load_pair_data(exchange, pair, timeframe, limit):
    """Загружает OHLCV данные для одной пары"""
    data = exchange.fetch_ohlcv(pair, timeframe, limit=limit)
    df = pd.DataFrame(data, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
    df.set_index('timestamp', inplace=True)
    df['close'] = df['close'].astype(float)

    # 3. Сохранение данных для будущего использования
    # with open('data.pkl', 'wb') as f:
    #     pickle.dump(df, f)

    return df
