from fastapi import APIRouter, HTTPException, Depends
from week3.schemas import book
from week3.db.database import Session
from week3.crud import crud
from typing import List

router = APIRouter()

def get_db(): # 요청 동안 세션이 열려있도록
    db = Session()
    try:
        yield db
    finally:
        db.close()

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

# 특정 도서를 특정 유저가 빌림
@router.post("/books/borrow/{bid}", response_model=book.Book)
def borrow_book(bid:int, uid:int, db: Session = Depends(get_db)):
    db_book = crud.borrow_book(db=db,book_id=bid,user_id=uid)
    if(db_book == 0):
        raise HTTPException(status_code=404, detail="Already borrowed")
    elif(not db_book):
        raise HTTPException(status_code=404, detail="Book does not exist")
    else:
        return db_book

# 특정 도서를 특정 유저가 반납
@router.post("/books/return/{bid}", response_model=book.Book)
def return_book(bid:int, uid:int, db: Session = Depends(get_db)):
    db_book = crud.return_book(db=db,book_id=bid,user_id=uid)

    if(db_book == 0): # 책이 빌려지지 않은 경우
        raise HTTPException(status_code=404, detail="Was not borrowed")
    elif(db_book == -1): # 해당 유저가 빌린 책이 아닌 경우
        raise HTTPException(status_code=404, detail="uid fail")
    elif(not db_book):
        raise HTTPException(status_code=404, detail="Book does not exist")
    else:
        return db_book
        