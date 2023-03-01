from pyrogram import Client, filters
from pymongo.errors import DuplicateKeyError
from database import db

class Waifu:
    app = Client("waifu_catcher_bot")
    waifus = [
        {"name": "waifu1", "photo": "https://example.com/waifu1.jpg"},
        {"name": "waifu2", "photo": "https://example.com/waifu2.jpg"},
        {"name": "waifu3", "photo": "https://example.com/waifu3.jpg"}
    ]

    @classmethod
    async def get_waifu(cls, name):
        for waifu in cls.waifus:
            if waifu["name"] == name:
                return waifu
        return None

    @classmethod
    async def send_photo(cls, chat_id, caption, photo):
        try:
            message = await cls.app.send_photo
