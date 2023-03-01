from pymongo import MongoClient

class Randikhana:
    def __init__(self, mongo_url):
        self.client = MongoClient(mongo_url)
        self.db = self.client["waifus"]

    def add_user(self, chat_id, user_id, waifu_name):
        """
        Adds a new user to the database, if not already present.
        Returns True if the user was added, False if the user already exists.
        """
        users = self.db.users
        user = users.find_one({"chat_id": chat_id, "user_id": user_id})
        if user:
            return False
        else:
            users.insert_one({"chat_id": chat_id, "user_id": user_id, "waifu_name": waifu_name})
            return True

    def get_users(self, chat_id):
        """
        Returns a list of all users in the given chat, with their corresponding waifu names.
        """
        users = self.db.users.find({"chat_id": chat_id})
        user_list = []
        for user in users:
            user_list.append((user["user_id"], user["waifu_name"]))
        return user_list
