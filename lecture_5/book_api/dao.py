"""DAO для работы с моделью Book."""
from typing import Any, List, Optional

from fastapi import HTTPException
from sqlalchemy import select, func

from book_api.database import async_session_maker
from book_api.forms import BookCreate, BookResponse
from book_api.models import Book


class BookDAO:
    model = Book

    @classmethod
    async def list_paginated(
            cls,
            page: int = 1,
            limit: int = 10
    ) -> List[BookResponse]:
        """Возвращает пагинированный список книг."""
        offset = (page - 1) * limit

        async with async_session_maker() as session:
            # Основной запрос с пагинацией
            query = select(cls.model).offset(offset).limit(limit)
            result = await session.execute(query)
            books = result.scalars().all()

            # Подсчет общего количества (опционально)
            total_query = select(func.count(cls.model.id))
            total_result = await session.execute(total_query)
            total = total_result.scalar()

            paginated_books = [BookResponse.model_validate(book) for book in books]
            return paginated_books

    @classmethod
    async def create(cls, book_data: BookCreate) -> BookResponse:
        """
        Асинхронно создает книгу из Pydantic-модели.

        Args:
            book_data: Pydantic-объект с данными книги.

        Returns:
            Pydantic-объект BookResponse с созданной книгой.
        """
        async with async_session_maker() as session:
            async with session.begin():
                book = cls.model(
                    title=book_data.title,
                    author=book_data.author,
                    year=book_data.year,
                )
                session.add(book)
                await session.flush()
                await session.refresh(book)
                return BookResponse.model_validate(book)

    @classmethod
    async def delete_by_id(cls, book_id: int) -> bool:
        """
        Удаляет книгу по ID.

        Returns:
            True, если запись была удалена, иначе False.
        """
        async with async_session_maker() as session:
            async with session.begin():
                book = await session.get(cls.model, book_id)
                if not book:
                    return False

                await session.delete(book)
                return True

    @classmethod
    async def update_by_id(
        cls,
        book_id: int,
        update_data: dict[str, Any],
    ) -> BookResponse:
        """
        Асинхронно обновляет книгу по ID.

        Args:
            book_id: ID книги для обновления.
            update_data: Словарь с полями для обновления (title, author, year).

        Returns:
            Обновленный объект BookResponse.
        """
        async with async_session_maker() as session:
            async with session.begin():
                book = await session.get(cls.model, book_id)
                if not book:
                    raise HTTPException(status_code=404, detail="Книга не найдена")

                for field, value in update_data.items():
                    if hasattr(book, field):
                        setattr(book, field, value)

                await session.flush()
                await session.refresh(book)
                return BookResponse.model_validate(book)

    @classmethod
    async def search(
        cls,
        title: Optional[str] = None,
        author: Optional[str] = None,
        year: Optional[int] = None,
    ) -> List[BookResponse]:
        """
        Ищет книги по title, author, year (частичное совпадение).

        Args:
            title: Название книги (или часть).
            author: Автор (или часть).
            year: Год издания.

        Returns:
            Список найденных книг.
        """
        async with async_session_maker() as session:
            query = select(cls.model)

            if title:
                query = query.where(cls.model.title.ilike(f"%{title}%"))
            if author:
                query = query.where(cls.model.author.ilike(f"%{author}%"))
            if year is not None:
                query = query.where(cls.model.year == year)

            result = await session.execute(query)
            books = result.scalars().all()
            return [BookResponse.model_validate(book) for book in books]


