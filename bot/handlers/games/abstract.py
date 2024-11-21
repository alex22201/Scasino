from abc import ABC, abstractmethod


class AbstractGame(ABC):
    """Abstract base class for games."""

    @staticmethod
    @abstractmethod
    async def start(*args, **kwargs):
        """Start the game and return a welcome message."""
        pass

    @staticmethod
    @abstractmethod
    async def set_bet(*args, **kwargs):
        pass
