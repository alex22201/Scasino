from datetime import datetime
from datetime import timedelta
from typing import Any

from sqlalchemy import Column
from sqlalchemy import create_engine
from sqlalchemy import DateTime
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker

from config import DATABASE_URL

Base = declarative_base()


class User(Base):  # type: ignore
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    telegram_user_id = Column(Integer, unique=True)
    username = Column(String, unique=True)
    balance = Column(Integer, default=100)
    registration_date = Column(DateTime, default=datetime.utcnow)
    phone_number = Column(String, unique=True)
    age = Column(Integer)
    last_bonus_claim = Column(DateTime, nullable=True)

    def can_claim_bonus(self) -> Any:
        BONUS_COOLDOWN = timedelta(days=1)
        if self.last_bonus_claim:
            return datetime.utcnow() - self.last_bonus_claim >= BONUS_COOLDOWN
        return True

    def claim_bonus(self, bonus_amount: int = 100) -> bool:
        if self.can_claim_bonus():
            self.balance += bonus_amount
            self.last_bonus_claim = datetime.utcnow()
            return True
        return False


engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)

Base.metadata.create_all(engine)
