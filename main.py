from pyrogram import Client
from commands import *
from config import API_ID, API_HASH, BOT_TOKEN

app = Client(
    "waifu_catcher_bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
    parse_mode="html"
)

if __name__ == "__main__":
    app.run()
