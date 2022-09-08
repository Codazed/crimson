import yaml
import logging
import re
import asyncio
import yt_dlp
import os
import threading
from datetime import datetime
import time

import commands
import handlers

from telegram import Update, error
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

if __name__ == '__main__':
    with open('config.yml', 'r') as stream:
        for data in yaml.safe_load_all(stream):
            parsed_config = data
        token = parsed_config['token']
        authorized_users = parsed_config['authorized_users']

    bot = ApplicationBuilder().token(token).build()

    start_handler = CommandHandler('start', commands.start)
    bot.add_handler(start_handler)

    audio_handler = CommandHandler('audio', commands.audio)
    bot.add_handler(audio_handler)

    ping_handler = CommandHandler('ping', commands.ping)
    bot.add_handler(ping_handler)

    message_handler = MessageHandler(filters=filters.ALL, callback=handlers.message)
    bot.add_handler(message_handler)
    bot.run_polling()