from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# Замените 'YOUR_BOT_TOKEN' на ваш токен
bot_token = "8091885160:AAH1Fsfqglo1O5tySdn70JJkoKZprNg-dkY"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Получаем chat_id
    chat_id = update.message.chat_id
    await update.message.reply_text(f"Ваш chat_id: {chat_id}")

# Создаем приложение и добавляем обработчик команды /start
app = ApplicationBuilder().token(bot_token).build()
app.add_handler(CommandHandler("start", start))

# Запускаем бота
print("Бот запущен...")
app.run_polling()

"""
-1002476063523
"""
