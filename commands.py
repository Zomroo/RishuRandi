from pyrogram import Client, filters
from config import ADMIN_ID

class Commands:
    app = Client("waifu_catcher_bot")

    @app.on_message(filters.command("start", "/"))
    async def start(_, message):
        if message.chat.type == "private":
            await message.reply("Hello! I'm the Waifu Catcher Bot. To catch a waifu, use the command /waifu followed by the waifu's name.")
        else:
            await message.reply("Please use this bot in private messages only.")

    @app.on_message(filters.command("waifu", "/"))
    async def waifu(_, message):
        name = message.text.split(" ", 1)[-1].lower()
        waifu = await Waifu.get_waifu(name)
        if waifu is None:
            await message.reply("Sorry, I don't have that waifu.")
            return
        message_id = await Waifu.send_photo(message.chat.id, waifu["name"], waifu["photo"])
        if message_id is not None:
            db.pending_messages.insert_one({"message_id": message_id, "waifu_name": waifu["name"], "chat_id": message.chat.id})

    @app.on_message(filters.command("my", "/"))
    async def mywaifus(_, message):
        if message.chat.type == "private":
            user_id = message.from_user.id
            user = db.users.find_one({"user_id": user_id})
            if user is not None and "waifus" in user:
                waifus = "\n- ".join(user["waifus"])
                await message.reply(f"Your waifus:\n- {waifus}")
            else:
                await message.reply("You haven't protecced any waifus yet!")
        else:
            await message.reply("Please use this command in private messages only.")

Commands.app.run()
