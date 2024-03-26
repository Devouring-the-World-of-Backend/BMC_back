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

@app.get("/books/{id}", summary="특정 도서 정보 반환")
def getBook(book_id:int):
    found = None
    for b in fake_db:
        if(b.id == book_id):
            found = b
    if found is None: # 해당 id의 도서가 없는 경우, 404 오류 반환
        raise HTTPException(status_code=404, detail="찾고자 하는 책이 없습니다.")
    return found

@app.put("/books/{id}", summary="특정 도서 정보 업데이트")
def putBook(book_id:int, book_update:BookCreate): #id가 없는 것은 동일하므로 모델 재사용
    foundInd = None
    for i in range(len(fake_db)):
        if(fake_db[i].id == book_id):
            foundInd = i
    if foundInd is None: # 해당 id의 도서가 없는 경우, 404 오류 반환
        raise HTTPException(status_code=404, detail="찾고자 하는 책이 없습니다.")
    # 그렇지 않다면 해당 인덱스의 책을 업데이트
    fake_db[i] = Book(id=book_id, **book_update.dict())


