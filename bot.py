from pyrogram import Client, filters
import requests
import os

BOT_TOKEN = "8356075235:AAGKQV0lTMNNewFDAfMbo-jmgdjcc4wyc44"
API_URL = "https://script.google.com/macros/s/AKfycbz9-eHwFBWTXzMak6Vfo54vZlJ_3BUA3h-GtctT477Ko-Xy0LCSrKglUyf7UdPfMLVj/exec"

app = Client(
    "lookup_bot",
    bot_token=BOT_TOKEN,
    api_id=34651589,
    api_hash="734f28c75622e7b933445988a89fae13"
)

@app.on_message(filters.command("start"))
async def start(client, message):
    await message.reply(
        "Send mobile number like:\n\n`/find 7864904682`",
        quote=True
    )

@app.on_message(filters.command("find"))
async def find_number(client, message):
    if len(message.command) < 2:
        await message.reply("Usage:\n/find 7864904682")
        return

    number = message.command[1]
    url = f"{API_URL}?term={number}"

    try:
        r = requests.get(url, timeout=10)
        data = r.json()

        if data["data"]["success"]:
            info = data["data"]["result"][0]

            reply = (
                f"📱 Mobile: {info.get('mobile')}\n"
                f"👤 Name: {info.get('name')}\n"
                f"👨 Father: {info.get('father_name')}\n"
                f"📍 Address: {info.get('address')}\n"
                f"📡 Circle: {info.get('circle')}"
            )
        else:
            reply = "❌ No data found"

    except Exception as e:
        reply = "⚠️ API error"

    await message.reply(reply)

app.run()

