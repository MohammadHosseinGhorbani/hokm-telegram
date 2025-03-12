from .exceptions import GameStartedError, CardDealtError, NotPlayableError, AlreadyPlayedError, PlayerInGameError
from .card import Card

from typing import TYPE_CHECKING, List, Literal

if TYPE_CHECKING:
    from .game import Game


class Player:
    instances = []

    def __init__(
            self,
            user_id: int,
            name: str,
            position: Literal['blue1', 'blue2', 'red1', 'red2']
    ):
        try:
            p = self.get_instance(user_id)
            raise PlayerInGameError(p.game.chat_id, p.user_id)
        except ValueError:
            pass

        self.user_id = user_id
        self.name = name
        self.position = position
        self.game = None
        self._deck: List[Card] = []
        self.ally = None
        self.wins = 0
        self.scores = 0

        self.instances.append(self)

    def play(self, card: Card):
        if self in self.game.round_cards.values():
            raise AlreadyPlayedError(self)
        if not self.is_playable(card):
            raise NotPlayableError(card, self.game.round_cards)
        self.game.round_cards.update({card: self})
        self.game.add_played_card(card)
        self._deck.remove(card)
        self.game.next_turn()

    def is_playable(self, card: Card):
        round_cards = self.game.round_cards
        player_suits = [_card.suit for _card in self._deck]
        round_suits = [_card.suit for _card in round_cards]
        hokm = self.game.hokm

        if round_suits and round_suits[0] == hokm:
            return (card.suit == hokm) if hokm in player_suits else True
        elif round_suits and round_suits[0] in player_suits:
            return card.suit == round_suits[0]
        else:
            return True

    def is_turn(self):
        return self.game.turn == self

    def set_ally(self, ally: 'Player'):
        from .game import GameStates
        if self.game.state and self.game.state != GameStates.FINISHED:
            raise GameStartedError(self.game.game_id)

        if self.ally:
            self.ally.ally = None
        self.ally = ally
        ally.ally = self

    def add_card(self, card: 'Card'):
        if card in self._deck:
            raise CardDealtError(card)
        self._deck.append(card)

    @property
    def deck(self):
        sorted_deck = []
        for suit in ('hearts', 'diamonds', 'clubs', 'spades'):
            suit_cards = []
            for card in self._deck:
                if card.suit == suit:
                    suit_cards.append(card)
            sorted_deck.extend(sorted(suit_cards))
        return sorted_deck

    def win(self):
        self.wins += 1
        self.ally.wins += 1

    def score(self, amount):
        self.scores += amount
        self.ally.scores += amount

    def join_game(self, game: 'Game'):
        if self.game:
            raise PlayerInGameError(self.game.game_id, self.user_id)
        self.game = game

    def exit_game(self):
        self.game = None
        self.instances.remove(self)

    @classmethod
    def get_instance(cls, user_id):
        for instance in cls.instances:
            if instance.user_id == user_id:
                return instance

        raise ValueError(f'No such user with id: {user_id}')

    def __repr__(self):
        return f'<Player {self.name}[{self.user_id}]>'

    def __str__(self):
        return self.name
