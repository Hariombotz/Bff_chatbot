import pymongo
from config import MONGO_URI, LOG_CHANNEL
import datetime
from pymongo import MongoClient
import shutil, os

def get_db():
    client = MongoClient(MONGO_URI)
    return client['bestiebot']

def remember_user_data(user):
    db = get_db()
    db.users.update_one(
        {"_id": user.id},
        {"$set": {"name": user.full_name, "username": user.username}},
        upsert=True,
    )

def get_user_data(user_id):
    db = get_db()
    return db.users.find_one({"_id": user_id})

async def send_birthday_reminders(bot):
    db = get_db()
    today = datetime.datetime.now().strftime('%d-%m')
    bdays = db.birthdays.find({"birthday": today})
    for user in bdays:
        try:
            await bot.send_message(user["_id"], f"HAPPY BIRTHDAY 🎉🎂 Bestie! Wishing you a magical day full of love 💖")
        except:
            pass

def log_event(message):
    # Can be enhanced with error logs or sent to log group
    print(f"[LOG] {message}")

def get_stats():
    db = get_db()
    total_users = db.users.count_documents({})
    used = shutil.disk_usage(".").used // (1024 ** 2)
    total = shutil.disk_usage(".").total // (1024 ** 2)
    return (
        f"📊 <b>Bot Stats</b>\n"
        f"👥 Total users: {total_users}\n"
        f"💾 Used: {used} MB / {total} MB\n"
        f"📝 Mood logs: {db.moods.count_documents({})}"
    )
