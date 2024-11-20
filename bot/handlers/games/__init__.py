from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes


async def handle_games(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Генерация списка игр
    reply_markup = InlineKeyboardMarkup([
        [InlineKeyboardButton('🎮 Coin Flip', callback_data='coin_flip_start')],
        [InlineKeyboardButton('🔙 Вернуться в меню',
                              callback_data='main_menu')],
    ])
    # Добавляем кнопку "Back to Menu"

    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text='🎮 Choose a game to play:',
        reply_markup=reply_markup
    )
