from price_check import *


# Функция для расчета арбитража
def calculate_arbitrage():
    # Получаем текущие цены (примерно так: {"ARB/USDC": 1.23, "WETH/USDC": 3500.0, "ARB/WETH": 0.00035})
    prices = price_check()

    # Извлекаем необходимые цены
    arb_usdc = prices["ARB/USDC"]  # Цена ARB в USDC
    weth_usdc = prices["WETH/USDC"]  # Цена WETH в USDC
    arb_weth = prices["ARB/WETH"]  # Цена ARB в WETH

    # Шаг 1: Покупаем WETH за ARB (по курсу ARB/WETH)
    arb_amount = 500  # Начальное количество ARB (можно задать любое)
    weth_received = arb_amount * arb_weth  # Количество WETH, полученное за ARB

    # Шаг 2: Продаем WETH за USDC (по курсу WETH/USDC)
    usdc_received = weth_received * weth_usdc  # Количество USDC, полученное за WETH

    # Шаг 3: Продаем USDC за ARB (по курсу ARB/USDC)
    arb_final = usdc_received / arb_usdc  # Количество ARB, полученное за USDC

    # Расчет арбитражной прибыли (если результат больше начального ARB)
    profit = arb_final - arb_amount

    print(profit)
    # Проверяем, есть ли арбитражная возможность
    if profit > 0:
        print(f"Arbitrage opportunity found! Profit: {profit:.6f} ARB")
    else:
        print("No arbitrage opportunity detected.")
calculate_arbitrage()