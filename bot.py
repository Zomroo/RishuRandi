import os
import time
import pymongo
import pyrogram
import random
import asyncio
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
    user_data = db.users.find_one({"user_id": user_id})

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
    waifus_data = db.waifus.find_one({"_id": "waifus"})
    waifus_names = waifus_data.get("names", [])

    # Update the global WAIFU_LIST variable
    global WAIFU_LIST
    WAIFU_LIST = waifus_names

# Define a function to send a random waifu to all users
async def send_random_waifu():
    while True:
        # Wait for 5 minutes
        await asyncio.sleep(10)

        # Choose a random waifu from the list
        waifu_name = random.choice(WAIFU_LIST)

        # Retrieve the list of user ids from the database
        user_ids = []
        async for user in db.users.find():
            user_ids.append(user["_id"])

        # Send the waifu to all users
        for user_id in user_ids:
            try:
                await app.send_photo(
                    chat_id=user_id,
                    photo=f"{waifu_name}.jpg",
                    caption=f"New waifu alert! You caught {waifu_name}!"
                )
            except pyrogram.errors.ChatWriteForbidden:
                # The bot doesn't have the permission to send messages to this chat
                pass

# Start the client
if __name__ == "__main__":
    # Start the task to load the waifus list from the database
    asyncio.get_event_loop().create_task(load_waifus())

    # Start the task to send a random waifu to all users
    asyncio.get_event_loop().create_task(send_random_waifu())

    # Start the Pyrogram client
    app.run()
