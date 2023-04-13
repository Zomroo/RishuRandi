import os
import pyrogram
from pyrogram import Client, filters
from pyrogram.types import Message
from database import save_image

api_id = 15849735
api_hash = "b8105dc4c17419dfd4165ecf1d0bc100"
bot_token = "5931504207:AAF-jzKC8USclrFYrtcaeAZifQcmEcwFNe4"
app = Client('waifu_bot', api_id, api_hash, bot_token=bot_token)

@app.on_message(filters.command('add'))
async def add_waifu_handler(client: Client, message: Message):
    # Ask user for image of waifu
    await message.reply_text('Please send me an image of your waifu.')

    # Wait for user to send image
    waifu_image = await app.listen(message.chat.id)

    # Save image to MongoDB
    if waifu_image.photo:
        file_id = waifu_image.photo.file_id
        save_image(file_id)

        # Send confirmation message
        await message.reply_text('Image saved to database.')
    else:
        await message.reply_text('No photo found in the message.')

app.run()
