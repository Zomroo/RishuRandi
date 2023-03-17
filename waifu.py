import os
import pymongo
import config
import pymongo
import config

# Connect to MongoDB
client = pymongo.MongoClient(config.MONGO_URI)
db = client[config.MONGO_DB_NAME]
collection = db[config.MONGO_COLLECTION_NAME]

def add_waifu(name: str, image_url: str):
    """
    Adds a new waifu to the database.

    Args:
        name (str): The name of the waifu.
        image_url (str): The URL of the waifu's image.
    """
    collection.update_one(
        {"_id": "waifus"},
        {"$addToSet": {"names": name, "images": image_url}},
        upsert=True
    )

# Add new waifus here
add_waifu("Asuna", "https://telegra.ph/file/42bd8eb989a5231e4b2f4.jpg")
add_waifu("Rem", "https://telegra.ph/file/a320819a5cb9006be7ba9.jpg")
add_waifu("Zero Two", "https://telegra.ph/file/9e42b21055b1ebf14cde3.jpg")
add_waifu("Megumin", "https://telegra.ph/file/311c1059f54af023d2747.jpg")
add_waifu("Kanna", "https://telegra.ph/file/bfcf25c726fe40d74b13a.jpg")


# Connect to MongoDB
client = pymongo.MongoClient(config.MONGO_URI)
db = client[config.MONGO_DB_NAME]
collection = db[config.MONGO_COLLECTION_NAME]


def add_waifu(name: str, image_url: str):
    """
    Adds a new waifu to the database.

    Args:
        name (str): The name of the waifu.
        image_url (str): The URL of the waifu's image.
    """
    collection.update_one(
        {"_id": "waifus"},
        {"$addToSet": {"names": name, "images": image_url}},
        upsert=True
    )


if __name__ == "__main__":
    # Add your waifus here
    add_waifu("Asuna", "https://telegra.ph/file/42bd8eb989a5231e4b2f4.jpg")
    add_waifu("Rem", "https://telegra.ph/file/a320819a5cb9006be7ba9.jpg")
