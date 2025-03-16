import requests
import os
import time
from dotenv import load_dotenv

# Загружаем переменные окружения из файла .env
load_dotenv()


class HyperliquidAPI:
    def __init__(self):
        self.base_url = "https://api.hyperliquid.xyz"  # Проверьте актуальность URL в документации
        self.api_key = os.getenv("HYPERLIQUID_API_KEY")
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }

    def get_market_data(self, symbol=None):
        """
        Получение рыночных данных по конкретному символу или всех токенов
        """
        endpoint = "/info"  # Уточните правильный эндпоинт в документации
        url = self.base_url + endpoint

        params = {}
        if symbol:
            params['symbol'] = symbol

        try:
            response = requests.get(
                url,
                headers=self.headers,
                params=params,
                timeout=5
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Ошибка запроса: {e}")
            return None

    def get_order_book(self, symbol):
        """
        Пример получения стакана для конкретного токена
        """
        endpoint = "/orderbook"  # Уточните эндпоинт
        url = self.base_url + endpoint

        try:
            response = requests.get(
                url,
                headers=self.headers,
                params={'symbol': symbol},
                timeout=5
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Ошибка получения стакана: {e}")
            return None

    def get_account_info(self):
        """
        Получение информации об аккаунте (требует аутентификации)
        """
        endpoint = "/account"  # Уточните эндпоинт
        url = self.base_url + endpoint

        try:
            response = requests.get(
                url,
                headers=self.headers,
                timeout=5
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Ошибка получения данных аккаунта: {e}")
            return None


# Пример использования
if __name__ == "__main__":
    api = HyperliquidAPI()

    # Получаем данные по рынку
    market_data = api.get_market_data("BTC")
    if market_data:
        print("Рыночные данные:")
        print(market_data)

    # Получаем стакан
    order_book = api.get_order_book("BTC")
    if order_book:
        print("\nСтакан:")
        print(order_book)

    # Получаем информацию об аккаунте
    account_info = api.get_account_info()
    if account_info:
        print("\nИнформация об аккаунте:")
        print(account_info)