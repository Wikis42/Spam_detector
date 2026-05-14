# AI Spam Detector

Итоговая практическая работа по дисциплине «Разработка веб-приложений».
Вариант №3 — классификация текста как SPAM / NOT_SPAM.

Backend-приложение (REST API) на FastAPI принимает текст, классифицирует его с помощью модели Hugging Face, сохраняет историю запросов в PostgreSQL и отдаёт её через API.

## Стек технологий

- Python 3.11 + FastAPI
- PostgreSQL 16
- SQLAlchemy
- Hugging Face Transformers
- Docker / Docker Compose

## Структура проекта

```
Spam_detector/
├── app/
│   ├── main.py
│   ├── db.py
│   ├── models.py
│   ├── schemas.py
│   ├── ml_service.py
│   ├── config.py
│   ├── logger.py
│   └── routes/
│       ├── analyze.py
│       └── history.py
├── postman/
│   └── collection.json
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── .env.example
└── README.md
```

## Запуск проекта

1. Клонировать репозиторий:

```bash
git clone https://github.com/Wikis42/Spam_detector.git
cd Spam_detector
```

2. Скопировать файл переменных окружения:

```bash
cp .env.example .env
```

3. Запустить проект через Docker Compose:

```bash
docker compose up --build
```

После старта API будет доступно по адресу: `http://localhost:8000`

Документация Swagger: `http://localhost:8000/docs`

## Переменные окружения

| Переменная        | Описание                              | По умолчанию |
|-------------------|---------------------------------------|--------------|
| DATABASE_URL      | Строка подключения к PostgreSQL       | см. .env.example |
| HF_MODEL          | Название модели Hugging Face          | RUSpam/spamNS_v1 |
| MAX_TEXT_LENGTH   | Максимальная длина текста (символов)  | 500 |
| POSTGRES_USER     | Пользователь PostgreSQL               | spam_user |
| POSTGRES_PASSWORD | Пароль PostgreSQL                     | spam_pass |
| POSTGRES_DB       | Имя БД                                | spam_db |

## API endpoints

### GET /health

Проверка доступности сервиса.

```bash
curl http://localhost:8000/health
```

Ответ:
```json
{"status": "ok"}
```

### POST /analyze

Классификация текста.

```bash
curl -X POST http://localhost:8000/analyze \
  -H "Content-Type: application/json" \
  -d '{"text": "Поздравляем! Вы выиграли айфон, переходите по ссылке прямо сейчас!"}'
```

Ответ:
```json
{"result": "SPAM", "score": 0.98}
```

### GET /history

Последние 20 запросов (можно настроить через пагинацию).

```bash
curl "http://localhost:8000/history?page=1&limit=20"
```

### GET /history/{id}

Получение одного запроса по идентификатору.

```bash
curl http://localhost:8000/history/1
```

## Структура БД

Таблица `requests_history`:

| Поле         | Тип            | Описание                       |
|--------------|----------------|--------------------------------|
| id           | SERIAL PK      | Идентификатор записи           |
| input_text   | TEXT           | Исходный текст запроса         |
| result_text  | VARCHAR(50)    | Результат классификации        |
| score        | FLOAT          | Уверенность модели             |
| model_name   | VARCHAR(255)   | Название модели Hugging Face   |
| created_at   | TIMESTAMP      | Дата и время создания записи   |

## Hugging Face модель

По умолчанию используется небольшая русскоязычная модель `RUSpam/spamNS_v1` (~29M параметров, основана на rubert-tiny2). Подходит для CPU и работает без видеокарты. Заменить можно через переменную окружения `HF_MODEL`.

## Тестирование через Postman

В папке `postman/` находится готовая коллекция запросов `collection.json`. Импортировать её можно через Postman → Import.

## Обработка ошибок

- 400 — пустой текст / некорректный JSON / превышение длины
- 404 — не найдена запись истории по id
- 500 — ошибка модели или базы данных

## Логирование

В консоль выводятся:

- запуск сервиса и загрузка модели
- входящие запросы пользователей
- ошибки модели
- ошибки подключения и работы с БД
