import time
import schedule
from pyrogram import Client, filters
from pyrogram.types import Message
from config import API_ID, API_HASH, BOT_TOKEN, MONGO_URI
from randi import Randi
from randikhana import Randikhana
from commands import start, help, waifu, randi, myrandi

bot = Client(
    "my_bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

# Add the command handlers to the bot
bot.add_handler(start)
bot.add_handler(help)
bot.add_handler(waifu)
bot.add_handler(randi)
bot.add_handler(myrandi)

# Start the bot
bot.start()

# Set the time interval for sending the waifu announcements
TIME_INTERVAL = 5 * 60  # 5 minutes in seconds

def send_waifu_announcement():
    for chat_id in Database.get_all_chats():
        waifu = Randi.get_random_waifu()
        message = bot.send_photo(chat_id, photo=waifu["pic"], caption=waifu["name"])
        Database.save_waifu(chat_id, waifu, message.message_id)

# Schedule the job to send the waifu announcements
schedule.every(5).minutes.do(send_waifu_announcement)

# Run the job scheduler
while True:
    schedule.run_pending()
    time.sleep(1)
