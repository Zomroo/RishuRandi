import pyrogram

from pyrogram import Client, filters
from pyrogram.types import Message


# Create a new bot using your API ID and API Hash
api_id = 14091414
api_hash = '1e26ebacf23466ed6144d29496aa5d5b'
bot_token = '5615528335:AAHOlk2j2TE5CWOv24mxBwpBMAx2ui3Zv1k'

app = Client("my_bot", api_id=api_id, api_hash=api_hash, bot_token=bot_token)


@app.on_message(filters.command(["add"]))
def add_command_handler(client: Client, message: Message):
    # Check if the command is invoked in a bot chat
    if isinstance(message.chat, pyrogram.types.PrivateChat):
        # Ask the user for a picture
        client.send_message(
            chat_id=message.chat.id,
            text="Please send me a picture to add."
        )
    else:
        # The "add" command is only allowed in private chats
        client.send_message(
            chat_id=message.chat.id,
            text="The 'add' command can only be used in private chats."
        )


@app.on_message(filters.photo)
def photo_handler(client: Client, message: Message):
    # Handle the received photo here
    # You can access the photo using `message.photo` attribute
    client.send_message(
        chat_id=message.chat.id,
        text="Thank you for the picture!"
    )


app.run()
