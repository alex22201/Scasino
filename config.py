import os

from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')
TIME_BONUS_AMOUNT = int(os.getenv('TIME_BONUS_AMOUNT', 100))
DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///db.sqlite3')
