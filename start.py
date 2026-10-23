import os
import time
import threading
import uvicorn

TELEGRAM_BOT_TOKEN = "8969205331:AAEbSajtwcmJ2NzlaMzg4Ksq0JkoQeURUqg"

# 1. إنشاء ملف bot.py تلقائياً للتيليجرام
bot_code = f"""
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

TELEGRAM_BOT_TOKEN = "{TELEGRAM_BOT_TOKEN}"
MPT_API_URL = "http://127.0.0.1:8080/api/v1/videos"

async def start(update, context):
    await update.message.reply_text("مرحباً بك! أرسل لي أي موضوع لتحويله إلى فيديو باستخدام MoneyPrinterTurbo 🎬")

async def handle_video_request(update, context):
    topic = update.message.text
    chat_id = update.message.chat_id
    await update.message.reply_text(f"⏳ جاري توليد الفيديو للموضوع: {{topic}}... يرجى الانتظار.")
    try:
        response = requests.post(MPT_API_URL, json={{"topic": topic, "video_subject": topic}})
        if response.status_code == 200:
            data = response.json()
            video_path = data.get("video_url") or data.get("path")
            if video_path:
                await context.bot.send_video(chat_id=chat_id, video=video_path, caption="✅ تم توليد الفيديو بنجاح!")
            else:
                await update.message.reply_text("⚠️ انتهت المعالجة، لكن لم يتم العثور على مسار الفيديو.")
        else:
            await update.message.reply_text(f"❌ حدث خطأ في النظام: {{response.status_code}}")
    except Exception as e:
        await update.message.reply_text(f"❌ خطأ غير متوقع: {{str(e)}}")

if __name__ == '__main__':
    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_video_request))
    print("🤖 Telegram Bot is running...")
    app.run_polling()
"""

with open("bot.py", "w", encoding="utf-8") as f:
    f.write(bot_code)

# 2. تشغيل بوت تيليجرام في الخلفية
def run_bot():
    time.sleep(6)
    print("🤖 بدء تشغيل بوت تيليجرام...")
    os.system("python bot.py")

bot_thread = threading.Thread(target=run_bot, daemon=True)
bot_thread.start()

# 3. تشغيل السيرفر بالمسار الصحيح وتجنب خطأ وحدة الاستيراد
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    print(f"🚀 تشغيل سيرفر MoneyPrinterTurbo على البورت {port}...")
    # التحقق من تشغيل الملف الأساسي للمشروع
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=False)
