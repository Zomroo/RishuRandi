import os
import time
import pymongo
import pyrogram
from pyrogram import Client, filters
from pyrogram.types import Message
import config


# Connect to MongoDB
client = pymongo.MongoClient(config.MONGO_URI)
db = client[config.MONGO_DB_NAME]
collection = db[config.MONGO_COLLECTION_NAME]

# Create the Pyrogram client
app = Client(
    "my_bot",
    api_id=config.API_ID,
    api_hash=config.API_HASH,
    bot_token=config.API_TOKEN
)


# Define a command handler
@app.on_message(filters.command("start"))
async def start_handler(client: Client, message: Message):
    # Send a welcome message
    await message.reply_text("Welcome to the waifu catcher bot!")


# Define a command handler
@app.on_message(filters.command("catch"))
async def catch_handler(client: Client, message: Message):
    # Get the waifu name from the command
    waifu_name = message.text.split()[1]
    
    # Check if the waifu name is valid
    if waifu_name not in WAIFU_LIST:
        await message.reply_text("Invalid waifu name. Please try again.")
        return
    
    # Save the waifu in the user's database
    user_id = message.from_user.id
    collection.update_one(
        {"_id": user_id},
        {"$addToSet": {"waifus": waifu_name}},
        upsert=True
    )
    
    # Send a message to confirm the catch
    await message.reply_text(f"Congratulations! You caught {waifu_name}!")


# Define a command handler
@app.on_message(filters.command("mywaifu"))
async def mywaifu_handler(client: Client, message: Message):
    # Get the user's waifus from the database
    user_id = message.from_user.id
    user_data = collection.find_one({"_id": user_id})
    waifus = user_data.get("waifus", [])
    
    # Create a list of waifu names
    waifu_names = "\n".join(waifus) if waifus else "None"
    
    # Send a message with the user's waifus
    await message.reply_text(f"Here are your waifus:\n{waifu_names}")


# Run the bot
app.run()
