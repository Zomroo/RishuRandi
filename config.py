import os
from dotenv import load_dotenv

load_dotenv()

API_ID = int(os.environ.get("API_ID", "15849735"))
API_HASH = os.environ.get("API_HASH", "b8105dc4c17419dfd4165ecf1d0bc100")
BOT_TOKEN = os.environ.get("BOT_TOKEN", "5562112612:AAH7Sbz2iIAdoPknjv0FnuiNbiDa_5OFYQA")
MONGO_URI = os.environ.get("MONGO_URI", "mongodb+srv://Lauda:Lauda@cluster0.niyuza9.mongodb.net/?retryWrites=true&w=majority/")
