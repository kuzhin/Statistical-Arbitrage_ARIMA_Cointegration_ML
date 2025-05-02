import ccxt
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.tsa.stattools import coint

# Настройка Binance API
exchange = ccxt.binance()

# Загрузка данных (1h таймфрейм, 1000 свечей)
def fetch_data(symbol, timeframe='1h', limit=1000):
    ohlcv = exchange.fetch_ohlcv(symbol, timeframe, limit=limit)
    df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
    df.set_index('timestamp', inplace=True)
    return df['close']  # Возвращаем только цены закрытия

# Загружаем данные
xlm = fetch_data('XLM/USDT')
xrp = fetch_data('XRP/USDT')
# Объединяем в один DataFrame
df = pd.DataFrame({'XLM': xlm, 'XRP': xrp}).dropna()
df1 = df.to_csv('1.csv')

plt.figure(figsize=(12, 6))
plt.plot(df['XLM'], label='XLM', color='blue', alpha=0.8)
plt.plot(df['XRP'], label='XRP', color='orange', alpha=0.8)
plt.title('Динамика цен XLM и XRP (Binance, 1h)')
plt.xlabel('Дата')
plt.ylabel('Цена (USDT)')
plt.legend()
plt.grid(True)
plt.show()


from statsmodels.tsa.stattools import adfuller

# Рассчитываем спред (линейная регрессия: XLM = beta * XRP + alpha)
beta = np.polyfit(df['XRP'], df['XLM'], 1)[0]  # beta (коэффициент наклона)
spread = df['XLM'] - beta * df['XRP']

# Проверяем стационарность спреда (ADF-тест)
adf_result = adfuller(spread)
print(f'ADF Statistic: {adf_result[0]:.3f}')
print(f'p-value: {adf_result[1]:.3f}')

# Интерпретация:
# p-value < 0.05 → спред стационарен → коинтеграция есть

plt.figure(figsize=(12, 6))
plt.plot(spread, label='Спред (XLM - β*XRP)', color='purple', alpha=0.7)

# Среднее и ±1.5σ
mean = spread.mean()
std = spread.std()
plt.axhline(mean, color='black', linestyle='--', label='Среднее')
plt.axhline(mean + 1.5*std, color='red', linestyle=':', label='+1.5σ (Продажа XLM, Покупка XRP)')
plt.axhline(mean - 1.5*std, color='green', linestyle=':', label='-1.5σ (Покупка XLM, Продажа XRP)')

# Разметка
plt.title('Спред XLM/XRP с зонами входа')
plt.xlabel('Дата')
plt.ylabel('Спред')
plt.legend()
plt.grid(True)
plt.show()