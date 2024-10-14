from web3 import Web3
from uniswap import Uniswap


# Адреса контрактов и токенов

# Это swap router
UNISWAP_V3_ROUTER_ADDRESS = "0xe592427a0aece92de3edee1f18e0157c05861564"  # Uniswap V3 router on Arbitrum

# 0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48 с coingeko адресс usdc. Не понял. 2 разных адресса. +Еще один для USDC Bridge
# 0xaf88d065e77c8cC2239327C5EDb3A432268e5831
usdc = "0xaf88d065e77c8cC2239327C5EDb3A432268e5831"
weth = "0x82af49447d8a07e3bd95bd0d56f35241523fbab1"  # WETH on Arbitrum
arb = "0x912ce59144191c1204e64559fe8253a0e49e6548"   # Arbitrum token on Arbitrum
# 0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48

# TODO:
# web3.py only accepts checksum addresses
# ошибка
usdc = Web3.to_checksum_address("0xaf88d065e77c8cC2239327C5EDb3A432268e5831")

# Подключение к сети Arbitrum через публичный RPC (можно использовать свой)
ARBITRUM_RPC_URL = "https://arb1.arbitrum.io/rpc"
web3 = Web3(Web3.HTTPProvider(ARBITRUM_RPC_URL))

# Настройка Uniswap SDK
# Private key и адрес кошелька можно оставить пустыми, если только читаете данные
uniswap = Uniswap(address=None, private_key=None, version=3, web3=web3)

# Функция для получения цены токена в WETH
def get_price_in_weth(token_address):
    try:
        price = uniswap.get_price_input(token_address, weth, 10**18)  # Цена за 1 токен (18 decimals)
        return price / (10**18)  # Возвращаем цену в виде float
    except Exception as e:
        print(f"Ошибка получения цены для токена {token_address}: {e}")
        return None

# Получаем цены для USDC, WETH и ARB
usdc_price_in_weth = get_price_in_weth(usdc)
arb_price_in_weth = get_price_in_weth(arb)

print(f"Цена USDC в WETH: {usdc_price_in_weth}")
print(f"Цена ARB в WETH: {arb_price_in_weth}")