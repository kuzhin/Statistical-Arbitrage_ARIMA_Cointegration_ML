from web3 import Web3
from uniswap import Uniswap


# Функция для преобразования адреса в нужный формат
def checksum_address(address):
    w3 = Web3()
    return w3.to_checksum_address(address)

def price_check():
    """
    Итоговая функция для получения цен.

    :return: словарь цен "ARB/USDC": arb_price_in_usdc,"WETH/USDC": weth_price_in_usdc,"USDC/USDC": usdc_price
    """
    usdc = "0xaf88d065e77c8cC2239327C5EDb3A432268e5831"  # USDC токен на Arbitrum
    weth = "0x82af49447d8a07e3bd95bd0d56f35241523fbab1"  # WETH на Arbitrum
    arb = "0x912ce59144191c1204e64559fe8253a0e49e6548"  # Arbitrum токен на Arbitrum

    # Подключение к сети Arbitrum
    ARBITRUM_RPC_URL = "https://arb1.arbitrum.io/rpc"
    web3 = Web3(Web3.HTTPProvider(ARBITRUM_RPC_URL))

    # Преобразование адресов в формат с контрольной суммой
    usdc = checksum_address(usdc)
    weth = checksum_address(weth)
    arb = checksum_address(arb)

    # Настройка Uniswap SDK (Uniswap V3)
    uniswap = Uniswap(address=None, private_key=None, version=3, web3=web3)

    # Вспомогательная функция для получения цены токена в эквиваленте USDC
    def get_price_in_usdc(token_address, fee=3000):
        try:
            # Получаем цену за 1 токен в USDC (1 токен имеет 18 десятичных, поэтому умножаем на 10^18)
            price = uniswap.get_price_input(token_address, usdc, 10 ** 18, fee=fee)
            # Приводим результат к float, так как USDC имеет 6 десятичных
            return price / (10 ** 6)
        except Exception as e:
            print(f"Ошибка получения цены для {token_address}: {e}")
            return None

    # Получаем цены для ARB и WETH в USDC
    arb_price_in_usdc = get_price_in_usdc(arb)
    weth_price_in_usdc = get_price_in_usdc(weth)
    usdc_price = 1  # Цена USDC в USDC равна 1

    # Проверка на ошибки получения цен
    if arb_price_in_usdc is None or weth_price_in_usdc is None:
        print("Ошибка при получении данных для некоторых токенов.")
        return None

    arb_weth_price = arb_price_in_usdc / weth_price_in_usdc

    prices_dict = {
        "ARB/USDC": arb_price_in_usdc,
        "WETH/USDC": weth_price_in_usdc,
        "ARB/WETH": arb_weth_price
    }
    # Возвращаем цены в виде словаря
    return prices_dict

# Пример использования функции get_prices
prices = price_check()
print(prices, type(prices))