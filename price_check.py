from web3 import Web3
from uniswap import Uniswap


# Можно эту и другие подобные функции, можно перенести в фал core.price_check.py
# Функция для преобразования адреса в формат с контрольной суммой
def checksum_address(address):
    w3 = Web3()
    return w3.to_checksum_address(address)

# Адреса токенов
UNISWAP_V3_ROUTER_ADDRESS = "0xe592427a0aece92de3edee1f18e0157c05861564"  # Uniswap V3 router на Arbitrum
usdc = "0xaf88d065e77c8cC2239327C5EDb3A432268e5831"  # USDC токен на Arbitrum
weth = "0x82af49447d8a07e3bd95bd0d56f35241523fbab1"  # WETH на Arbitrum
arb = "0x912ce59144191c1204e64559fe8253a0e49e6548"   # Arbitrum токен на Arbitrum

# Подключение к сети Arbitrum
ARBITRUM_RPC_URL = "https://arb1.arbitrum.io/rpc"
web3 = Web3(Web3.HTTPProvider(ARBITRUM_RPC_URL))

# Преобразование адресов в формат с контрольной суммой
usdc = checksum_address(usdc)
weth = checksum_address(weth)
arb = checksum_address(arb)

# Настройка Uniswap SDK
uniswap = Uniswap(address=None, private_key=None, version=3, web3=web3)

# Функция для получения цены токена в WETH с учетом сборов
def get_price_in_usdc(token_address, fee=3000):
    price = uniswap.get_price_input(token_address, usdc, 10**18, fee=fee)  # Цена за 1 токен в USDC
    return price / (10**6)  # Возвращаем цену в виде float (USDC имеет 6 десятичных)

# Получение цен для ARB и WETH в эквиваленте USDC
try:
    arb_price_in_usdc = get_price_in_usdc(arb)
    weth_price_in_usdc = get_price_in_usdc(weth)
    usdc_price = 1  # Цена USDC в USDC равна 1

    # Вывод цен
    print(f"Цена ARB в эквиваленте USDC: {arb_price_in_usdc:.6f} USDC")
    print(f"Цена WETH в эквиваленте USDC: {weth_price_in_usdc:.6f} USDC")
    print("USDC: "+str(usdc_price))  # Цена USDC в USDC равна 1
except Exception as e:
    print(f"Ошибка при получении цен: {e}")