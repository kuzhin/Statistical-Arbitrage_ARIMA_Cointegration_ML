import numpy as np
import pandas as pd
import statsmodels.api as sm
from statsmodels.tsa.stattools import coint, adfuller
from typing import Tuple, Optional
import psycopg2
from data_collection.filler import DB_CONFIG

class CointegrationTester:
    def __init__(self, db_config: dict):
        self.conn = psycopg2.connect(**db_config)

    def _fetch_pair_data(self, pair1: str, pair2: str) -> Optional[pd.DataFrame]:
        """Загрузка исторических данных для двух пар из БД."""
        query = """
            SELECT 
                ph1.timestamp,
                ph1.close AS price1,
                ph2.close AS price2
            FROM price_history ph1
            JOIN price_history ph2 
                ON ph1.timestamp = ph2.timestamp
            WHERE 
                ph1.pair = %s AND 
                ph2.pair = %s
            ORDER BY ph1.timestamp;
        """
        try:
            df = pd.read_sql(query, self.conn, params=(f"{pair1}/USDT", f"{pair2}/USDT"))
            df.set_index('timestamp', inplace=True)
            return df
        except Exception as e:
            print(f"Ошибка загрузки данных для {pair1}/{pair2}: {e}")
            return None

    def test_cointegration(self, pair1: str, pair2: str) -> dict:
        """Запуск тестов коинтеграции для пары активов."""
        data = self._fetch_pair_data(pair1, pair2)
        if data is None or len(data) < 100:
            return {"error": "Недостаточно данных"}

        # Регрессия для расчета хедж-коэффициента (β)
        X = sm.add_constant(data['price2'])
        model = sm.OLS(data['price1'], X)
        results = model.fit()
        beta = results.params[1]

        # Расчет спреда
        spread = data['price1'] - beta * data['price2']

        # Тест Энгла-Грейнджера
        coint_stat, pvalue_eg, _ = coint(data['price1'], data['price2'])

        # ADF-тест для спреда
        adf_result = adfuller(spread)
        pvalue_adf = adf_result[1]

        return {
            "pair1": pair1,
            "pair2": pair2,
            "beta": beta,
            "spread_mean": spread.mean(),
            "spread_std": spread.std(),
            "coint_pvalue": pvalue_eg,
            "adf_pvalue": pvalue_adf,
            "is_cointegrated": pvalue_eg < 0.05 and pvalue_adf < 0.05
        }

    def calculate_zscore(self, spread: pd.Series, window: int = 30) -> pd.Series:
        """Расчет Z-скора спреда с скользящим окном."""
        mean = spread.rolling(window=window).mean()
        std = spread.rolling(window=window).std()
        return (spread - mean) / std

    def close(self):
        """Закрытие подключения к БД."""
        self.conn.close()


# Пример использования
if __name__ == "__main__":
    tester = CointegrationTester(DB_CONFIG)

    # Пример теста для пары BTC/ETH
    result = tester.test_cointegration("BTC", "ETH")
    print(f"Результаты коинтеграции BTC/ETH:")
    print(f"P-value (Энгл-Грейнджер): {result['coint_pvalue']:.4f}")
    print(f"P-value (ADF): {result['adf_pvalue']:.4f}")
    print(f"Коинтегрированы: {'Да' if result['is_cointegrated'] else 'Нет'}")

    tester.close()