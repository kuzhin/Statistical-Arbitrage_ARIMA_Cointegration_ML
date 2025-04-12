import os
import requests
import csv
from datetime import datetime, timedelta

BYBIT_KLINE_URL = "https://api.bybit.com/v5/market/kline"
SYMBOL = "BTCUSDT"
INTERVAL = "1"  # 1 минута


def fetch_bybit_kline_data():
    # Рассчитываем временные метки
    end_time = datetime.now()
    start_time = end_time - timedelta(days=7)

    params = {
        'category': 'spot',
        'symbol': SYMBOL,
        'interval': INTERVAL,
        'start': int(start_time.timestamp() * 1000),  # в миллисекундах
        'end': int(end_time.timestamp() * 1000),
        'limit': 1000  # максимальное количество данных за один запрос
    }

    try:
        response = requests.get(BYBIT_KLINE_URL, params=params)
        response.raise_for_status()
        return response.json()['result']['list']
    except Exception as e:
        print(f"Ошибка получения данных: {str(e)}")
        return []


def save_kline_to_csv(data, filename='bybit_kline_1m.csv'):
    if not data:
        print("Нет данных для сохранения")
        return

    # Заголовки для CSV
    fieldnames = [
        'timestamp', 'open', 'high', 'low', 'close',
        'volume', 'turnover'
    ]

    with open(filename, mode='w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(fieldnames)

        for candle in data:
            # Преобразуем timestamp в читаемую дату
            timestamp = datetime.fromtimestamp(int(candle[0]) / 1000).strftime('%Y-%m-%d %H:%M:%S')
            row = [timestamp] + candle[1:]
            writer.writerow(row)

    print(f"Данные сохранены в {filename}")


# Пример использования
if __name__ == "__main__":
    kline_data = fetch_bybit_kline_data()
    if kline_data:
        save_kline_to_csv(kline_data)
        print(f"Получено {len(kline_data)} минутных свечей")