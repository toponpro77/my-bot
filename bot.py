import os
import asyncio
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes, CallbackQueryHandler
import yt_dlp

# --- الإعدادات النهائية ---
TOKEN = "7832802757:AAFZVB4zmUrsf3X4KNJtk-7Ku30oXKM-5Ik"
ADMIN_ID = 6359223126 
CHANNEL_ID = "@nasar778" 
CHANNEL_LINK = "https://t.me/nasar778"

# معرف الملف الخاص بالهدية الذي أرسلته
GIFT_FILE_ID = "BQACAgQAAxkBAAO9aYohqEoVKbWGiGUy3U_G2SDuyIgAAqweAAJHcVBQ-CWCdtvLKG46BA"

async def is_subscribed(user_id, context):
    try:
        member = await context.bot.get_chat_member(chat_id=CHANNEL_ID, user_id=user_id)
        return member.status in ['member', 'administrator', 'creator']
    except:
        return False

async def download_video(url):
    ydl_opts = {
        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
        'outtmpl': 'video_%(id)s.%(ext)s',
        'merge_output_format': 'mp4',
        'quiet': True,
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        return ydl.prepare_filename(info)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if await is_subscribed(user_id, context):
        await update.message.reply_text("✅ أهلاً بك! أنت مشترك بالفعل. يمكنك الآن إرسال روابط يوتيوب للتحميل.")
    else:
        keyboard = [[InlineKeyboardButton("📢 اشترك في القناة", url=CHANNEL_LINK)],
                    [InlineKeyboardButton("✅ تم الاشتراك (استلام الهدية)", callback_data="check_sub")]]
        await update.message.reply_text("⚠️ يجب عليك الاشتراك في القناة أولاً لتفعيل البوت والحصول على هديتك:", reply_markup=InlineKeyboardMarkup(keyboard))

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id
    
    if await is_subscribed(user_id, context):
        await query.edit_message_text("✅ تم التحقق بنجاح! جاري إرسال هديتك...")
        # إرسال الملف (الهدية) تلقائياً باستخدام الـ File ID
        await context.bot.send_document(chat_id=user_id, document=GIFT_FILE_ID, caption="🎁 إليك هديتك الخاصة!")
        await context.bot.send_message(chat_id=user_id, text="🚀 الآن يمكنك البدء بتحميل فيديوهات يوتيوب بصوت عالي الجودة.")
    else:
        await query.message.reply_text("❌ لم يتم العثور على اشتراكك. فضلاً اشترك في القناة ثم اضغط على الزر.")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await is_subscribed(update.effective_user.id, context):
        await start(update, context)
        return

    url = update.message.text
    if "youtube.com" in url or "youtu.be" in url:
        msg = await update.message.reply_text("⏳ جاري معالجة الرابط وتحميل الفيديو مع الصوت...")
        try:
            file_path = await download_video(url)
            await update.message.reply_video(video=open(file_path, 'rb'), caption="✅ تم التحميل بنجاح!")
            os.remove(file_path)
        except Exception as e:
            await update.message.reply_text(f"❌ حدث خطأ أثناء التحميل: {str(e)}")
        finally:
            await msg.delete()

if __name__ == '__main__':
    application = ApplicationBuilder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button_handler))
    application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
    
    print("✅ البوت يعمل بنظام الهدية التلقائية (ملف)...")
    application.run_polling()
