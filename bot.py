import os
import yt_dlp
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, CallbackQueryHandler, ContextTypes, filters

TOKEN = "8192666745:AAGjgMY_nM71CNzbbtA4baROqcJHdNFf97M"

# START COMMAND
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("⬇ Download Video", callback_data="download")],
        [InlineKeyboardButton("🤖 Chatbot Help", callback_data="chatbot")]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        "Welcome! I can download videos from social media.\n\nSend a link or use the buttons.",
        reply_markup=reply_markup
    )

# BUTTON HANDLER
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "download":
        await query.edit_message_text("Send me a TikTok, YouTube, or Instagram link.")

    elif query.data == "chatbot":
        await query.edit_message_text("Send a message like 'hello' or 'help'.")

# VIDEO DOWNLOADER
async def download_video(update: Update, context: ContextTypes.DEFAULT_TYPE):

    url = update.message.text

    if "http" in url:

        await update.message.reply_text("Downloading video...")

        ydl_opts = {
            'outtmpl': 'video.%(ext)s'
        }

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                filename = ydl.prepare_filename(info)

            await update.message.reply_text("Sending video...")

            await update.message.reply_video(video=open(filename, "rb"))

            os.remove(filename)

        except Exception as e:
            await update.message.reply_text("Failed to download video.")

# CHATBOT
async def chatbot(update: Update, context: ContextTypes.DEFAULT_TYPE):

    text = update.message.text.lower()

    if "hello" in text:
        await update.message.reply_text("Hello 👋 How can I help?")

    elif "help" in text:
        await update.message.reply_text("Send a video link and I will download it.")

    elif "hi" in text:
        await update.message.reply_text("Hi there!")

# MAIN
app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(button))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, download_video))
app.add_handler(MessageHandler(filters.TEXT, chatbot))

print("Bot running...")

app.run_polling()