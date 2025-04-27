import pandas as pd
import numpy as np

def align_pair_data(pair1_df, pair2_df):
    """Выравнивает данные двух пар по времени"""
    common_index = pair1_df.index.intersection(pair2_df.index)
    return (
        pair1_df.loc[common_index],
        pair2_df.loc[common_index]
    )


def calculate_log_returns(df):
    """Вычисляет логарифмические доходности"""
    return (df['close'] / df['close'].shift(1)).apply(lambda x: x if x > 0 else 1e-10).apply(np.log)


def prepare_data_for_analysis(pair1_df, pair2_df):
    """Подготавливает данные для анализа коинтеграции"""
    # Выравниваем данные
    pair1_aligned, pair2_aligned = align_pair_data(pair1_df, pair2_df)

    # Вычисляем лог-доходности
    pair1_log = calculate_log_returns(pair1_aligned)
    pair2_log = calculate_log_returns(pair2_aligned)

    return pair1_log, pair2_log