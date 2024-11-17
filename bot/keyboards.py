from dataclasses import dataclass

from telegram import (InlineKeyboardButton, InlineKeyboardMarkup,
                      KeyboardButton, ReplyKeyboardMarkup)


@dataclass
class KeyboardTemplates:
    @staticmethod
    def main_menu_keyboard() -> InlineKeyboardMarkup:
        keyboard = [
            [
                InlineKeyboardButton('🎲 Games', callback_data='games'),
                InlineKeyboardButton('👤 Cabinet', callback_data='cabinet'),
            ],
            [
                InlineKeyboardButton('📈 Rating', callback_data='rating'),
                InlineKeyboardButton('🎁 Bonuses', callback_data='daily_bonus'),
            ],
        ]
        return InlineKeyboardMarkup(keyboard)

    @staticmethod
    def get_phone_share_keyboard() -> ReplyKeyboardMarkup:
        contact_button = KeyboardButton('Share number 📞', request_contact=True)
        contact_keyboard = ReplyKeyboardMarkup(
            [[contact_button]], resize_keyboard=True, one_time_keyboard=True)
        return contact_keyboard
