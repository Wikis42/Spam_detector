from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from app.db import get_db
from app.config import settings
from app.logger import logger
from app.schemas import AnalyzeRequest, AnalyzeResponse
from app.models import RequestHistory
from app.ml_service import classify_text

router = APIRouter()


@router.post("/analyze", response_model=AnalyzeResponse)
def analyze(payload: AnalyzeRequest, db: Session = Depends(get_db)):
    text = payload.text.strip()
    if not text:
        raise HTTPException(status_code=400, detail="Поле text не может быть пустым")

    if len(text) > settings.MAX_TEXT_LENGTH:
        raise HTTPException(
            status_code=400,
            detail=f"Текст слишком длинный, максимум {settings.MAX_TEXT_LENGTH} символов",
        )

    try:
        result, score = classify_text(text)
    except Exception:
        raise HTTPException(status_code=500, detail="Ошибка обработки текста моделью")

    try:
        record = RequestHistory(
            input_text=text,
            result_text=result,
            score=score,
            model_name=settings.HF_MODEL,
        )
        db.add(record)
        db.commit()
        db.refresh(record)
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Ошибка записи в базу данных: {e}")
        raise HTTPException(status_code=500, detail="Ошибка базы данных")

    return AnalyzeResponse(result=result, score=round(score, 4))
