import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

# Получаем токен из переменной окружения Railway
TOKEN = os.getenv("BOT_TOKEN")

# Команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет! Я бот для подсчёта хлебных единиц 🥖\n"
                                    "Просто напиши: <углеводы в граммах> <ХЕ на 100г>")

# Обработка сообщений с цифрами
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        text = update.message.text.strip()
        carbs, xe_per_100 = map(float, text.split())

        xe = carbs * xe_per_100 / 100

        if xe <= 5.9:
            status = "✅ В пределах нормы"
        else:
            status = "⚠️ Высокое количество хлебных единиц"

        await update.message.reply_text(
            f"Углеводы: {carbs} г\n"
            f"ХЕ на 100 г: {xe_per_100}\n"
            f"Хлебных единиц: {xe:.1f}\n"
            f"Статус: {status}"
        )

    except:
        await update.message.reply_text("⚠️ Формат неверный. Напишите так: 120 15")

# Основной запуск бота
def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("Бот запущен и работает...")
    app.run_polling()

if __name__ == "__main__":
    main()
