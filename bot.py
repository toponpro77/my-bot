import telebot
from datetime import datetime
import os
from flask import Flask
from telebot import types

# إعداد Flask لإرضاء Render
app = Flask(__name__)

@app.route('/')
def index():
    return "Zaman Bot is Online!"

# التوكن الخاص بك
API_TOKEN = '7832802757:AAGImT_NlBRXsp0PD4BUQoRjJYzTZ3vq228'
bot = telebot.TeleBot(API_TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.InlineKeyboardMarkup()
    share_button = types.InlineKeyboardButton(
        text="شارك البوت | Share Bot 🚀", 
        url=f"https://t.me/share/url?url=https://t.me/wollf77_bot&text=احسب عمرك بالتفصيل (سنين، شهور، أيام) هنا!"
    )
    markup.add(share_button)
    
    welcome_msg = (
        "👋 أهلاً بك في ZamanBot!\n"
        "أرسل تاريخ ميلادك بهذا الشكل: يوم/شهر/سنة\n"
        "مثال: 01/05/1998\n\n"
        "👋 Welcome to ZamanBot!\n"
        "Send your birthdate: DD/MM/YYYY"
    )
    bot.reply_to(message, welcome_msg, reply_markup=markup)

@bot.message_handler(func=lambda message: True)
def calculate(message):
    try:
        birth_date = datetime.strptime(message.text, "%d/%m/%Y")
        today = datetime.now()
        
        # حساب الفرق الزمني بدقة
        years = today.year - birth_date.year
        months = today.month - birth_date.month
        days = today.day - birth_date.day

        if days < 0:
            months -= 1
            # إضافة عدد أيام الشهر السابق
            days += 30 
        if months < 0:
            years -= 1
            months += 12

        result = (
            f"📊 تفاصيل عمرك هي:\n"
            f"🔹 {years} سنة، و {months} شهر، و {days} يوم.\n"
            f"----------------------------\n"
            f"📊 Your age details:\n"
            f"🔹 {years} years, {months} months, {days} days."
        )
        bot.reply_to(message, result)
    except:
        error_msg = "⚠️ صيغة التاريخ خطأ! أرسله هكذا: 01/01/2000"
        bot.reply_to(message, error_msg)

if __name__ == "__main__":
    import threading
    threading.Thread(target=lambda: bot.polling(none_stop=True)).start()
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
