from telegram import Update
from telegram.ext import ContextTypes

from bot.keyboards import KeyboardTemplates


async def back_to_main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    await query.edit_message_text(
        text='📋 Main Menu\nChoose an option:',
        reply_markup=KeyboardTemplates.main_menu_keyboard(),
    )
