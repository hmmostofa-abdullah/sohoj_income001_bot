from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# এখানে তোমার Bot Token বসাবে
TOKEN = "8356832405:AAFk4r1XL04lFTjyuu4pD3ClmsrXpv19Sd8"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    await update.message.reply_text(
        f"👋 স্বাগতম {user.first_name}!\n\n"
        "আমি তোমার Earn Bot চালু করেছি ✅\n"
        "এখন আমরা ধাপে ধাপে system তৈরি করব।"
    )

def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))

    print("Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
