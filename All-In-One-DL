import telebot
from telebot import types
from yt_dlp import YoutubeDL
import os
import threading
import static_ffmpeg

# جلب أدوات معالجة الفيديو تلقائياً لضمان العمل على Render
static_ffmpeg.add_paths()

# التوكن الخاص بك تم إدراجه هنا
API_TOKEN = '1576873297:AAEcH0Zu3obbOcebUByjnRQYOCpSCByiv0A'
bot = telebot.TeleBot(API_TOKEN)

user_links = {}

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "🎬 **أهلاً بك في بوت التحميل الذكي!**\n\nأرسل رابطاً من (Instagram, TikTok, YouTube, FB) وسأقوم بتحميله لك فوراً.")

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    url = message.text
    if "http" in url:
        user_links[message.chat.id] = url
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("🎥 فيديو", callback_data="video"),
                   types.InlineKeyboardButton("🎵 صوت MP3", callback_data="audio"))
        bot.reply_to(message, "اختر صيغة التحميل المطلوبة:", reply_markup=markup)
    else:
        bot.reply_to(message, "الرجاء إرسال رابط صحيح يبدأ بـ http")

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    url = user_links.get(call.message.chat.id)
    if not url:
        bot.answer_callback_query(call.id, "انتهت الجلسة، أرسل الرابط مرة أخرى.")
        return
    
    bot.edit_message_text("⏳ جاري المعالجة والتحميل... يرجى الانتظار.", call.message.chat.id, call.message.message_id)
    threading.Thread(target=download_and_send, args=(call.message, url, call.data)).start()

def download_and_send(msg, url, mode):
    file_name = f"file_{msg.chat.id}.{'mp4' if mode == 'video' else 'mp3'}"
    ydl_opts = {
        'format': 'best' if mode == 'video' else 'bestaudio/best',
        'outtmpl': file_name,
        'max_filesize': 48 * 1024 * 1024, # حماية للسيرفر لضمان عدم تجاوز 50 ميجا
    }
    
    try:
        with YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        
        with open(file_name, 'rb') as f:
            if mode == 'video':
                bot.send_video(msg.chat.id, f, caption="✨ تم التحميل بنجاح عبر بوتك!")
            else:
                bot.send_audio(msg.chat.id, f, caption="🎶 تم استخراج الصوت بنجاح!")
        
        os.remove(file_name) # حذف الملف لتوفير المساحة
    except Exception as e:
        bot.send_message(msg.chat.id, "❌ خطأ: الرابط غير مدعوم أو حجم الملف كبير جداً (يجب أن يكون أقل من 50 ميجا).")
        if os.path.exists(file_name): os.remove(file_name)

bot.infinity_polling()
