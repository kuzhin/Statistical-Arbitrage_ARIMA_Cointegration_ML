


from connect_to_CEX import *
bybit_ticker = bybit.fetch_ticker('ERYTS/USD')
print(print(bybit_ticker['close']))