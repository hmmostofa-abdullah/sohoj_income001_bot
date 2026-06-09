import sqlite3
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

TOKEN = "8356832405:AAFk4r1XL04lFTjyuu4pD3ClmsrXpv19Sd8"

conn = sqlite3.connect("bot.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY,
    balance INTEGER DEFAULT 0,
    ref_by INTEGER
)
""")
conn.commit()

keyboard = [
    ["🏠 Home", "💰 Balance"],
    ["📢 Earn", "👥 Referral"],
    ["💸 Withdraw"]
]

reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

# START with referral
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    ref_id = None
    if context.args:
        ref_id = context.args[0]

    cursor.execute("SELECT * FROM users WHERE user_id=?", (user_id,))
    user = cursor.fetchone()

    if not user:
        cursor.execute("INSERT INTO users (user_id, ref_by) VALUES (?, ?)", (user_id, ref_id))
        conn.commit()

        # referral bonus
        if ref_id:
            cursor.execute("UPDATE users SET balance = balance + 2 WHERE user_id=?", (ref_id,))
            conn.commit()

    await update.message.reply_text(
        "👋 Welcome to Earn Bot 💰",
        reply_markup=reply_markup
    )

# HANDLE
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    text = update.message.text

    if text == "💰 Balance":
        cursor.execute("SELECT balance FROM users WHERE user_id=?", (user_id,))
        balance = cursor.fetchone()[0]
        await update.message.reply_text(f"💰 Balance: {balance} TK")

    elif text == "👥 Referral":
        bot_username = "@sohoj_income001_bot"
        link = f"https://t.me/{bot_username}?start={user_id}"
        await update.message.reply_text(f"👥 Your Referral Link:\n{link}")

def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("Bot running...")
    app.run_polling()

if __name__ == "__main__":
    main()
