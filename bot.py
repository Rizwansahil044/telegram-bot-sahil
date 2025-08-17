from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import requests

# Config
TOKEN = "8242730853:AAFeXmR_3mnp7jQRLkqkOs6Pd-hzBtMoFzE"
CHANNEL_ID = "@kpksahil"
API_URL = "https://famofcfallxd.serv00.net/apis/api.php?number={}&amount=1"

# Start Command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    member = await context.bot.get_chat_member(CHANNEL_ID, user_id)

    if member.status not in ["member", "administrator", "creator"]:
        keyboard = [[InlineKeyboardButton("📢 Join Channel", url=f"https://t.me/{CHANNEL_ID[1:]}")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text(
            "Bhai Sharafat se Channel Join tu pehly Kr le 😎",
            reply_markup=reply_markup
        )
        return

    await update.message.reply_text("Meri Jaan Number Dail kr 923**** is trah ❤️")

# Message Handler (Number Search)
async def handle_number(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()
    if not text.isdigit() or not text.startswith("92"):
        await update.message.reply_text("Sahi format use karo: 923XXXXXXXXX")
        return
    
    url = API_URL.format(text)
    try:
        r = requests.get(url, timeout=10)
        result = r.text
    except Exception as e:
        result = f"Error: {e}"

    await update.message.reply_text(result)

# Main
def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_number))
    app.run_polling()

if __name__ == "__main__":
    main()