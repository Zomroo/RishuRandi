import os

# Telegram API settings
API_ID = int(os.environ.get('API_ID', '15849735'))
API_HASH = os.environ.get('API_HASH', 'b8105dc4c17419dfd4165ecf1d0bc100')
BOT_TOKEN = os.environ.get('BOT_TOKEN', '5562112612:AAH7Sbz2iIAdoPknjv0FnuiNbiDa_5OFYQA')
OWNER_CHAT_ID = os.environ.get('OWNER_CHAT_ID', '5148561602')

# MongoDB settings
MONGO_URI = os.environ.get('MONGO_URI', 'mongodb+srv://Zoro:Zoro@cluster0.x1vigdr.mongodb.net/?retryWrites=true&w=majority"')
MONGO_DB_NAME = os.environ.get('DB_NAME', 'Waify')
COLLECTION_NAME = os.environ.get('COLLECTION_NAME', 'Khana')
