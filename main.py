# main.py
import time
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors import FloodWait
from config import Config
from modules.waifu import get_random_waifu, save_waifu, delete_waifu, get_user_waifus
from modules.database import get_user_waifus_by_chat

app = Client('waifu_catcher_bot', api_id=Config.API_ID, api_hash=Config.API_HASH, bot_token=Config.BOT_TOKEN)


def send_random_waifu(chat_id):
    waifu = get_random_waifu()
    app.send_photo(
        chat_id=chat_id,
        photo=waifu.file_id,
        caption=f"Write /catch {waifu.name} to catch this waifu!"
    )


def check_timeout(chat_id):
    if chat_id in timeout_timers:
        if time.time() - timeout_timers[chat_id] >= 600:
            send_random_waifu(chat_id)
            timeout_timers[chat_id] = time.time()


@app.on_message(filters.command('start'))
def start_command(client, message):
    client.send_message(
        chat_id=message.chat.id,
        text='Welcome to the Waifu Catcher Bot! Use /catch to catch a random waifu!'
    )
    chat_id = message.chat.id
    send_random_waifu(chat_id)


@app.on_message(filters.command('catch') & filters.group)
def catch_command(client, message):
    if message.chat.id not in waifu_catchers:
        client.send_message(
            chat_id=message.chat.id,
            text="No waifu is currently appearing. Please wait for the next waifu to appear."
        )
        return

    waifu_name = message.text.split('/catch', 1)[1].strip()
    chat_id = message.chat.id

    waifu_info = waifu_catchers[chat_id]
    if waifu_info["name"].lower() == waifu_name.lower():
        client.send_message(
            chat_id=chat_id,
            text=f"Congratulations! You caught {waifu_info['name']}!"
        )
        save_waifu(waifu_info["file_id"], waifu_info["name"], message.from_user.id)
        waifu_catchers.pop(chat_id)
    else:
        client.send_message(
            chat_id=chat_id,
            text="Your guess is wrong!"
        )



@app.on_message(filters.text)
def timeout_check(client, message):
    chat_id = message.chat.id
    if chat_id in waifu_catchers and chat_id not in timeout_timers:
        timeout_timers[chat_id] = time.time()

    check_timeout(chat_id)


@app.on_message(filters.command('mywaifu'))
def mywaifu_command(client, message):
    # Retrieve the user's waifus from the database
    user_waifus = get_user_waifus(message.from_user.id)

    if not user_waifus:
        client.send_message(
            chat_id=message.chat.id,
            text="You haven't caught any waifus yet!"
        )
        return

    page_size = 20
    page = 1

    # Calculate the starting and ending indices for the current page
    start_index = (page - 1) * page_size
    end_index = start_index + page_size

    # Extract the waifus for the current page
    waifus_for_page = user_waifus[start_index:end_index]

    # Build the waifu list message
    waifu_list = ""
    for i, waifu in enumerate(waifus_for_page, start=start_index + 1):
        waifu_list += f"{i}. {waifu['name']}\n"

    # Build the pagination buttons
    buttons = []
    if start_index > 0:
        buttons.append(InlineKeyboardButton("Previous", callback_data=f"prev_page:{page}"))
    if end_index < len(user_waifus):
        buttons.append(InlineKeyboardButton("Next", callback_data=f"next_page:{page}"))

    reply_markup = InlineKeyboardMarkup([buttons])

    # Send the waifu list message with pagination buttons
    client.send_message(
        chat_id=message.chat.id,
        text=waifu_list,
        reply_markup=reply_markup
    )

@app.on_message(filters.command('add') & filters.private)
def add_command(client, message):
    if message.reply_to_message is None or not message.reply_to_message.photo:
        client.send_message(
            chat_id=message.chat.id,
            text="Please reply to a photo with the /add command."
        )
        return

    # Save the waifu photo and request the name
    waifu_photo = message.reply_to_message.photo.file_id
    client.send_message(
        chat_id=message.chat.id,
        text="Please enter the name of the waifu:"
    )
    client.register_next_step_handler(message, process_waifu_name, waifu_photo)



def process_waifu_name(client, message, waifu_photo):
    waifu_name = message.text.strip()

    # Send a preview of the waifu with buttons to save or delete
    client.send_photo(
        chat_id=message.chat.id,
        photo=waifu_photo,
        caption=f"Preview: {waifu_name}",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("Save", callback_data=f"save_waifu:{waifu_photo}:{waifu_name}")],
            [InlineKeyboardButton("Delete", callback_data=f"delete_waifu:{waifu_photo}")]
        ])
    )



# Register other necessary handlers and callbacks here

# Bot's data
waifu_catchers = {}  # chat_id -> waifu_info
timeout_timers = {}  # chat_id -> timeout_timer

app.run()
