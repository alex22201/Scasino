from telegram.ext import Application
from telegram.ext import CallbackQueryHandler
from telegram.ext import CommandHandler
from telegram.ext import ConversationHandler
from telegram.ext import filters
from telegram.ext import MessageHandler

from bot.handlers.bonuses import claim_bonus
from bot.handlers.bonuses import handle_bonuses
from bot.handlers.games.coinflip import CoinFlipGame
from bot.handlers.games.dice import DiceGame
from bot.handlers.menu import back_to_main_menu
from bot.handlers.menu import handle_bet
from bot.handlers.menu import handle_cabinet
from bot.handlers.menu import handle_games
from bot.handlers.menu import handle_rating
from bot.handlers.registration import AGE
from bot.handlers.registration import ask_age
from bot.handlers.registration import start_command
from config import BOT_TOKEN


def main() -> None:
    app = Application.builder().token(BOT_TOKEN).build()

    # Registration handler
    registration_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start_command)],
        states={
            AGE: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_age)],
        },
        fallbacks=[CommandHandler('start', start_command)],
    )

    # Add handlers for general features
    app.add_handler(registration_handler)
    app.add_handler(CallbackQueryHandler(handle_cabinet, pattern='^cabinet$'))
    app.add_handler(
        CallbackQueryHandler(
            back_to_main_menu, pattern='^main_menu$',
        ),
    )
    app.add_handler(CallbackQueryHandler(handle_games, pattern='^games$'))
    app.add_handler(CallbackQueryHandler(handle_rating, pattern='^rating$'))
    app.add_handler(
        CallbackQueryHandler(
            handle_bonuses, pattern='^daily_bonus$',
        ),
    )
    app.add_handler(CallbackQueryHandler(claim_bonus, pattern='^claim_bonus$'))

    # CoinFlip handlers
    app.add_handler(
        CallbackQueryHandler(
            CoinFlipGame.start, pattern='^coin_flip_start$',
        ),
    )
    app.add_handler(
        CallbackQueryHandler(
            CoinFlipGame.flip_coin, pattern='^coin_flip_(heads|tails)$',
        ),
    )

    # DiceGame handlers
    app.add_handler(
        CallbackQueryHandler(
            DiceGame.start, pattern='^dice_start$',
        ),
    )
    app.add_handler(
        CallbackQueryHandler(
            DiceGame.choose_number,
            pattern='^dice_choice_(1|2|3|4|5|6)$',
        ),
    )
    app.add_handler(
        CallbackQueryHandler(
            DiceGame.roll_dice, pattern='^dice_roll$',
        ),
    )

    app.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND, handle_bet,
        ),
    )

    app.run_polling()
