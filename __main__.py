




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
    await pbot.send_photo(
        message.chat.id,
        photo=carbon,
        caption=f"✨ For More : @AxeBotz",
    )
    await m.delete()
    carbon.close()
