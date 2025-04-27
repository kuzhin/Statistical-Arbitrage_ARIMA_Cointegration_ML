import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import ccxt
import pickle
from data_collection.collector import *

# Статистика
from statsmodels.tsa.stattools import coint
from statsmodels.tsa.stattools import adfuller


print('Алгоритм начал работу:')

def find_cointegrated_pairs(data, significance_level=0.5):
    """
    Ищет коинтегрированные пары в предзагруженных данных

    :param data: Словарь {пара: DataFrame}
    :param significance_level: Пороговый p-value
    :return: DataFrame с результатами
    """
    pairs = list(data.keys())
    results = []

    for i in range(len(pairs)):
        for j in range(i + 1, len(pairs)):
            pair1, pair2 = pairs[i], pairs[j]

            try:
                # Объединяем данные по времени
                merged = pd.merge(data[pair1]['close'], data[pair2]['close'],
                                  left_index=True, right_index=True, how='inner')
                merged.columns = [pair1, pair2]
                df = merged.dropna()

                # Проверка на I(1)
                pval1 = adfuller(np.log(df[pair1]))[1]
                pval2 = adfuller(np.log(df[pair2]))[1]

                if pval1 > 0.05 and pval2 > 0.05:  # Оба ряда нестационарны
                    # Тест коинтеграции
                    _, pvalue, _ = coint(np.log(df[pair1]), np.log(df[pair2]))

                    if pvalue <= significance_level:
                        results.append({
                            'Active 1': pair1.split('/')[0],
                            'Active 2': pair2.split('/')[0],
                            'P-value': round(pvalue, 4),
                            # Можно добавить таймфрейм и количество свеч
                        })

            except Exception as e:
                print(f"Ошибка анализа {pair1}-{pair2}: {str(e)}")

    return pd.DataFrame(results).sort_values('P-value').reset_index(drop=True)


data = load_all_pairs(pairs, timeframe='5m', limit=50)


# 2. Анализ коинтеграции (можем выполнять многократно без повторной загрузки)
cointegrated_df = find_cointegrated_pairs(data, significance_level=0.5)
print(cointegrated_df)


