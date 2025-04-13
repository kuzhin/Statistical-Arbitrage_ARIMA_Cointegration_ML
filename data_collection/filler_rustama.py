import ccxt
import pandas as pd
from datetime import datetime, timedelta

# Инициализация клиента Bybit
exchange = ccxt.bybit({
    'options': {
        'defaultType': 'spot',  # Для спотовой торговли
    },
})

# Параметры
symbol = 'XRP/USDT'  # Пара Dogecoin к USDT TODO: XLM, XRP
timeframe = '5m'      # 5-минутный таймфрейм
limit = 200           # Максимум 200 свечей за один запрос

# Вычисление временного диапазона
end_time = exchange.milliseconds()  # Текущее время
start_time = end_time - (1460 * 24 * 60 * 60 * 1000)  # Год назад... TODO: Найти для нескольких лет

# Сбор данных
all_ohlcv = []
current_time = start_time

while current_time < end_time:
    try:
        ohlcv = exchange.fetch_ohlcv(symbol, timeframe, since=current_time, limit=limit)
        if not ohlcv:
            break  # Если данных больше нет
        all_ohlcv.extend(ohlcv)
        current_time = ohlcv[-1][0] + 1  # Переход к следующему блоку
        print(f"Собрано: {len(all_ohlcv)} свечей")
    except Exception as e:
        print(f"Ошибка: {e}")
        break

# Преобразование в DataFrame
columns = ['timestamp', 'open', 'high', 'low', 'close', 'volume']
df = pd.DataFrame(all_ohlcv, columns=columns)

# Конвертация timestamp в datetime
df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')

# Сохранение в CSV
df.to_csv('XRP_5m_yearly_data.csv', index=False)
print("Данные сохранены в doge_5m_yearly_data.csv")