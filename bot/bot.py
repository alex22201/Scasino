from telegram.ext import (Application, CallbackQueryHandler, CommandHandler,
                          ConversationHandler, MessageHandler, filters)

from bot.handlers.registration import (AGE, CONTACT, ask_age, ask_contact,
                                       handle_menu, start_command)
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
    app.add_handler(CallbackQueryHandler(handle_menu))

    print('Bot is running...')
    app.run_polling()
