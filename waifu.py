import pymongo
import config
import random

# Connect to MongoDB
client = pymongo.MongoClient(config.MONGO_URI)
db = client[config.MONGO_DB_NAME]
collection = db[config.MONGO_COLLECTION_NAME]

def get_random_waifu():
    """
    Returns a random waifu from the database.

    Returns:
        tuple: A tuple containing the waifu's name and image URL.
    """
    waifus = collection.find_one({"_id": "waifus"})
    if not waifus or not waifus.get("names") or not waifus.get("images"):
        return None, None
    index = random.randint(0, len(waifus["names"]) - 1)
    return waifus["names"][index], waifus["images"][index]

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
add_waifu("Mikasa", "https://telegra.ph/file/3c1f3b4816e38bf16d7db.jpg")

# Get a random waifu
name, image_url = get_random_waifu()
print(f"Selected waifu: {name}")
print(f"Image URL: {image_url}")
