from pymongo import MongoClient
from config import MONGODB_URL

client = MongoClient(MONGO_URL)
db = client.get_database(database_name)


if "users" not in db.list_collection_names():
    db.create_collection("users")
    db.users.create_index([("user_id", 1)], unique=True)
