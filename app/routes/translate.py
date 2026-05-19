from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
import logging

from ..schemas import TranslateRequest, TranslateResponse
from ..ml_service import translate
from ..models import TranslationHistory
from ..db import get_db

router = APIRouter(prefix="/translate", tags=["translate"])
logger = logging.getLogger(__name__)

@router.post("/", response_model=TranslateResponse)
async def translate_text(req: TranslateRequest, db: AsyncSession = Depends(get_db)):
    # Проверка длины текста (макс. 500 символов)
    import os
    max_length = int(os.getenv("MAX_TEXT_LENGTH", 500))
    if len(req.text) > max_length:
        raise HTTPException(status_code=400, detail=f"Text too long, max {max_length} characters")

    try:
        translated, model_name = translate(req.text, req.direction)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Model error: {e}")
        raise HTTPException(status_code=500, detail="Translation model error")

    # Сохраняем в БД
    history = TranslationHistory(
        input_text=req.text,
        translated_text=translated,
        model_name=model_name,
        direction=req.direction
    )
    try:
        db.add(history)
        await db.commit()
        await db.refresh(history)
    except Exception as e:
        logger.error(f"DB error: {e}")
        await db.rollback()
        raise HTTPException(status_code=500, detail="Database error")

    return TranslateResponse(
        translated_text=translated,
        model_used=model_name,
        direction=req.direction
    )