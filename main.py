import os
import pymongo
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

# Import database functions
from database import save_waifu

# Create Pyrogram client instance
api_id = os.environ.get("API_ID")
api_hash = os.environ.get("API_HASH")
bot_token = os.environ.get("BOT_TOKEN")
app = Client("waifu_catcher_bot", api_id, api_hash, bot_token=bot_token)

# Create MongoDB client instance and connect to database
mongo_client = pymongo.MongoClient(os.environ.get("MONGO_URL"))
db = mongo_client["waifu_db"]


# Start command
@app.on_message(filters.command("start"))
async def start_command(client, message):
    # Send welcome message
    await message.reply_text("Welcome to Waifu Catcher Bot!")


# Add command
@app.on_message(filters.private & filters.command("add"))
async def add_command(client, message):
    # Ask for waifu picture
    await message.reply_text("Please send me a picture of your waifu.")

    # Wait for waifu picture
    waifu_picture = await app.listen(message.chat.id)

    # Ask for waifu name
    await message.reply_text("Please tell me the name of your waifu.")

    # Wait for waifu name
    waifu_name = await app.listen(message.chat.id)

    # Create inline keyboard with rarity options
    rarity_keyboard = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("Common", callback_data="common"),
                InlineKeyboardButton("Rare", callback_data="rare"),
            ],
            [
                InlineKeyboardButton("Epic", callback_data="epic"),
                InlineKeyboardButton("Legendary", callback_data="legendary"),
            ],
        ]
    )

    # Ask for waifu rarity
    await message.reply_text(
        "Please select the rarity of your waifu:", reply_markup=rarity_keyboard
    )

    # Wait for waifu rarity
    waifu_rarity = await app.listen(message.chat.id)

    # Send waifu preview with name and rarity
    await client.send_photo(
        message.chat.id,
        waifu_picture.audio or waifu_picture.document or waifu_picture.photo or waifu_picture.video,
        caption=f"{waifu_name.text}\nRarity: {waifu_rarity.data}",
    )

    # Save waifu in database
    save_waifu(db, waifu_name.text, waifu_rarity.data)
    
    # Send message to owner to confirm successful addition
    await message.reply_text("Waifu added successfully!")


# Done command
@app.on_message(filters.private & filters.command("done"))
async def done_command(client, message):
    # Send message to owner informing them that the command is only available in group chats
    await message.reply_text("This command is only available in group chats.")


# Catch callback queries from inline keyboards
@app.on_callback_query()
async def catch_callback_query(client, query):
    # Answer callback query
    await query.answer()

    # Send message to owner informing them that the command is only available in group chats
    await query.message.reply_text(
        "This command is only available in group chats.", reply_markup=None
    )


# Run the bot
app.run()
