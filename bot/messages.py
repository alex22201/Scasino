from datetime import timedelta
from typing import Any
from typing import Optional

from bot.utils import convert_time_delta
from database.models import User


class RegistrationMessages:
    SHARE_NUMBER_MESSAGE: str = 'Now please share your phone number so that we can contact you.'
    PLEASE_ENTER_CORRECT_AGE: str = 'Please enter the correct age.'
    SHARE_PHONE_BUTTON_MESSAGE: str = 'Please press the button to share your phone number.'
    UNDERAGE_MESSAGE: str = 'You are too young to play! 😜 Go study some more math! 📚'

    @staticmethod
    def get_welcome_message(username: str, balance: int) -> str:
        return f'Welcome back, {username}! 🎰\nBalance: {balance} S💰'

    @staticmethod
    def get_registration_message(username: str) -> str:
        return (
            f'Welcome to S-Casino, {username}! 🎰\nYou have been registered with a starting balance of 100 S💰.\n'
            'Please tell me, how old are you?'
        )

    @staticmethod
    def get_registration_completed_message(username: str) -> str:
        return f'Registration is complete! Welcome, {username}! 🎉\nSelect an action from the menu below:'


class ErrorMessages:
    REGISTRATION_ERROR_MESSAGE: str = 'An error occurred during registration.'
    AGE_SAVE_ERROR: str = 'There was an error in saving your age.'
    CONTACT_SAVE_ERROR: str = 'There was an error in saving your phone number.'


class MenuMessages:
    GAMES_SELECTED: str = '🎲 You selected Games!'
    CABINET_SELECTED: str = '👤 This is your Cabinet.'
    RATING_SELECTED: str = '📈 Player Ranking.'
    DAILY_BONUS_SELECTED: str = '🎁 Claim your daily bonus!'
    CHOOSE_GAME: str = '🎮 Choose a game to play:'
    MAIN_MENU: str = '📋 Main Menu\nChoose an option:'

    @staticmethod
    def get_cabinet_message(user: User) -> str:
        text = (
            f'📋 *Your Cabinet*\n\n'
            f'👤 *Username:* {user.username}\n'
            f"📅 *Registration Date:* {user.registration_date.strftime('%d %B %Y %H:%M:%S')}\n"
            f'💰 *Balance:* {user.balance} S\n'
        )
        return text

    @staticmethod
    def generate_balance_ranking_text(top_users: list[User], rank: Any) -> str:
        # Header
        text = '🏆 *Leaderboard: Top-10 Users by Balance* 🏆\n\n'
        text += '🔝 *Top 10 Users:*\n'

        # Add top-10 users
        for index, user in enumerate(top_users, start=1):
            text += f'{index}. 👤 *{user.username}* — 💰 `{user.balance} S`\n'

        # Add user rank
        if rank:
            text += '\n🎖 *Your Position:*\n'
            if rank > 10:
                text += f'📊 You are ranked *{rank}* in the leaderboard!\n'
            else:
                text += f'🌟 You are in the *Top-10*, ranked *{rank}*!\n'
        else:
            text += '\n⚠️ *User not found in the database.*\n'

        # Footer
        text += '\n💡 *Keep gambling to improve your rank!*'

        return text


class BonusMessages:
    CLAIM_BONUS_MESSAGE = '🎉 Bonus successfully claimed!'
    CLAIM_BONUS_UNAVAILABLE_MESSAGE = '⏳ Bonus is not yet available!'

    @staticmethod
    def get_bonus_available_message(time: Optional[timedelta] = None) -> str:
        if time:
            bonus_status = f'⏳ Bonus will be available in {convert_time_delta(time)}.'
        else:
            bonus_status = '✅ Bonus is available!'
        return f'*Bonus Status:*\n{bonus_status}'

    @staticmethod
    def get_successful_claimed_bonus_message(balance: int) -> str:
        text = (
            f'Your new balance: {balance}.\n '
            f'Come back for the next bonus tomorrow!'
        )
        return text


class CoinFlipMessages:
    """Class to store Coin Flip game messages."""
    INSUFFICIENT_BALANCE = "❌ You don't have enough funds for this bet."
    INVALID_BET = '❗ Please enter a valid bet (a number greater than zero).'
    GAME_NOT_FOUND = '❗ Please start a new game.'
    USER_NOT_FOUND = '❌ User not found. Please try again.'
    COIN_FLIPPING = 'The coin is flipping... 🌀'
    NO_GAME_IN_PROGRESS = '❗ Please start a new game.'

    @staticmethod
    def welcome_message(balance: float) -> str:
        return (
            f"🎮 Welcome to the 'Coin Flip' game!\n\n"
            f'Your current balance: {balance} S\nPlease enter your bet amount:'
        )

    @staticmethod
    def bet_accepted(bet: float) -> str:
        return f'Your bet: {bet}. Choose the side of the coin:'

    @staticmethod
    def win_message(side: str, winnings: float, balance: float) -> str:
        return (
            f'🎉 You won! The coin shows {side}.\n'
            f'Your winnings: {winnings}!\nCurrent balance: {balance}'
        )

    @staticmethod
    def loss_message(side: str, balance: float) -> str:
        return (
            f'😞 You lost. The coin shows {side}.\n'
            f'Current balance: {balance} S'
        )


class DiceGameMessages:
    GAME_NOT_FOUND = 'No active game found. Start a new game first.'
    INVALID_BET = 'Invalid bet amount. Please enter a positive number.'
    INSUFFICIENT_BALANCE = "You don't have enough balance to play."
    INSUFFICIENT_FUNDS = "You don't have enough balance for this bet."
    USER_NOT_FOUND = 'User not found in the database.'

    @staticmethod
    def welcome_message(balance: float) -> str:
        return f'🎲 Welcome to the Dice Game! Your current balance: {balance}. Place your bet:'

    @staticmethod
    def bet_accepted(bet: float) -> str:
        return f'Your bet of {bet} has been accepted. Choose a number (1-6):'

    @staticmethod
    def number_chosen(choice: int) -> str:
        return f'You chose the number {choice}. Now roll the dice!'

    @staticmethod
    def win_message(dice_result: int, choice: int, winnings: float, balance: float) -> str:
        return (
            f'🎉 Congratulations! The dice rolled {dice_result}, and you guessed {choice}. '
            f'You won {winnings}! Your new balance: {balance}.'
        )

    @staticmethod
    def loss_message(dice_result: int, choice: int, bet: float, balance: float) -> str:
        return (
            f'😢 The dice rolled {dice_result}, but you guessed {choice}. '
            f'You lost {bet}. Your new balance: {balance}.'
        )
