from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError

from app.logger import logger
from app.config import settings
from app.db import init_db
from app.routes import analyze, history

app = FastAPI(title="AI Spam Detector", version="1.0.0")

app.include_router(analyze.router)
app.include_router(history.router)


@app.on_event("startup")
def on_startup():
    logger.info("Запуск сервиса AI Spam Detector")
    logger.info(f"Используемая модель: {settings.HF_MODEL}")
    try:
        init_db()
        logger.info("База данных инициализирована")
    except Exception as e:
        logger.error(f"Ошибка при инициализации базы данных: {e}")


@app.middleware("http")
async def log_requests(request: Request, call_next):
    logger.info(f"Входящий запрос: {request.method} {request.url.path}")
    response = await call_next(request)
    return response


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=400,
        content={"detail": "Некорректный JSON или отсутствуют обязательные поля"},
    )


@app.get("/health")
def health():
    return {"status": "ok"}
