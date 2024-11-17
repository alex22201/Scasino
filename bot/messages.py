class RegistrationMessages:
    SHARE_NUMBER_MESSAGE = 'Now please share your phone number so that we can contact you.'
    PLEASE_ENTER_CORRECT_AGE = 'Please enter the correct age.'
    REGISTRATION_COMPLETED = 'Registration is complete! Welcome, {username}! 🎉\nSelect an action from the menu below:'
    SHARE_PHONE_BUTTON_MESSAGE = 'Please press the button to share your phone number.'
    UNDERAGE_MESSAGE = 'You are too young to play! 😜 Go study some more math! 📚'

    @staticmethod
    def get_welcome_message(username: str, balance: int) -> str:
        return f'Welcome back, {username}! 🎰\nBalance: {balance}💰'

    @staticmethod
    def get_registration_message(username: str) -> str:
        return f'Welcome to S-Casino, {username}! 🎰\nYou have been registered with a starting balance of 100💰.\n' \
               'Please tell me, how old are you?'

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
