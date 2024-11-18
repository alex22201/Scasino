import logging

from database.models import Session, User

logger = logging.getLogger(__name__)


def get_user_by_username(username: str) -> User:
    with Session() as session:
        try:
            user = session.query(User).filter_by(username=username).first()
        except Exception as e:
            logger.error(e)
    return user


def create_user(username: str, telegram_id: int) -> User:
    with Session() as session:
        new_user = User(username=username, telegram_user_id=telegram_id)
        session.add(new_user)
        session.commit()
        session.refresh(new_user)

    return new_user


def update_user_age(telegram_id: int, age: int) -> User | None:
    with Session() as session:
        user = session.query(User).filter_by(
            telegram_user_id=telegram_id).first()
        if user:
            user.age = age
            session.commit()
            session.refresh(user)
            return user
        return None


def update_user_phone_number(telegram_id: int, phone_number: str) -> User | None:
    with Session() as session:
        user = session.query(User).filter_by(
            telegram_user_id=telegram_id).first()
        if user:
            user.phone_number = phone_number
            session.commit()
            session.refresh(user)
            return user
        return None
