import asyncio
import random

from telegram import Update
from telegram.ext import ContextTypes

from bot.handlers.games.abstract import AbstractGame
from bot.keyboards import KeyboardTemplates
from bot.messages import CoinFlipMessages
from bot.services import GameService
from config import COIN_FLIP_GIF_URL
from database.models import Session
from database.models import User
from database.queries import get_user_by_username


class CoinFlipGame(AbstractGame):
    gif_url: str = COIN_FLIP_GIF_URL

    @classmethod
    async def start(cls, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Start the game: check user balance and request a bet amount."""
        chat_id = update.effective_chat.id
        username = update.effective_user.username
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
            text=CoinFlipMessages.welcome_message(balance=balance),
        )
        GameService.start_game(user.telegram_user_id, CoinFlipGame)

    @classmethod
    async def set_bet(cls, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        chat_id = update.effective_chat.id

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

        if not await CoinFlipGame.check_balance(chat_id, bet, update, context):
            return

        GameService.set_bet(update.effective_user.id, bet)

        await context.bot.send_message(
            chat_id=chat_id,
            text=CoinFlipMessages.bet_accepted(bet=bet),
            reply_markup=KeyboardTemplates.coin_flip_choice_keyboard(),
        )

    @classmethod
    async def flip_coin(cls, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Handle user's choice and perform the coin flip."""
        query = update.callback_query
        chat_id = query.message.chat_id

        bet = GameService.get_bet(update.effective_user.id)

        user_choice = query.data.split('_')[-1]
        coin_result = random.choice(['heads', 'tails'])

        # Send GIF for the coin flip
        message = await query.message.reply_animation(cls.gif_url)
        await asyncio.sleep(3)
        await message.delete()

        # Process the coin flip result and update user balance
        result_text = await CoinFlipGame.process_flip_result(chat_id, user_choice, coin_result, bet)

        keyboard = KeyboardTemplates.coin_flip_result_keyboard()
        GameService.pop_game(update.effective_user.id)
        await query.edit_message_text(text=result_text, reply_markup=keyboard)

    @staticmethod
    async def check_balance(chat_id: int, bet: int, update: Update, context: ContextTypes.DEFAULT_TYPE) -> bool:
        """Check if the user has enough balance to place the bet."""
        with Session() as session:
            user = session.query(User).filter_by(
                telegram_user_id=chat_id,
            ).first()
            if not user or user.balance < bet:
                await context.bot.send_message(
                    chat_id=chat_id,
                    text=CoinFlipMessages.INSUFFICIENT_BALANCE,
                )
                return False
        return True

    @staticmethod
    async def process_flip_result(chat_id: int, user_choice: str, coin_result: str, bet: int) -> str:
        """Process the coin flip result and update the user's balance."""
        with Session() as session:
            user = session.query(User).filter_by(
                telegram_user_id=chat_id,
            ).first()
            if not user:
                return CoinFlipMessages.USER_NOT_FOUND

            if coin_result == user_choice:
                winnings = bet * 2
                user.balance += winnings
                session.commit()
                session.refresh(user)
                return CoinFlipMessages.win_message(
                    side='Heads' if coin_result == 'heads' else 'Tails',
                    winnings=winnings,
                    balance=user.balance,
                )
            else:
                user.balance -= bet
                session.commit()
                session.refresh(user)
                return CoinFlipMessages.loss_message(
                    side='Heads' if coin_result == 'heads' else 'Tails',
                    balance=user.balance,
                )
