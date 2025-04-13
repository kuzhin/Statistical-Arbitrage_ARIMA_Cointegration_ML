import os
import psycopg2
import time
import ccxt

from tqdm import tqdm
from dotenv import load_dotenv
from datetime import datetime, timedelta, timezone

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
list_top_10 = ['XLM', 'XRP']  # 'BTC', 'ETH', 'SOL','TRX', 'MNT',
               #'DOGE', 'TON', 'SUI', 'ADA', 'AVAX'

start_date = datetime(2023,8,1)
start_date_for_data_update = datetime(2025,4,10)
BATCH_SIZE = 1000  # Максимально разрешенный батч сайз


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
    return ccxt.bybit({
        'enableRateLimit': True,
        'options': {
            'defaultType': 'spot',
            'adjustForTimeDifference': True,
        },
    })


def ensure_tables_exist(conn):
    """Проверка существования таблиц"""
    with conn.cursor() as cursor:
        # Список таблиц для проверки
        tables_to_check = ['tokens', 'price_history']
        missing_tables = []

        for table_name in tables_to_check:
            cursor.execute("""
                SELECT EXISTS (
                    SELECT FROM information_schema.tables 
                    WHERE table_name = %s
                );
            """, (table_name,))
            exists = cursor.fetchone()[0]
            if not exists:
                missing_tables.append(table_name)

        if missing_tables:
            print(f"Отсутствуют таблицы: {', '.join(missing_tables)}")
        else:
            print("Все необходимые таблицы существуют.")

def ensure_tokens_exist(conn):
    """Проверка существования токенов в базе"""
    with conn.cursor() as cursor:
        for pair in list_top_10:
            # Извлекаем символ из пары (первые 3-4 символа до USDT)
            symbol = pair.replace('USDT', '')
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

    start_time = time.time()

    with tqdm(desc=f"Загрузка {pair} ({current_start.strftime('%Y-%m-%d')})", unit="batch") as pbar:
        while not end_reached:
            try:
                # Получение данных с Bybit
                data = client.fetch_ohlcv(
                    symbol=f"{symbol}USDT",  # Формат Bybit: BTCUSDT
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
                        datetime.fromtimestamp(d[0] / 1000, tz=timezone.utc),
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
                    current_start = datetime.fromtimestamp(data[-1][0] / 1000, tz=timezone.utc) + timedelta(minutes=1)  # Исправлено

                # Обновление описания прогресс-бара
                pbar.set_description(f"Загрузка {pair} ({current_start.strftime('%Y-%m-%d')})")
                pbar.update(1)

                time.sleep(client.rateLimit / 1000)  # Увеличиваем задержку

            except ccxt.NetworkError as e:
                print(f"Сетевая ошибка для {pair}: {e}")
            except ccxt.ExchangeError as e:
                print(f"Ошибка биржи для {pair}: {e}")
                print("Подробности:", str(e))
            except Exception as e:
                print(f"Неожиданная ошибка для {pair}: {e}")
    end_time = time.time()
    total_time = end_time - start_time
    print(f"\nЗагрузка данных для {pair} завершена за {total_time/60:.2f} минут.")


def main():
    """Основная функция выполнения"""
    print("Инициализация подключений...")
    conn = init_db_connection()
    client = init_bybit_client()

    print("Проверка таблиц...")
    ensure_tables_exist(conn)

    print("Проверка токенов в БД...")
    ensure_tokens_exist(conn)

    print("Начало загрузки данных...")
    for pair in list_top_10:
        load_pair_data(conn, client, pair)

    conn.close()
    print("Загрузка завершена!")


if __name__ == "__main__":
    main()