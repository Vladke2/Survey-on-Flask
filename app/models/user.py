from datetime import datetime
from app.models import Base
from flask_login import UserMixin
from sqlalchemy import Column, String, Integer, Text, DateTime


class User(UserMixin, Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    # nickname = Column(Text, nullable=False, unique=True)
    username = Column(Text, nullable=False, unique=True)
    email = Column(String(50), nullable=False, unique=True)
    # phone = Column(String(30), nullable=False, unique=True)
    password = Column(String(250), nullable=False, unique=True)
    age = Column(String(4), nullable=False)
    about_me = Column(String(140))
    last_seen = Column(DateTime(), default=datetime.utcnow)
