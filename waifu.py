import os
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


if __name__ == "__main__":
    # Add your waifus here
    add_waifu("Asuna", "https://telegra.ph/file/42bd8eb989a5231e4b2f4.jpg")
    add_waifu("Rem", "https://telegra.ph/file/42bd8eb989a5231e4b2f4.jpg")
    add_waifu("Megumin", "https://telegra.ph/file/42bd8eb989a5231e4b2f4.jpg")
