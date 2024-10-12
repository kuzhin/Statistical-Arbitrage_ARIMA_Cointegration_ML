# Комиссия биржи, учитывайте реальные данные



commission_rate = 0.021  # 0.1%

comm  = commission_rate - 0.1
# Рассчитываем возможный арбитражный спред с учетом комиссии
def calculate_arbitrage(binance_price, kraken_price):
    buy_price = min(binance_price, kraken_price)
    sell_price = max(binance_price, kraken_price)

    # Спред между ценами на биржах
    spread = sell_price - buy_price

    # Учитываем комиссию бирж
    effective_spread = spread - (buy_price * commission_rate + sell_price * commission_rate)

    if effective_spread > 0:
        print(
            f"Возможен арбитраж: купите на {'Binance' if buy_price == binance_price else 'Kraken'}, продайте на {'Kraken' if sell_price == kraken_price else 'Binance'}")
    else:
        print("Арбитраж Nевозможен")

print(comm)
# Пример расчета
calculate_arbitrage(binance_price, kraken_price)
