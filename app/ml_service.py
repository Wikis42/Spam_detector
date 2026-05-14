from transformers import pipeline

from app.config import settings
from app.logger import logger

_pipeline = None


def get_pipeline():
    global _pipeline
    if _pipeline is None:
        try:
            logger.info(f"Загрузка модели Hugging Face: {settings.HF_MODEL}")
            _pipeline = pipeline("text-classification", model=settings.HF_MODEL)
            logger.info("Модель успешно загружена")
        except Exception as e:
            logger.error(f"Ошибка загрузки модели: {e}")
            raise
    return _pipeline


def classify_text(text: str):
    clf = get_pipeline()
    try:
        prediction = clf(text)[0]
    except Exception as e:
        logger.error(f"Ошибка при работе модели: {e}")
        raise

    label = prediction.get("label", "").upper()
    score = float(prediction.get("score", 0.0))

    if label in ("LABEL_1", "SPAM", "1"):
        result = "SPAM"
    elif label in ("LABEL_0", "HAM", "NOT_SPAM", "0"):
        result = "NOT_SPAM"
    else:
        result = label

    return result, score
