"""Pydantic-модели для работы с книгами."""
from typing import Any, Optional

from pydantic import BaseModel, ConfigDict


class BookCreate(BaseModel):
    """Модель для создания книги."""
    title: str
    author: str
    year: Optional[int] = None


class BookResponse(BaseModel):
    """Модель ответа с данными книги."""
    id: int
    title: str
    author: str
    year: Optional[int] = None

    model_config = ConfigDict(from_attributes=True)


class BookUpdate(BaseModel):
    """Модель для частичного обновления книги."""
    title: Optional[str] = None
    author: Optional[str] = None
    year: Optional[int] = None

    model_config = ConfigDict(from_attributes=True)

    def model_dump_excludes(self) -> dict[str, Any]:
        """Возвращает только непустые поля."""
        return {k: v for k, v in self.model_dump().items() if v is not None}
