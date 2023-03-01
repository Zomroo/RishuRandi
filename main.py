import time
import schedule
from pyrogram import Client
from config import API_ID, API_HASH, BOT_TOKEN, MONGO_URI
from randi import Randi
from database import Database

bot = Client(
    "my_bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
)

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
schedule.every(TIME_INTERVAL).seconds.do(send_waifu_announcement)

# Run the job scheduler
while True:
    schedule.run_pending()
    time.sleep(1)
