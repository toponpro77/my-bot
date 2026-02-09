import telebot
import os
import yt_dlp
from telebot import types

# جلب التوكن من إعدادات Render
TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
bot = telebot.TeleBot(TOKEN)

# رسالة ترحيبية احترافية
START_TEXT = """
✨ **مرحباً بك في بوت التحميل الذكي!** ✨

أرسل لي رابط المقطع (يوتيوب، تيك توك، إنستغرام) وسأقوم بتحميله لك فوراً.

📥 **أرسل الرابط الآن لنبدأ!**
"""

@bot.message_handler(commands=['start'])
def welcome(message):
    bot.reply_to(message, START_TEXT, parse_mode="Markdown")

@bot.message_handler(func=lambda message: "http" in message.text)
def ask_format(message):
    url = message.text
    markup = types.InlineKeyboardMarkup(row_width=2)
    btn_vid = types.InlineKeyboardButton("🎬 فيديو (MP4)", callback_data=f"vid|{url}")
    btn_aud = types.InlineKeyboardButton("🎵 صوت (MP3)", callback_data=f"aud|{url}")
    markup.add(btn_vid, btn_aud)
    bot.reply_to(message, "⚙️ **اختر التنسيق الذي تريده:**", reply_markup=markup, parse_mode="Markdown")

@bot.callback_query_handler(func=lambda call: True)
def handle_download(call):
    action, url = call.data.split("|")
    bot.edit_message_text("⏳ **جاري معالجة طلبك...**", call.message.chat.id, call.message.message_id)
    
    ydl_opts = {
        'format': 'best' if action == "vid" else 'bestaudio/best',
        'outtmpl': 'downloaded_file.%(ext)s',
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            file_path = ydl.prepare_filename(info)
            with open(file_path, 'rb') as f:
                if action == "vid":
                    bot.send_video(call.message.chat.id, f)
                else:
                    bot.send_audio(call.message.chat.id, f)
            os.remove(file_path)
    except Exception as e:
        bot.send_message(call.message.chat.id, f"❌ خطأ: {str(e)}")

bot.infinity_polling()
