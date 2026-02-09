import os
import yt_dlp
import asyncio
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# التوكن الخاص بك
TOKEN = "7832802757:AAGImT_NlBRXsp0PD4BUQoRjJYzTZ3vq228"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """واجهة البوت الاحترافية عند البدء"""
    user = update.effective_user
    
    # رسالة المهام والتعليمات
    welcome_text = (
        f"👋 **أهلاً بك يا {user.first_name} في Ultimate Downloader!**\n\n"
        "🚀 **ما هي قدرات هذا البوت؟**\n"
        "✨ تحميل من **تيك توك** (بدون علامة مائية).\n"
        "✨ تحميل من **إنستغرام** (Reels و فيديوهات).\n"
        "✨ تحميل من **فيسبوك** بجودة عالية.\n"
        "✨ تحميل من **بينترست** (Pinterest).\n"
        "✨ تحميل من **سناب شات** و **يوتيوب**.\n\n"
        "📖 **طريقة الاستخدام:**\n"
        "فقط أرسل رابط الفيديو، وسأقوم بالباقي!"
    )

    # أزرار التفاعل (مشاركة البوت)
    keyboard = [
        [
            InlineKeyboardButton("📢 مشاركة البوت", switch_inline_query="جرب هذا البوت الرهيب لتحميل الفيديوهات! 🔥")
        ],
        [
            InlineKeyboardButton("👨‍💻 المطور", url="https://t.me/BotFather") # يمكنك وضع رابط حسابك هنا
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(welcome_text, reply_markup=reply_markup, parse_mode='Markdown')

async def download_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text
    
    # التحقق من أن النص المرسل هو رابط
    if not url.startswith(("http://", "https://")):
        return

    status_msg = await update.message.reply_text("🔍 جاري فحص الرابط واستخراج الفيديو...")

    # إعدادات yt-dlp المتقدمة لدعم كافة المنصات
    ydl_opts = {
        'format': 'best',
        'outtmpl': f'downloads/{update.effective_user.id}_%(title)s.%(ext)s',
        'quiet': True,
        'no_warnings': True,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # استخراج المعلومات والتحميل
            info = ydl.extract_info(url, download=True)
            file_path = ydl.prepare_filename(info)
            
            await status_msg.edit_text("⚡ تم التحميل بنجاح! جاري إرسال الفيديو...")

            # إرسال الفيديو
            with open(file_path, 'rb') as video:
                await update.message.reply_video(
                    video=video, 
                    caption=f"✅ تم التحميل بواسطة: @{context.bot.username}\n🎬 العنوان: {info.get('title', 'Video')}"
                )
            
            # حذف الملف من السيرفر لتوفير المساحة
            if os.path.exists(file_path):
                os.remove(file_path)
            
            await status_msg.delete()

    except Exception as e:
        await status_msg.edit_text(f"❌ عذراً، لا يمكن تحميل هذا الرابط حالياً.\nتأكد أن الحساب عام وليس خاص.")
        print(f"Error: {e}")

def main():
    # بناء التطبيق
    application = Application.builder().token(TOKEN).build()

    # الأوامر والمراقبين
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, download_video))

    print("✅ البوت يعمل الآن بنجاح...")
    application.run_polling()

if __name__ == '__main__':
    # إنشاء مجلد التحميل إذا لم يكن موجوداً
    if not os.path.exists('downloads'):
        os.makedirs('downloads')
    main()
