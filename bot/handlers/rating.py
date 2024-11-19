from telegram import Update
from telegram.ext import ContextTypes

from bot.keyboards import KeyboardTemplates
from bot.messages import MenuMessages


async def handle_rating(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=MenuMessages.generate_balance_ranking_text(
            update.effective_user.id),
        reply_markup=KeyboardTemplates.get_cabinet_keyboard(),
        parse_mode='Markdown',
    )
