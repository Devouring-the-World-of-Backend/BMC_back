from fastapi import FastAPI
from pydantic import BaseModel, Field
from datetime import datetime

class BookCreate(BaseModel): #클라이언트에서 제공하는 모델 형식
    title: str
    author: str
    description: str
    published_year: int = Field(..., ge=1800, le=datetime.now().year)

class Book(BookCreate): #서버에서 처리하는 모델 형식
    id: int

fake_data = {
    "id": 1,
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
    new_id = len(fake_db) + 1
    new_book = Book(id=new_id, **book.dict())
    fake_db.append(new_book)


