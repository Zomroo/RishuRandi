import os
import pymongo
from pymongo import MongoClient

mongo_url = os.environ.get('mongodb+srv://Zoro:Zoro@cluster0.x1vigdr.mongodb.net/?retryWrites=true&w=majority')
mongo_client = MongoClient(mongo_url)
db = mongo_client['waifus']
collection = db['images']

def save_image(file_id):
    collection.insert_one({'file_id': file_id})
