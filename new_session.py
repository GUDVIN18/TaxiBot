from pyrogram import Client
from config import API_ID, API_HASH, PHONE_NUMBER

app = Client("userbot", api_id=API_ID, api_hash=API_HASH, phone_number=PHONE_NUMBER)

with app:
    print("Сессия создана!")
