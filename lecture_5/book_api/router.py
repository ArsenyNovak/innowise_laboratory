"""Роутер для API книг."""
from typing import List, Optional

from fastapi import APIRouter, HTTPException, Query

from book_api.dao import BookDAO
from book_api.forms import BookCreate, BookResponse, BookUpdate


router_pages = APIRouter(prefix="/books", tags=["books"])


@router_pages.get("/", response_model=List[BookResponse])
async def list_books(
    page: int = Query(1, ge=1, description="Номер страницы"),
    limit: int = Query(10, ge=1, le=100, description="Записей на странице"),
):
    """Возвращает список всех книг с пагинацией."""
    return await BookDAO.list_paginated(page, limit)


@router_pages.post("/", response_model=BookResponse)
async def create_book(book_data: BookCreate) -> BookResponse:
    """Создает новую книгу."""
    return await BookDAO.create(book_data)


@router_pages.delete("/{book_id}")
async def delete_book(book_id: int):
    """Удаляет книгу по ID."""
    deleted = await BookDAO.delete_by_id(book_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Книга не найдена")
    return {"message": f"Книга с id = {book_id} удалена"}


@router_pages.put("/{book_id}", response_model=BookResponse)
async def update_book(book_id: int, book_update: BookUpdate):
    """Обновляет книгу по ID."""
    update_data = book_update.model_dump_excludes()
    if not update_data:
        raise HTTPException(status_code=400, detail="Нет данных для обновления")

    return await BookDAO.update_by_id(book_id, update_data)


@router_pages.get("/search", response_model=List[BookResponse])
async def search_books(
    title: Optional[str] = Query(None, description="Часть названия книги"),
    author: Optional[str] = Query(None, description="Часть имени автора"),
    year: Optional[int] = Query(None, description="Год издания"),
):
    """Поиск книг по названию, автору, году."""
    books = await BookDAO.search(title, author, year)
    return books
