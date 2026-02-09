import telebot
from datetime import datetime

API_TOKEN = '7832802757:AAGImT_NlBRXsp0PD4BUQoRjJYzTZ3vq228'
bot = telebot.TeleBot(API_TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "✅ البوت يعمل! أرسل تاريخ ميلادك (يوم/شهر/سنة)")

@bot.message_handler(func=lambda message: True)
def calculate(message):
    try:
        birth_date = datetime.strptime(message.text, "%d/%m/%Y")
        today = datetime.now()
        age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
        bot.reply_to(message, f"عمرك هو: {age} سنة.")
    except:
        bot.reply_to(message, "⚠️ أرسل التاريخ هكذا: 01/01/1990")

bot.polling()
