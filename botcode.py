import random
import telebot

TELEGRAM_TOKEN = "9186019187:AAEdvFJZjI6ZazFaC9Y98F-v48I29kR0-nw"
bot = telebot.TeleBot(TELEGRAM_TOKEN)


@bot.message_handler(commands=["start"])
def send_welcome(message):
    bot.reply_to(
        message,
        "Привет! Команды: /start, /help, /roll, /ping. Любой другой текст я просто повторю.",
    )


@bot.message_handler(commands=["help"])
def send_help(message):
    help_text = (
        "/start — приветствие\n"
        "/help — список команд\n"
        "/roll [N] — случайное число от 1 до N (по умолчанию до 6)\n"
        "/ping — проверка работы бота\n"
        "Обычный текст бот повторяет."
    )
    bot.reply_to(message, help_text)


@bot.message_handler(commands=["roll"])
def send_roll(message):
    parts = message.text.split(maxsplit=1)
    max_num = 6

    if len(parts) == 2:
        try:
            parsed = int(parts[1].strip())
            if parsed >= 1:
                max_num = parsed
            else:
                bot.reply_to(message, "Введите число больше 0, например: /roll 20")
                return
        except ValueError:
            bot.reply_to(message, "После /roll нужно указать целое число, например: /roll 50")
            return

    number = random.randint(1, max_num)
    bot.reply_to(message, f"Выпало число: {number} (1–{max_num})")


@bot.message_handler(commands=["ping"])
def send_ping(message):
    bot.reply_to(message, "Pong!")


@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.reply_to(message, message.text)


print("Бот запущен...")
bot.infinity_polling()