from ..database.funcs import set_gorup_language, database_config
from hokm_game import Game, GameStates, Player, Card, PlayerInGameError
from telegram import InlineKeyboardMarkup, InlineKeyboardButton
from html import escape
import i18n


def new_game_markup(blue1=None, blue2=None, red1=None, red2=None, game_id=None):
    keyboard = [
        [InlineKeyboardButton(f"🔵 {i18n.t('hokm.messages.blue')} 🔵", callback_data='user0'), InlineKeyboardButton(f"🔴 {i18n.t('hokm.messages.red')} 🔴", callback_data='user0')],
        [
            InlineKeyboardButton(
                text=blue1.name if blue1 else "+",
                callback_data=f"user{blue1.user_id}" if blue1 else "join_blue1"
            ),
            InlineKeyboardButton(
                text=red1.name if red1 else "+",
                callback_data=f"user{red1.user_id}" if red1 else "join_red1"
            )
        ],
        [
            InlineKeyboardButton(
                text=blue2.name if blue2 else "+",
                callback_data=f"user{blue2.user_id}" if blue2 else "join_blue2"
            ),
            InlineKeyboardButton(
                text=red2.name if red2 else "+",
                callback_data=f"user{red2.user_id}" if red2 else "join_red2"
            )
        ],
    ]
    if game_id:
        keyboard.extend([
            [InlineKeyboardButton(i18n.t('hokm.messages.choose_rounds'), callback_data=f"user0")],
            [InlineKeyboardButton(str(rounds), callback_data=f'start{rounds}_{game_id}') for rounds in (1, 3, 5, 7)]
        ])
    return InlineKeyboardMarkup(keyboard)


def organized_players(players):
    if not players:
        return []
    for position in ['blue1', 'blue2', 'red1', 'red2']:
        found = False
        for player in players:
            if player.position == position:
                yield player
                found = True
                break
        if not found:
            yield


@database_config
async def newgame_command(update, context):
    message = update.message

    if message.chat.id in {game.chat_id for game in Game.instances}:
        game = Game.get_instance(message.chat.id)
        if game.state and game.state != GameStates.FINISHED:
            await message.reply_text(i18n.t('hokm.messages.game_already_started'))
            return
        else:
            game.finish()

    game = Game(message.chat.id)
    markup = new_game_markup()
    await message.chat.send_message(i18n.t('hokm.messages.new_game'), reply_markup=markup)


@database_config
async def join_button(update, context):
    query = update.callback_query
    message = query.message
    chat = message.chat
    user = query.from_user

    game = Game.get_instance(chat.id)

    # try:
    #     await user.send_message(f"You've joined a game in the chat {chat.title}. When it starts, I'll let you know.")
    # except:
    #     await query.answer("You should start the bot first, in order to join a game.", show_alert=True)
    #     return

    if user.id in game:
        game.remove_player(user.id)
    try:
        game.add_player(Player(user.id, user.first_name, query.data.lstrip('join_')))
    except PlayerInGameError:
        chat_name = (await context.bot.get_chat(Player.get_instance(user.id).game.chat_id)).title
        await query.answer(i18n.t('hokm.messages.already_in_game', chat_name=chat_name), show_alert=True)
        return

    await message.edit_reply_markup(new_game_markup(
        *organized_players(game.players),
        game_id=game.game_id if len(game.players) == 4 else None
    ))

    await query.answer(i18n.t('hokm.messages.joined'))


@database_config
async def user_button(update, context):
    query = update.callback_query
    message = query.message
    chat = message.chat
    user = query.from_user

    game = Game.get_instance(chat.id)

    if user.id == int(query.data.lstrip('user')):
        game.remove_player(user.id)
        await message.edit_reply_markup(new_game_markup(
            *organized_players(game.players),
            game_id=game.game_id if len(game.players) == 4 else None
        ))
        await query.answer(i18n.t('hokm.messages.left'))
    else:
        await query.answer()


