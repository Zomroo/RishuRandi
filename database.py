import pymongo
import config

class Database:
    def __init__(self):
        self.client = pymongo.MongoClient(config.MONGO_URI)
        self.db = self.client[config.MONGO_DB_NAME]
        self.collection = self.db[config.MONGO_COLLECTION_NAME]

    def add_waifu(self, waifu_data):
        self.collection.insert_one(waifu_data)

    def get_all_waifus(self):
        return list(self.collection.find())

    def get_waifu_by_id(self, waifu_id):
        return self.collection.find_one({'_id': waifu_id})
