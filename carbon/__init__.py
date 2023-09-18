## DEVELOPED BY #ZENO 
## This software is part of AxeBotz 

from pyrogram import Client
from os import getenv
from dotenv import load_dotenv

load_dotenv()


API_ID = getenv("API_ID")
API_HASH = getenv("API_HASH")
TOKEN = getenv("TOKEN")
OWNER_ID = getenv("OWNER_ID")

bot = Client(
  "CARBON",
  api_id=API_ID,
  api_hash=API_HASH,
  bot_token=TOKEN
)
print("[INFO]: STARTING BOT")
bot.start()

print("[INFO]: GATHERING INFO")
x = bot.get_me()
BOT_NAME = x.first_name
BOT_USERNAME = x.username
BOT_ID = x.id
