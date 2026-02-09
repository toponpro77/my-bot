import os
import yt_dlp
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# التوكن الخاص بك
TOKEN = "7832802757:AAGImT_NlBRXsp0PD4BUQoRjJYzTZ3vq228"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """المقدمة الاحترافية عند بدء البوت"""
    user_name = update.effective_user.first_name
    
    # نص المقدمة والتعليمات
    welcome_text = (
        f"👋 **أهلاً بك يا {user_name} في بوت التحميل الشامل!**\n\n"
        "🚀 **ماذا يمكنني أن أفعل لك؟**\n"
        "✨ **تنزيل الفيديوهات:** من (TikTok, Pinterest, Instagram, Facebook).\n"
        "✨ **تنزيل المقاطع الصوتية:** تحويل أي فيديو إلى ملف صووتي MP3 بجودة عالية.\n"
        "✨ **دعم الروابط:** أتعامل مع الروابط المباشرة والقصيرة لضمان التحميل.\n\n"
        "📖 **طريقة الاستخدام:**\n"
        "1️⃣ **للفيديو:** أرسل رابط المقطع مباشرة.\n"
        "2️⃣ **للصوت:** أرسل الرابط واكتب معه كلمة **'صوت'**.\n\n"
        "⚠️ *تأكد أن الحساب صاحب الفيديو عام وليس خاصاً لضمان عمل البوت.*"
    )

    # أزرار المشاركة والدعم
    keyboard = [
        [InlineKeyboardButton("📢 مشاركة البوت", switch_inline_query="أفضل بوت لتحميل الفيديوهات والصوتيات! 🔥")],
        [InlineKeyboardButton("👨‍💻 مطور البوت", url="https://t.me/BotFather")] # يمكنك استبدال الرابط بحسابك
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(welcome_text, reply_markup=reply_markup, parse_mode='Markdown')

async def handle_download(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    if not text.startswith("http"):
        return

    is_audio = "صوت" in text
    url = text.replace("صوت", "").strip()
    
    status_msg = await update.message.reply_text("⏳ جاري معالجة طلبك... يرجى الانتظار.")

    ydl_opts = {
        'outtmpl': 'downloads/%(title)s.%(ext)s',
        'quiet': True,
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
        ydl_opts.update({'format': 'best[ext=mp4]/best'})

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            file_path = ydl.prepare_filename(info)
            
            if is_audio:
                file_path = os.path.splitext(file_path)[0] + ".mp3"

            await status_msg.edit_text("⚡ تم التحميل بنجاح! جاري الإرسال...")

            with open(file_path, 'rb') as f:
                if is_audio:
                    await update.message.reply_audio(audio=f, title=info.get('title'))
                else:
                    await update.message.reply_video(video=f, caption=f"🎬: {info.get('title')}")

            if os.path.exists(file_path):
                os.remove(file_path)
            await status_msg.delete()

    except Exception as e:
        await status_msg.edit_text("❌ عذراً، حدث خطأ. تأكد من صحة الرابط أو جرب رابطاً آخر.")

def main():
    if not os.path.exists('downloads'): os.makedirs('downloads')
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_download))
    
    print("✅ البوت يعمل الآن...")
    app.run_polling()

if __name__ == "__main__":
    main()
