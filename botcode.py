import telebot

TOKEN = "9186019187:AAEdvFJZjI6ZazFaC9Y98F-v48I29kR0-nw"
bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=["start"])
def send_welcome(message):
    bot.reply_to(
        message,
        "Привет! Я твой первый Telegram-бот. Напиши мне что-нибудь!",
    )


@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.reply_to(message, f"Ты написал: {message.text}")


print("Бот запущен...")
bot.infinity_polling()