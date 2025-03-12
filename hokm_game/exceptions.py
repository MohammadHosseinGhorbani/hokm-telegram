from typing import TYPE_CHECKING, List

if TYPE_CHECKING:
    from .card import Card
    from .player import Player


class PlayerInGameError(Exception):
    def __init__(self, game_id, player_id):
        super().__init__(f"Player {player_id} is already in game {game_id}.")


class PlayerNotInGameError(Exception):
    def __init__(self, game_id, player_id):
        super().__init__(f"Player {player_id} is not joined in game {game_id}.")


class GameStartedError(Exception):
    def __init__(self, game_id):
        super().__init__(f"Game {game_id} is already started.")


class GameFinishedError(Exception):
    def __init__(self, game_id):
        super().__init__(f"Game {game_id} is already finished.")


class TooManyPlayersError(Exception):
    def __init__(self, game_id):
        super().__init__(f"Game {game_id} has already 4 players.")


class CardDealtError(Exception):
    def __init__(self, card: 'Card'):
        super().__init__(f"The card {card.rank} of {card.suit} is already dealt.")


class DifferentSuitsError(Exception):
    def __init__(self, card1: 'Card', card2: 'Card'):
        super().__init__(f"These cards have different suits and aren't comparable: {card1.suit}, {card2.suit}.")


class NotEnoughPlayersError(Exception):
    def __init__(self, game_id):
        super().__init__(f"Game {game_id} doesn't have enough players.")
        
        
class NotEnoughCardsError(Exception):
    def __init__(self):
        super().__init__(f"All players should play a card first.")


class NotPlayableError(Exception):
    def __init__(self, card: 'Card', round_cards: List['Card']):
        super().__init__(f"In this situation ({round_cards}), {card} is not playable")


class AlreadyPlayedError(Exception):
    def __init__(self, player: 'Player'):
        super().__init__(f"Player {player} has already played a card.")
