import sys
import traceback

from io import BytesIO

from functools import wraps
from pyrogram import filters, Client
from pyrogram.errors.exceptions.forbidden_403 import ChatWriteForbidden

from aiohttp import ClientSession


async def make_carbon(code):
    url = "https://carbonara.solopov.dev/api/cook"
    async with ClientSession().post(url, json={"code": code}) as resp:
        image = BytesIO(await resp.read())
    image.name = "carbon.png"
    return image
  

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
    await m.edit_text("🔄 | Processing....")
    await bot.send_photo(
        message.chat.id,
        photo=carbon,
        caption=f"✨ For More : @AxeBotz",
    )
    await m.delete()
    carbon.close()