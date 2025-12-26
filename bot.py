import os
import threading
import requests
from flask import Flask
from pyrogram import Client, filters

BOT_TOKEN = os.getenv("BOT_TOKEN")
API_ID = os.getenv("API_ID")
API_HASH = os.getenv("API_HASH")

if not BOT_TOKEN or not API_ID or not API_HASH:
    raise RuntimeError("Missing environment variables")

API_ID = int(API_ID)

API_URL = "https://script.google.com/macros/s/AKfycbz9-eHwFBWTXzMak6Vfo54vZlJ_3BUA3h-GtctT477Ko-Xy0LCSrKglUyf7UdPfMLVj/exec"

# ---------------- FLASK SERVER ----------------
app_web = Flask(__name__)

@app_web.route("/")
def home():
    return "Bot is running"

def run_web():
    port = int(os.environ.get("PORT", 10000))
    app_web.run(host="0.0.0.0", port=port)

# ---------------- TELEGRAM BOT ----------------
bot = Client(
    "lookup_bot",
    bot_token=BOT_TOKEN,
    api_id=API_ID,
    api_hash=API_HASH
)

@bot.on_message(filters.command("start"))
async def start(client, message):
    await message.reply("Send:\n/find 7864904682")

@bot.on_message(filters.command("find"))
async def find(client, message):
    if len(message.command) < 2:
        await message.reply("Usage:\n/find 7864904682")
        return

    number = message.command[1]
    r = requests.get(f"{API_URL}?term={number}")
    data = r.json()

    if data["data"]["success"]:
        info = data["data"]["result"][0]
        reply = (
            f"📱 {info.get('mobile')}\n"
            f"👤 {info.get('name')}\n"
            f"👨 {info.get('father_name')}\n"
            f"📍 {info.get('address')}\n"
            f"📡 {info.get('circle')}"
        )
    else:
        reply = "❌ No data found"

    await message.reply(reply)

# ---------------- START BOTH ----------------
if __name__ == "__main__":
    threading.Thread(target=run_web).start()
    bot.run()


