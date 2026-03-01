import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

from func_get_symbols import get_tradeable_symbols
from func_cointegration import get_cointegrated_pairs
import json

from func_price_klines import get_price_klines
# Store price histry for all available pairs

def store_price_history(symbols):
    """
    Получает исторические данные цен для списка токенов и сохраняет в JSON

    Args:
        symbols: Множество базовых токенов (в формате: {'BTC', 'ETH', 'SOL', ...})
    """
    # Преобразуем токены в торговые пары (добавляем USDT)
    trading_pairs = [f"{token}USDT" for token in symbols]

    # Get prices and store in DataFrame
    counts = 0
    price_history_dict = {}
    for pair in trading_pairs:
        price_history = get_price_klines(pair)  # Используем готовую функцию get_price_klines

        if len(price_history) > 0:
            price_history_dict[pair] = price_history
            counts += 1
            print(f"{counts} {pair} stored")
        else:
            print(f"{pair} not stored")

    # Output prices to JSON
    if len(price_history_dict) > 0:
        with open("1_price_list.json", "w") as fp:
            json.dump(price_history_dict, fp, indent=4)
        print("Prices saved successfully.")

    # Return output
    return

"""STRATEGY CODE"""
if __name__ == "__main__":

    # STEP 1 - Get list of symbols
    print("Getting symbols...")

    pass
    # Уже загружено 25 монет.

    sym_response = get_tradeable_symbols(include_spot=False, include_linear=True, max_tokens=25)

    # STEP 2 - Construct and save price history
    print("Constructing and saving price data to JSON...")
    if len(sym_response) > 0:
        store_price_history(sym_response)
    pass

    # STEP 3 - Find Cointegrated pairs
    print("Calculating co-integration...")
    with open("1_price_list.json") as json_file:
        price_data = json.load(json_file)
        if len(price_data) > 0:
            coint_pairs = get_cointegrated_pairs(price_data)
