from pyrogram import Client
from config import Config
from pymongo import MongoClient
from config import MONGO_URI

client = MongoClient(MONGO_URI)
db = client.randi_database


def init_bot():
    # Set up Pyrogram client
    api_id = Config.API_ID
    api_hash = Config.API_HASH
    bot_token = Config.BOT_TOKEN
    app = Client("my_bot", api_id, api_hash, bot_token=bot_token)

    return app
