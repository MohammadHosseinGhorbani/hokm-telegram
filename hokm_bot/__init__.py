from telegram.ext import ApplicationBuilder, filters, CommandHandler, CallbackQueryHandler, MessageHandler, InlineQueryHandler

from .handlers import start_command, help_command, newgame_command, join_button, user_button, start_button, sticker_handler, card_choosing, get_sticker_id, language_command, language_buttons, announce_command, leave_command, replace_button, end_command, get_played_cards
from .utils import BOT_TOKEN


app = ApplicationBuilder().token(BOT_TOKEN).build()

app.add_handler(CommandHandler('start', get_played_cards, filters.Regex('info')))
app.add_handler(CommandHandler('start', start_command))
app.add_handler(CommandHandler('help', help_command))
app.add_handler(CommandHandler('newgame', newgame_command))
# app.add_handler(MessageHandler(filters.Sticker.ALL & filters.User(1615262687), get_sticker_id))
app.add_handler(CallbackQueryHandler(join_button, r'^join_'))
app.add_handler(CallbackQueryHandler(user_button, r'^user'))
app.add_handler(CallbackQueryHandler(start_button, r'^start'))
app.add_handler(MessageHandler(filters.Sticker.ALL & filters.VIA_BOT, sticker_handler))
app.add_handler(InlineQueryHandler(card_choosing))
app.add_handler(CommandHandler('lang', language_command))
app.add_handler(CallbackQueryHandler(language_buttons, r'^lang_'))
app.add_handler(CommandHandler('announce', announce_command))
app.add_handler(CommandHandler('leave', leave_command))
app.add_handler(CallbackQueryHandler(replace_button, r'^replace_'))
app.add_handler(CommandHandler('end', end_command))
