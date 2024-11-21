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
            [[contact_button]], resize_keyboard=True, one_time_keyboard=True
        )
        return contact_keyboard

    @staticmethod
    def get_cabinet_keyboard() -> InlineKeyboardMarkup:
        keyboard = [
            [InlineKeyboardButton('Back to Menu', callback_data='main_menu')],
        ]
        return InlineKeyboardMarkup(keyboard)

    @staticmethod
    def get_bonus_keyboard(bonus_available: bool = False) -> InlineKeyboardMarkup:
        keyboard_buttons = []
        if bonus_available:
            keyboard_buttons.append([InlineKeyboardButton(
                '🎁 Claim', callback_data='claim_bonus')])
        keyboard_buttons.append([InlineKeyboardButton(
            '🔙 Back to Menu', callback_data='main_menu')])
        keyboard = InlineKeyboardMarkup(keyboard_buttons)
        return keyboard

    @staticmethod
    def get_claim_bonus_keyboard() -> InlineKeyboardMarkup:
        return InlineKeyboardMarkup([
            [InlineKeyboardButton('🔙 Back to Menu', callback_data='main_menu')]
        ])

    @staticmethod
    def coin_flip_choice_keyboard() -> InlineKeyboardMarkup:
        return InlineKeyboardMarkup([
            [
                InlineKeyboardButton(
                    '🪙 Heads', callback_data='coin_flip_heads'),
                InlineKeyboardButton(
                    '🪙 Tails', callback_data='coin_flip_tails'),
            ],
            [InlineKeyboardButton(
                '🔙 Back to Game Menu', callback_data='games')],
        ])

    @staticmethod
    def coin_flip_result_keyboard() -> InlineKeyboardMarkup:
        return InlineKeyboardMarkup([
            [InlineKeyboardButton(
                '🔄 Play Again', callback_data='coin_flip_start')],
            [InlineKeyboardButton(
                '🔙 Back to Game Menu', callback_data='games')],
        ])

    @staticmethod
    def dice_number_keyboard():
        return InlineKeyboardMarkup([
            [InlineKeyboardButton(
                str(i), callback_data=f'dice_choice_{i}') for i in range(1, 7)]
        ])

    @staticmethod
    def dice_roll_keyboard():
        return InlineKeyboardMarkup([
            [InlineKeyboardButton('🎲 Roll the Dice!',
                                  callback_data='dice_roll')]
        ])

    @staticmethod
    def dice_result_keyboard():
        return InlineKeyboardMarkup([
            [InlineKeyboardButton('🔄 Play Again', callback_data='dice_start')],
            [InlineKeyboardButton('🔙 Back to Game Menu',
                                  callback_data='games')],
        ])

    @staticmethod
    def get_games_keyboard() -> InlineKeyboardMarkup:
        reply_markup = InlineKeyboardMarkup([
            [InlineKeyboardButton(
                '🎮 Coin Flip', callback_data='coin_flip_start')],
            [InlineKeyboardButton('🎲 Dice Game', callback_data='dice_start')],
            [InlineKeyboardButton('🔙 Back to menu',
                                  callback_data='main_menu')],
        ])
        return reply_markup
