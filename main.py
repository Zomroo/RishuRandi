from pyrogram import Client, filters
from commands import *
from config import API_ID, API_HASH, BOT_TOKEN

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
    await start(message, client)

@app.on_message(filters.command("help"))
async def help_command_handler(client: Client, message: Message):
    await help(message, client)

@app.on_message(filters.command("waifu"))
async def catch_waifu_command_handler(client: Client, message: Message):
    await catch_waifu(message, client)

@app.on_message(filters.command("randi"))
async def protect_waifu_command_handler(client: Client, message: Message):
    await protect_waifu(message, client)

@app.on_message(filters.command("mywaifus"))
async def list_waifus_command_handler(client: Client, message: Message):
    await list_waifus(message, client)

if __name__ == "__main__":
    app.run()
