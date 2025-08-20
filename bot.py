import os
import random
import requests
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Configuration
TOKEN = os.environ['BOT_TOKEN']
CHANNEL_ID = os.environ.get('CHANNEL_ID', '@kpksahil')
API_BASE_URL = "https://shadowscriptz.xyz/public_apis/smsbomberapi.php"

# Start Command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    
    try:
        member = await context.bot.get_chat_member(CHANNEL_ID, user_id)
        if member.status not in ["member", "administrator", "creator"]:
            keyboard = [[InlineKeyboardButton("JOIN CHANNEL", url=f"https://t.me/{CHANNEL_ID[1:]}")]]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await update.message.reply_text(
                "Please join channel first then use this tool",
                reply_markup=reply_markup
            )
            return
    except Exception as e:
        print(f"Channel check error: {e}")

    await update.message.reply_text("R SAHIL BOMBER\n\nSend number in format: 923XXXXXXXXX")

# Message Handler (Number Search)
async def handle_number(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        text = update.message.text.strip()
        
        if not text.isdigit() or not text.startswith("92") or len(text) != 12:
            await update.message.reply_text("Invalid format! Use: 923XXXXXXXXX")
            return
        
        # API Call
        url = f"{API_BASE_URL}?num={text}"
        response = requests.get(url, timeout=15)
        
        if response.status_code == 200:
            await update.message.reply_text(f"R SAHIL BOMBER - Success\n\n{response.text}")
        else:
            await update.message.reply_text("Error: Target may be protected")
            
    except requests.Timeout:
        await update.message.reply_text("Server busy. Try again later")
    except Exception as e:
        print(f"Error: {e}")
        await update.message.reply_text("System error. Contact support")

# Main function - Simple and clean
def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_number))
    
    # Clean startup
    print("R SAHIL BOMBER - Bot Started")
    app.run_polling(drop_pending_updates=True)

if __name__ == "__main__":
    main()
