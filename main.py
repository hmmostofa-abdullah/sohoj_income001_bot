from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

TOKEN = "8356832405:AAFk4r1XL04lFTjyuu4pD3ClmsrXpv19Sd8"

# Menu Buttons
keyboard = [
    ["🏠 Home", "💰 Balance"],
    ["📢 Earn", "👥 Referral"],
    ["💸 Withdraw"]
]

reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    await update.message.reply_text(
        f"👋 স্বাগতম {user.first_name}!\n\n"
        "আমাদের Earn Bot-এ আপনাকে স্বাগতম 💰",
        reply_markup=reply_markup
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    if text == "🏠 Home":
        await update.message.reply_text("🏠 তুমি Home এ আছো")

    elif text == "💰 Balance":
        await update.message.reply_text("💰 তোমার ব্যালেন্স: 0 TK")

    elif text == "📢 Earn":
        await update.message.reply_text("📢 এখানে তুমি কাজ করে আয় করতে পারবে (পরের ধাপে যোগ হবে)")

    elif text == "👥 Referral":
        await update.message.reply_text("👥 তোমার রেফারেল লিংক পরে যোগ করা হবে")

    elif text == "💸 Withdraw":
        await update.message.reply_text("💸 মিনিমাম উইথড্র 100 TK")

def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
