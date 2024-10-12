from os import close
import ccxt
import requests

# Инициализация бирж
byb2 = ccxt.bybit()

# Получение инфы об активе на бирже
bybit_ticker = byb2.fetch_ticker('FTT/USDT') # dict

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

def get_bybit_order_book(cex_api_url, symbol):
    """
    Получение данных о ценах, объемах, ликвидности, комиссиях для Bybit

    :param cex_api_url: URL API Bybit
    :param symbol: Пара для получения ордеров, например 'BTCUSDT'
    :return: Данные ордербука в формате JSON
    """
    response = requests.get(f"{cex_api_url}/v2/public/orderBook/L2?symbol={symbol}")
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception("order error book")

# Пример использования
order_book = get_bybit_order_book('https://api.bybit.com', 'BTCUSDT')
print(order_book)
