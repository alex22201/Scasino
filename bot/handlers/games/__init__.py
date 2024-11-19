from telegram import Update
from telegram.ext import ContextTypes

from bot.keyboards import KeyboardTemplates
from bot.messages import MenuMessages
from database.models import User
from database.queries import get_user_by_username


async def handle_games(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_details: User = get_user_by_username(update.effective_user.username)

    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=MenuMessages.get_cabinet_message(user_details),
        reply_markup=KeyboardTemplates.get_cabinet_keyboard(),
        parse_mode='Markdown',
    )
