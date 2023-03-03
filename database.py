from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError
from config import MONGO_URL, MONGO_DB_NAME

client = MongoClient(MONGO_URL)
db = client[MONGO_DB_NAME]
users = db["users"]

class Database:
    def add_user(self, user_id, user_name):
        try:
            users.insert_one({"_id": user_id, "name": user_name})
        except DuplicateKeyError:
            pass # user already exists

    def get_user(self, user_id):
        return users.find_one({"_id": user_id})
    
    def catch_waifu(self, user_id, user_name):
        waifu = f"{user_name}'s waifu"
        users.update_one({"_id": user_id}, {"$set": {"waifu": waifu}})
        return waifu

    def protect_waifu(self, user_id):
        users.update_one({"_id": user_id}, {"$set": {"protected": True}})

    def unprotect_waifu(self, user_id):
        users.update_one({"_id": user_id}, {"$unset": {"protected": ""}})

    def get_waifu(self, user_id):
        user = self.get_user(user_id)
        return user.get("waifu") if user else None
