from pybit.unified_trading import HTTP
import dotenv
import requests
from dotenv import load_dotenv
# Загрузка конфигурации из .env файла
load_dotenv()
import os

# api_key = "1s1qfWTvpUOq7h66FL"
# api_secret = "VeKh5diCdoUFGTGIx4LbH7doaxAV3gkyKD5V"

api_key = os.getenv("API_KEY")
api_secret = os.getenv("API_SECRET")

def one():
    session = HTTP(
        api_key=api_key,
        api_secret=api_secret,
        demo=True
    )

    # Simple public endpoint test (no auth needed)
    print(session.get_orderbook(category="linear", symbol="BTCUSDT"))


    try:
        balance = session.get_wallet_balance(accountType="UNIFIED")  # <-- Typo here! Should be "UNIFIED"
        print("Balance:", balance)
    except Exception as e:
        print("Error:", e)

def place_order():
    # Пример размещения рыночного ордера на фьючерсы (USDT perpetual)
    session = HTTP(
        api_key=api_key,
        api_secret=api_secret,
        demo=True
    )
    order = session.place_order(
        category="linear",        # "linear" для USDT/USDC perpetual/futures
        symbol="BTCUSDT",         # торговая пара
        side="Buy",               # "Buy" или "Sell"
        orderType="Market",       # "Market" или "Limit"
        qty='0.01'                  # количество (например, 0.01 BTC)
    )
    print(order)
place_order()
