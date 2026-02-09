import os
import yt_dlp
from datetime import datetime
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# التوكن الخاص بك
TOKEN = "7832802757:AAGImT_NlBRXsp0PD4BUQoRjJYzTZ3vq228"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """واجهة البوت والتعريف بالمهام"""
    welcome_text = (
        "🌟 **مرحباً بك في بوت الخدمات الذكي!**\n\n"
        "🚀 **ماذا يمكنني أن أفعل لك؟**\n"
        "1️⃣ **تحميل فيديوهات:** أرسل رابط من (تيك توك، إنستا، فيسبوك، يوتيوب، بينترست).\n"
        "2️⃣ **تحميل صوت (MP3):** أرسل الرابط متبوعاً بكلمة 'صوت' أو 'صوتية'.\n"
        "3️⃣ **حساب العمر:** أرسل تاريخ ميلادك بهذا الشكل: `1995/05/15` وسأحسب عمرك بالتفصيل.\n\n"
        "📢 **شارك البوت مع أصدقائك عبر الزر أدناه!**"
    )
    
    keyboard = [[InlineKeyboardButton("📢 مشاركة البوت", switch_inline_query="جرب هذا البوت المتكامل للتحميل وحساب العمر! 🔥")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(welcome_text, reply_markup=reply_markup, parse_mode='Markdown')

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    
    # 1. التحقق إذا كان الطلب حساب عمر (تاريخ)
    if "/" in text and len(text.split("/")) == 3:
        await calculate_age(update, text)
        return

    # 2. التحقق إذا كان الرابط لتحميل فيديو أو صوت
    if text.startswith(("http://", "https://")):
        is_audio = "صوت" in text or "صوتية" in text
        await download_content(update, text, is_audio)
    else:
        await update.message.reply_text("❌ عذراً، أرسل رابطاً صالحاً أو تاريخ ميلاد صحيح (مثلاً: 2000/01/01).")

async def calculate_age(update: Update, birth_date_str: str):
    """حساب العمر بالتفصيل"""
    try:
        birth_date = datetime.strptime(birth_date_str, "%Y/%m/%d")
        today = datetime.now()
        
        years = today.year - birth_date.year
        months = today.month - birth_date.month
        days = today.day - birth_date.day

        if days < 0:
            months -= 1
            days += 30
        if months < 0:
            years -= 1
            months += 12

        result = (
            f"📅 **تحليل عمرك بالتفصيل:**\n\n"
            f"✅ عمرك الآن: `{years}` سنة و `{months}` شهر و `{days}` يوم.\n"
            f"🎂 تاريخ ميلادك: `{birth_date.strftime('%Y-%m-%d')}`"
        )
        await update.message.reply_text(result, parse_mode='Markdown')
    except:
        await update.message.reply_text("⚠️ صيغة التاريخ خاطئة! يرجى الإرسال هكذا: سنة/شهر/يوم (مثال: 1998/12/30)")

async def download_content(update: Update, url: str, is_audio: bool):
    """تحميل الفيديو أو الصوت"""
    status_msg = await update.message.reply_text("⏳ جاري المعالجة... يرجى الانتظار.")
    
    # تنظيف الرابط من كلمة "صوت" إذا وجدت
    clean_url = url.replace("صوت", "").replace("صوتية", "").strip()

    ydl_opts = {
        'outtmpl': f'downloads/%(title)s.%(ext)s',
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
        ydl_opts.update({'format': 'best'})

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(clean_url, download=True)
            filename = ydl.prepare_filename(info)
            if is_audio: filename = filename.rsplit('.', 1)[0] + ".mp3"

            if is_audio:
                await update.message.reply_audio(audio=open(filename, 'rb'), caption="🎵 تم استخراج الصوت بنجاح.")
            else:
                await update.message.reply_video(video=open(filename, 'rb'), caption="🎬 تم تحميل الفيديو بنجاح.")
            
            os.remove(filename)
            await status_msg.delete()
    except Exception as e:
        await status_msg.edit_text("❌ حدث خطأ! تأكد من الرابط أو حاول لاحقاً.")

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    if not os.path.exists('downloads'): os.makedirs('downloads')
    app.run_polling()

if __name__ == "__main__":
    main()
