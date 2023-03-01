from pymongo import MongoClient
from config import MONGO_URL

waifu = "waifu"

client = MongoClient(MONGO_URL)
db = client.get_database(waifu)

if "users" not in db.list_collection_names():
    db.create_collection("users")
    db.users.create_index([("user_id", 1)], unique=True)
