import os
import time
import json
import requests
import pandas as pd
from datetime import datetime
from websockets import connect

# Настройка путей
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
RAW_DATA_DIR = os.path.join(BASE_DIR, 'raw_data')
PROCESSED_DATA_DIR = os.path.join(BASE_DIR, 'processed_data')
BACKUP_DIR = os.path.join(BASE_DIR, 'backups')

# Создание директорий при необходимости
for directory in [RAW_DATA_DIR, PROCESSED_DATA_DIR, BACKUP_DIR]:
    os.makedirs(directory, exist_ok=True)


class HyperliquidDataCollector:
    def __init__(self, symbols=['ETH', 'BTC']):
        self.base_api_url = "https://api.hyperliquid.xyz"
        self.wss_url = "wss://api.hyperliquid.xyz/ws"
        self.symbols = symbols

    def get_orderbook(self, symbol):
        """Получение стакана ордеров через REST API"""
        endpoint = "/info"
        params = {'type': 'l2Book', 'symbol': symbol}

        try:
            response = requests.get(f"{self.base_api_url}{endpoint}", params=params)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"Error fetching orderbook: {e}")
            return None

    async def websocket_connection(self):
        """Подключение к WebSocket для получения данных в реальном времени"""
        async with connect(self.wss_url) as ws:
            # Подписка на данные (нужно уточнить формат для Hyperliquid)
            await ws.send(json.dumps({
                "method": "SUBSCRIBE",
                "params": [f"{symbol}@depth@100ms" for symbol in self.symbols],
                "id": 1
            }))

            while True:
                try:
                    data = await ws.recv()
                    self.save_raw_data(data, 'ws_data')

                    # Обработка данных в реальном времени
                    processed = self.process_ws_data(data)
                    if processed:
                        self.save_processed_data(processed)

                except Exception as e:
                    print(f"WebSocket error: {e}")
                    break

    def save_raw_data(self, data, data_type):
        """Сохранение сырых данных с временной меткой"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S%f")
        filename = f"{data_type}_{timestamp}.json"
        filepath = os.path.join(RAW_DATA_DIR, filename)

        with open(filepath, 'w') as f:
            json.dump(data, f)
        print(f"Saved raw data: {filename}")

    def process_ws_data(self, data):
        """Обработка данных WebSocket"""
        try:
            # Пример обработки данных (нужно адаптировать под структуру Hyperliquid)
            processed = {
                'timestamp': datetime.now().isoformat(),
                'symbol': data.get('s'),
                'bid': float(data.get('b')[0][0]),
                'ask': float(data.get('a')[0][0]),
                'bid_qty': float(data.get('b')[0][1]),
                'ask_qty': float(data.get('a')[0][1])
            }
            return processed
        except Exception as e:
            print(f"Error processing data: {e}")
            return None

    def save_processed_data(self, data):
        """Сохранение обработанных данных в CSV"""
        filename = f"processed_{datetime.now().strftime('%Y%m%d')}.csv"
        filepath = os.path.join(PROCESSED_DATA_DIR, filename)

        df = pd.DataFrame([data])
        if not os.path.exists(filepath):
            df.to_csv(filepath, index=False)
        else:
            df.to_csv(filepath, mode='a', header=False, index=False)

    def backup_data(self):
        """Создание резервных копий данных"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M")
        backup_name = f"backup_{timestamp}.zip"
        # Здесь можно реализовать архивирование данных
        # Например, с использованием библиотеки zipfile


if __name__ == "__main__":
    collector = HyperliquidDataCollector()

    # Пример периодического сбора данных через REST API
    while True:
        for symbol in collector.symbols:
            orderbook = collector.get_orderbook(symbol)
            if orderbook:
                collector.save_raw_data(orderbook, f"orderbook_{symbol}")
        time.sleep(60)  # Интервал сбора данных

    # Для WebSocket потребуется асинхронный запуск
    # import asyncio
    # asyncio.run(collector.websocket_connection())