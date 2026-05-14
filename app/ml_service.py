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

    label = str(prediction.get("label", "")).upper()
    score = float(prediction.get("score", 0.0))

    spam_labels = ("LABEL_1", "SPAM", "1", "TOXIC", "INAPPROPRIATE")
    ham_labels = ("LABEL_0", "HAM", "NOT_SPAM", "0", "NORMAL", "NEUTRAL")

    if label in spam_labels:
        result = "SPAM"
    elif label in ham_labels:
        result = "NOT_SPAM"
    else:
        result = label

    return result, score
