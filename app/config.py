import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    DATABASE_URL = os.getenv(
        "DATABASE_URL",
        "postgresql+psycopg2://spam_user:spam_pass@postgres:5432/spam_db",
    )
    HF_MODEL = os.getenv("HF_MODEL", "mrm8488/bert-tiny-finetuned-sms-spam-detection")
    MAX_TEXT_LENGTH = int(os.getenv("MAX_TEXT_LENGTH", "500"))
    APP_HOST = os.getenv("APP_HOST", "0.0.0.0")
    APP_PORT = int(os.getenv("APP_PORT", "8000"))


settings = Settings()
