import os
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
from keep_alive import keep_alive
import google.generativeai as genai

# ======= STARTUP =======
print("\n🚀 Starting up Gemini Telegram Bot...")

# ======= ENV CONFIG =======
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")

if not GEMINI_API_KEY:
    print("❌ GEMINI_API_KEY not found!")
    exit(1)

if not TELEGRAM_TOKEN:
    print("❌ TELEGRAM_TOKEN not found!")
    exit(1)

# ======= Gemini Setup =======
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("models/gemini-1.5-pro")  # Use available model

# ======= MESSAGE HANDLER =======
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.message.text:
        return await update.message.reply_text("❗ Please send a valid text message.")

    user_input = update.message.text
    print(f"📩 Received: {user_input}")

    try:
        response = model.generate_content(user_input)
        reply = response.text if hasattr(response, 'text') else str(response)
        await update.message.reply_text(reply)
        print("✅ Replied successfully")
    except Exception as e:
        error_message = f"❌ Error: {str(e)}"
        print(error_message)
        await update.message.reply_text(error_message)

# ======= MAIN =======
if __name__ == '__main__':
    keep_alive()
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("🤖 Gemini Telegram Bot is running...")
    print("✅ Ready to receive messages!")
    app.run_polling()
