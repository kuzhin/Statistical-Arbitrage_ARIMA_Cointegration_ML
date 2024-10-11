from os import close

import ccxt

# Инициализация бирж
bybit = ccxt.bybit()

# Получение инфы об активе на бирже
bybit_ticker = bybit.fetch_ticker('FTT/USDT') # dict

"""
{'symbol': 'BTC/USDT', 'timestamp': None, 'datetime': None, 'high': 62316.0, 'low': 58941.85,
'bid': 62247.81, 'bidVolume': 1.245768, 'ask': 62247.82, 'askVolume': 0.206516,
 'vwap': 60523.360403494495, 'open': 60659.8, 'close': 62247.81, 'last': 62247.81,
  'previousClose': None, 'change': 1588.01, 'percentage': 2.62, 'average': 61453.8,
   'baseVolume': 18371.517403, 'quoteVolume': 1111905968.9408402, 'markPrice': None,
    'indexPrice': None, 'info': {'symbol': 'BTCUSDT', 'bid1Price': '62247.81', 
    'bid1Size': '1.245768', 'ask1Price': '62247.82', 'ask1Size': '0.206516', 'lastPrice': '62247.81', 'prevPrice24h': '60659.8', 'price24hPcnt': '0.0262', 'highPrice24h': '62316', 'lowPrice24h': '58941.85', 'turnover24h': '1111905968.9408402', 'volume24h': '18371.517403', 'usdIndexPrice': '62233.160752'}}
Price BTC/USDT = {'symbol': 'BTC/USDT', 'timestamp': None, 'datetime': None, 'high': 62316.0, 'low': 58941.85, 'bid': 62247.81, 'bidVolume': 1.245768, 'ask': 62247.82, 'askVolume': 0.206516, 'vwap': 60523.360403494495, 'open': 60659.8, 'close': 62247.81, 'last': 62247.81, 'previousClose': None, 'change': 1588.01, 'percentage': 2.62, 'average': 61453.8, 'baseVolume': 18371.517403, 'quoteVolume': 1111905968.9408402, 'markPrice': None, 'indexPrice': None, 'info': {'symbol': 'BTCUSDT', 'bid1Price': '62247.81', 'bid1Size': '1.245768', 'ask1Price': '62247.82', 'ask1Size': '0.206516', 'lastPrice': '62247.81', 'prevPrice24h': '60659.8', 'price24hPcnt': '0.0262', 'highPrice24h': '62316', 'lowPrice24h': '58941.85', 'turnover24h': '1111905968.9408402', 'volume24h': '18371.517403', 'usdIndexPrice': '62233.160752'}}

<class 'dict'>
"""

print(bybit_ticker['close'])

# print('Price BTC/USDT = {0}'.format(str(bybit_ticker)))