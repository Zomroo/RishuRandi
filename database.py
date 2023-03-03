from pymongo import MongoClient
from pymongo.collection import Collection
import pymongo
from config import MONGO_URI, MONGO_DB_NAME

client = pymongo.MongoClient(MONGO_URI)
db = client[MONGO_DB_NAME]

def get_db():
    return db


class Database:
    def __init__(self, url, db_name):
        self.client = MongoClient(url)
        self.db = self.client[db_name]
        self.users = self.db.users

    def add_user(self, user_id, user_name):
        user = {"_id": user_id, "name": user_name}
        self.users.insert_one(user)

    def get_user(self, user_id):
        return self.users.find_one({"_id": user_id})

    def catch_waifu(self, user_id, user_name):
        waifu = f"{user_name}'s waifu"
        self.users.update_one({"_id": user_id}, {"$set": {"waifu": waifu}})
        return waifu

    def protect_waifu(self, user_id):
        self.users.update_one({"_id": user_id}, {"$set": {"protected": True}})

    def unprotect_waifu(self, user_id):
        self.users.update_one({"_id": user_id}, {"$unset": {"protected": ""}})

    def get_waifu(self, user_id):
        user = self.get_user(user_id)
        return user.get("waifu") if user else None
