import telebot
import os
import yt_dlp
from telebot import types

# جلب الأسرار من Render
TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
bot = telebot.TeleBot(TOKEN)

# رسالة المقدمة الاحترافية
START_MSG = """
🌟 **أهلاً بك في بوت التحميل الاحترافي!** 🌟

يمكنني تحميل الفيديوهات والمقاطع الصوتية من:
🔹 YouTube  🔹 TikTok  🔹 Instagram 🔹 Facebook

فقط أرسل الرابط، واختر الصيغة التي تفضلها! 🚀
"""

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, START_MSG, parse_mode="Markdown")

@bot.message_handler(func=lambda message: "http" in message.text)
def handle_link(message):
    url = message.text
    
    # إنشاء أزرار الاختيار
    markup = types.InlineKeyboardMarkup()
    btn_video = types.InlineKeyboardButton("🎥 فيديو (Video)", callback_data=f"vid|{url}")
    btn_audio = types.InlineKeyboardButton("🎵 صوت (Audio)", callback_data=f"aud|{url}")
    markup.add(btn_video, btn_audio)
    
    bot.reply_to(message, "اختر نوع التحميل المطلوب:", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def download_choice(call):
    action, url = call.data.split("|")
    bot.edit_message_text("⏳ جاري المعالجة... قد يستغرق الأمر ثواني.", call.message.chat.id, call.message.message_id)
    
    ydl_opts = {
        'format': 'best' if action == "vid" else 'bestaudio/best',
        'outtmpl': 'downloaded_file.%(ext)s',
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)
            
            with open(filename, 'rb') as f:
                if action == "vid":
                    bot.send_video(call.message.chat.id, f, caption="تم التحميل بواسطة بوتك ✅")
                else:
                    bot.send_audio(call.message.chat.id, f, caption="تم التحميل بواسطة بوتك ✅")
            
            os.remove(filename) # حذف الملف بعد الإرسال لتوفير المساحة
    except Exception as e:
        bot.send_message(call.message.chat.id, f"❌ حدث خطأ: {str(e)}")

print("🚀 البوت الاحترافي يعمل الآن...")
bot.infinity_polling()
