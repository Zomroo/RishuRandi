# waifu.py
import random
from pyrogram.types import InputMediaPhoto
from modules.database import save_user_waifu, get_user_waifus


def get_random_waifu():
    # Retrieve random waifu from the database
    user_waifus = get_all_waifus()
    if user_waifus:
        return random.choice(user_waifus)
    return None


def save_waifu(file_id, name, user_id):
    # Save the waifu to the database
    waifu = {
        'file_id': file_id,
        'name': name
    }
    save_user_waifu(user_id, waifu)


def delete_waifu(file_id):
    # Delete the waifu from the database
    # Implement the delete functionality as per your requirements
    pass


def get_user_waifus(user_id):
    # Retrieve the user's waifus from the database
    return get_user_waifus(user_id)
