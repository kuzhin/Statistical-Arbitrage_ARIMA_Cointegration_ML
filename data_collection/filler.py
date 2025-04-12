import os
import psycopg2
from datetime import datetime, timedelta
import time
from tqdm import tqdm
import ccxt
from dotenv import load_dotenv

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

# Ключи API Bybit
BYBIT_API_KEY = os.getenv('BYBIT_API_KEY')
BYBIT_SECRET = os.getenv('BYBIT_SECRET')

# Список криптовалютных пар
list_top_10 = ['BTC', 'ETH', 'SOL', 'TRX', 'MNT', 'DOGE', 'TON', 'SUI', 'ADA', 'AVAX']
start_date = datetime(2021, 8, 1)
BATCH_SIZE = 1000  # Максимальное количество свечей за запрос


def init_db_connection():
    """Инициализация подключения к TimescaleDB"""
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        return conn
    except Exception as e:
        print(f"Ошибка подключения к БД: {e}")
        raise


def init_bybit_client():
    """Инициализация клиента Bybit через CCXT"""
    exchange = ccxt.bybit({
        'apiKey': BYBIT_API_KEY,
        'secret': BYBIT_SECRET,
        'options': {
            'defaultType': 'spot',  # или 'future' для фьючерсов
        },
        'recvWindow': 100000,  # Увеличиваем recv_window
    })
    return exchange



def ensure_tokens_exist(conn):
    """Проверка существования токенов в базе"""
    with conn.cursor() as cursor:
        for symbol in list_top_10:
            cursor.execute("""
                INSERT INTO tokens (symbol) 
                VALUES (%s)
                ON CONFLICT (symbol) DO NOTHING
            """, (symbol,))
        conn.commit()


def load_pair_data(conn, client, symbol):
    """Загрузка данных для одной пары"""
    pair = f"{symbol}/USDT"
    current_start = start_date
    end_reached = False

    with tqdm(desc=f"Загрузка {pair}", unit="batch") as pbar:
        while not end_reached:
            try:
                # Получение данных с Bybit
                data = client.fetch_ohlcv(
                    symbol=pair,
                    timeframe='1m',
                    since=int(current_start.timestamp() * 1000),
                    limit=BATCH_SIZE
                )

                if not data:
                    end_reached = True
                    continue

                # Подготовка данных для вставки
                batch = []
                for d in data:
                    batch.append((
                        pair,
                        datetime.utcfromtimestamp(d[0] / 1000),
                        float(d[1]),  # open
                        float(d[2]),  # high
                        float(d[3]),  # low
                        float(d[4]),  # close
                        float(d[5])   # volume
                    ))

                # Пакетная вставка в БД
                with conn.cursor() as cursor:
                    cursor.executemany("""
                        INSERT INTO price_history 
                        (pair, timestamp, open, high, low, close, volume)
                        VALUES (%s, %s, %s, %s, %s, %s, %s)
                        ON CONFLICT (pair, timestamp) DO NOTHING
                    """, batch)
                    conn.commit()

                # Обновление временного диапазона
                if len(data) < BATCH_SIZE:
                    end_reached = True
                else:
                    current_start = datetime.utcfromtimestamp(data[-1][0] / 1000) + timedelta(minutes=1)

                pbar.update(1)
                time.sleep(client.rateLimit / 1000)  # Соблюдение rate limit

            except ccxt.NetworkError as e:
                print(f"Сетевая ошибка для {pair}: {e}")
            except ccxt.ExchangeError as e:
                print(f"Ошибка биржи для {pair}: {e}")
            except Exception as e:
                print(f"Неожиданная ошибка для {pair}: {e}")


def main():
    """Основная функция выполнения"""
    print("Инициализация подключений...")
    conn = init_db_connection()
    client = init_bybit_client()

    print("Проверка токенов в БД...")
    ensure_tokens_exist(conn)

    print("Начало загрузки данных...")
    for symbol in list_top_10:
        load_pair_data(conn, client, symbol)

    conn.close()
    print("Загрузка завершена!")


if __name__ == "__main__":
    main()