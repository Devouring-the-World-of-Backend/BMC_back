from fastapi import FastAPI
from pydantic import BaseModel, Field
from datetime import datetime

class Book(BaseModel):
    id: int
    title: str
    author: str
    description: str
    published_year: int = Field(..., ge=1800, le=datetime.now().year)

fake_id = 1
fake_data = {
    "id": fake_id,
    "title": "new book",
    "author": "BMC",
    "description": "Book data for test",
    "published_year": 2021
}
fake_id += 1

fake_db = [Book(fake_data)]

app = FastAPI()

@app.get("/", summary="루트 경로로 Hello Library를 반환")
def root():
    return "Hello Library!"

@app.get("/books/", summary="모든 도서 목록을 반환")
def getBooks():
    return fake_db
