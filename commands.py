from pyrogram import filters
from waifu import Waifu
from database import db

@Waifu.app.on_message(filters.command("start"))
async def start(_, message):
    await message.reply_text("Hi! I'm your waifu catcher bot.")

@Waifu.app.on_message(filters.command("waifu"))
async def waifu(_, message):
    waifu_name = message.text.split(" ", 1)[1].lower()
    waifu = await Waifu.get_waifu(waifu_name)
    if waifu:
        await Waifu.send_photo(message.chat.id, waifu["name"], waifu["photo"])
    else:
        await message.reply_text("There's no waifu with that name.")

@Waifu.app.on_message(filters.command("mywaifu"))
async def mywaifu(_, message):
    user_id = message.from_user.id
    waifus = db.users.find_one({"user_id": user_id})
    if waifus:
        waifus = waifus["waifus"]
        if waifus:
            waifu_list = "\n".join([waifu.capitalize() for waifu in waifus])
            await message.reply_text(f"Your waifus:\n\n{waifu_list}")
        else:
            await message.reply_text("You haven't protecced any waifus yet.")
    else:
        await message.reply_text("You haven't protecced any waifus yet.")
