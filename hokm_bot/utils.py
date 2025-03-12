from dotenv import load_dotenv
import os
import json
import i18n
from hokm_game import Game, GameStates

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
BOT_ID = int(os.getenv("BOT_ID"))
BOT_USERNAME = os.getenv("BOT_USERNAME")

stickers: dict = json.load(open('stickers.json'))
stickers_unique: dict = json.load(open('stickers_unique.json'))

i18n.load_path.append("hokm_bot/locales")
i18n.set('locale', 'fa')
i18n.set('fallback', 'en')
