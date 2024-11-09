import ccxt
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
import time

# Инициализация биржи KuCoin
exchange = ccxt.kucoin({
    'apiKey': 'ВАШ_API_КЛЮЧ',
    'secret': 'ВАШ_СЕКРЕТНЫЙ_КЛЮЧ',
    'password': 'ВАШ_ПАРОЛЬ',  # Некоторые биржи требуют дополнительный пароль
})

def get_price_data(symbol, timeframe='1h', limit=500):
    """Получение исторических данных для символа"""
    ohlcv = exchange.fetch_ohlcv(symbol, timeframe=timeframe, limit=limit)
    df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
    return df

# Получение данных для пар DOGE/USDT и ELON/USDT
doge_data = get_price_data('DOGE/USDT')
elon_data = get_price_data('ELON/USDT')

# Объединение данных по временным меткам
data = pd.merge(doge_data, elon_data, on='timestamp', suffixes=('_DOGE', '_ELON'))
data['return_DOGE'] = data['close_DOGE'].pct_change()
data['return_ELON'] = data['close_ELON'].pct_change()
data['spread'] = data['close_DOGE'] - data['close_ELON']
data['sma_spread'] = data['spread'].rolling(window=50).mean()
data['volatility_DOGE'] = data['close_DOGE'].rolling(window=50).std()
data['volatility_ELON'] = data['close_ELON'].rolling(window=50).std()

# Целевая переменная для классификации
# Если разница между DOGE и ELON увеличивается, присваиваем метку 1, иначе 0
data['target'] = np.where(data['spread'].shift(-1) > data['spread'], 1, 0)

# Удаление пропусков
data.dropna(inplace=True)

# Подготовка данных для обучения
X = data[['return_DOGE', 'return_ELON', 'sma_spread', 'volatility_DOGE', 'volatility_ELON']]
y = data['target']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# Обучение модели
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Оценка модели
y_pred = model.predict(X_test)
print("Accuracy:", accuracy_score(y_test, y_pred))
print(classification_report(y_test, y_pred))

# Реализация торгового алгоритма
def execute_trade():
    live_data_doge = get_price_data('DOGE/USDT', limit=1)
    live_data_elon = get_price_data('ELON/USDT', limit=1)

    # Подготовка данных для текущего предсказания
    current_data = {
        'return_DOGE': live_data_doge['close'].pct_change().iloc[-1],
        'return_ELON': live_data_elon['close'].pct_change().iloc[-1],
        'sma_spread': live_data_doge['close'].iloc[-1] - live_data_elon['close'].iloc[-1],
        'volatility_DOGE': live_data_doge['close'].rolling(window=50).std().iloc[-1],
        'volatility_ELON': live_data_elon['close'].rolling(window=50).std().iloc[-1]
    }

    input_df = pd.DataFrame([current_data])
    prediction = model.predict(input_df)[0]

    if prediction == 1:
        print("Ожидается увеличение спреда: рассмотрите покупку DOGE и продажу ELON.")
    else:
        print("Ожидается уменьшение спреда: рассмотрите продажу DOGE и покупку ELON.")

# Запуск торгового алгоритма каждые 15 минут
while True:
    execute_trade()
    time.sleep(900)  # Пауза на 15 минут
