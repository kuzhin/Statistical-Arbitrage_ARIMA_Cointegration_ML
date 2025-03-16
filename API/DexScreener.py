import requests

DEXSCREENER_URL = "https://api.dexscreener.com/latest/dex/solana/pairs"

def get_dexscreener_prices(base_token_address, quote_token_address):
    params = {
        'tokens': f"{base_token_address},{quote_token_address}"
    }
    response = requests.get(DEXSCREENER_URL, params=params)
    if response.status_code != 200:
        raise Exception(f"Error fetching data from DEXScreener: {response.text}")
    data = response.json()
    prices = {}
    for pair in data.get("pairs", []):
        base_symbol = pair["baseToken"]["symbol"]
        quote_symbol = pair["quoteToken"]["symbol"]
        price_usd = float(pair["priceUsd"])
        prices[f"{base_symbol}/{quote_symbol}"] = price_usd
    return prices

# Пример использования
base_token_address = "So1qanlogcontractaddress"
quote_token_address = "So1qusdtcontractaddress"
dex_prices = get_dexscreener_prices(base_token_address, quote_token_address)
print(dex_prices)


