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
        "/num <number>
    )

# ---------- FIND COMMAND ----------
@bot.on_message(filters.command("num"))
async def num(client, message):
    if len(message.command) < 2:
        await message.reply("Usage:\n/num 7864904682")
        return

    number = message.command[1]

    try:a"]["result"][0]
            reply = (
                f"📱 Mobile number: {info.get('mobile', 'N/A')}\n"
                f"👤 Owner name: {info.get('name', 'N/A')}\n"
                f"👨 Father name: {info.get('father_name', 'N/A')}\n"
                f"📍 Address: {info.get('address', 'N/A')}\n"
                f"📡 Circle: {info.get('circle', 'N/A')}"
            )
        else:
            reply = "❌ No data found"

    except Exception as e:
        reply = f"⚠️ Error: {e}"

    await message.reply(reply)



# ---------------- START BOTH ----------------
if __name__ == "__main__":
    threading.Thread(target=run_web).start()
    bot.run()

