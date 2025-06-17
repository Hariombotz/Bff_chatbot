import os

TOKEN = os.getenv("BOT_TOKEN")
MONGO_URI = os.getenv("MONGO_URI")
LOG_CHANNEL = os.getenv("LOG_CHANNEL_ID")  # int or str
ADMIN_IDS = list(map(int, os.getenv("ADMIN_IDS", "").split()))
BOT_NAME = os.getenv("BOT_NAME", "BestieBot")
