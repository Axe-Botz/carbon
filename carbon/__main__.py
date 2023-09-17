import sys
import traceback

from io import BytesIO

from functools import wraps
from pyrogram import filters, idle
from pyrogram.errors.exceptions.forbidden_403 import ChatWriteForbidden
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from aiohttp import ClientSession

from carbon import *

## ---------------------------------------------------- ##

async def make_carbon(code):
    url = "https://carbonara.solopov.dev/api/cook"
    async with ClientSession().post(url, json={"code": code}) as resp:
        image = BytesIO(await resp.read())
    image.name = "carbon.png"
    return image

def split_limits(text):
    if len(text) < 2048:
        return [text]

    lines = text.splitlines(True)
    small_msg = ""
    result = []
    for line in lines:
        if len(small_msg) + len(line) < 2048:
            small_msg += line
        else:
            result.append(small_msg)
            small_msg = line

    result.append(small_msg)

    return result

def capture_err(func):
    @wraps(func)
    async def capture(client, message, *args, **kwargs):
        try:
            return await func(client, message, *args, **kwargs)
        except ChatWriteForbidden:
            return
        except Exception as err:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            errors = traceback.format_exception(
                exc_type,
                value=exc_obj,
                tb=exc_tb,
            )
            error_feedback = split_limits(
                "**ERROR** | `{}` | `{}`\n\n```{}```\n\n```{}```\n".format(
                    0 if not message.from_user else message.from_user.id,
                    0 if not message.chat else message.chat.id,
                    message.text or message.caption,
                    "".join(errors),
                ),
            )
            for x in error_feedback:
                await bot.send_message(OWNER_ID, x)
            raise err

    return capture


## ---------------------------------------------------- ##

@bot.on_message(filters.command("start"))
async def start(_, message):
  await message.reply_text(
    text="""**Hello **

**I'm carbon generator. I can convert your text/reply to carbon.**

**Syntax :-**
`/carbon Axe Botz`
    """,
    reply_markup=InlineKeyboardMarkup(
      [
        [
          InlineKeyboardButton(
            text="ℹ️ Source",
            url=f""
          ),
          InlineKeyboardButton(
            text="🔗 Updates",
            url=f""
          )
        ]
      ]
    ),
    disable_web_page_preview=True
  )

@bot.on_message(filters.command("carbon"))
@capture_err
async def carbon_func(_, message):
    if message.reply_to_message:
        if message.reply_to_message.text:
            txt = message.reply_to_message.text
        else:
            return await message.reply_text("**Syantax :-**\n\n/carbon Axe Botz")
    else:
        try:
            txt = message.text.split(None, 1)[1]
        except IndexError:
            return await message.reply_text("**Syantax :-**\n\n/carbon Axe Botz")
    m = await message.reply_text("🔄 | Processing....")
    carbon = await make_carbon(txt)
    #await m.edit_text("🔄 | Processing....")
    await bot.send_photo(
        message.chat.id,
        photo=carbon,
        caption=f"✨ For More : @AxeBotz",
    )
    await m.delete()
    carbon.close()


## ---------------------------------------------------- ##
if __name__ == "__main__":
  #loop.run_until_complete(start_bot())
  idle()
