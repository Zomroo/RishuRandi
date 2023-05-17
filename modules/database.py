# database.py
from pymongo import MongoClient
from config import Config

# Connect to the MongoDB database
client = MongoClient(Config.MONGO_URI)
db = client[Config.DB_NAME]

# Collection names
COLLECTION_USERS = 'users'


def save_user_waifu(user_id, waifu):
    user_collection = db[COLLECTION_USERS]

    # Check if the user already exists in the database
    user = user_collection.find_one({'user_id': user_id})

    if user:
        # Update the user's waifu list
        user_collection.update_one({'user_id': user_id}, {'$push': {'waifus': waifu}})
    else:
        # Create a new user entry with the waifu list
        user_collection.insert_one({'user_id': user_id, 'waifus': [waifu]})


def get_user_waifus(user_id):
    user_collection = db[COLLECTION_USERS]

    # Retrieve the user's waifus from the database
    user = user_collection.find_one({'user_id': user_id})

    if user:
        return user['waifus']
    else:
        return []


def get_user_waifus_by_chat(user_id, chat_id):
    user_collection = db[COLLECTION_USERS]

    # Retrieve the user's waifus for the specific chat from the database
    user = user_collection.find_one({'user_id': user_id, 'chat_id': chat_id})

    if user:
        return user['waifus']
    else:
        return []
