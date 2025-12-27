import os
import time
import threading
import requests
from flask import Flask
from pyrogram import Client, filters

# ---------------- CONFIG ----------------
BOT_TOKEN = os.environ.get("BOT_TOKEN")
API_ID = int(os.environ.get("API_ID"))
API_HASH = os.environ.get("API_HASH")

API_URL = "https://script.google.com/macros/s/AKfycbz9-eHwFBWTXzMak6Vfo54vZlJ_3BUA3h-GtctT477Ko-Xy0LCSrKglUyf7UdPfMLVj/exec"

# ---------------- FLASK (RENDER NEEDS THIS) ----------------
app = Flask(__name__)

@app.route("/")
def home():
    return "Bot is running"

def run_flask():
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

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
        "🤖 Bot is running on Render\n\n"
        "Command:\n"
        "/num <mobile_number>\n\n"
        "⚠️ If server is busy, try again later."
    )

@bot.on_message(filters.command("num"))
async def num_cmd(client, message):
    if len(message.command) < 2:
        await message.reply("Usage:\n/num 7864904682")
        return

    number = message.command[1]

    try:
        time.sleep(1)
        r = requests.get(
            API_URL,
            params={"term": number},
            timeout=20,
            headers={"User-Agent": "Mozilla/5.0"}
        )

        r.raise_for_status()
        data = r.json()

        if data.get("data", {}).get("success"):
            info = data["data"]["result"][0]
            reply = (
                f"📱 Mobile No: {info.get('mobile', 'N/A')}\n"
                f"👤 Owner name: {info.get('name', 'N/A')}\n"
                f"👨 Father Name: {info.get('father_name', 'N/A')}\n"
                f"📍 Address: {info.get('address', 'N/A')}\n"
                f"📡 Circle: {info.get('circle', 'N/A')}"
            )
        else:
            reply = "❌ No data found"

    except requests.exceptions.RequestException:
        reply = (
            "⚠️ Data server is temporarily unavailable.\n"
            "Please try again later."
        )

    await message.reply(reply)

# ---------------- START BOTH ----------------
def run_bot():
    bot.run()

if __name__ == "__main__":
    threading.Thread(target=run_bot, daemon=True).start()
    run_flask()
