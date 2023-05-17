# main.py

import os
import logging
from pymongo import MongoClient
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors import BotInlineDisabled

from config import Config

# Connect to MongoDB
mongo_client = MongoClient(Config.MONGO_URL)
db = mongo_client[Config.DB_NAME]

# Get the waifus collection
waifus_collection = db[Config.MONGO_COLLECTION_NAME]

# Create the Pyrogram Client
bot = Client(
    'waifu_bot',
    api_id=Config.API_ID,
    api_hash=Config.API_HASH,
    bot_token=Config.BOT_TOKEN
)


@bot.on_message(filters.command('start'))
def start_command(client, message):
    bot_name = bot.get_me().username
    text = f"Hello! I'm {bot_name}, your waifu bot. Use /add command to add a waifu."
    message.reply_text(text)


@bot.on_message(filters.command('add') & filters.private & filters.bot)
def add_waifu(client, message):
    try:
        chat_id = message.from_user.id
        message.reply_text("Please send me a waifu picture.")
        bot.register_next_step_handler(message, save_waifu, chat_id)
    except BotInlineDisabled:
        pass


def save_waifu(client, message, chat_id):
    if message.photo:
        # Get the largest photo size
        photo = message.photo[-1].file_id
        message.reply_text("Please provide a name for the waifu.")
        bot.register_next_step_handler(message, save_name, chat_id, photo)


def save_name(client, message, chat_id, photo):
    name = message.text.strip()
    if name:
        # Create a preview message with the waifu picture and name
        preview_text = f"Name: {name}\n\nSave or delete?"
        preview_message = message.reply_photo(
            photo=photo,
            caption=preview_text,
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton('Save', callback_data='save')],
                [InlineKeyboardButton('Delete', callback_data='delete')]
            ])
        )
        # Store the waifu details in the database
        waifus_collection.insert_one({
            'chat_id': chat_id,
            'name': name,
            'photo': photo,
            'preview_message_id': preview_message.message_id
        })


@bot.on_callback_query()
def handle_callback(client, callback_query):
    query = callback_query.data
    message = callback_query.message
    chat_id = message.chat.id

    if query == 'save':
        # Retrieve the waifu details from the database
        waifu = waifus_collection.find_one({'chat_id': chat_id})
        if waifu:
            # Save the waifu picture with a serial number
            serial_number = waifus_collection.count_documents({})
            file_id = waifu['photo']
            file_path = client.download_media(file_id, file_name=f'{serial_number}.jpg')
            message.reply_text(f"Waifu saved with serial number {serial_number}.")
        else:
            message.reply_text("Waifu details not found.")
    elif query == 'delete':
        # Retrieve the waifu details from the database
        waifu = waifus_collection.find_one({'chat_id': chat_id})
        if waifu:
            # Delete the waifu details and the preview message
            waifus_collection.delete_one({'chat_id': chat_id})
            message.reply_text("Waifu deleted.")
            client.delete_messages(chat_id, message.message_id)
            client.delete_messages(chat_id, waifu['preview_message_id'])
        else:
            message.reply_text("Waifu details not found.")


# Start the bot
if __name__ == '__main__':
    bot.run()
    
    logging.basicConfig(level=logging.DEBUG)
