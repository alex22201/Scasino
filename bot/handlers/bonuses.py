from datetime import datetime
from datetime import timedelta

from telegram import Update
from telegram.ext import ContextTypes

from bot.keyboards import KeyboardTemplates
from bot.messages import BonusMessages
from config import TIME_BONUS_AMOUNT
from database.models import Session
from database.models import User
from database.queries import get_user_by_username

BONUS_COOLDOWN = timedelta(days=1)


async def handle_bonuses(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_details: User = get_user_by_username(update.effective_user.username)

    if user_details.last_bonus_claim:
        time_since_last_claim = datetime.utcnow() - user_details.last_bonus_claim
        bonus_available = time_since_last_claim >= BONUS_COOLDOWN
        message_text = BonusMessages.get_bonus_available_message(
            BONUS_COOLDOWN - time_since_last_claim,
        )
    else:
        message_text = BonusMessages.get_bonus_available_message()
        bonus_available = True

    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=message_text,
        reply_markup=KeyboardTemplates.get_bonus_keyboard(bonus_available),
        parse_mode='Markdown',
    )


async def claim_bonus(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    with Session() as session:
        user_details: User = session.query(User).filter_by(
            telegram_user_id=query.from_user.id,
        ).first()

        if user_details.last_bonus_claim:
            time_since_last_claim = datetime.utcnow() - user_details.last_bonus_claim
            bonus_available = time_since_last_claim >= BONUS_COOLDOWN
        else:
            bonus_available = True

        if bonus_available:
            user_details.balance += TIME_BONUS_AMOUNT
            user_details.last_bonus_claim = datetime.utcnow()
            session.commit()

            await query.answer(BonusMessages.CLAIM_BONUS_MESSAGE)
            await query.edit_message_text(
                text=BonusMessages.get_successful_claimed_bonus_message(
                    user_details.balance,
                ),
                reply_markup=KeyboardTemplates.get_bonus_keyboard(),
                parse_mode='Markdown',
            )
        else:
            await query.answer(BonusMessages.CLAIM_BONUS_UNAVAILABLE_MESSAGE, show_alert=True)
