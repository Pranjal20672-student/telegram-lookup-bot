import threading
import requests
import asyncio
import time
import json
import os
from datetime import datetime
from pyrogram.enums import ParseMode
from pyrogram import Client, filters

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

# ---------------- CONFIG ----------------
BOT_TOKEN = "8356075235:AAGKQV0lTMNNewFDAfMbo-jmgdjcc4wyc44"
API_ID = 34651589
API_HASH = "734f28c75622e7b933445988a89fae13"

API_URL = "https://script.google.com/macros/s/AKfycbz9-eHwFBWTXzMak6Vfo54vZlJ_3BUA3h-GtctT477Ko-Xy0LCSrKglUyf7UdPfMLVj/exec"
TGUID_URL = "https://meowmeow.rf.gd/gand/encoredaddy.php"


def run_web():
    app_web.run(host="0.0.0.0", port=10000)

# ---------------- TELEGRAM BOT ----------------
bot = Client(
    "lookup_bot",
    bot_token=BOT_TOKEN,
    api_id=API_ID,
    api_hash=API_HASH
)

# ---------- START ----------
@bot.on_message(filters.command("start"))
async def start(client, message):
    await message.reply(
        "🤖 Bot is running successfully.\n\n"
        "Commands:\n"
        "/num <mobile_number>\n"
        "/tg <tg_id>\n\n"
        "⚠️ Note:\n"
        "If you see server error, it means data source is temporarily down.\n"
        "Please try again after some time."
    )

# ---------- NUM COMMAND (was /find) ----------
@bot.on_message(filters.command("num"))
async def num_cmd(client, message):
    if len(message.command) < 2:
        await message.reply("Usage:\n/num 7864904682")
        return

    number = message.command[1]

    try:
        r = requests.get(API_URL, params={"term": number}, timeout=15)
        data = r.json()

        # ✅ SAVE EVERY SEARCH
        save_data(number, data)

        pretty = json.dumps(data, indent=2, ensure_ascii=False)

        if len(pretty) > 4000:
            pretty = pretty[:4000] + "\n...truncated"

        await message.reply(
            f"<pre>{pretty}</pre>",
            parse_mode=ParseMode.HTML
        )

    except Exception as e:
        await message.reply(f"⚠️ Error: {e}")

# ---------- TG COMMAND (was /tguid) ----------
@bot.on_message(filters.command("tg"))
async def tg_cmd(client, message):
    if len(message.command) < 2:
        await message.reply("Usage:\n/tg 123456")
        return

    tguid = message.command[1]

    try:
        time.sleep(1)
        r = requests.get(
            TGUID_URL,
            params={"tguid": tguid},
            timeout=20,
            headers={"User-Agent": "Mozilla/5.0"}
        )

        r.raise_for_status()
        text = r.text.strip()

        if not text:
            text = "❌ No data found"

        if len(text) > 4000:
            text = text[:4000] + "\n\n...truncated"

    except requests.exceptions.RequestException:
        text = (
            "⚠️ Data server is temporarily unavailable.\n"
            "Please try again later."
        )

    await message.reply(text)

# ---------------- START BOTH ----------------
def run_bot():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    bot.run()


if __name__ == "__main__":
    bot.run()

