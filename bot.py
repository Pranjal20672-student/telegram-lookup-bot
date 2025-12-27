import os
import threading
import requests
from flask import Flask
from pyrogram import Client, filters

# ---------------- CONFIG ----------------
BOT_TOKEN = os.getenv("BOT_TOKEN")
API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")

API_URL = "https://script.google.com/macros/s/AKfycbz9-eHwFBWTXzMak6Vfo54vZlJ_3BUA3h-GtctT477Ko-Xy0LCSrKglUyf7UdPfMLVj/exec"
TGUID_URL = "https://meowmeow.rf.gd/gand/encoredaddy.php"

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

# ---------- START ----------
@bot.on_message(filters.command("start"))
async def start(client, message):
    await message.reply(
        "🤖 Bot is running\n\n"
        "Commands:\n"
        "/find <number>\n"
        "/tguid <id>"
    )

# ---------- FIND COMMAND ----------
@bot.on_message(filters.command("find"))
async def find(client, message):
    if len(message.command) < 2:
        await message.reply("Usage:\n/find 7864904682")
        return

    number = message.command[1]

    try:
        r = requests.get(API_URL, params={"term": number}, timeout=15)
        data = r.json()

        if data.get("data", {}).get("success"):
            info = data["data"]["result"][0]
            reply = (
                f"📱 Mobile: {info.get('mobile', 'N/A')}\n"
                f"👤 Name: {info.get('name', 'N/A')}\n"
                f"👨 Father: {info.get('father_name', 'N/A')}\n"
                f"📍 Address: {info.get('address', 'N/A')}\n"
                f"📡 Circle: {info.get('circle', 'N/A')}"
            )
        else:
            reply = "❌ No data found"

    except Exception as e:
        reply = f"⚠️ Error: {e}"

    await message.reply(reply)

# ---------- TGUID COMMAND ----------
@bot.on_message(filters.command("tguid"))
async def tguid(client, message):
    if len(message.command) < 2:
        await message.reply("Usage:\n/tguid 123456")
        return

    tguid = message.command[1]

    try:
        r = requests.get(TGUID_URL, params={"tguid": tguid}, timeout=15)

        if r.status_code != 200:
            await message.reply("⚠️ API error")
            return

        text = r.text.strip()

        if not text:
            await message.reply("❌ No data found")
            return

        if len(text) > 4000:
            text = text[:4000] + "\n\n...truncated"

        await message.reply(f"✅ Result:\n\n{text}")

    except Exception as e:
        await message.reply(f"⚠️ Error: {e}")

# ---------------- START BOTH ----------------
if __name__ == "__main__":
    threading.Thread(target=run_web).start()
    bot.run()
