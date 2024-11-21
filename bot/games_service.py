from bot.handlers.games.abstract import AbstractGame


class GameService:
    """Service to manage game states for users."""
    active_games = {}

    @classmethod
    def start_game(cls, telegram_user_id: int, game: AbstractGame):
        """Start a game for a user and check their balance."""

        if telegram_user_id in cls.active_games:
            del cls.active_games[telegram_user_id]

        cls.active_games[telegram_user_id] = {}
        cls.active_games[telegram_user_id] = {
            'game': game,
            'state': 'awaiting_bet',
            'bet': 0,
        }

    @classmethod
    def set_bet(cls, telegram_user_id: int, bet_amount: int):
        cls.active_games[telegram_user_id]['bet'] = bet_amount
        cls.active_games[telegram_user_id]['state'] = 'awaiting_choice'

    @classmethod
    def get_bet(cls, telegram_user_id: int):
        bet = cls.active_games[telegram_user_id]['bet']

        return bet

    @classmethod
    def pop_game(cls, telegram_user_id: int):
        if telegram_user_id in cls.active_games:
            del cls.active_games[telegram_user_id]

    @classmethod
    def choose_number(cls, telegram_user_id: int, choice: int):
        cls.active_games[telegram_user_id]['state'] = 'awaiting_choice'
        cls.active_games[telegram_user_id]['choice'] = choice

    @classmethod
    def get_choice(cls, telegram_user_id: int):
        return cls.active_games[telegram_user_id]['choice']
