from pyrogram import Client

API_ID =
API_HASH = ""
TOKEN = ""

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
