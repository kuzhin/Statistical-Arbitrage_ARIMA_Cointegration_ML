import pandas as pd
import numpy as np
from statsmodels.tsa.stattools import coint, adfuller
from data_collection.collector import PAIRS, get_all_pairs
from analysis.preprocessing import prepare_data_for_analysis


# def check_stationarity(series):
#     """Проверяет стационарность ряда с помощью ADF"""
#     result = adfuller(series)
#     return result[1]  # p-value


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


def run_cointegration_analysis(timeframe, since_days):
    # Загружаем данные
    pairs_data = get_all_pairs(timeframe, since_days)

    # Находим коинтегрированные пары
    results_df = find_cointegrated_pairs(pairs_data)

    # Сохраняем результаты
    results_df.to_csv('saved_data/cointegration_results.csv', index=False)
    print(f"Найдено {len(results_df)} коинтегрированных пар")
    return results_df