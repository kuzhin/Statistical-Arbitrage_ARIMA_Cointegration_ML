"""
Базовый скрипт для наполнения TimescaleDB данными с Bybit (упрощенная версия)
Требования: psycopg2, requests, python-dotenv
"""

import os
import requests
import psycopg2
from datetime import datetime
from dotenv import load_dotenv

# 1. Загрузка конфигурации
load_dotenv()
DB_CONFIG = {
    'dbname': os.getenv('DB_NAME'),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'host': os.getenv('DB_HOST')
}

BYBIT_API_URL = "https://api.bybit.com/v5/market/tickers"
SYMBOL_FILTER = "BTCUSDT,ETHUSDT"

# 2. Функция для получения данных с Bybit (исправлено)
def fetch_bybit_data():
    params = {'category': 'spot', 'symbol': SYMBOL_FILTER}
    try:
        response = requests.get(BYBIT_API_URL, params=params)
        response.raise_for_status()
        return response.json()['result']['list']
    except Exception as e:
        print(f"Ошибка получения данных: {str(e)}")
        return []

# 3. Работа с таблицей tokens (базовая версия)
def get_or_create_token(conn, symbol, exchange):
    with conn.cursor() as cursor:
        # Условные метаданные
        blockchain = 'Bitcoin' if symbol == 'BTC' else 'Ethereum'
        contract_address = None

        cursor.execute("""
            INSERT INTO tokens (symbol, exchange, blockchain, contract_address)
            VALUES (%s, %s, %s, %s)
            ON CONFLICT (symbol, exchange) DO UPDATE SET
                blockchain = EXCLUDED.blockchain,
                contract_address = EXCLUDED.contract_address
            RETURNING token_id
        """, (symbol, exchange, blockchain, contract_address))

        return cursor.fetchone()[0]

# 4. Вставка данных в price_history (исправлено)
def insert_price_data(conn, token_id, price, timestamp):
    with conn.cursor() as cursor:
        cursor.execute("""
            INSERT INTO price_history (token_id, price, timestamp)
            VALUES (%s, %s, %s)
            ON CONFLICT DO NOTHING
        """, (token_id, price, timestamp))

# 5. Основной процесс
def main():
    conn = psycopg2.connect(**DB_CONFIG)

    for ticker in fetch_bybit_data():
        symbol = ticker['symbol'].replace('USDT', '')  # Базовая обработка символа

        try:
            # Получение/создание токена
            token_id = get_or_create_token(conn, symbol=symbol, exchange='Bybit')

            # Вставка цены
            insert_price_data(
                conn,
                token_id=token_id,
                price=float(ticker['lastPrice']),
                timestamp=datetime.utcnow()  # Используем UTC время
            )
        except KeyError as e:
            print(f"Ошибка в структуре данных: {str(e)}")
            continue

    conn.commit()
    conn.close()

if __name__ == "__main__":
    main()