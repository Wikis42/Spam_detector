from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from app.db import get_db
from app.logger import logger
from app.models import RequestHistory
from app.schemas import HistoryItem

router = APIRouter()


@router.get("/history", response_model=list[HistoryItem])
def get_history(
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
):
    try:
        offset = (page - 1) * limit
        rows = (
            db.query(RequestHistory)
            .order_by(RequestHistory.created_at.desc())
            .offset(offset)
            .limit(limit)
            .all()
        )
        return rows
    except SQLAlchemyError as e:
        logger.error(f"Ошибка чтения истории из БД: {e}")
        raise HTTPException(status_code=500, detail="Ошибка базы данных")


@router.get("/history/{item_id}", response_model=HistoryItem)
def get_history_item(item_id: int, db: Session = Depends(get_db)):
    try:
        row = db.query(RequestHistory).filter(RequestHistory.id == item_id).first()
    except SQLAlchemyError as e:
        logger.error(f"Ошибка чтения записи из БД: {e}")
        raise HTTPException(status_code=500, detail="Ошибка базы данных")

    if row is None:
        raise HTTPException(status_code=404, detail="Запись не найдена")
    return row
