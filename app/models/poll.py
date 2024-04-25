from app.models import Base
from sqlalchemy import Column, String, Integer


class Poll(Base):
    __tablename__ = 'polls'

    id = Column(Integer, primary_key=True)
    author = Column(String(50), nullable=False)
    title = Column(String(100), nullable=False)
    description = Column(String(100), nullable=False)
    question = Column(String(999), nullable=False)
    answer_one = Column(String(100), nullable=False)
    answer_two = Column(String(100), nullable=False)
    answer_tree = Column(String(100), nullable=False, default=None)
    answer_four = Column(String(100), nullable=False, default=None)
    answer_five = Column(String(100), nullable=False, default=None)
