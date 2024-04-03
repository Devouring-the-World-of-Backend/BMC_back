from fastapi import APIRouter, HTTPException
from week3.schemas import book
from week3.db.database import Session
from week3.crud import crud
from typing import List

router = APIRouter()

# 새로운 책을 데이터베이스에 추가
@router.post("/books/", response_model=book.Book)
def create_book(book: book.BookCreate):
    db = Session()
    db_book = crud.create_book(db=db, book=book)
    db.close()
    return db_book

# 모든 책을 불러옴
@router.get("/books/", response_model=List[book.Book])
def get_books():
    db = Session()
    db_books = crud.get_books(db=db)
    db.close()
    return db_books

# 특정 도서 업데이트
@router.put("/books/{bid}", response_model=book.BookUpdate)
def update_book(bid:int, book:book.BookUpdate):
    db = Session()
    db_book = crud.update_book(db=db, book=book, book_id = bid)
    db.close()
    return db_book

# 특정 도서 삭제
@router.delete("/books/{bid}", response_model=book.Book)
def delete_book(bid:int):
    db = Session()
    db_book = crud.delete_book(db=db, book_id = bid)
    db.close()
    return db_book