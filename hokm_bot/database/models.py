from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy import String
from sqlalchemy import create_engine

import pathlib


class Base(DeclarativeBase):
    pass


class GroupSettings(Base):
    __tablename__ = 'group_settings'
    id: Mapped[int] = mapped_column(primary_key=True)
    chat_id: Mapped[int] = mapped_column(unique=True)
    language: Mapped[str] = mapped_column(String(2))
    announce_played_cards: Mapped[bool] = mapped_column(default=False)

    def __repr__(self):
        return f"<Group {self.chat_id}>"


engine = create_engine("sqlite:///hokm_bot/database/groups.db")
Base.metadata.create_all(engine)
