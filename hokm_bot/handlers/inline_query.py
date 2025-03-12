from hokm_game import Player, GameStates, Card
from telegram import InlineQueryResultCachedSticker, InlineQueryResultArticle, InputTextMessageContent
from ..utils import stickers
from ..database.funcs import database_config
from uuid import uuid4
import i18n


@database_config
async def card_choosing(update, context):
    query = update.inline_query
    user = query.from_user

    try:
        player = Player.get_instance(user.id)
    except ValueError:
        await query.answer([
            InlineQueryResultArticle(
                str(uuid4()),
                i18n.t('hokm.messages.not_playing'),
                input_message_content=InputTextMessageContent("/newgame"),
                description=i18n.t('hokm.messages.click_to_new_game.start')
            )
        ], 0)
        return
    game = player.game

    if game.state and game.state != GameStates.FINISHED:
        results = [
            InlineQueryResultArticle(
                str(uuid4()),
                "Played Cards",
                description=f"{' '.join([f'{Card.rank_translations.get(card.rank)[0] if card.rank > 10 or card.rank == 1 else card.rank}{Card.suits_emojis.get(card.suit)}' for card in game.round_cards])}",
                input_message_content=InputTextMessageContent(i18n.t('hokm.messages.not_card'))
            )
        ]

    match game.state:
        case GameStates.CHOOSING_HOKM:
            if game.hakem == player:
                results.extend(
                    [
                        InlineQueryResultCachedSticker(
                            str(uuid4()),
                            stickers.get(suit),
                        )
                        for suit in ('hearts', 'diamonds', 'clubs', 'spades')
                    ] +
                    [
                        InlineQueryResultCachedSticker(
                            str(uuid4()),
                            card.get_file_id(),
                            input_message_content=InputTextMessageContent(i18n.t('hokm.messages.card_not_ready'))
                        ) for card in player.deck
                    ] +
                    [
                        InlineQueryResultCachedSticker(
                            str(uuid4()), stickers.get(player.position[:-1]),
                            input_message_content=InputTextMessageContent(i18n.t('hokm.messages.card_not_ready'))
                        ) for i in range(8)
                    ]
                )
            else:
                results.extend([
                    InlineQueryResultCachedSticker(
                        str(uuid4()),
                        stickers.get(player.position[:-1]),
                        input_message_content=InputTextMessageContent(i18n.t('hokm.messages.card_not_ready'))
                    ) for i in range(13)
                ])

        case GameStates.PLAYING:
            deck = [card for card in player.deck if player.is_playable(card)] + [card for card in player.deck if not player.is_playable(card)]
            results.extend([
                InlineQueryResultCachedSticker(
                    id=str(uuid4()),
                    sticker_file_id=card.get_file_id() if player.is_playable(card) else card.get_file_id(True),
                    input_message_content=
                    InputTextMessageContent("This is not your turn.") if game.turn != player
                    else InputTextMessageContent(i18n.t('hokm.messages.card_not_ready')) if not player.is_playable(card)
                    else None
                )
                for card in deck
            ])
        case _:
            results = [
                InlineQueryResultArticle(
                    str(uuid4()),
                    i18n.t('hokm.messages.not_playing'),
                    input_message_content=InputTextMessageContent("/newgame"),
                    description=i18n.t('hokm.messages.click_to_new_game')
                )
            ]

    await query.answer(results, 0)
