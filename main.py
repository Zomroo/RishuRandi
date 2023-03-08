import asyncio
import config
from pyrogram import Client
from waifu_bot import waifu_bot
from waifu_commands import waifu_commands
from waifu_inline import waifu_inline

if __name__ == "__main__":
    # Start Telegram client and event loop
    app = Client("my_bot", api_id=config.TELEGRAM_API_ID, api_hash=config.TELEGRAM_API_HASH, bot_token=config.TELEGRAM_TOKEN)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(asyncio.gather(app.start(), waifu_bot(), waifu_commands(), waifu_inline()))
    loop.run_forever()
