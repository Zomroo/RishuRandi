import time
from pyrogram import Client, filters
from pyrogram.types import Message, InlineQuery, InlineQueryResultPhoto
from config import API_ID, API_HASH, BOT_TOKEN, MONGO_URI
from randi import Randi
from database import Database
from randikhana import Randikhana
import schedule

bot = Client(
    "my_bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

TIME_INTERVAL = 5 * 60  # 5 minutes in seconds

def send_waifu_announcement():
    for chat_id in Database.get_all_chats():
        waifu = Randi.get_random_waifu()
        message = bot.send_photo(chat_id, photo=waifu["pic"], caption=waifu["name"])
        Database.save_waifu(chat_id, waifu, message.message_id)

schedule.every(5).minutes.do(send_waifu_announcement)

@bot.on_message(filters.command("start"))
def start_handler(client: Client, message: Message):
    message.reply_text(
        "Hi! I'm a waifu catcher bot. Send me /waifu command to get a random waifu."
    )

@bot.on_message(filters.command("waifu"))
def waifu_handler(client: Client, message: Message):
    # delete the previous waifu's message
    prev_waifu = Database.get_current_waifu(message.chat.id)
    if prev_waifu:
        bot.delete_messages(message.chat.id, prev_waifu["message_id"])

    # send a new waifu message
    waifu = Randi.get_random_waifu()
    message = bot.send_photo(message.chat.id, photo=waifu["pic"], caption=waifu["name"])
    Database.save_waifu(message.chat.id, waifu, message.message_id)

@bot.on_message(filters.command("randi"))
def randi_handler(client: Client, message: Message):
    # get the waifu name from the command
    waifu_name = message.text.split(maxsplit=1)[1].strip()

    # get the current waifu and its chat ID
    current_waifu = Database.get_current_waifu(message.chat.id)
    if not current_waifu:
        message.reply_text("No waifu currently available.")
        return
    chat_id = current_waifu["chat_id"]

    # check if the waifu name matches
    if waifu_name.lower() == current_waifu["waifu"]["name"].lower():
        message.reply_text("You have protected the waifu!")
        Database.add_user(chat_id, message.from_user.id)
    else:
        message.reply_text("Wrong waifu name!")

@bot.on_message(filters.command("myrandi"))
def myrandi_handler(client: Client, message: Message):
    chat_id = message.chat.id
    users = Database.get_users(chat_id)

    if not users:
        message.reply_text("No users have protected the waifu yet.")
        return

    user_list = "\n".join([f"{u['first_name']} ({u['id']})" for u in users])
    message.reply_text(f"Users who have protected the waifu:\n{user_list}")

while True:
    schedule.run_pending()
    time.sleep(1)
