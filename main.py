


from connect_to_CEX import *
bybit_ticker = bybit.fetch_ticker('ART/USD')
print(print(bybit_ticker['close']))