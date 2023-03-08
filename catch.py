import random
import asyncio
import db
from pyrogram import Client, filters
from pyrogram.types import Message

waifus = db.get_waifus()

# Define a filter that looks for the "/catch" command
catch_filter = filters.command("catch", prefixes="/")

@Client.on_message(catch_filter)
async def catch_waifu(client: Client, message: Message):
    # Get the waifu name from the command arguments
    waifu_name = message.text.split(" ", 1)[1].lower()

    # Check if the waifu exists in the database
    if waifu_name not in waifus:
        await message.reply(f"Sorry, there is no waifu named '{waifu_name}'")
        return

    # Check if the user has already caught this waifu
    user_waifus = db.get_user_waifus(message.chat.id)
    if waifu_name in user_waifus:
        await message.reply(f"You have already caught '{waifu_name}'!")
        return

    # Add the waifu to the user's collection
    db.add_user_waifu(message.chat.id, waifu_name)

    # Send a reply message and delete the waifu message
    await message.reply(f"Congratulations, you caught '{waifu_name}'!")
    await message.delete()

    # Update the list of available waifus
    waifus = db.get_waifus()

# Define a coroutine that removes all waifu messages after a certain time
async def delete_waifus():
    while True:
        await asyncio.sleep(300)  # Delete waifus every 5 minutes
        messages = db.get_waifu_messages()
        for message in messages:
            try:
                await message.delete()
            except:
                pass
        db.delete_waifu_messages()

# Start the delete_waifus coroutine
loop = asyncio.get_event_loop()
loop.create_task(delete_waifus())
loop.run_forever()
