import pymongo
import config


# Connect to MongoDB
client = pymongo.MongoClient(config.MONGO_URI)
db = client[config.MONGO_DB_NAME]
collection = db[config.MONGO_COLLECTION_NAME]


def add_user(user_id: int):
    """
    Adds a new user to the database.

    Args:
        user_id (int): The ID of the user to add.
    """
    collection.update_one(
        {"_id": user_id},
        {"$setOnInsert": {"waifus": []}},
        upsert=True
    )


def add_waifu_to_user(user_id: int, waifu_name: str):
    """
    Adds a waifu to a user's collection.

    Args:
        user_id (int): The ID of the user to add the waifu to.
        waifu_name (str): The name of the waifu to add.
    """
    collection.update_one(
        {"_id": user_id},
        {"$addToSet": {"waifus": waifu_name}}
    )


def get_user_waifus(user_id: int):
    """
    Retrieves a user's collection of waifus.

    Args:
        user_id (int): The ID of the user to retrieve the waifus for.

    Returns:
        A list of waifu names.
    """
    user = collection.find_one({"_id": user_id})
    if user:
        return user.get("waifus", [])
    else:
        return []


if __name__ == "__main__":
    # Example usage:
    user_id = 123456789
    add_user(user_id)
    add_waifu_to_user(user_id, "Asuna")
    add_waifu_to_user(user_id, "Rem")
    waifus = get_user_waifus(user_id)
    print(waifus)
