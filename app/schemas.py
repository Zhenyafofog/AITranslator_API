from pydantic import BaseModel, Field, field_validator
from typing import Optional
from datetime import datetime

class TranslateRequest(BaseModel):
    text: str
    direction: str = Field(default="en-ru", pattern="^(en-ru|ru-en)$")

    @field_validator("text")
    @classmethod
    def text_must_not_be_empty(cls, v: str):
        if not v.strip():
            raise ValueError("Text must not be empty")
        return v.strip()

class TranslateResponse(BaseModel):
    translated_text: str
    model_used: str
    direction: str

class HistoryItem(BaseModel):
    id: int
    input_text: str
    translated_text: str
    model_name: str
    direction: str
    created_at: datetime

    class Config:
        from_attributes = True

class HistoryList(BaseModel):
    total: int
    page: int
    limit: int
    items: list[HistoryItem]