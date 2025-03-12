from .card import Card
from .exceptions import PlayerInGameError, PlayerNotInGameError, GameFinishedError, TooManyPlayersError, GameStartedError, CardDealtError, NotEnoughPlayersError, NotEnoughCardsError

from typing import TYPE_CHECKING, Optional, List, Literal, Dict, Union
import random

if TYPE_CHECKING:
    from .player import Player


class Game:
    instances: List['Game'] = []

    def __init__(
            self,
            chat_id: int,
            game_id: Optional[int] = None,
            rounds: Optional[Literal[1, 3, 5, 7]] = None
    ):
        self.game_id = game_id or (self.instances[-1].game_id + 1 if self.instances else 1)
        self.chat_id = chat_id
        self.players: List['Player'] = []
        self._hakem: Optional['Player'] = None
        self._hokm: Optional[Literal['hearts', 'diamonds', 'spades', 'clubs']] = None
        self.cards: List[Card] = Card.all.copy()
        self.round_cards: Dict[Card, Player] = {}
        self._all_played_cards: List[Card] = []
        self.state = None
        self._rounds: Optional[Literal[1, 3, 5, 7]] = rounds
        self.round = 0
        self._turn: Optional[Player] = None

        self.instances.append(self)

    def add_player(self, player: 'Player', ally: Optional['Player'] = None):
        if player in self.players:
            raise PlayerInGameError(self.game_id, player.user_id)

        if len(self.players) == 4:
            raise TooManyPlayersError(self.game_id)

        if ally:
            player.set_ally(ally)

        player.join_game(self)
        self.players.append(player)

    def remove_player(self, player: Union[int, 'Player']):
        from .player import Player

        if not isinstance(player, (int, Player)):
            raise ValueError("the type of argument should be int or Player.")

        if (player not in self.players) and (player not in [_player.user_id for _player in self.players]):
            raise PlayerNotInGameError(self.game_id, player.user_id if isinstance(player, Player) else player)

        if isinstance(player, Player):
            player.exit_game()
            self.players.remove(player)
        else:
            Player.get_instance(player).exit_game()
            self.players.remove(self[player])

    @property
    def hokm(self):
        if not self._hokm:
            raise ValueError("hokm is currently None and should have a value.")
        return self._hokm

    @hokm.setter
    def hokm(self, value: Literal['hearts', 'diamonds', 'spades', 'clubs']):
        if value not in ['hearts', 'diamonds', 'spades', 'clubs']:
            raise ValueError("hokm can only be set to 'hearts', 'diamonds', 'spades' or 'clubs'")
        self._hokm = value
        self.state = GameStates.PLAYING

    @property
    def hakem(self):
        if not self._hakem:
            raise ValueError("hakem is currently None and should have a value.")
        return self._hakem

    @hakem.setter
    def hakem(self, value: 'Player'):
        from .player import Player
        if not isinstance(value, Player):
            raise ValueError("hakem can only be set to an instance of the Player class.")
        self._hakem = value

    @property
    def rounds(self):
        if not self._rounds:
            raise ValueError("rounds variable is currently None and should have a value.")
        return self._rounds

    @rounds.setter
    def rounds(self, value: Literal[1, 3, 5, 7]):
        if value not in [1, 3, 5, 7]:
            raise ValueError("rounds variable can only be set to 1, 3, 5 or 7.")
        self._rounds = value

    @property
    def turn(self):
        if not self._turn:
            raise ValueError("turn variable is currently None and should have a value.")
        return self._turn

    @turn.setter
    def turn(self, value: 'Player'):
        from .player import Player
        if not isinstance(value, Player):
            raise ValueError("variable turn can only be set to an instance of the Player class.")
        self._turn = value

    def deal_card(self, player: 'Player', card: Card):
        if card not in self.cards:
            raise CardDealtError(card)

        player.add_card(card)
        self.cards.remove(card)

    @property
    def all_played_cards(self):
        sorted_cards = []
        for suit in ('hearts', 'diamonds', 'clubs', 'spades'):
            suit_cards = []
            for card in self._all_played_cards:
                if card.suit == suit:
                    suit_cards.append(card)
            sorted_cards.extend(sorted(suit_cards))
        return sorted_cards

    def add_played_card(self, card: Card):
        if card not in self._all_played_cards:
            self._all_played_cards.append(card)
        else:
            raise ValueError("This card is already played.")

    def next_hakem(self):
        if (hakem_index := self.players.index(self.hakem)) != 3:
            self.hakem = self.players[hakem_index + 1]
        else:
            self.hakem = self.players[0]

    def next_turn(self):
        if (turn_index := self.players.index(self.turn)) != 3:
            self.turn = self.players[turn_index + 1]
        else:
            self.turn = self.players[0]

    def deal_to_hakem(self):
        for i in range(5):
            self.deal_card(self.hakem, random.choice(self.cards))

    def deal_to_all(self):
        # Assume that the first 5 cards are already dealt to the hakem

        # Deal next 8 cars to the hakem
        for i in range(8):
            self.deal_card(self.hakem, random.choice(self.cards))

        # Deal 13 cards to other players
        _players = self.players.copy()
        _players.remove(self.hakem)
        for player in _players:
            for i in range(13):
                self.deal_card(player, random.choice(self.cards))

    def process_cards(self):
        if len(self.round_cards) < 4:
            raise NotEnoughCardsError

        if self.hokm in [card.suit for card in self.round_cards]:
            for card in self.round_cards.copy():
                if card.suit != self.hokm:
                    self.round_cards.pop(card)
        else:
            first_card = list(self.round_cards)[0]
            for card in self.round_cards.copy():
                if card.suit != first_card.suit:
                    self.round_cards.pop(card)
        winner_card = max(list(self.round_cards))
        winner = self.round_cards.get(winner_card)
        winner.win()
        self.turn = winner
        self.round_cards.clear()
        self.state = GameStates.PLAYING

        if winner.wins == 7:
            losers = self.players.copy()
            losers.remove(winner)
            losers.remove(winner.ally)
            if self.hakem == winner and losers[0].wins == 0:
                winner.score(2)
            elif self.hakem in losers and self.hakem.wins == 0:
                winner.score(3)
            else:
                winner.score(1)

            for player in self.players:
                player.wins = 0

            if self.round == self.rounds:
                self.round -= 1
                self.finish()
                return winner

            if winner not in (self.hakem, self.hakem.ally):
                self.next_hakem()

            self.cards = Card.all.copy()
            self.deal_to_hakem()
            self.round += 1
            self.turn = self.hakem
            self.state = GameStates.CHOOSING_HOKM

        return winner

    def start(self):
        if self.state and self.state != GameStates.FINISHED:
            raise GameStartedError(self.game_id)

        if len(self.players) < 4:
            raise NotEnoughPlayersError(self.game_id)

        # Organizing Players
        _players = self.players.copy()
        self.players.clear()
        self.players.append(_players[0])
        ally = _players[0].ally
        _players.pop(0)
        _players.remove(ally)
        list(map(self.players.append, (_players[0], ally, _players[1])))
        del _players

        # Choosing the Hakem randomly and deal him 5 random cards
        self.hakem = random.choice(self.players)
        self.deal_to_hakem()
        self.turn = self.hakem

        self.state = GameStates.CHOOSING_HOKM
        self.round += 1

    def finish(self):
        if self.state == GameStates.FINISHED:
            raise GameFinishedError(self.game_id)

        for player in self.players:
            player.exit_game()
        self.state = GameStates.FINISHED
        self.instances.remove(self)

    @classmethod
    def get_instance(cls, game_or_chat_id: Union['Game', int]):
        for instance in cls.instances:
            if game_or_chat_id in (instance.game_id, instance.chat_id):
                return instance

        raise ValueError(f"No game with id {game_or_chat_id}")

    def __getitem__(self, user_name_or_id: Union[str, int]):
        for player in self.players:
            if user_name_or_id in (player.user_id, player.name):
                return player

        raise ValueError(f"No player in game {self.game_id} with id/name {user_name_or_id}")

    def __contains__(self, user_name_or_id: Union[str, int]):
        for player in self.players:
            if user_name_or_id in (player.user_id, player.name):
                return True

    def __repr__(self):
        return f"<Game {self.game_id}>"


class GameStates:
    FINISHED = 'finished'
    CHOOSING_HOKM = 'choosing_hokm'
    PLAYING = 'playing'
