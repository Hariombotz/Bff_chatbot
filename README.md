# 💖 BestieBot — Telegram BFF Chatbot

A sweet Telegram-based girl chatbot BFF powered by OpenAI and MongoDB. She checks on your mood, remembers your birthday, sends you love, and even supports voice!

## 🌸 Features

- Casual bestie personality
- Birthday memory + daily reminders 🎂
- Mood check-ins 💭
- Voice message support 🎙️
- Cute hug/GIF command 💞
- Admin-only broadcast 💌
- Bot stats dashboard 🧠
- Custom bot name 🧁
- MongoDB memory 💾
- Easy deploy: Render, Heroku, Koyeb ☁️

## 🚀 Deployment

1. Create `.env` or configure environment:
   - `BOT_TOKEN`
   - `MONGO_URI`
   - `LOG_CHANNEL_ID`
   - `ADMIN_IDS` (comma separated)
   - `BOT_NAME` (optional)

2. Deploy to:
   - Render (use `start.sh`)
   - Heroku (`app.json`, `Procfile`)
   - Koyeb (Docker)

---

## 🛠 Commands

- `/start` – Start talking
- `/setbirthday DD-MM` – Save your birthday
- `/mood` – Daily mood check
- `/hug` or `/gif` – Sends a hug
- `/broadcast` – Admin only
- `/stats` – Bot statistics
- `/run_reminders` – Admin-only (cron based)

---

## 🧠 Built with

- Python + Aiogram
- MongoDB Atlas
- OpenAI GPT-4 / GPT-3.5 (future)
