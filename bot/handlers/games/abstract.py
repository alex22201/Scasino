from abc import ABC
from abc import abstractmethod

from telegram import Update
from telegram.ext import ContextTypes


class AbstractGame(ABC):
    """Abstract base class for games."""

    @classmethod
    @abstractmethod
    async def start(cls, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        pass

    @classmethod
    @abstractmethod
    async def set_bet(cls, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        pass
