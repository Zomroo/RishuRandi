from pymongo import MongoClient

class Database:
    def __init__(self, url, db_name):
        self.client = MongoClient(url)
        self.db = self.client[db_name]

    def add_new_waifu(self, name, picture_url, rarity):
        waifu_collection = self.db.waifus

        # Create a new waifu document
        waifu = {
            "name": name,
            "picture_url": picture_url,
            "rarity": rarity
        }
        # Insert the waifu into the 'waifus' collection
        result = waifu_collection.insert_one(waifu)
        # Return the ID of the new waifu document
        return str(result.inserted_id)

    def get_waifus(self):
        waifu_collection = self.db.waifus
        return waifu_collection.find()

    def get_waifu_by_name(self, name):
        waifu_collection = self.db.waifus
        return waifu_collection.find_one({"name": name})

    def add_new_user(self, user_id):
        user_collection = self.db.users
        user = {
            "user_id": user_id,
            "waifus_collected": []
        }
        result = user_collection.insert_one(user)
        return str(result.inserted_id)

    def add_waifu_to_user(self, user_id, waifu_id):
        user_collection = self.db.users
        user = user_collection.find_one({"user_id": user_id})
        if user:
            waifus_collected = user.get("waifus_collected", [])
            if waifu_id not in waifus_collected:
                waifus_collected.append(waifu_id)
                user_collection.update_one({"user_id": user_id}, {"$set": {"waifus_collected": waifus_collected}})
