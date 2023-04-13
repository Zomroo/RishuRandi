import os
import pymongo


def connect_to_database():
    # Create MongoDB client instance and connect to database
    mongo_client = pymongo.MongoClient(os.environ.get("mongodb+srv://Zoro:Zoro@cluster0.x1vigdr.mongodb.net/?retryWrites=true&w=majority"))
    db = mongo_client["waifu_db"]
    return db


def save_waifu(db, name, rarity, image):
    # Save waifu in database
    db.waifus.insert_one({"name": name, "rarity": rarity, "image": image})
