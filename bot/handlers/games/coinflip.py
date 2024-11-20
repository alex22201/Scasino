import asyncio
import random

from telegram import Update
from telegram.ext import ContextTypes

from bot.keyboards import KeyboardTemplates
from bot.messages import CoinFlipMessages
from database.models import Session, User
from database.queries import get_user_by_username


class CoinFlipGame:
    """Класс игры 'Coin Flip'."""

    active_games = {}

    @staticmethod
    async def start_game(update, context):
        """Start the game: check user balance and request a bet amount."""
        chat_id = update.effective_chat.id
        username = update.effective_user.username or f'User{chat_id}'

        user: User = get_user_by_username(username=username)
        balance = user.balance

        if balance <= 0:
            await context.bot.send_message(
                chat_id=chat_id,
                text=CoinFlipMessages.INSUFFICIENT_BALANCE,
            )
            return

        await context.bot.send_message(
            chat_id=chat_id,
            text=CoinFlipMessages.WELCOME_MESSAGE.format(balance=balance),
        )
        CoinFlipGame.active_games[chat_id] = {'state': 'awaiting_bet'}

    @staticmethod
    async def set_bet(update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Set the bet and allow the user to choose a side."""
        chat_id = update.effective_chat.id
        if chat_id not in CoinFlipGame.active_games or CoinFlipGame.active_games[chat_id].get(
                'state') != 'awaiting_bet':
            await context.bot.send_message(
                chat_id=chat_id,
                text=CoinFlipMessages.GAME_NOT_FOUND,
            )
            return

        try:
            bet = int(update.message.text)
            if bet <= 0:
                raise ValueError
        except ValueError:
            await context.bot.send_message(
                chat_id=chat_id,
                text=CoinFlipMessages.INVALID_BET,
            )
            return

        with Session() as session:
            user = session.query(User).filter_by(
                telegram_user_id=chat_id).first()
            if not user or user.balance < bet:
                await context.bot.send_message(
                    chat_id=chat_id,
                    text=CoinFlipMessages.INSUFFICIENT_BALANCE,
                )
                return

        CoinFlipGame.active_games[chat_id] = {
            'state': 'awaiting_choice', 'bet': bet}
        keyboard = KeyboardTemplates.coin_flip_choice_keyboard()

        await context.bot.send_message(
            chat_id=chat_id,
            text=CoinFlipMessages.BET_ACCEPTED.format(bet=bet),
            reply_markup=keyboard,
        )

    @staticmethod
    async def flip_coin(update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle user's choice and perform the coin flip."""
        query = update.callback_query
        chat_id = query.message.chat_id

        if chat_id not in CoinFlipGame.active_games or CoinFlipGame.active_games[chat_id].get(
                'state') != 'awaiting_choice':
            await query.answer(CoinFlipMessages.NO_GAME_IN_PROGRESS, show_alert=True)
            return

        user_choice = query.data.split('_')[-1]
        bet = CoinFlipGame.active_games[chat_id]['bet']
        coin_result = random.choice(['heads', 'tails'])

        await query.answer(CoinFlipMessages.COIN_FLIPPING)
        await asyncio.sleep(2)

        with Session() as session:
            user = session.query(User).filter_by(
                telegram_user_id=chat_id).first()
            if not user:
                await query.edit_message_text(text=CoinFlipMessages.USER_NOT_FOUND)
                return

            if coin_result == user_choice:
                winnings = bet * 2
                user.balance += winnings
                session.commit()
                session.refresh(user)
                result_text = CoinFlipMessages.WIN_MESSAGE.format(
                    side='Heads' if coin_result == 'heads' else 'Tails',
                    winnings=winnings,
                    balance=user.balance,
                )
            else:
                user.balance -= bet
                session.commit()
                session.refresh(user)
                result_text = CoinFlipMessages.LOSS_MESSAGE.format(
                    side='Heads' if coin_result == 'heads' else 'Tails',
                    balance=user.balance,
                )

        keyboard = KeyboardTemplates.coin_flip_result_keyboard()
        CoinFlipGame.active_games.pop(chat_id, None)

        await query.edit_message_text(text=result_text, reply_markup=keyboard)
