from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.orm import declarative_base
from datetime import datetime

Base = declarative_base()

class TranslationHistory(Base):
    __tablename__ = "requests_history"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    input_text = Column(Text, nullable=False)
    translated_text = Column(Text, nullable=False)
    model_name = Column(String(128), nullable=False)
    direction = Column(String(10), nullable=False)   # "en-ru" или "ru-en"
    created_at = Column(DateTime, default=datetime.utcnow)