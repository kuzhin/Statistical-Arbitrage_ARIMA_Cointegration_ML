import os
import psycopg2
import time
from tqdm import tqdm
import ccxt
from dotenv import load_dotenv
from datetime import datetime, timedelta, timezone
# Задаём дату начала (например, 1 августа 2021)
start_date = datetime(2021, 8, 1)
since_timestamp = int(start_date.timestamp() * 1000)  # Умножаем на 1000 для миллисекунд
print(since_timestamp)  # Выведет: 1627776000000

# Загрузка конфигурации из .env файла
load_dotenv()

# Конфигурация базы данных
DB_CONFIG = {
    'dbname': os.getenv('DB_NAME'),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'host': os.getenv('DB_HOST'),
    'port': os.getenv('DB_PORT', '5432')
}

# Список криптовалютных пар (в формате Bybit: BTCUSDT)
list_top_10 = ['BTCUSDT', 'ETHUSDT', 'SOLUSDT', 'TRXUSDT', 'MNTUSDT',
               'DOGEUSDT', 'TONUSDT', 'SUIUSDT', 'ADAUSDT', 'AVAXUSDT']
start_date = datetime(2021, 8, 1)
BATCH_SIZE = 200  # Уменьшенный размер батча для надежности

def init_bybit_client():
    """Инициализация клиента Bybit через CCXT"""
    return ccxt.bybit({
        'enableRateLimit': True,
        'options': {
            'defaultType': 'spot',
            'adjustForTimeDifference': True,
        },
    })
client = init_bybit_client()

def get_ohlcv_with_limits(client, symbol, timeframe, since, limit):
    try:
        # Делаем запрос
        data = client.fetch_ohlcv(symbol, timeframe, since, limit)

        # Получаем лимиты из последних заголовков
        limits = {
            'limit_1m': client.last_response_headers.get('x-ratelimit-limit-1m'),
            'remaining_1m': client.last_response_headers.get('x-ratelimit-remaining-1m'),
            'reset_time': client.last_response_headers.get('x-ratelimit-reset')
        }
        return data, limits
    except ccxt.BaseError as e:
        print(f"Ошибка: {e}")
        return None, None

print(f"Remaining: {client.last_response_headers['x-ratelimit-remaining-1m']}/120")
# Использование:
data, limits = get_ohlcv_with_limits(client, 'BTC/USDT', '1m', since_timestamp, 200)
print(f"Лимиты: {limits}")