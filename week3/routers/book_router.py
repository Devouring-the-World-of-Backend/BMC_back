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
    db_user = crud.create_book(db=db, book=book)
    db.close()
    return db_user

@router.get("/books/", response_model=List[book.Book])
def get_books():
    db = Session()
    db_users = crud.get_books(db=db)
    db.close()
    return db_users