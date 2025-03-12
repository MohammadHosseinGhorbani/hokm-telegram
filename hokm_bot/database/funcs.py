import os
import i18n

from .models import GroupSettings, engine
from sqlalchemy.orm import Session
from sqlalchemy import select
from telegram import InlineKeyboardMarkup, InlineKeyboardButton
from hokm_game import Player


def create_group(chat_id: int):
    with Session(engine) as session:
        session.add(GroupSettings(chat_id=chat_id, language='en'))
        session.commit()


def update_group(chat_id: int, language: str = None, announce_played_cards: bool = None):
    stmt = select(GroupSettings).where(GroupSettings.chat_id == chat_id)
    with Session(engine) as session:
        group = session.scalars(stmt).one()
        if language is not None:
            group.language = language
        if announce_played_cards is not None:
            group.announce_played_cards = announce_played_cards
        session.commit()


def get_setting(chat_id: int, setting: str):
    stmt = select(GroupSettings).where(GroupSettings.chat_id == chat_id)
    with Session(engine) as session:
        group = session.scalars(stmt).one()
    return getattr(group, setting)


def make_languages_keyboard():
    keyboard = InlineKeyboardMarkup([
        [
            InlineKeyboardButton(lang.split('.')[1], callback_data=f"lang_{lang.split('.')[1]}")] for lang in os.listdir("./hokm_bot/locales")
        ]
    )
    return keyboard


def set_gorup_language(chat_id: int):
    i18n.set('locale', get_setting(chat_id, 'language'))


def database_config(func):
    async def wrapper(update, context):
        chat_id = update.message.chat.id if update.message \
            else update.callback_query.message.chat.id if update.callback_query \
            else Player.get_instance(update.inline_query.from_user.id).game.chat_id if update.inline_query and update.inline_query.from_user.id in Player.instances \
            else None
        if not chat_id:
            return await func(update, context)
        stmt = select(GroupSettings).where(GroupSettings.chat_id == chat_id)
        with Session(engine) as session:
            group = session.scalars(stmt).one_or_none()
        if not group:
            create_group(chat_id)
        set_gorup_language(chat_id)
        return await func(update, context)
    return wrapper
