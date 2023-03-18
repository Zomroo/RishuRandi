import os
import time
import pymongo
import pyrogram
import random
import asyncio
from pyrogram import Client, filters
from pyrogram.types import Message
import config
from waifu import get_random_waifu

# Connect to MongoDB
client = pymongo.MongoClient(config.MONGO_URI)
db = client[config.MONGO_DB_NAME]
collection = db[config.MONGO_COLLECTION_NAME]

# Create the Pyrogram client
api_id = config.API_ID
api_hash = config.API_HASH
bot_token = config.API_TOKEN
app = Client("my_bot", api_id=api_id, api_hash=api_hash, bot_token=bot_token)

# Define a list of waifus
WAIFU_LIST = []

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
async def mywaifu_handler(client, message):
    # Get the user ID
    user_id = message.from_user.id

    # Retrieve the user data from the database
    user_data = collection.find_one({"_id": user_id})

    if user_data is None:
        # User not found in the database
        await message.reply_text("You haven't added any waifus yet.")
        return

    # Retrieve the waifus list from the user data
    waifus = user_data.get("waifus", [])

    if not waifus:
        # Waifus list is empty
        await message.reply_text("You haven't added any waifus yet.")
        return

    # Build the message with the user's waifus
    waifu_list = "\n- ".join(waifus)
    message_text = f"Your waifus:\n- {waifu_list}"

    # Reply to the user with the waifus list
    await message.reply_text(message_text)
# Define a function to load the waifus list from the database
async def load_waifus():
    # Retrieve the waifus list from the database
    waifus_data = collection.find_one({"_id": "waifus"})
    if waifus_data is None:
        # Handle the case where no data was returned
        print("No waifus found in the database.")
        return
    waifus_names = waifus_data.get("names", [])

    # Update the global WAIFU_LIST variable
    global WAIFU_LIST
    WAIFU_LIST = waifus_names

# Function to send a random waifu image to a group chat
def send_waifu():
    # Get a random waifu from the database
    waifus = collection.find_one({"_id": "waifus"})
    if waifus is None or not waifus["names"]:
        print("No waifus found in the database.")
        return

    name = random.choice(waifus["names"])
    image_url = waifus["images"][waifus["names"].index(name)]

    # Send the waifu image to a random group chat where the bot is a member
    group_chats = [chat for chat in app.getUpdates() if chat.message.chat.type == pyrogram.Chat.PRIVATE]
    if not group_chats:
        print("Bot is not a member of any group chat.")
        return

    group_chat = random.choice(group_chats).message.chat
    app.send_photo(chat_id=group_chat.id, photo=image_url, caption=f"Here's your waifu: {name}")

# Start the client
if __name__ == "__main__":
    # Load the waifus list from the database
    asyncio.get_event_loop().run_until_complete(load_waifus())

    # Start the Pyrogram client
    app.start()

    # Send waifus every 10 seconds
    while True:
        send_waifu()
        time.sleep(10)

    # Stop the client
    app.stop()
