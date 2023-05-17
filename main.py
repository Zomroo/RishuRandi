import pyrogram
from pyrogram import filters

# Get your API ID, hash, and bot token from @BotFather
api_id = 14091414
api_hash = '1e26ebacf23466ed6144d29496aa5d5b'
bot_token = '5615528335:AAHOlk2j2TE5CWOv24mxBwpBMAx2ui3Zv1k'

# Create a Pyrogram client
client = pyrogram.Client(
    "my_bot",
    api_id=api_id,
    api_hash=api_hash,
    bot_token=bot_token
)

# Define a command handler for the "add" command
@client.on_message(filters=filters.command("add"))
async def add_command(client, message):
    # Check if the message was sent in a bot command
    if message.chat.type == "private":
        # Ask the user for a picture
        await message.reply("Please send me a picture.")

        # Get the picture from the user
        photo = await message.photo

        # Save the picture to the bot's filesystem
        await photo.download("./my_picture.jpg")


client.run()
