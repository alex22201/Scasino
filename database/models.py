from datetime import datetime

from sqlalchemy import Column, DateTime, Integer, String, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from config import DATABASE_URL

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    telegram_user_id = Column(Integer, unique=True)
    username = Column(String, unique=True)
    balance = Column(Integer, default=100)
    last_check_in = Column(DateTime, default=datetime.utcnow)
    registration_date = Column(DateTime, default=datetime.utcnow)
    phone_number = Column(String, unique=True)
    age = Column(Integer)


engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)


Base.metadata.create_all(engine)
