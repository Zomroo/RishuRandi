from pyrogram import Client, filters
from pymongo.errors import DuplicateKeyError
from database import db
import random
import time

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
            message = await cls.app.send_photo(
                chat_id=chat_id,
                photo=photo,
                caption=caption,
                reply_markup={"inline_keyboard": [[{"text": "Protecc", "callback_data": f"protecc_{caption.lower()}"}]]}
            )
            return message.message_id
        except Exception as e:
            print(e)
            return None

    @classmethod
    async def delete_message(cls, chat_id, message_id):
        try:
            await cls.app.delete_messages(chat_id, message_id)
        except Exception as e:
            print(e)

    @classmethod
    async def protecc(cls, user_id, waifu_name):
        try:
            db.users.update_one({"user_id": user_id}, {"$addToSet": {"waifus": waifu_name}}, upsert=True)
        except DuplicateKeyError:
            pass

    @classmethod
    async def handle_callback(cls, _, callback_query):
        user_id = callback_query.from_user.id
        waifu_name = callback_query.data.split("_")[1]
        cls.protecc(user_id, waifu_name)
        await callback_query.answer(f"You have protecced {waifu_name}!")
        time.sleep(10)
        cls.delete_message(callback_query.message.chat.id, callback_query.message.message_id)

    @classmethod
    async def list_waifus(cls, _, query):
        results = []
        for waifu in cls.waifus:
            results.append({
                "type": "photo",
                "id": str(random.randint(0, 999999999)),
                "photo_url": waifu["photo"],
                "thumb_url": waifu["photo"],
                "caption": waifu["name"],
                "reply_markup": {"inline_keyboard": [[{"text": "Protecc", "callback_data": f"protecc_{waifu['name'].lower()}"}]]}
            })
        await cls.app.answer_inline_query(query.id, results)

Waifu.app.on_callback_query(filters.regex("^protecc_"), Waifu.handle_callback)
Waifu.app.on_inline_query(Waifu.list_waifus)
