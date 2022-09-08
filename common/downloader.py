from threading import Thread
from telegram import Bot
from datetime import datetime
from yt_dlp import YoutubeDL
from .utils import humanize_bytes
import time

class Downloader:
    url: str
    bot: Bot
    chat_id: int
    options: dict
    thread: Thread
    download_status: dict
    processing_status: dict
    def __init__(self, url: str, bot: Bot, chat_id: int, audio_only = False):
        self.url = url
        self.bot = bot
        self.chat_id = chat_id
        self.download_status = {}
        self.processing_status = {}
        
        options = {
            # 'outtmpl': 'cache/%(title)s.%(ext)s'.format(datetime.now().strftime('%Y%m%d-%H%M%S')),
            'ratelimit': 5242880,
            'progress_hooks': [self.download_hook],
            'postprocessor_hooks': [self.process_hook],
            'paths': {
                'home': 'cache'
            }
        }

        if audio_only:
            options['format'] = 'bestaudio'
            options['postprocessors'] = [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': 320
            }]
        else:
            options['format'] = 'bestvideo+bestaudio'
            options['postprocessors'] = [{
                'key': 'FFmpegVideoConvertor',
                'preferedformat': 'mp4'
            }]

        self.options = options

    async def run(self):
        def fn_downloader_thread():
            with YoutubeDL(self.options) as ydl:
                ydl.download([self.url])

        self.thread = Thread(target=fn_downloader_thread)
        self.thread.start()

        status_message = await self.bot.send_message(chat_id=self.chat_id, text=f"Downloading {self.url}")

        dots = 0
        while self.thread.is_alive():
            # Sometimes the message doesn't change at all and that's okay, but Telegram will get angy
            if not self.download_status.get('status') in ['error', 'finished']:
                try:
                    message = []
                    message.append(f"Downloading {self.url}")
                    message.append(f"Time Elapsed: {time.strftime('%H:%M:%S', time.gmtime(self.download_status.get('elapsed')))}")
                    message.append(f"Download Speed: {humanize_bytes(self.download_status.get('speed'))}/s")
                    message.append(f"ETA: {time.strftime('%H:%M:%S', time.gmtime(self.download_status.get('eta')))}")
                    await status_message.edit_text("\n".join(message))
                except:
                    pass
            elif self.processing_status.get('status'):
                message = []
                message.append(f"Processing {self.url}{'.'*dots}")
                await status_message.edit_text("\n".join(message))
                dots += 1

            time.sleep(2)

        await status_message.delete()


    def download_hook(self, d: dict):
        self.download_status = d
    
    def process_hook(self, d: dict):
        self.processing_status = d