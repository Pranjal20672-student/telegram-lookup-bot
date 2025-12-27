import os
import threading
import asyncio
import requests
import json
from datetime import datetime
from flask import Flask
from pyrogram import Client, filters
from pyrogram.enums import ParseMode

# ---------------- FLASK ----------------
app = Flask(__name__)

@app.route("/")
def home():
    return "OK"

def start_flask():
    port = int(os.environ["PORT"])  # ⬅️ MUST EXIST
    app.run(host="0.0.0.0", port=port)

# ---------------- DATA ----------------
DATA_FILE = "data_store.json"

def save_data(query, response):
    entry = {
        "time": datetime.now().isoformat(),
        "query": query,
        "response": response
    }

    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, "w") as f:
            json.dump([], f)

    with open(DATA_FILE, "r+") as f:
        data = json.load(f)
        data.append(entry)
        f.seek(0)
        json.dump(data, f, indent=2)

# ---------------- CONFIG ----------------
BOT_TOKEN = os.environ["BOT_TOKEN"]
API_ID = int(os.environ["API_ID"])
API_HASH = os.environ["API_HASH"]

API_URL = "https://script.google.com/macros/s/AKfycbz9-eHwFBWTXzMak6Vfo54vZlJ_3BUA3h-GtctT477Ko-Xy0LCSrKglUyf7UdPfMLVj/exec"

# ---------------- BOT ----------------
bot = Client(
    "lookup_bot",
    bot_token=BOT_TOKEN,
    api_id=API_ID,
    api_hash=API_HASH
)

@bot.on_message(filters.command("start"))
async def start(_, message):
    await message.reply("Bot running")

@bot.on_message(filters.command("num"))
async def num_cmd(_, message):
    if len(message.command) < 2:
        await message.reply("/num 9876543210")
        return

    r = requests.get(API_URL, params={"term": message.command[1]}, timeout=15)
    data = r.json()

    save_data(message.command[1], data)

    pretty = json.dumps(data, indent=2)
    await message.reply(f"<pre>{pretty[:4000]}</pre>", parse_mode=ParseMode.HTML)

# ---------------- MAIN ----------------
if __name__ == "__main__":
    threading.Thread(target=start_flask, daemon=True).start()
    bot.run()
