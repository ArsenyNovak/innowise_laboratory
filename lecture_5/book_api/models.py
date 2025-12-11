"""Модель книги для работы с базой данных."""
from typing import Optional

from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from book_api.database import Base


class Book(Base):
    """Модель книги."""
    __tablename__ = 'books'

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True
    )
    title: Mapped[str] = mapped_column(String, nullable=False)
    author: Mapped[str] = mapped_column(String, nullable=False)
    year: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)



