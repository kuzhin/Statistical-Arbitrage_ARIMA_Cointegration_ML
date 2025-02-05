from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes


bot_token = "8091885160:AAH1Fsfqglo1O5tySdn70JJkoKZprNg-dkY"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Проверяем, есть ли message_thread_id в сообщении
    if update.message and update.message.message_thread_id is not None:
        thread_id = update.message.message_thread_id
        await update.message.reply_text(f"Thread ID этой темы: {thread_id}")
    else:
        await update.message.reply_text("Это сообщение не из темы. Убедитесь, что темы включены в группе.")

# Создаем приложение и добавляем обработчик команды /start
app = ApplicationBuilder().token(bot_token).build()
app.add_handler(CommandHandler("start", start))

# Запускаем бота
print("Бот запущен...")
app.run_polling()

