from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
import config
from database import Database

# Create a Pyrogram client and connect to MongoDB
app = Client('my_bot', api_id=config.API_ID, api_hash=config.API_HASH, bot_token=config.BOT_TOKEN)
db = Database()

# Define a filter to only allow the owner to use the /add and /done commands
owner_filter = filters.create(lambda _, __, update: str(update.chat.id) == config.OWNER_CHAT_ID)

# Define a callback function for the /add command
@app.on_message(owner_filter & filters.command('add', prefixes='/'))
async def add_waifu(client, message):
    # Ask for the waifu pic
    await message.reply('Send me the waifu pic.')
    waifu_pic = await client.ask(message.chat.id, timeout=60)
    if not waifu_pic.photo:
        await message.reply('That was not a photo. Aborting.')
        return

    # Ask for the waifu name
    await message.reply('What is the waifu name?')
    waifu_name = await client.ask(message.chat.id, timeout=60)
    if not waifu_name.text:
        await message.reply('You did not provide a name. Aborting.')
        return

    # Ask for the waifu rarity using a custom keyboard
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton('Common', callback_data='common')],
        [InlineKeyboardButton('Rare', callback_data='rare')],
        [InlineKeyboardButton('Epic', callback_data='epic')],
        [InlineKeyboardButton('Legendary', callback_data='legendary')],
    ])
    await message.reply('Select the waifu rarity:', reply_markup=keyboard)
    rarity_data = await client.listen(message.chat.id)
    rarity = rarity_data.data

    # Save the waifu data to MongoDB
    waifu_data = {
        'name': waifu_name.text,
        'pic': waifu_pic.photo[-1].file_id,
        'rarity': rarity,
    }
    db.add_waifu(waifu_data)

    # Send a preview of the waifu data
    rarity_text = {
        'common': 'Common',
        'rare': 'Rare',
        'epic': 'Epic',
        'legendary': 'Legendary',
    }[rarity]
    caption = f'{waifu_name.text}\n{rarity_text}'
    await client.send_photo(message.chat.id, waifu_pic.photo[-1].file_id, caption=caption)

    # Tell the user to use the /done command to complete the waifu adding process
    await message.reply('Please use the /done command to complete the waifu adding process.')

# Define a callback function for the /done command
@app.on_message(owner_filter & filters.command('done', prefixes='/'))
async def finish_add_waifu(client, message):
    # Tell the user that the waifu adding process is complete
    await message.reply('Waifu adding process complete.')

# Start the Pyrogram client
app.run()
