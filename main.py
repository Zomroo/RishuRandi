from pyrogram import Client, filters
from pyrogram.types import Message
from commands import *
from config import API_ID, API_HASH, BOT_TOKEN
from database import db

app = Client(
    "waifu_catcher_bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
    parse_mode="html"
)

# Add the command handlers using the `app.on_message()` decorator
@app.on_message(filters.command("start"))
async def start_command_handler(client: Client, message: Message):
    user_id = message.from_user.id
    user_name = message.from_user.first_name
    db.add_user(user_id, user_name)
    await start(message, client)

@app.on_message(filters.command("help"))
async def help_command_handler(client: Client, message: Message):
    await help(message, client)

@app.on_message(filters.command("waifu"))
async def catch_waifu_command_handler(client: Client, message: Message):
    user_id = message.from_user.id
    user_name = message.from_user.first_name
    waifu = db.get_waifu(user_id)

    if waifu:
        text = f"Sorry {user_name}, you already have a waifu named {waifu}. Use /randi to protect your waifu from getting caught."
    else:
        waifu = db.catch_waifu(user_id, user_name)
        text = f"Congratulations {user_name}, you have successfully caught a new waifu named {waifu}."
        
    await message.reply_text(text)

@app.on_message(filters.command("randi"))
async def protect_waifu_command_handler(client: Client, message: Message):
    user_id = message.from_user.id
    user_name = message.from_user.first_name
    waifu = db.get_waifu(user_id)

    if waifu:
        db.protect_waifu(user_id)
        text = f"Your waifu {waifu} is now protected from getting caught by other users."
    else:
        text = f"Sorry {user_name}, you don't have any waifus to protect. Use /waifu to catch a new waifu."
        
    await message.reply_text(text)

@app.on_message(filters.command("mywaifus"))
async def list_waifus_command_handler(client: Client, message: Message):
    user_id = message.from_user.id
    user_name = message.from_user.first_name
    waifus = db.get_all_waifus(user_id)

    if waifus:
        text = f"{user_name}, your waifus:\n\n"
        for waifu in waifus:
            text += f"- {waifu}\n"
    else:
        text = f"Sorry {user_name}, you don't have any waifus yet. Use /waifu to catch a new waifu."
        
    await message.reply_text(text)

if __name__ == "__main__":
    app.run()
