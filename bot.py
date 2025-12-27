import threading
import requests
import asyncio
import json
import os
from flask import Flask
from datetime import datetime
from pyrogram.enums import ParseMode
from pyrogram import Client, filters

# ---------------- FLASK WEB SERVER ----------------
app_web = Flask(__name__)

@app_web.route("/")
def home():
    return "Bot is running!"

def run_web():
    port = int(os.environ.get("PORT", 10000))
    app_web.run(host="0.0.0.0", port=port)

# ---------------- DATA STORE ----------------
DATA_FILE = "data_store.json"

def save_data(query_value, api_response):
    entry = {
        "time": datetime.now().isoformat(),
        "query": query_value,
        "response": api_response
    }

    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump([], f)

    with open(DATA_FILE, "r+", encoding="utf-8") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            data = []

        data.append(entry)
        f.seek(0)
        json.dump(data, f, indent=2, ensure_ascii=False)

# ---------------- CONFIG (USE ENV VARS IN RENDER) ----------------
BOT_TOKEN = os.environ.get("BOT_TOKEN")
API_ID = int(os.environ.get("API_ID"))
API_HASH = os.environ.get("API_HASH")

API_URL = "https://script.google.com/macros/s/AKfycbz9-eHwFBWTXzMak6Vfo54vZlJ_3BUA3h-GtctT477Ko-Xy0LCSrKglUyf7UdPfMLVj/exec"
TGUID_URL = "https://meowmeow.rf.gd/gand/encoredaddy.php"

# ---------------- TELEGRAM BOT ----------------
bot = Client(
    "lookup_bot",
    bot_token=BOT_TOKEN,
    api_id=API_ID,
    api_hash=API_HASH
)

@bot.on_message(filters.command("start"))
async def start(client, message):
    await message.reply(
        "🤖 Bot is running successfully.\n\n"
        "Commands:\n"
        "/num <mobile_number>\n"
        "/tg <tg_id>"
    )

@bot.on_message(filters.command("num"))
async def num_cmd(client, message):
    if len(message.command) < 2:
        await message.reply("Usage:\n/num 7864904682")
        return

    number = message.command[1]

    try:
        r = requests.get(API_URL, params={"term": number}, timeout=15)
        data = r.json()

        save_data(number, data)

        pretty = json.dumps(data, indent=2, ensure_ascii=False)

        if len(pretty) > 4000:
            pretty = pretty[:4000] + "\n...truncated"

        await message.reply(f"<pre>{pretty}</pre>", parse_mode=ParseMode.HTML)

    except Exception as e:
        await message.reply(f"⚠️ Error: {e}")

@bot.on_message(filters.command("tg"))
async def tg_cmd(client, message):
    if len(message.command) < 2:
        await message.reply("Usage:\n/tg 123456")
        return

    await asyncio.sleep(1)

    try:
        r = requests.get(
            TGUID_URL,
            params={"tguid": message.command[1]},
            timeout=20,
            headers={"User-Agent": "Mozilla/5.0"}
        )

        text = r.text.strip() or "❌ No data found"

        if len(text) > 4000:
            text = text[:4000] + "\n...truncated"

    except requests.exceptions.RequestException:
        text = "⚠️ Server unavailable. Try later."

    await message.reply(text)

# ---------------- START BOTH ----------------
if __name__ == "__main__":
    threading.Thread(target=run_web).start()
    bot.run()
