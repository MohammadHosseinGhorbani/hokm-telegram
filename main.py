from hokm_bot import app
from telegram import Update
import os

if __name__ == "__main__":
    if 'groups.db' not in os.listdir('./hokm_bot/database/'):
        with open('./hokm_bot/database/groups.db'):
            pass

    print("Starting the bot...")
    app.run_polling(allowed_updates=Update.ALL_TYPES, drop_pending_updates=True)
