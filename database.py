from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError

# Connect to MongoDB
client = MongoClient("mongodb+srv://Lauda:Lauda@cluster0.niyuza9.mongodb.net/?retryWrites=true&w=majority/")
db = client["my_database"]


class Database:
    @staticmethod
    def save_waifu(chat_id, waifu, message_id):
        """
        Save the waifu information in the database.
        """
        collection = db["waifus"]
        data = {"chat_id": chat_id, "waifu": waifu, "message_id": message_id}
        try:
            collection.insert_one(data)
        except DuplicateKeyError:
            # If the message ID already exists, update the waifu information
            collection.update_one({"message_id": message_id}, {"$set": {"waifu": waifu}})

    @staticmethod
    def get_current_waifu(chat_id):
        """
        Get the current waifu for the given chat.
        """
        collection = db["waifus"]
        return collection.find_one({"chat_id": chat_id}, sort=[("_id", -1)])

    @staticmethod
    def add_user(chat_id, user_id):
        """
        Add a user to the list of users who have protected the current waifu.
        """
        collection = db["users"]
        data = {"chat_id": chat_id, "user_id": user_id}
        try:
            collection.insert_one(data)
        except DuplicateKeyError:
            pass  # If the user already exists, do nothing

    @staticmethod
    def get_users(chat_id):
        """
        Get the list of users who have protected the current waifu.
        """
        collection = db["users"]
        return list(collection.find({"chat_id": chat_id}))
    
    @staticmethod
    def get_all_chats():
        """
        Get the list of all chat IDs in the database.
        """
        collection = db["waifus"]
        return collection.distinct("chat_id")
