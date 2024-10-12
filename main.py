


from connect_to_CEX import *
bybit_ticker = bybit.fetch_ticker('FTT/USDC')
print(print(bybit_ticker['close']))