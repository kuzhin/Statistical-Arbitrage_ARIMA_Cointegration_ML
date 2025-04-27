from analysis.cointegration import run_cointegration_analysis

if __name__ == "__main__":
    # Запуск анализа с параметрами:
    # - timeframe: '5m' (5 минут)
    # - since_days: 30 (последние 30 дней)
    results = run_cointegration_analysis(timeframe='5m', since_days=5)
    print(results)