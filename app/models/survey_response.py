from app.models import Base
from sqlalchemy import Column, String, Integer, Text


class SurveyResponses(Base):
    __tablename__ = 'survey_responses'

    id = Column(Integer, primary_key=True)
    survey_title = Column(String(100), nullable=False)
    question = Column(String(999), nullable=False)
    answer_options = Column(String(9999), nullable=False)
    user_response = Column(String(999), nullable=False)
    username = Column(Text(), nullable=False)
    user_age = Column(Integer, nullable=False)
