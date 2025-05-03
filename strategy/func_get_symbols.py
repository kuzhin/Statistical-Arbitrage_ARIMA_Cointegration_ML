import requests
from config_strategy_api import session

# Get symbols that are tradeable

# def get_tradeable_symbols():
#
#     # Get available symbols
#     sym_list = []
#     symbols = session.query_symbol()
#     if "ret_msg" in symbols.keys():
#         if symbols["ret_msg"] == "OK":
#             symbols = symbols["result"]
#             for symbol in symbols:
#                 if symbol["quote_currency"] == "USDT" and symbol["status"] == "Trading": # symbol["maker_fee"]) < 0 removed as ByBit changed terms
#                     sym_list.append(symbol)
#
#     # Return ouput
#     return sym_list

def get_tradeable_symbols():
    """

    Return: Список всех токенов ( set{'LISTA', 'CFX'} )
    """

    # 1. Получаем все спотовые пары (там полный список базовых токенов)
    # Спот пары:
    spot_url = "https://api.bybit.com/v5/market/instruments-info?category=spot"
    # spot_data = requests.get(spot_url).json()
    # spot_base_coins = list({item["baseCoin"] for item in spot_data["result"]["list"]})

    # 2. Получаем фьючерсы (inverse + linear) с пагинацией
    futures_coins = set()

    for category in ["linear"]: # , "inverse" - предполагаю, что инверс не нужны (усложнение какое-то)
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
    return list(futures_coins)