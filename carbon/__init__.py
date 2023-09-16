from pyrogram import Client

API_ID = 7745211
API_HASH = "2ea42beae4e2410ce32eeaec0bdfd18e"
TOKEN = "6443975769:AAEmiiKJ76HncAoNfRTM0FGiQ8JBu7qklYY"

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
