from abc import ABC, abstractmethod


class AbstractGame(ABC):
    """Abstract base class for games."""

    name: str

    @abstractmethod
    def start(self) -> str:
        """Start the game and return a welcome message."""
        pass
