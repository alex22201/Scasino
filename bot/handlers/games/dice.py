import asyncio
import random

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes

from bot.games_service import GameService
from bot.handlers.games.abstract import AbstractGame
from bot.keyboards import KeyboardTemplates
from bot.messages import DiceGameMessages
from config import DICE_GIT_URL
from database.models import Session, User


class DiceGame(AbstractGame):
    """Class for the 'Dice Game'."""

    gif_url: str = DICE_GIT_URL

    @staticmethod
    async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Start the game and check the player's balance."""
        chat_id = update.effective_chat.id

        with Session() as session:
            user = session.query(User).filter_by(
                telegram_user_id=chat_id).first()
            if not user or user.balance <= 0:
                await context.bot.send_message(
                    chat_id=chat_id,
                    text=DiceGameMessages.INSUFFICIENT_BALANCE,
                )
                return

            balance = user.balance

        await context.bot.send_message(
            chat_id=chat_id,
            text=DiceGameMessages.welcome_message(balance=balance),
        )
        GameService.start_game(user.telegram_user_id, DiceGame)

    @staticmethod
    async def set_bet(update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Allow the player to place a bet."""
        chat_id = update.effective_chat.id

        try:
            bet = int(update.message.text)
            if bet <= 0:
                raise ValueError
        except ValueError:
            await context.bot.send_message(
                chat_id=chat_id,
                text=DiceGameMessages.INVALID_BET,
            )
            return

        with Session() as session:
            user = session.query(User).filter_by(
                telegram_user_id=chat_id).first()
            if not user or user.balance < bet:
                await context.bot.send_message(
                    chat_id=chat_id,
                    text=DiceGameMessages.INSUFFICIENT_FUNDS,
                )
                return

        GameService.set_bet(update.effective_user.id, bet)

        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton(
                str(i), callback_data=f'dice_choice_{i}') for i in range(1, 7)]
        ])
        await context.bot.send_message(
            chat_id=chat_id,
            text=DiceGameMessages.bet_accepted(bet=bet),
            reply_markup=keyboard,
        )

    @staticmethod
    async def choose_number(update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle the player's choice of a dice number."""
        query = update.callback_query
        choice = int(query.data.split('_')[-1])

        GameService.choose_number(update.effective_user.id, choice)
        await query.edit_message_text(
            text=DiceGameMessages.number_chosen(choice=choice),
            reply_markup=KeyboardTemplates.dice_roll_keyboard(),
        )

    @classmethod
    async def roll_dice(cls, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle the dice roll and calculate the result."""
        query = update.callback_query
        chat_id = query.message.chat_id

        bet = GameService.get_bet(update.effective_user.id)
        player_choice = GameService.get_choice(update.effective_user.id)
        dice_result = random.randint(1, 6)

        message = await query.message.reply_animation(cls.gif_url)
        await asyncio.sleep(3)
        await message.delete()

        with Session() as session:
            user = session.query(User).filter_by(
                telegram_user_id=chat_id).first()
            if not user:
                await query.edit_message_text(text=DiceGameMessages.USER_NOT_FOUND)
                return

            if player_choice == dice_result:
                winnings = bet * 6
                user.balance += winnings
                result_text = DiceGameMessages.win_message(
                    choice=player_choice,
                    dice_result=dice_result,
                    winnings=winnings,
                    balance=user.balance,
                )
            else:
                user.balance -= bet
                result_text = DiceGameMessages.loss_message(
                    choice=player_choice,
                    dice_result=dice_result,
                    bet=bet,
                    balance=user.balance,
                )

            session.commit()
            session.refresh(user)

        keyboard = KeyboardTemplates.dice_result_keyboard()
        GameService.pop_game(update.effective_user.id)

        await query.edit_message_text(text=result_text, reply_markup=keyboard)
