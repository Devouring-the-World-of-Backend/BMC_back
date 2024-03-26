from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from datetime import datetime

class BookCreate(BaseModel): #클라이언트에서 제공하는 모델 형식
    title: str
    author: str
    description: str
    published_year: int = Field(..., ge=1800, le=datetime.now().year)

class Book(BookCreate): #서버에서 처리하는 모델 형식
    id: int

fake_id = 1
fake_data = {
    "id": fake_id,
    "title": "new book",
    "author": "BMC",
    "description": "Book data for test",
    "published_year": 2021
}

fake_db = [Book(fake_data)]

app = FastAPI()

@app.get("/", summary="루트 경로로 Hello Library를 반환")
def root():
    return "Hello Library!"

@app.get("/books/", summary="모든 도서 목록을 반환")
def getBooks():
    return fake_db

@app.post("/books/", summary="새로운 도서 추가")
def postBooks(book: BookCreate):
    new_id = fake_id + 1
    new_book = Book(id=new_id, **book.dict())
    fake_db.append(new_book)

@app.post("/books/{id}", summary="특정 도서 정보 반환")
def getBook(book_id:int):
    b = next((b for book in fake_db if b["id"] == book_id), None)
    if b is None: # 해당 id의 도서가 없는 경우, 404 오류 반환
        raise HTTPException(status_code=404, detail="찾고자 하는 책이 없습니다.")
    return b