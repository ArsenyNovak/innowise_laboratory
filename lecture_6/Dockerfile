# Используем многостадийную сборку
FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim AS base

# Устанавливаем переменные окружения
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app

# Создаем рабочую директорию
WORKDIR /app

# Копируем файлы зависимостей для кэширования слоев Docker
COPY pyproject.toml uv.lock ./

# Синхронизируем зависимости с кэшем
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-dev

# Копируем исходный код
COPY . .

# Документируем порт
EXPOSE 8000

# Запуск через uv run (стандарт для uv в Docker)
CMD ["uv", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
