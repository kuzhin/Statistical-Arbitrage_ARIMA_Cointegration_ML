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
        balance = session.get_wallet_balance(accountType="UNIFIED")
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
# place_order()

# session = HTTP(api_key=api_key, api_secret=api_secret)
# symbols_info = session.get_tickers()
# print(symbols_info)


# url = "https://api.bybit.com/v5/market/instruments-info?category=inverse"
# # Аналогичная обработка, как в примере выше.
# response = requests.get(url)
# data = response.json()

# if data['retCode'] == 0:
#     symbols = [symbol['name'] for symbol in data['result']['list']]
#     print("Спотовые символы:", symbols)
# else:
#     print("Ошибка:", data['retMsg'])
# if data['retCode'] == 0:
#     base_coins = [item['baseCoin'] for item in data['result']['list']]
#     print(base_coins)


def get_all_tokens():
    """

    Return: Список всех токенов ( set{'LISTA', 'CFX'} )
    """
    # 1. Получаем все спотовые пары (там полный список базовых токенов)
    spot_url = "https://api.bybit.com/v5/market/instruments-info?category=spot"

    # Спот пары:
    # spot_data = requests.get(spot_url).json()
    # spot_base_coins = list({item["baseCoin"] for item in spot_data["result"]["list"]})

    # 2. Получаем фьючерсы (inverse + linear) с пагинацией
    futures_coins = set()

    for category in ["linear", "inverse"]:
        cursor = None
        while True:
            url = f"https://api.bybit.com/v5/market/instruments-info?category={category}&limit=1000"
            if cursor:
                url += f"&cursor={cursor}"

            data = requests.get(url).json()
            if data["retCode"] != 0:
                break

            futures_coins.update({item["baseCoin"] for item in data["result"]["list"]})
            cursor = data["result"].get("nextPageCursor")
            if not cursor:
                break

    # Объединяем спот и фьючерсы, убираем дубли
    return futures_coins


# Запуск
all_tokens = get_all_tokens()
print(f"Всего токенов: {len(all_tokens)}")
print(all_tokens)