from hokm_bot import app
from telegram import Update

if __name__ == "__main__":
    print("Starting the bot...")
    app.run_polling(allowed_updates=Update.ALL_TYPES, drop_pending_updates=True)
