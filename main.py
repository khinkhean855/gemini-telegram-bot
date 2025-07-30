import os
import google.generativeai as genai
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
from keep_alive import keep_alive

print("🚀 Starting up Gemini Bot...")

# ======= CONFIG =======
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")

# ======= ENV CHECK =======
if not GEMINI_API_KEY:
    print("❌ GEMINI_API_KEY not found in environment variables!")
    exit(1)

if not TELEGRAM_TOKEN:
    print("❌ TELEGRAM_TOKEN not found in environment variables!")
    exit(1)

# ======= GEMINI SETUP =======
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("models/gemini-pro")  # Correct model name

# ======= MESSAGE HANDLER =======
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message
    if message is None or message.text is None:
        return

    user_message = message.text
    print(f"📩 Received: {user_message}")

    try:
        response = model.generate_content(user_message)
        await message.reply_text(response.text)
        print("✅ Response sent.")
    except Exception as e:
        error_msg = f"Sorry, I encountered an error: {str(e)}"
        await message.reply_text(error_msg)
        print(f"❌ Error: {e}")

# ======= MAIN ENTRY =======
if __name__ == '__main__':
    keep_alive()  # Start Flask server for uptime monitoring

    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("🤖 Gemini Telegram Bot is running...")
    print("✅ Ready to receive messages!")

    app.run_polling()
