# config.py

import os

class Config:
    # Telegram API settings
    API_ID = 14091414
    API_HASH = os.environ.get('API_HASH', '1e26ebacf23466ed6144d29496aa5d5b')
    BOT_TOKEN = os.environ.get('BOT_TOKEN', '5615528335:AAHOlk2j2TE5CWOv24mxBwpBMAx2ui3Zv1k')

    # MongoDB settings
    MONGO_URL = os.environ.get('MONGO_URL', 'mongodb+srv://Zoro:Zoro@cluster0.x1vigdr.mongodb.net/?retryWrites=true&w=majority')
    DB_NAME = os.environ.get('DB_NAME', 'Waify')
    MONGO_COLLECTION_NAME = os.environ.get('COLLECTION_NAME', 'Khana')
