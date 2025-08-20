import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import requests

# Get configuration from environment variables
TOKEN = os.environ['BOT_TOKEN']
CHANNEL_ID = os.environ.get('CHANNEL_ID', '@kpksahil')
# FIXED: Direct API URL - Environment variable nahi use karo
API_BASE_URL = "https://shadowscriptz.xyz/public_apis/smsbomberapi.php"

# Start Command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    try:
        member = await context.bot.get_chat_member(CHANNEL_ID, user_id)
        if member.status not in ["member", "administrator", "creator"]:
            keyboard = [[InlineKeyboardButton("📢 Join Channel", url=f"https://t.me/{CHANNEL_ID[1:]}")]]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await update.message.reply_text(
                "Bhai Sharafat se Channel Join tu pehly Kr le 😎",
                reply_markup=reply_markup
            )
            return
    except Exception as e:
        print(f"Channel check error: {e}")

    await update.message.reply_text("Meri Jaan Number Dail kr 923**** is trah ❤️")

# Message Handler (Number Search)
async def handle_number(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        text = update.message.text.strip()
        if not text.isdigit() or not text.startswith("92"):
            await update.message.reply_text("Sahi format use karo: 923XXXXXXXXX")
            return
        
        url = f"{API_BASE_URL}?num={text}"
        response = requests.get(url, timeout=10)
        await update.message.reply_text(response.text)
        
    except Exception as e:
        error_msg = f"Error: {str(e)}"
        print(error_msg)
        await update.message.reply_text("Server mein masla aa gaya. Thori der baad try karo.")

# FIXED: Webhook code hata kar simple polling use karo
def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_number))
    app.run_polling()  # ✅ Sirf yeh line rahegi

if __name__ == "__main__":
    main()
