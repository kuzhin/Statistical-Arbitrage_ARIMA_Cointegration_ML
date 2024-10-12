


from connect_to_CEX import *
bybit_ticker = bybit.fetch_ticker('FTT/USDT')
print(print(bybit_ticker['close']))