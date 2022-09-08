from telegram import Update
from telegram.ext import ContextTypes

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    # Make message an array and join it into a string with newlines later
    message = []
    message.append(f"Hi {update.effective_user.full_name}, I'm {context.bot.name}!")
    message.append(f"Send me links to download videos!")
    await context.bot.send_message(chat_id=update.effective_chat.id, text="\n".join(message))
