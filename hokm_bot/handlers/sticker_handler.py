from hokm_game import Player, Card, GameStates
from telegram import InlineKeyboardMarkup, InlineKeyboardButton, helpers
from html import escape
import i18n

from ..utils import BOT_ID, stickers
from ..database.funcs import get_setting, database_config


@database_config
async def sticker_handler(update, context):
    message = update.message
    chat = message.chat
    user = message.from_user

    if not message.via_bot.id == BOT_ID:
        return

    player = Player.get_instance(user.id)
    game = player.game

    match game.state:
        case GameStates.CHOOSING_HOKM:
            game.hokm = dict(zip(Card.suits_emojis.values(), Card.suits_emojis.keys())).get(message.text)
            await chat.send_sticker(stickers.get(game.hokm))
            game.deal_to_all()
            # await chat.send_sticker(stickers.get('honor_' + f'{game.hokm} {Card.suits_emojis.get(game.hokm)}'))
            await chat.send_message(i18n.t('hokm.picked_hokm', hokm=i18n.t('hokm.suits.' + game.hokm) + Card.suits_emojis.get(game.hokm)))
        case GameStates.PLAYING:
            suit = dict(zip(Card.suits_emojis.values(), Card.suits_emojis.keys())).get(message.text.split()[1])
            player.play(Card(suit, int(message.text.split()[0])))
            await chat.send_sticker(stickers.get(f'{int(message.text.split()[0])}{suit[0].upper()}'))
            if len(game.round_cards) == 4:
                winner = game.process_cards()
                await chat.send_message(i18n.t(
                    'hokm.win',
                    team_emoji='🔵' if winner.position.startswith('blue') else '🔴',
                    winner=str(winner),
                    ally=str(winner.ally),
                    wins=winner.wins
                ))
        case GameStates.FINISHED:
            _players = game.players.copy()
            winner_score = [_player.scores for _player in _players]
            for _player in _players:
                if _player.scores == winner_score:
                    winner = _player
                    _players.remove(winner)
                    _players.remove(winner.ally)
                    break
            await chat.send_message(i18n.t(
                'hokm.finished',
                winner_emoji='🔵' if player.position.startswith('blue') else '🔴',
                winner1=winner,
                winner2=winner.ally,
                winner_score=winner.scores,
                loser_emoji='🔵' if _players[0].position.startswith('blue') else '🔴',
                loser1=_players[0],
                loser2=_players[1],
                loser_score=_players[0].scores,
            ))
            del _players
        case _:
            pass

    if game.state and game.state != GameStates.FINISHED:
        blue_team = [player for player in game.players if player.position.startswith('blue')]
        red_team = [player for player in game.players if player not in blue_team]
        await chat.send_message(
            i18n.t(
                'hokm.update',
                round=escape(str(game.round)),
                total_rounds=escape(str(game.rounds)),
                hakem=escape(str(game.hakem)),
                hokm=escape(str(i18n.t('hokm.suits.' + game.hokm)) + Card.suits_emojis.get(game.hokm)),
                blue1=escape(str(blue_team[0])),
                blue2=escape(str(blue_team[1])),
                blue_wins=escape(str(blue_team[0].wins)),
                blue_scores=escape(str(blue_team[0].scores)),
                red1=escape(str(red_team[0])),
                red2=escape(str(red_team[1])),
                red_wins=escape(str(red_team[0].wins)),
                red_scores=escape(str(blue_team[0].scores)),
                played_cards='\n'.join([
                    ('🔵' if player.position.startswith('blue') else '🔴') + escape(f"{str(player.name)}: {Card.rank_translations.get(card.rank)[0] if card.rank > 10 or card.rank == 1 else card.rank} {i18n.t('hokm.suits.' + card.suit)} {Card.suits_emojis.get(card.suit)}") for card, player in game.round_cards.items()
                ]),
                turn=f'<a href="tg://user?id={escape(str(game.turn.user_id))}">{escape(str(game.turn))}</a>'
            ),
            parse_mode='html',
            reply_markup=InlineKeyboardMarkup(
                [
                    [InlineKeyboardButton(i18n.t('hokm.messages.play'), switch_inline_query_current_chat='')] + \
                    ([InlineKeyboardButton(i18n.t("hokm.messages.played_cards_button"), url=helpers.create_deep_linked_url(context.bot.username, f"info{chat.id}"))] if get_setting(game.chat_id, 'announce_played_cards') else [])
                ]
            )
        )

    # for _player in game.players:
    #     await context.bot.send_message(_player.user_id, f"Your Deck:\n{'\n'.join([str(card) for card in _player.deck])}")
