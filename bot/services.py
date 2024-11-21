from typing import Any

from bot.handlers.games.abstract import AbstractGame


class GameService:
    """Service to manage game states for users."""
    active_games: dict[int, dict[str, Any[AbstractGame | str | int]]] = {}

    @classmethod
    def start_game(cls, telegram_user_id: int, game: type[AbstractGame]) -> None:
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
    def set_bet(cls, telegram_user_id: int, bet_amount: int) -> None:
        cls.active_games[telegram_user_id]['bet'] = bet_amount
        cls.active_games[telegram_user_id]['state'] = 'awaiting_choice'

    @classmethod
    def get_bet(cls, telegram_user_id: int) -> int:
        bet: int = cls.active_games[telegram_user_id]['bet']

        return bet

    @classmethod
    def pop_game(cls, telegram_user_id: int) -> None:
        if telegram_user_id in cls.active_games:
            del cls.active_games[telegram_user_id]

    @classmethod
    def choose_number(cls, telegram_user_id: int, choice: int) -> None:
        cls.active_games[telegram_user_id]['state'] = 'awaiting_choice'
        cls.active_games[telegram_user_id]['choice'] = choice

    @classmethod
    def get_choice(cls, telegram_user_id: int) -> int:
        choice: int = cls.active_games[telegram_user_id]['choice']
        return choice
