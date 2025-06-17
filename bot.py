import logging
from aiogram import Bot, Dispatcher, executor, types
from config import TOKEN, MONGO_URI, LOG_CHANNEL, ADMIN_IDS, BOT_NAME
from utils import get_db, remember_user_data, get_user_data, send_birthday_reminders, log_event, get_stats
import datetime

logging.basicConfig(level=logging.INFO)

bot = Bot(token=TOKEN, parse_mode="HTML")
dp = Dispatcher(bot)
db = get_db()

# --- Startup ---
@dp.message_handler(commands=['start'])
async def start(msg: types.Message):
    await remember_user_data(msg.from_user)
    log_event(f"👋 New user started: {msg.from_user.id}")
    await msg.reply(f"Hey {msg.from_user.first_name}! 💖\nI’m {BOT_NAME}, your cute lil bestie bot! 🌸\nYou can tell me your birthday with /setbirthday 🎂\nOr check in with /mood 🫶")

# --- Set Birthday ---
@dp.message_handler(commands=['setbirthday'])
async def set_birthday(msg: types.Message):
    args = msg.get_args()
    try:
        bday = datetime.datetime.strptime(args, '%d-%m')
        db.birthdays.update_one({"_id": msg.from_user.id}, {"$set": {"birthday": args}}, upsert=True)
        await msg.reply("Yayyy! 🥳 I saved your birthday, bestie!")
    except:
        await msg.reply("Oopsie! 😅 Use like this: /setbirthday 25-12")

# --- Mood Check ---
@dp.message_handler(commands=['mood'])
async def mood_check(msg: types.Message):
    await msg.reply("How are you feeling today, bestie? 💭\n(Just reply to this message!)")

@dp.message_handler(lambda message: message.reply_to_message and 'How are you feeling today' in message.reply_to_message.text)
async def save_mood(msg: types.Message):
    db.moods.insert_one({"user_id": msg.from_user.id, "mood": msg.text, "time": datetime.datetime.now()})
    await msg.reply("Got it bestie 💖 I'm always here for you! 💕")

# --- Hug/GIF ---
@dp.message_handler(commands=['hug', 'gif'])
async def hug_gif(msg: types.Message):
    await msg.reply("Sending virtual hugs 💞 *squeezes you tight*\n(pretend there's a cute GIF here 🧸)")

# --- Broadcast ---
@dp.message_handler(commands=['broadcast'])
async def broadcast(msg: types.Message):
    if msg.from_user.id not in ADMIN_IDS:
        return await msg.reply("Sorryy cutie, only admin can do this 😘")
    text = msg.get_args()
    users = db.users.find()
    count = 0
    for user in users:
        try:
            await bot.send_message(user["_id"], text)
            count += 1
        except:
            pass
    await msg.reply(f"Broadcast sent to {count} bffs 💌")

# --- Stats ---
@dp.message_handler(commands=['stats'])
async def stats(msg: types.Message):
    if msg.from_user.id not in ADMIN_IDS:
        return await msg.reply("Only admin bby 😗")
    stat_text = get_stats()
    await msg.reply(stat_text)

# --- Daily Reminder Cron Handler (external trigger) ---
@dp.message_handler(commands=['run_reminders'])
async def run_birthday_reminder(msg: types.Message):
    if msg.from_user.id in ADMIN_IDS:
        await send_birthday_reminders(bot)

# --- Voice Support ---
@dp.message_handler(content_types=types.ContentType.VOICE)
async def voice_reply(msg: types.Message):
    await msg.reply("Aww I got your voice 💕 I can't listen yet but it means a lot 😚")

# --- Fallback ---
@dp.message_handler()
async def fallback(msg: types.Message):
    await remember_user_data(msg.from_user)
    await msg.reply("Hey bby! 💗 Use /mood or /setbirthday to try something fun!")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
