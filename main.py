from pyrogram import Client
from pyrogram import filters
from pyrogram.types import InlineQueryResultArticle, InputTextMessageContent
from init import init_bot
from config import Config


app = init_bot()


@app.on_message(filters.command("send_waifu"))
def send_waifu(client, message):
    # TODO: Implement this function
    pass


@app.on_message(filters.command("randi"))
def protect_waifu(client, message):
    # TODO: Implement this function
    pass


@app.on_message(filters.command("myrandi"))
def myrandi(client, message):
    # TODO: Implement this function
    pass


@app.on_inline_query()
def inline_query(client, inline_query):
    # TODO: Implement this function
    pass


if name == 'main':
    app.run()
