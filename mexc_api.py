import requests
from dotenv import load_dotenv
import os
# Ваши API-ключи

a=0

# Загрузка переменных окружения из .env файла
load_dotenv()

# API ключи
COINGECKO_API_KEY = os.getenv('COINGECKO_API_KEY')
MEXC_API_KEY = os.getenv('MEXC_API_KEY')
MEXC_SECRET_KEY = os.getenv('MEXC_SECRET_KEY')

# URL для API CoinGecko
COINGECKO_URL = "https://api.coingecko.com/api/v3/coins/markets"

# URL для API MEXC
MEXC_TICKER_URL = "https://api.mexc.com/api/v3/ticker/price"
MEXC_EXCHANGE_INFO_URL = "https://api.mexc.com/api/v3/exchangeInfo"

def get_coingecko_prices(vs_currency='usd', limit=100):
    params = {
        'vs_currency': vs_currency,
        'order': 'market_cap_desc',
        'per_page': limit,
        'page': 1,
        'sparkline': False
    }
    headers = {
        'Accepts': 'application/json',
        'x-cg-demo-api-key': COINGECKO_API_KEY
    }
    response = requests.get(COINGECKO_URL, headers=headers, params=params)
    if response.status_code != 200:
        raise Exception(f"Error fetching data from CoinGecko: {response.text}")
    data = response.json()
    prices = {}
    for currency in data:
        symbol = currency['symbol'].upper()
        price = float(currency['current_price'])
        prices[symbol] = price
    return prices

def get_mexc_exchange_info():
    response = requests.get(MEXC_EXCHANGE_INFO_URL)
    if response.status_code != 200:
        raise Exception(f"Error fetching data from MEXC: {response.text}")
    data = response.json()
    symbols = [symbol['symbol'] for symbol in data['symbols']]
    return symbols

def get_mexc_price(symbol):
    params = {
        'symbol': symbol
    }
    response = requests.get(MEXC_TICKER_URL, params=params)
    if response.status_code != 200:
        raise Exception(f"Error fetching data from MEXC: {response.text}")
    data = response.json()
    try:
        price = float(data['price'])
    except (KeyError, ValueError):
        raise Exception("Invalid data format from MEXC")
    return price

def find_arbitrage_opportunities(threshold=0.10):
    try:
        coingecko_prices = get_coingecko_prices()
        mexc_symbols = get_mexc_exchange_info()

        for symbol in mexc_symbols:
            if symbol.endswith('USDT'):
                base_symbol = symbol[:-4]
                if base_symbol in coingecko_prices:
                    try:
                        coingecko_price = coingecko_prices[base_symbol]
                        mexc_price = get_mexc_price(symbol)

                        price_difference = abs(coingecko_price - mexc_price)
                        price_ratio = price_difference / min(coingecko_price, mexc_price)

                        if price_ratio >= threshold:
                            if coingecko_price > mexc_price:
                                profit_percentage = ((coingecko_price - mexc_price) / mexc_price) * 100
                                print(f"Arbitrage opportunity found: Buy on MEXC, Sell on CoinGecko")
                                print(f"Coin: {base_symbol}, MEXC Symbol: {symbol}")
                                print(f"CoinGecko Price: {coingecko_price}, MEXC Price: {mexc_price}")
                                print(f"Profit Percentage: {profit_percentage:.2f}%")
                            else:
                                profit_percentage = ((mexc_price - coingecko_price) / coingecko_price) * 100
                                print(f"Arbitrage opportunity found: Buy on CoinGecko, Sell on MEXC")
                                print(f"Coin: {base_symbol}, MEXC Symbol: {symbol}")
                                print(f"CoinGecko Price: {coingecko_price}, MEXC Price: {mexc_price}")
                                print(f"Profit Percentage: {profit_percentage:.2f}%")
                    except Exception as e:
                        print(f"Error processing token {base_symbol}: {e}")
            else:
                print(f"No USDT pair found for symbol {symbol}")

    except Exception as e:
        print(f"An error occurred: {e}")

# Пример использования
find_arbitrage_opportunities()
