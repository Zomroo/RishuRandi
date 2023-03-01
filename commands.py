from pyrogram import Client, filters
from config import ADMIN_ID
from waifu import Waifu
from database import db


class StartCommand:
    app = Client("waifu_catcher_bot")

    @app.on_message(filters.command("start", "/") & filters.private)
    async def start(_, message):
        await message.reply("Hello! I'm the Waifu Catcher Bot. To catch a waifu, use the command /waifu followed by the waifu's name.")

class HelpCommand:
    app = Client("waifu_catcher_bot")

    @app.on_message(filters.command("help", "/"))
    async def help(_, message):
        help_text = '''
        Here are the available commands:
        /start - Start the bot
        /help - Show this help message
        /waifu waifu_name - Catch a waifu with the given name
        /randi waifu_name - Protect a waifu with the given name
        /myrandi - Show your protected waifus
        '''
        await message.reply_text(help_text)
