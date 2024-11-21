from telegram import Update
from telegram.ext import ContextTypes

from bot.games_service import GameService
from bot.handlers.games.abstract import AbstractGame
from bot.keyboards import KeyboardTemplates
from bot.messages import MenuMessages
from database.models import User
from database.queries import (get_user_by_username,
                              get_users_by_balance_and_rank)


async def back_to_main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query

    await query.edit_message_text(
        text=MenuMessages.MAIN_MENU,
        reply_markup=KeyboardTemplates.main_menu_keyboard(),
        parse_mode='Markdown'
    )


async def handle_games(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=MenuMessages.CHOOSE_GAME,
        reply_markup=KeyboardTemplates.get_games_keyboard(),
        parse_mode='Markdown'
    )


async def handle_rating(update: Update, context: ContextTypes.DEFAULT_TYPE):
    top_users, rank = get_users_by_balance_and_rank(update.effective_user.id)

    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=MenuMessages.generate_balance_ranking_text(top_users, rank),
        reply_markup=KeyboardTemplates.get_cabinet_keyboard(),
        parse_mode='Markdown',
    )


async def handle_cabinet(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_details: User = get_user_by_username(update.effective_user.username)

    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=MenuMessages.get_cabinet_message(user_details),
        reply_markup=KeyboardTemplates.get_cabinet_keyboard(),
        parse_mode='Markdown',
    )


# I don't know where to put it.
async def handle_bet(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_telegram_id = update.effective_user.id
    game: AbstractGame = GameService.active_games[user_telegram_id].get('game')
    await game.set_bet(update, context)
#
