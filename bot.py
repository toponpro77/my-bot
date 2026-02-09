import os
import yt_dlp
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# --- الإعدادات الأساسية ---
TOKEN = "7832802757:AAGImT_NlBRXsp0PD4BUQoRjJYzTZ3vq228"
MY_ID = 12345678  # ⚠️ ضع هنا رقم ID حسابك الشخصي لتصلك الإشعارات

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    
    # 1. إشعار المطور (أنت) بدخول مستخدم جديد
    try:
        notification = (
            f"🔔 **مستخدم جديد انضم للبوت!**\n\n"
            f"👤 الاسم: {user.first_name}\n"
            f"🆔 الآيدي: `{user.id}`\n"
            f"🔗 اليوزر: @{user.username if user.username else 'لا يوجد'}"
        )
        await context.bot.send_message(chat_id=MY_ID, text=notification, parse_mode='Markdown')
    except:
        pass

    # 2. رسالة الترحيب الاحترافية والمختصرة
    welcome_text = (
        f"👋 **أهلاً بك {user.first_name} في بوت التحميل الشامل!**\n\n"
        "🚀 **ماذا يقدم لك البوت؟**\n"
        "• تحميل من: (TikTok, YouTube, Pinterest, Insta, Snap).\n"
        "• ميزة ذكية: يرسل لك الفيديو والصوت معاً تلقائياً.\n\n"
        "💡 **طريقة الاستخدام:**\n"
        "فقط أرسل رابط الفيديو، وسأقوم بالباقي!"
    )
    
    keyboard = [[InlineKeyboardButton("📢 مشاركة البوت", switch_inline_query="جرب أسرع بوت تحميل! 🔥")]]
    await update.message.reply_text(welcome_text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode='Markdown')

async def handle_download(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text.strip()
    if not url.startswith("http"):
        return

    status_msg = await update.message.reply_text("⏳ جاري تحضير الفيديو والصوت... يرجى الانتظار.")

    # إعدادات التحميل (تنزيل أفضل جودة فيديو وأفضل جودة صوت)
    # سيتم تنزيل الفيديو أولاً ثم استخراج الصوت منه
    ydl_opts_video = {
        'format': 'best[ext=mp4]/best',
        'outtmpl': 'downloads/%(id)s_video.%(ext)s',
        'quiet': True,
    }
    
    ydl_opts_audio = {
        'format': 'bestaudio/best',
        'outtmpl': 'downloads/%(id)s_audio.%(ext)s',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'quiet': True,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts_video) as ydl_v, yt_dlp.YoutubeDL(ydl_opts_audio) as ydl_a:
            # تحميل الفيديو
            info_v = ydl_v.extract_info(url, download=True)
            video_path = ydl_v.prepare_filename(info_v)
            
            # تحميل الصوت
            info_a = ydl_a.extract_info(url, download=True)
            audio_path = ydl_a.prepare_filename(info_a).rsplit('.', 1)[0] + ".mp3"

            await status_msg.edit_text("⚡ تم التحميل! جاري الإرسال...")

            # إرسال الفيديو والصوت معاً
            with open(video_path, 'rb') as v, open(audio_path, 'rb') as a:
                await update.message.reply_video(video=v, caption="🎬 تم تحميل الفيديو بنجاح")
                await update.message.reply_audio(audio=a, title=info_v.get('title'), caption="🎵 ملف الصوت المستخرج")

            # حذف الملفات بعد الإرسال
            if os.path.exists(video_path): os.remove(video_path)
            if os.path.exists(audio_path): os.remove(audio_path)
            await status_msg.delete()

    except Exception as e:
        await status_msg.edit_text("❌ عذراً، فشل التحميل. تأكد من أن الرابط عام وصحيح.")

def main():
    if not os.path.exists('downloads'): os.makedirs('downloads')
    app = Application.builder().token(TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_download))
    
    print("✅ البوت يعمل الآن ويراقب المستخدمين...")
    app.run_polling()

if __name__ == "__main__":
    main()
