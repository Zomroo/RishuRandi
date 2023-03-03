from pyrogram import Client
from database import db

async def start(message, client):
    user_id = message.from_user.id
    user_name = message.from_user.username
    db = get_db()
    db.users.insert_one({"user_id": user_id, "user_name": user_name})
    await message.reply("Welcome to the Waifu Catcher Bot! Use /help to see the list of available commands."
    )

async def help(message, client: Client):
    text = """
    <b>Commands List:</b>
    /start - Start the bot
    /help - Get a list of available commands
    /waifu - Catch a waifu
    /randi - Protect your waifu from getting caught
    /mywaifus - List all your waifus
    """
    await message.reply_text(text, parse_mode="html")
async def catch_waifu(message, client: Client):
    user_id = message.from_user.id
    user_name = message.from_user.first_name
    waifu = db.get_waifu(user_id)

    if waifu:
        text = f"Sorry {user_name}, you already have a waifu named {waifu}. Use /randi to protect your waifu from getting caught."
    else:
        waifu = db.catch_waifu(user_id, user_name)
        text = f"Congratulations {user_name}, you have successfully caught a new waifu named {waifu}."
        
    await message.reply_text(text)

async def protect_waifu(message, client: Client):
    user_id = message.from_user.id
    user_name = message.from_user.first_name
    waifu = db.get_waifu(user_id)

    if waifu:
        db.protect_waifu(user_id)
        text = f"Your waifu {waifu} is now protected from getting caught by other users."
    else:
        text = f"Sorry {user_name}, you don't have any waifus to protect. Use /waifu to catch a new waifu."
        
    await message.reply_text(text)
async def list_waifus(message, client: Client):
    user_id = message.from_user.id
    user_name = message.from_user.first_name
    waifus = db.list_waifus(user_id)

    if not waifus:
        text = f"Sorry {user_name}, you don't have any waifus. Use /waifu to catch a new waifu."
    else:
        text = f"Your waifus:\n\n"
        for index, waifu in enumerate(waifus):
            text += f"{index+1}. {waifu['name']}\n"

    await message.reply_text(text)

async def release_waifu(message, client: Client):
    user_id = message.from_user.id
    user_name = message.from_user.first_name
    waifu = db.get_waifu(user_id)

    if not waifu:
        text = f"Sorry {user_name}, you don't have any waifus to release. Use /waifu to catch a new waifu."
    else:
        db.release_waifu(user_id)
        text = f"You have successfully released your waifu {waifu}. Use /waifu to catch a new waifu."

    await message.reply_text(text)
async def list_waifus(message, client: Client):
    user_id = message.from_user.id
    user_name = message.from_user.first_name
    waifus = db.get_user_waifus(user_id)

    if not waifus:
        text = f"Sorry {user_name}, you don't have any waifus yet. Use /waifu to catch a new waifu."
    else:
        waifu_list = "\n".join([f"- {w}" for w in waifus])
        text = f"{user_name}, here are all your waifus:\n{waifu_list}"
        
    await message.reply_text(text)


async def release_waifu(message, client: Client):
    user_id = message.from_user.id
    user_name = message.from_user.first_name
    waifu = db.get_waifu(user_id)

    if not waifu:
        text = f"Sorry {user_name}, you don't have any waifus to release."
    else:
        db.release_waifu(user_id)
        text = f"{user_name}, your waifu {waifu} has been released and is now available to be caught by other users."
        
    await message.reply_text(text)


async def rename_waifu(message, client: Client):
    user_id = message.from_user.id
    user_name = message.from_user.first_name
    waifu = db.get_waifu(user_id)

    if not waifu:
        text = f"Sorry {user_name}, you don't have any waifus to rename."
    else:
        new_name = " ".join(message.text.split()[1:])
        db.rename_waifu(user_id, new_name)
        text = f"{user_name}, your waifu {waifu} has been renamed to {new_name}."
        
    await message.reply_text(text)

async def delete_user_data(message, client: Client):
    user_id = message.from_user.id
    user_name = message.from_user.first_name
    db.delete_user(user_id)
    text = f"All your data has been deleted, {user_name}."
    await message.reply_text(text)


async def error_handler(update, context):
    try:
        raise context.exception
    except Exception as e:
        print(f"An error occurred: {e}")

