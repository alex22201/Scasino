from gettext import textdomain
from imghdr import tests

from bot.utils import convert_time_delta
from database.models import User
from database.queries import get_users_by_balance_and_rank


class RegistrationMessages:
    SHARE_NUMBER_MESSAGE = (
        'Now please share your phone number so that we can contact you.'
    )
    PLEASE_ENTER_CORRECT_AGE = 'Please enter the correct age.'
    REGISTRATION_COMPLETED = 'Registration is complete! Welcome, {username}! 🎉\nSelect an action from the menu below:'
    SHARE_PHONE_BUTTON_MESSAGE = 'Please press the button to share your phone number.'
    UNDERAGE_MESSAGE = 'You are too young to play! 😜 Go study some more math! 📚'

    @staticmethod
    def get_welcome_message(username: str, balance: int) -> str:
        return f'Welcome back, {username}! 🎰\nBalance: {balance}💰'

    @staticmethod
    def get_registration_message(username: str) -> str:
        return (
            f'Welcome to S-Casino, {username}! 🎰\nYou have been registered with a starting balance of 100💰.\n'
            'Please tell me, how old are you?'
        )

    @staticmethod
    def get_registration_completed_message(username: str) -> str:
        return RegistrationMessages.REGISTRATION_COMPLETED.format(username=username)


class ErrorMessages:
    REGISTRATION_ERROR_MESSAGE: str = 'An error occurred during registration.'
    AGE_SAVE_ERROR: str = 'There was an error in saving your age.'
    CONTACT_SAVE_ERROR: str = 'There was an error in saving your phone number.'


class MenuMessages:
    GAMES_SELECTED: str = '🎲 You selected Games!'
    CABINET_SELECTED: str = '👤 This is your Cabinet.'
    RATING_SELECTED: str = '📈 Player Ranking.'
    DAILY_BONUS_SELECTED: str = '🎁 Claim your daily bonus!'

    @staticmethod
    def get_cabinet_message(user: User) -> str:
        text = (
            f'📋 *Your Cabinet*\n\n'
            f'👤 *Username:* {user.username}\n'
            f"📅 *Registration Date:* {user.registration_date.strftime('%d %B %Y %H:%M:%S')}\n"
            f'💰 *Balance:* {user.balance}\n'
        )
        return text

    @staticmethod
    def generate_balance_ranking_text(telegram_id: int) -> str:
        """
        Generate a beautifully formatted text showing the top-10 users by balance
        and the current user's rank.
        :param telegram_id: Telegram ID of the current user.
        :return: Generated text.
        """
        top_users, rank = get_users_by_balance_and_rank(telegram_id)

        # Header
        text = '🏆 *Leaderboard: Top-10 Users by Balance* 🏆\n\n'
        text += '🔝 *Top 10 Users:*\n'

        # Add top-10 users
        for index, user in enumerate(top_users, start=1):
            text += f'{index}. 👤 *{user.username}* — 💰 `{user.balance} $`\n'

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
        text += '\n💡 *Keep trading to improve your rank!*'

        return text


class BonusMessages:
    CLAIM_BONUS_MESSAGE = '🎉 Bonus successfully claimed!'
    CLAIM_BONUS_UNAVAILABLE_MESSAGE = '⏳ Bonus is not yet available!'

    @staticmethod
    def get_bonus_available_message(time=None) -> str:
        if time:
            bonus_status = f'⏳ Bonus will be available in {convert_time_delta(time)}.'
        else:
            bonus_status = '✅ Bonus is available!'
        return f'*Bonus Status:*\n{bonus_status}'

    @staticmethod
    def get_successful_claimed_bonus_message(balance: int) -> str:
        text = (f'Your new balance: {balance}.\n '
                f'Come back for the next bonus tomorrow!')
        return text
