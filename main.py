import sqlite3
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

TOKEN = "8356832405:AAFk4r1XL04lFTjyuu4pD3ClmsrXpv19Sd8"

# Database setup
conn = sqlite3.connect("bot.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY,
    balance INTEGER DEFAULT 0
)
""")
conn.commit()

# Menu
keyboard = [
    ["🏠 Home", "💰 Balance"],
    ["📢 Earn", "👥 Referral"],
    ["💸 Withdraw"]
]

reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

# Start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    cursor.execute("INSERT OR IGNORE INTO users (user_id) VALUES (?)", (user_id,))
    conn.commit()

    await update.message.reply_text(
        "👋 Welcome to Earn Bot 💰",
        reply_markup=reply_markup
    )

# Message handler
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    text = update.message.text

    if text == "🏠 Home":
        await update.message.reply_text("🏠 Home Section")

    elif text == "💰 Balance":
        cursor.execute("SELECT balance FROM users WHERE user_id=?", (user_id,))
        balance = cursor.fetchone()[0]
        await update.message.reply_text(f"💰 Your Balance: {balance} TK")

    elif text == "📢 Earn":
        # demo earning
        cursor.execute("UPDATE users SET balance = balance + 1 WHERE user_id=?", (user_id,))
        conn.commit()
        await update.message.reply_text("📢 You earned 1 TK (Demo Task)")

    elif text == "👥 Referral":
        await update.message.reply_text(f"👥 Your ID: {user_id}")

    elif text == "💸 Withdraw":
        await update.message.reply_text("💸 Minimum withdraw: 10 TK")

# App
def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
