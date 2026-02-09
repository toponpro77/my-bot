import telebot
from datetime import datetime
import os
from flask import Flask
from telebot import types

# إعداد Flask لضمان استمرارية الخدمة على Render
app = Flask(__name__)

@app.route('/')
def index():
    return "ZamanBot is Live and Running!"

# التوكن الخاص بك (تم تحديثه بناءً على صورك)
API_TOKEN = '7832802757:AAGImT_NlBRXsp0PD4BUQoRjJYzTZ3vq228'
bot = telebot.TeleBot(API_TOKEN)

# دالة لإنشاء لوحة المفاتيح التفاعلية (زر المشاركة)
def main_markup():
    markup = types.InlineKeyboardMarkup()
    share_btn = types.InlineKeyboardButton(
        text="شارك البوت | Share Bot 🚀", 
        url=f"https://t.me/share/url?url=https://t.me/wollf77_bot&text=احسب عمرك بالتفصيل (سنة، شهر، يوم) مجاناً!"
    )
    markup.add(share_btn)
    return markup

# معالجة أوامر /start و /help
@bot.message_handler(commands=['start', 'help'])
def welcome(message):
    welcome_msg = (
        "✨ **مرحباً بك في ZamanBot** ✨\n\n"
        "أنا بوت متخصص في حساب عمرك بدقة متناهية.\n\n"
        "📖 **طريقة الاستخدام:**\n"
        "فقط أرسل تاريخ ميلادك بالتنسيق التالي:\n"
        "👈 `يوم/شهر/سنة` (مثال: `15/05/1998`)\n\n"
        "--------------------------\n"
        "✨ **Welcome to ZamanBot** ✨\n\n"
        "I calculate your exact age in detail.\n\n"
        "📖 **How to use:**\n"
        "Just send your birthdate as:\n"
        "👈 `DD/MM/YYYY` (Example: `15/05/1998`)"
    )
    bot.reply_to(message, welcome_msg, parse_mode='Markdown', reply_markup=main_markup())

# معالجة النصوص وحساب العمر
@bot.message_handler(func=lambda message: True)
def calculate_age(message):
    # تجاهل الأوامر لكي لا يظهر خطأ "الصيغة"
    if message.text.startswith('/'):
        return

    try:
        # محاولة قراءة التاريخ
        birth_date = datetime.strptime(message.text, "%d/%m/%Y")
        today = datetime.now()
        
        # العملية الحسابية للدقة
        years = today.year - birth_date.year
        months = today.month - birth_date.month
        days = today.day - birth_date.day

        if days < 0:
            months -= 1
            days += 30 
        if months < 0:
            years -= 1
            months += 12

        response = (
            f"📊 **نتيجة حساب العمر:**\n"
            f"━━━━━━━━━━━━━━\n"
            f"🔹 عمرك هو: **{years}** سنة و **{months}** شهر و **{days}** يوم.\n"
            f"━━━━━━━━━━━━━━\n"
            f"📊 **Age Calculation Result:**\n"
            f"🔹 Your age: **{years}** years, **{months}** months, **{days}** days."
        )
        bot.reply_to(message, response, parse_mode='Markdown', reply_markup=main_markup())
        
    except ValueError:
        error_text = (
            "⚠️ **خطأ في الصيغة!**\n"
            "يرجى إرسال التاريخ بشكل صحيح: `يوم/شهر/سنة`\n"
            "مثال: `01/01/2000`"
        )
        bot.reply_to(message, error_text, parse_mode='Markdown')

# تشغيل البوت
if __name__ == "__main__":
    import threading
    threading.Thread(target=lambda: bot.polling(none_stop=True)).start()
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
