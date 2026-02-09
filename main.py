import os
from dotenv import load_dotenv
import telebot

# تحميل التوكن من ملف .env الموجود في نفس المجلد
load_dotenv(os.path.join(os.path.dirname(__file__), '.env'))
TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def welcome(message):
    bot.reply_to(message, "✅ مبروك! البوت يعمل الآن من هاتفك.")

print("البوت بدأ العمل... جربه الآن في تليجرام!")
bot.infinity_polling()
# في ملف main.py
TOKEN = os.getenv('TELEGRAM_BOT_TOKEN') 

