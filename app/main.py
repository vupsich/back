from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware  # Импорт CORS
from . import models
from .database import engine
from .routes import router

# Создание таблиц базы данных
models.Base.metadata.create_all(bind=engine)

# Инициализация приложения
app = FastAPI()

# Настройка CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Замените на URL фронтенда, если он отличается
    allow_credentials=True,
    allow_methods=["*"],  # Разрешить все методы (GET, POST, PUT, DELETE и т.д.)
    allow_headers=["*"],  # Разрешить все заголовки
)

# Подключение маршрутов
app.include_router(router)
