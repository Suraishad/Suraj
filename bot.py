import os
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters
import google.generativeai as genai

# Logging setup
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# API Keys (Yahan apni keys daalni hongi ya Environment variables use karne honge)
TELEGRAM_BOT_TOKEN = "APNA_TELEGRAM_BOT_TOKEN_YAHAN_DAALO"
GEMINI_API_KEY = "APNA_GEMINI_API_KEY_YAHAN_DAALO"

# Gemini configure
genai.configure(api_key=GEMINI_API_KEY)
# Fast aur smart model use kar rahe hain Jarvis ke liye
model = genai.GenerativeModel('gemini-2.5-flash')

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    try:
        # Jarvis style prompt instruction
        prompt = f"You are Jarvis, a highly intelligent, witty, and extremely fast AI assistant created by Tony Stark. Respond to this message in that persona (mix of English and Hinglish): {user_message}"
        response = model.generate_content(prompt)
        await update.message.reply_text(response.text)
    except Exception as e:
        await update.message.reply_text(f"Error aa gaya Boss: {e}")

if __name__ == '__main__':
    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
    print("Jarvis Bot is running...")
    app.run_polling()
