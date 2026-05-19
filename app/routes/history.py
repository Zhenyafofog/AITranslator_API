from fastapi import APIRouter, HTTPException, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from ..db import get_db
from ..models import TranslationHistory
from ..schemas import HistoryItem, HistoryList

router = APIRouter(prefix="/history", tags=["history"])

@router.get("/", response_model=HistoryList)
async def get_history(
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db)
):
    # Сколько всего записей
    total_q = select(func.count(TranslationHistory.id))
    total_res = await db.execute(total_q)
    total = total_res.scalar() or 0

    offset = (page - 1) * limit
    query = select(TranslationHistory).order_by(TranslationHistory.created_at.desc()).offset(offset).limit(limit)
    result = await db.execute(query)
    rows = result.scalars().all()

    items = [HistoryItem.model_validate(r) for r in rows]
    return HistoryList(total=total, page=page, limit=limit, items=items)

@router.get("/{item_id}", response_model=HistoryItem)
async def get_history_item(item_id: int, db: AsyncSession = Depends(get_db)):
    query = select(TranslationHistory).where(TranslationHistory.id == item_id)
    result = await db.execute(query)
    row = result.scalar_one_or_none()
    if not row:
        raise HTTPException(status_code=404, detail="Record not found")
    return HistoryItem.model_validate(row)