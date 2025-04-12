import asyncio
import ccxt
from solana.rpc.api import Client
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# Конфигурация
CEX_EXCHANGES = ['mexc', 'gate']
DEX_PAIRS = {
    'SOL/USDC': 'So11111111111111111111111111111111111111112',  # Пример контракта
}
SOLANA_RPC_URL = "https://api.mainnet-beta.solana.com"
MIN_VOLUME = 0  # Минимальный объем для учета
BOT_TOKEN = "8091885160:AAH1Fsfqglo1O5tySdn70JJkoKZprNg-dkY"


async def get_cex_prices(symbol: str):
    """Получение цен с CEX бирж"""
    prices = {}
    for exchange_id in CEX_EXCHANGES:
        try:
            exchange = getattr(ccxt, exchange_id)()
            ticker = exchange.fetch_ticker(symbol)
            prices[exchange_id] = {
                'price': ticker['last'],
                'volume': ticker['quoteVolume']
            }
        except Exception as e:
            print(f"Error fetching {exchange_id}: {str(e)}")
    return prices


async def get_dex_price(symbol: str):
    """Получение цены с DEX на Solana (упрощенный пример)"""
    solana_client = Client(SOLANA_RPC_URL)

    # Здесь должна быть логика получения цены из пула ликвидности
    # Пример для Raydium (требуется реализация через RPC)
    dex_price = 0  # Заглушка
    dex_volume = 0  # Заглушка

    return {
        'price': dex_price,
        'volume': dex_volume,
        'contract': DEX_PAIRS[symbol],
        'network': 'Solana'
    }


async def find_arbitrage(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Поиск арбитражных возможностей"""
    symbol = 'SOL/USDC'

    # Получаем данные с CEX
    cex_prices = await get_cex_prices(symbol)

    # Получаем данные с DEX
    dex_data = await get_dex_price(symbol)

    # Поиск спредов между CEX
    for exchange1, data1 in cex_prices.items():
        for exchange2, data2 in cex_prices.items():
            if exchange1 != exchange2 and data1['volume'] > MIN_VOLUME and data2['volume'] > MIN_VOLUME:
                spread = abs(data1['price'] - data2['price']) / min(data1['price'], data2['price']) * 100
                if spread > 0.1:
                    message = (
                        f"🚨 CEX-CEX Arbitrage ({symbol})\n"
                        f"{exchange1.upper()}: ${data1['price']:.2f}\n"
                        f"{exchange2.upper()}: ${data2['price']:.2f}\n"
                        f"Spread: {spread:.2f}%\n"
                        f"Volume: ${max(data1['volume'], data2['volume']):.0f}"
                    )
                    await update.message.reply_text(message)

    # Поиск спредов между CEX и DEX
    for exchange, cex_data in cex_prices.items():
        if cex_data['volume'] > MIN_VOLUME and dex_data['volume'] > MIN_VOLUME:
            spread = abs(cex_data['price'] - dex_data['price']) / min(cex_data['price'], dex_data['price']) * 100
            if spread > 0.1:
                message = (
                    f"🚨 CEX-DEX Arbitrage ({symbol})\n"
                    f"{exchange.upper()}: ${cex_data['price']:.2f}\n"
                    f"DEX (Solana): ${dex_data['price']:.2f}\n"
                    f"Spread: {spread:.2f}%\n"
                    f"Contract: {dex_data['contract']}\n"
                    f"Network: {dex_data['network']}\n"
                    f"Volume: ${max(cex_data['volume'], dex_data['volume']):.0f}"
                )
                await update.message.reply_text(message)


if __name__ == "__main__":
    # Инициализация Telegram бота
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("scan", find_arbitrage))

    print("Бот запущен...")
    app.run_polling()