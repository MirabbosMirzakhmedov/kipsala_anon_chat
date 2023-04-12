import os
from dotenv import load_dotenv

load_dotenv()
MY_USER_ID = os.getenv('MY_USER_ID')
BOT_TOKEN = os.getenv('BOT_TOKEN')