@database_config
async def start_button(update, context):
    query = update.callback_query
    message = query.message
    chat = message.chat

    data_list = query.data.split('_')
    game_id = int(data_list[-1])
    rounds = int(data_list[0].lstrip('start'))
    game = Game.get_instance(game_id)
    game.rounds = rounds

    if game.state and game.state != GameStates.FINISHED:
        await query.answer(i18n.t('hokm.messages.game_already_started'), show_alert=True)
        return

    players = [
        [player for player in game.players if player.position.startswith('blue')],
        [player for player in game.players if player.position.startswith('red')]
    ]
    players[0][0].set_ally(players[0][1])
    players[1][0].set_ally(players[1][1])
    game.start()

    # for player in game.players:
    #     announcement = f"The game in chat {chat.title} has started! "
    #     if player == game.hakem:
    #         announcement += f"You are Hakem and these are your cards:\n{'\n'.join([str(card) for card in player.deck])}"
    #     elif player.ally == game.hakem:
    #         announcement += f"Your ally {player.ally.name} is Hakem."
    #     else:
    #         announcement += f"Unfortunately neither you nor your ally are Hakem."
    #     await context.bot.send_message(player.user_id, announcement)

    await message.edit_text(i18n.t('hokm.messages.game_started'))
    await chat.send_message(
        i18n.t(
            'hokm.game_start',
            hakem=f'<a href="tg://user?id={escape(str(game.hakem.user_id))}">{escape(str(game.hakem))}</a>'
        ),
        parse_mode='html',
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(i18n.t('hokm.messages.pick_suit'), switch_inline_query_current_chat='')]])
    )


@database_config
async def leave_command(update, context):
    message = update.message
    chat = message.chat
    user = message.from_user

    try:
        game = Game.get_instance(chat.id)
    except ValueError:
        return
    if game.state not in (GameStates.PLAYING, GameStates.CHOOSING_HOKM):
        await message.reply_text("بازی در جریان نیست")
        return
    team = game[user.id].position[:-1]
    await message.reply_text(i18n.t(f'hokm.messages.{team}_leave'), reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(f'Join {team}', callback_data=f'replace_{user.id}')]]))


@database_config
async def replace_button(update, context):
    query = update.callback_query
    message = query.message
    chat = message.chat
    new_user = query.from_user

    game = Game.get_instance(chat.id)

    if new_user.id in game:
        chat_name = (await context.bot.get_chat(Player.get_instance(new_user.id).game.chat_id)).title
        await query.answer(i18n.t('hokm.messages.already_in_game', chat_name=chat_name), show_alert=True)
        return

    old_user = game[int(query.data.lstrip('replace_'))]
    team = old_user.position[:-1]
    old_user.user_id = new_user.id
    old_user.name = new_user.first_name

    await message.edit_text(i18n.t(f'hokm.messages.new_{team}', new_player=new_user.first_name))
    await query.answer()


async def get_played_cards(update, context):
    message = update.message

    chat_id = int(message.text.lstrip('/start info'))
    game = Game.get_instance(chat_id)

    played_cards = game.all_played_cards
    unplayed_cards = [card for card in Card.all if card not in played_cards]

    set_gorup_language(chat_id)
    await message.reply_text(i18n.t(
        "hokm.all_played_cards",
        played_cards=', '.join([f'{Card.rank_translations.get(card.rank)[0] if card.rank > 10 or card.rank == 1 else card.rank}{Card.suits_emojis.get(card.suit)}' for card in played_cards]),
        remaining_cards=', '.join(([f'{Card.rank_translations.get(card.rank)[0] if card.rank > 10 or card.rank == 1 else card.rank}{Card.suits_emojis.get(card.suit)}' for card in unplayed_cards]))
    ))


@database_config
async def end_command(update, context):
    chat = update.message.chat

    try:
        game = Game.get_instance(chat.id)
    except ValueError:
        await chat.send_message(i18n.t('hokm.messages.no_game'))
        return

    if not game.state or game.state == GameStates.FINISHED:
        await chat.send_message(i18n.t('hokm.messages.no_game'))
        return

    blue_team = [player for player in game.players if player.position.startswith('blue')]
    red_team = [player for player in game.players if player not in blue_team]
    game.finish()

    await chat.send_message(i18n.t(
        'hokm.manual_end',
        round=game.round,
        total_rounds=game.rounds,
        blue1=str(blue_team[0]),
        blue2=str(blue_team[1]),
        blue_score=blue_team[0].scores,
        red1=str(red_team[0]),
        red2=str(red_team[1]),
        red_score=red_team[0].scores,
        played_cards=len(game.all_played_cards),
        remaining_cards=len(Card.all) - len(game.all_played_cards),

    ))
