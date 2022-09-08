import re
import time
import os
from telegram import Update
from telegram.ext import ContextTypes

from common import Downloader, humanize_bytes

async def message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url_regex = "(?P<url>https?://[^\s]+)"

    url = re.search(url_regex, update.message.text)

    if not url:
        return

    url = url.group("url")

    downloader = Downloader(url, context.bot, update.effective_chat.id, False)
    await downloader.run()

    final_filename = downloader.processing_status['info_dict']['filepath']

    if os.path.getsize(final_filename) > 50000000:
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Sorry, the resulting file is too big to send, and I don't support transcoding yet. 😭\nTry a shorter video.")
    else:
        await context.bot.send_video(chat_id=update.effective_chat.id, video=open(final_filename, 'rb'), supports_streaming=True)

    os.remove(final_filename)
