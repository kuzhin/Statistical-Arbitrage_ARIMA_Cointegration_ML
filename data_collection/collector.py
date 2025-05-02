import pandas as pd
import ccxt
from pathlib import Path
from datetime import datetime, timedelta

# Папка для сохранения данных
DATA_DIR = Path(__file__).parent.parent / 'data'  # Папка "data" в корне проекта
DATA_DIR.mkdir(parents=True, exist_ok=True)  # Создаем папку, если не существует

PAIRS = [
    'XLM/USDT', 'SOL/USDT', 'ONDO/USDT', 'ETC/USDT',
    'BNB/USDT', 'ADA/USDT', 'XRP/USDT', 'TRX/USDT', 'SUI/USDT'
]


def fetch_data_from_exchange(pair, timeframe, since_days):
    """Загружает данные с биржи Bybit"""
    exchange = ccxt.bybit({'enableRateLimit': True})

    # Вычисляем дату начала (since_days дней назад)
    since = int((datetime.now() - timedelta(days=since_days)).timestamp() * 1000)

    try:
        # Загружаем OHLCV данные
        data = exchange.fetch_ohlcv(pair, timeframe, since=since)
    except Exception as e:
        print(f"Ошибка загрузки данных для {pair}: {str(e)}")
        return pd.DataFrame()

    # Создаем DataFrame
    df = pd.DataFrame(data, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
    df.set_index('timestamp', inplace=True)
    return df


def save_data_to_file(pair, timeframe, df):
    """Сохраняет данные в файл"""
    filename = f"{pair.replace('/', '_')}_{timeframe}.csv"
    file_path = DATA_DIR / filename
    df.to_csv(file_path)
    print(f"Данные сохранены в {file_path}")


def load_data_from_file(pair, timeframe):
    """Загружает данные из файла, если он существует"""
    filename = f"{pair.replace('/', '_')}_{timeframe}.csv"
    file_path = DATA_DIR / filename

    if file_path.exists():
        print(f"Загружаю данные из файла: {file_path}")
        return pd.read_csv(file_path, index_col='timestamp', parse_dates=True)
    else:
        print(f"Файл {file_path} не найден.")
        return pd.DataFrame()


def update_data(pair, timeframe, since_days, force_update=False):
    """
    Обновлено: Добавлен флаг force_update
    Если force_update=False - использует существующие данные без проверки обновлений
    """
    filename = f"{pair.replace('/', '_')}_{timeframe}.csv"
    file_path = DATA_DIR / filename

    if file_path.exists() and not force_update:
        print(f"Используем существующие данные из файла: {file_path}")
        return load_data_from_file(pair, timeframe)

    # Остальная логика для загрузки/обновления данных
    if file_path.exists():
        existing_data = load_data_from_file(pair, timeframe)
        last_timestamp = existing_data.index.max()
        since_days_for_new_data = max(1, (datetime.now() - last_timestamp).days)
        new_data = fetch_data_from_exchange(pair, timeframe, since_days_for_new_data)

        if not new_data.empty:
            combined_data = pd.concat([existing_data, new_data]) \
                .drop_duplicates() \
                .sort_index()
            save_data_to_file(pair, timeframe, combined_data)
            return combined_data
        return existing_data
    else:
        new_data = fetch_data_from_exchange(pair, timeframe, since_days)
        if not new_data.empty:
            save_data_to_file(pair, timeframe, new_data)
        return new_data


def get_all_pairs(timeframe, since_days, force_update=False):
    """
    Получает данные для всех пар с контролем обновления

    Параметры:
        timeframe: таймфрейм данных (например, '5m', '1h')
        since_days: за сколько дней загружать данные (если force_update=True)
        force_update: принудительно обновить данные (по умолчанию False)

    Возвращает:
        Словарь {пара: DataFrame} только с успешно загруженными данными
    """
    result = {}
    failed_pairs = []

    for pair in PAIRS:
        try:
            df = update_data(pair, timeframe, since_days, force_update)
            if not df.empty:
                result[pair] = df
            else:
                failed_pairs.append(pair)
        except Exception as e:
            print(f"Ошибка загрузки {pair}: {str(e)}")
            failed_pairs.append(pair)

    if failed_pairs:
        print(f"\nНе удалось загрузить: {', '.join(failed_pairs)}")

    print(f"\nУспешно загружено {len(result)}/{len(PAIRS)} пар")
    return result


# if __name__ == "__main__":
#     # Указываем таймфрейм и количество дней для загрузки данных
#     timeframe = "1h"  # Например, часовой таймфрейм
#     since_days = 30   # Загружаем данные за последние 30 дней
#
#     # Получаем данные для всех пар
#     all_data = get_all_pairs(timeframe, since_days)
#
#     # Проверяем результат
#     for pair, data in all_data.items():
#         print(f"Данные для {pair}:")
#         print(data.head())  # Выводим первые строки данных