from ..database.funcs import make_languages_keyboard, update_group, get_setting, database_config


@database_config
async def language_command(update, context):
    message = update.message
    await message.reply_text("Choose your desired language.", reply_markup=make_languages_keyboard())


@database_config
async def language_buttons(update, context):
    query = update.callback_query
    message = query.message
    chat = message.chat

    language = query.data.lstrip('lang_')
    update_group(chat.id, language=language)

    await message.edit_text("The group language has been changed to " + language)


@database_config
async def announce_command(update, context):
    message = update.message
    chat = message.chat

    new_setting = not get_setting(chat.id, 'announce_played_cards')
    update_group(chat.id, announce_played_cards=new_setting)
    await message.reply_text("The bot will%s announce the played cards from now on." % (" not" if not new_setting else ''))
