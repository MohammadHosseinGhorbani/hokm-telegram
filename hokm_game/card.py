from .exceptions import DifferentSuitsError

from typing import Literal
import json


class Card:
    all = []
    file_ids: dict = json.load(open("stickers.json"))
    file_unique_ids: dict = json.load(open("stickers_unique.json"))
    short_suits = {'H': 'hearts', 'D': 'diamonds', 'C': 'clubs', 'S': 'spades'}
    suits_emojis = {'hearts': '❤️', 'diamonds': '♦️', 'clubs': '♣️', 'spades': '♠️'}
    rank_translations = {1: 'Ace', 11: 'Jack', 12: 'Queen', 13: 'King'}

    def __init__(
            self,
            suit: Literal["hearts", "diamonds", "clubs", "spades"],
            rank: Literal[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13],
    ):
        self.suit = suit
        self.rank = rank

    @staticmethod
    def from_file_id(file_id: str) -> 'Card':
        card_title = dict(zip(Card.file_ids.values(), Card.file_ids.keys())).get(file_id)
        return Card(Card.short_suits.get(card_title[-1]), int(card_title[:-1]))  # type: ignore

    def get_file_id(self, disabled: bool = False) -> str:
        card_title = f"{self.rank}{self.suit[0].upper()}"
        return self.file_ids.get(card_title + ('_disabled' if disabled else ''))

    @staticmethod
    def from_file_unique_id(file_unique_id: str) -> 'Card':
        card_title = dict(zip(Card.file_unique_ids.values(), Card.file_unique_ids.keys())).get(file_unique_id)
        return Card(Card.short_suits.get(card_title[-1]), int(card_title[:-1]))  # type: ignore

    def get_file_unique_id(self, disabled: bool = False) -> str:
        card_title = f"{self.rank}{self.suit[0].upper()}"
        return self.file_unique_ids.get(card_title + ('_disabled' if disabled else ''))

    def __gt__(self, other: 'Card') -> bool:
        if not isinstance(other, Card):
            raise ValueError('A card is only comparable with another card')

        if self.suit != other.suit:
            raise DifferentSuitsError(self, other)

        if self.rank == other.rank == 1:
            return False
        elif self.rank == 1:
            return True
        elif other.rank == 1:
            return False

        return self.rank > other.rank

    def __lt__(self, other: 'Card') -> bool:
        if not isinstance(other, Card):
            raise ValueError('A card is only comparable with another card')

        if self.suit != other.suit:
            raise DifferentSuitsError(self, other)

        if self.rank == other.rank == 1:
            return False
        elif self.rank == 1:
            return False
        elif other.rank == 1:
            return True

        return self.rank < other.rank

    def __eq__(self, other: 'Card') -> bool:
        return (self.rank == other.rank and self.suit == other.suit) if isinstance(other, Card) else False

    def __hash__(self):
        return hash((self.suit, self.rank))

    def __repr__(self):
        return f"<Card({self.rank}, {self.suit})>"

    def __str__(self):
        return f"{self.rank_translations.get(self.rank, self.rank)} of {self.suit} {self.suits_emojis.get(self.suit)}"


for s in ['hearts', 'diamonds', 'clubs', 'spades']:
    for r in range(1, 14):
        Card.all.append(Card(s, r))  # type: ignore
