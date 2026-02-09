import os
import yt_dlp
import asyncio
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# التوكن الخاص بك
TOKEN = "7832802757:AAGImT_NlBRXsp0PD4BUQoRjJYzTZ3vq228"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """رسالة الترحيب والتعليمات"""
    welcome_text = (
        "👋 **أهلاً بك في بوت التحميل السريع!**\n\n"
        "📹 **لتحميل فيديو:** أرسل الرابط مباشرة.\n"
        "🎵 **لتحميل صوت (MP3):** أرسل الرابط متبوعاً بكلمة **صوت**.\n\n"
        "✅ **المنصات المدعومة:**\n"
        "TikTok, Instagram, Facebook, YouTube, Pinterest, Snapchat."
    )
    
    keyboard = [[InlineKeyboardButton("📢 مشاركة البوت", switch_inline_query="أفضل بوت لتحميل الفيديوهات والصوتيات! 🔥")]]
    await update.message.reply_text(welcome_text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='Markdown')

async def download_content(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url_text = update.message.text
    if not url_text.startswith("http"):
        return

    is_audio = "صوت" in url_text
    # تنظيف الرابط من الكلمات الإضافية
    url = url_text.replace("صوت", "").strip()
    
    status_msg = await update.message.reply_text("⏳ جاري المعالجة... قد يستغرق الأمر دقيقة.")

    # إعدادات التحميل الاحترافية
    ydl_opts = {
        'outtmpl': f'downloads/%(title)s.%(ext)s',
        'restrictfilenames': True,
        'noplaylist': True,
    }

    if is_audio:
        ydl_opts.update({
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        })
    else:
        # تحميل أفضل جودة فيديو متاحة لا تتعدى حجم محدد (لتجنب أخطاء التلجرام)
        ydl_opts.update({'format': 'best[ext=mp4]/best'})

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            file_path = ydl.prepare_filename(info)
            
            # إذا كان طلباً صوتياً، نقوم بتغيير الامتداد في المسار للبحث عن الملف الناتج
            if is_audio:
                file_path = os.path.splitext(file_path)[0] + ".mp3"

            await status_msg.edit_text("⚡ تم التحميل! جاري الرفع إلى تلجرام...")

            with open(file_path, 'rb') as f:
                if is_audio:
                    await update.message.reply_audio(audio=f, caption=f"🎵: {info.get('title')}")
                else:
                    await update.message.reply_video(video=f, caption=f"🎬: {info.get('title')}")

            # حذف الملف بعد الإرسال
            if os.path.exists(file_path):
                os.remove(file_path)
            await status_msg.delete()

    except Exception as e:
        print(f"Error: {e}")
        await status_msg.edit_text("❌ حدث خطأ! الرابط قد يكون خاصاً أو غير مدعوم حالياً.")

def main():
    if not os.path.exists('downloads'):
        os.makedirs('downloads')
        
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, download_content))
    
    print("البوت يعمل...")
    app.run_polling()

if __name__ == "__main__":
    main()
