from fastapi import APIRouter, HTTPException, Depends
from week3.schemas import book
from week3.db.database import Session
from week3.crud import crud
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter()

# 비동기 SQLAlchemy 세션 의존성
async def get_db():
    async with Session() as session:
        yield session

# 새로운 책을 데이터베이스에 추가
@router.post("/books/", response_model=book.Book)
async def create_book(book: book.BookCreate):
    db = Session()
    db_book = await crud.create_book(db=db, book=book)
    db.close()
    return db_book

# 모든 책을 불러옴
@router.get("/books/", response_model=List[book.Book])
async def get_books():
    db = Session()
    db_books = await crud.get_books(db=db)
    db.close()
    return db_books

# 특정 도서 업데이트
@router.put("/books/{bid}", response_model=book.BookUpdate)
async def update_book(bid:int, book:book.BookUpdate):
    db = Session()
    db_book = await crud.update_book(db=db, book=book, book_id = bid)
    db.close()
    return db_book

# 특정 도서 삭제
@router.delete("/books/{bid}", response_model=book.Book)
async def delete_book(bid:int):
    db = Session()
    db_book = await crud.delete_book(db=db, book_id = bid)
    db.close()
    return db_book

# 특정 도서를 특정 유저가 빌림
@router.post("/books/borrow/{bid}", response_model=book.Book)
async def borrow_book(bid: int, uid: int, db: AsyncSession = Depends(get_db)):
    db_book = await crud.borrow_book(db=db,book_id=bid,user_id=uid)
    if(db_book == 0):
        raise HTTPException(status_code=404, detail="Already borrowed")
    elif(not db_book):
        raise HTTPException(status_code=404, detail="Book does not exist")
    else:
        return db_book

# 특정 도서를 특정 유저가 반납
@router.post("/books/return/{bid}", response_model=book.Book)
async def return_book(bid:int, uid:int, db: AsyncSession = Depends(get_db)):
    db_book = await crud.return_book(db=db,book_id=bid,user_id=uid)

    if(db_book == 0): # 책이 빌려지지 않은 경우
        raise HTTPException(status_code=404, detail="Was not borrowed")
    elif(db_book == -1): # 해당 유저가 빌린 책이 아닌 경우
        raise HTTPException(status_code=404, detail="uid fail")
    elif(not db_book):
        raise HTTPException(status_code=404, detail="Book does not exist")
    else:
        return db_book
        