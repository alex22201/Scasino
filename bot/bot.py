from telegram.ext import (Application, CallbackQueryHandler, CommandHandler,
                          ConversationHandler, MessageHandler, filters)

from bot.handlers.bonuses import claim_bonus, handle_bonuses
from bot.handlers.cabinet import handle_cabinet
from bot.handlers.games import handle_games
from bot.handlers.games.coinflip import CoinFlipGame
from bot.handlers.menu import back_to_main_menu
from bot.handlers.rating import handle_rating
from bot.handlers.registration import (AGE, CONTACT, ask_age, ask_contact,
                                       start_command)
from config import BOT_TOKEN


def main():
    app = Application.builder().token(BOT_TOKEN).build()

    registration_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start_command)],
        states={
            AGE: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_age)],
            CONTACT: [MessageHandler(filters.CONTACT, ask_contact)],
        },
        fallbacks=[CommandHandler('start', start_command)],
    )

    app.add_handler(registration_handler)
    app.add_handler(CallbackQueryHandler(handle_cabinet, pattern='^cabinet$'))
    app.add_handler(CallbackQueryHandler(
        back_to_main_menu, pattern='^main_menu$'))
    app.add_handler(CallbackQueryHandler(handle_games, pattern='^games$'))
    app.add_handler(CallbackQueryHandler(handle_rating, pattern='^rating$'))
    app.add_handler(CallbackQueryHandler(
        handle_bonuses, pattern='^daily_bonus$'))
    app.add_handler(CallbackQueryHandler(claim_bonus, pattern='^claim_bonus$'))

    app.add_handler(CallbackQueryHandler(
        CoinFlipGame.start_game, pattern='^coin_flip_start$'))
    app.add_handler(CallbackQueryHandler(
        CoinFlipGame.flip_coin, pattern='^coin_flip_(heads|tails)$'))
    app.add_handler(MessageHandler(
        filters.TEXT & ~filters.COMMAND, CoinFlipGame.set_bet))

    print('Bot is running...')
    app.run_polling()
