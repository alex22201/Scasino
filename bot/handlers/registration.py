import sqlite3
from typing import Any

from telegram import Update
from telegram.ext import ContextTypes
from telegram.ext import ConversationHandler

from bot.keyboards import KeyboardTemplates
from bot.messages import ErrorMessages
from bot.messages import RegistrationMessages
from bot.utils import validate_age
from database.models import User
from database.queries import create_user
from database.queries import get_user_by_username
from database.queries import update_user_age

AGE, CONTACT = range(2)


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> Any:
    user = update.effective_user
    try:
        existing_user = get_user_by_username(user.username)

        if existing_user:
            return await handle_existing_user(update, existing_user)

        return await handle_new_user(update, user)

    except (ValueError, sqlite3.DatabaseError):
        await update.message.reply_text(ErrorMessages.REGISTRATION_ERROR_MESSAGE)


async def handle_existing_user(update: Update, existing_user: User) -> Any:
    """Handles existing users' registration process."""
    if not existing_user.age:
        await update.message.reply_text(
            text=RegistrationMessages.get_registration_message(
                existing_user.username,
            ),
        )
        return AGE

    await update.message.reply_text(
        text=RegistrationMessages.get_welcome_message(
            existing_user.username, existing_user.balance,
        ),
        reply_markup=KeyboardTemplates.main_menu_keyboard(),
    )
    return ConversationHandler.END


async def handle_new_user(update: Update, user: User) -> Any:
    """Handles new user registration process."""
    try:
        new_user = create_user(user.username, user.id)
    except sqlite3.IntegrityError:
        return ConversationHandler.END

    await update.message.reply_text(
        RegistrationMessages.get_registration_message(new_user.username),
    )
    return AGE


async def handle_age_validation(update: Update, age: int) -> bool:
    if age < 18:
        await update.message.reply_text(RegistrationMessages.UNDERAGE_MESSAGE)
        return False
    return True


async def update_user_age_in_db(update: Update, user_id: int, age: int) -> bool:
    try:
        updated_user = update_user_age(user_id, age)
        if not updated_user:
            await update.message.reply_text(ErrorMessages.AGE_SAVE_ERROR)
            return False
        return True
    except (ValueError, sqlite3.DatabaseError):
        await update.message.reply_text(ErrorMessages.AGE_SAVE_ERROR)
        return False


async def ask_age(update: Update, context: ContextTypes.DEFAULT_TYPE) -> Any:
    age = update.message.text
    validated_age = validate_age(age)

    if validated_age is None:
        await update.message.reply_text(RegistrationMessages.PLEASE_ENTER_CORRECT_AGE)
        return AGE

    if not await handle_age_validation(update, validated_age):
        return AGE

    if not await update_user_age_in_db(update, update.effective_user.id, validated_age):
        return AGE

    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=RegistrationMessages.get_registration_completed_message(
            update.effective_user.username,
        ),
        reply_markup=KeyboardTemplates.main_menu_keyboard(),
    )
    return ConversationHandler.END
