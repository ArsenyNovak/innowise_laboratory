"""Точка входа FastAPI-приложения и настройка жизненного цикла."""
from contextlib import asynccontextmanager

from fastapi import FastAPI

from book_api.database import init_db
from book_api.router import router_pages


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Жизненный цикл приложения: инициализация БД при старте."""
    await init_db()
    yield


app = FastAPI(lifespan=lifespan)

app.include_router(router_pages)



