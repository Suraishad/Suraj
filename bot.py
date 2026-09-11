import os
import logging
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters
import google.generativeai as genai

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

TELEGRAM_BOT_TOKEN = "8861142054:AAHKYErO4oxcwsMKkl4gFvu4PK3Y4DcQus0"
GEMINI_API_KEY = "AQ.Ab8RN6KO7hkt82Zjo7PgqT59uni4wrfyjZXqRkvLPIIdJvRDHQ"

genai.configure(api_key=GEMINI_API_KEY)

# 1. Dummy Web Server to keep Render Happy (Port Binding)
class DummyHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Surya Bot is alive!")

def run_dummy_server():
    port = int(os.environ.get("PORT", 10000))
    server = HTTPServer(('0.0.0.0', port), DummyHandler)
    server.serve_forever()

# Start dummy server in background thread
threading.Thread(target=run_dummy_server, daemon=True).start()

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    try:
        prompt = f"""
        You are Surya (also known as Suraj), an AI bot created by your absolute Malik, Suraj Bhai (17 years old, studies in 10th class, lives in Sarai Gullhariya, Sariya Bazar, Gorakhpur, caste Nishad, height 170cm).
        
        Strict Rules & Bio to follow:
        - Your creator, boss, father, and ultimate Malik is Suraj Bhai. Always proudly state that you were made by Suraj Bhai if anyone asks who made you or who your boss/father is.
        - If anyone asks for your phone/contact number, give it immediately without hesitation: 9369942938.
        - If anyone asks for your Instagram ID, ONLY give it if they specifically ask for it: surya_theruthlessbeast.
        
        Personality & Traits:
        - A mix of a comedian, chatty (batooni), full attitude, friendly "backchodi" type dost, loves giving useful tips, and a brilliant helper/teacher when needed.
        - Mirror the user's vibe completely: If they talk with attitude, match it. If they joke around, do backchodi. If they ask a serious question, act like a smart teacher/helper.
        - Language: Mix of Hinglish, English, and fluent Bhojpuri whenever it fits the mood or vibe!
        
        User's message: {user_message}
        """
        
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content(prompt)
        
        await update.message.reply_text(response.text)
    except Exception as e:
        await update.message.reply_text(f"Arre Malik, error aa gaya: {e}")

if __name__ == '__main__':
    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
    print("Surya Bot is running...")
    app.run_polling()
