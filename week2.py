from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel, Field
from datetime import datetime
from typing import List, Optional
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

class BookCreate(BaseModel): #클라이언트에서 제공하는 모델 형식
    title: str
    author: str
    description: str
    published_year: int = Field(..., ge=1800, le=datetime.now().year) #년 데이터에 대한 데이터 검증 

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

fake_db = [Book(**fake_data)]

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 허용할 오리진들의 리스트, 호스팅 될 도메인만 리소스 접근 허용 (테스트를 위해 전부 허용)
    allow_methods=["*"],  # 허용할 HTTP 메서드들
    allow_headers=["*"],  # 허용할 HTTP 헤더들
)

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=422,  # Unprocessable Entity
        content={"message": "test", "details": exc.errors()},
    )

@app.get("/", summary="루트 경로로 Hello Library를 반환")
def root():
    return "Hello Library!"

@app.get("/books/", status_code=200, summary="모든 도서 목록을 반환")
def getBooks():
    return fake_db

@app.post("/books/", status_code=201, summary="새로운 도서 추가")
def postBooks(book: BookCreate):
    new_id = fake_id + 1
    new_book = Book(id=new_id, **book.dict())
    fake_db.append(new_book)

@app.get("/books/{id}/", summary="특정 도서 정보 반환")
def getBook(id:int):
    found = None
    for b in fake_db:
        if(b.id == id):
            found = b
    if found is None: # 해당 id의 도서가 없는 경우, 404 오류 반환
        raise HTTPException(status_code=404, detail="찾고자 하는 책이 없습니다.")
    return found

@app.put("/books/{id}/", status_code=204, summary="특정 도서 정보 업데이트")
def putBook(id:int, book_update:BookCreate): #id가 없는 것은 동일하므로 모델 재사용
    foundInd = None
    for i in range(len(fake_db)):
        if(fake_db[i].id == id):
            foundInd = i
    if foundInd is None: # 해당 id의 도서가 없는 경우, 404 오류 반환
        raise HTTPException(status_code=404, detail="찾고자 하는 책이 없습니다.")
    # 그렇지 않다면 해당 인덱스의 책을 업데이트
    fake_db[i] = Book(id=id, **book_update.dict())

@app.delete("/books/{id}/", status_code=204,summary="특정 도서 삭제")
def deleteBook(id:int):
    foundInd = None
    for i in range(len(fake_db)):
        if(fake_db[i].id == id):
            foundInd = i
    if foundInd is None: # 해당 id의 도서가 없는 경우, 404 오류 반환
        raise HTTPException(status_code=404, detail="찾고자 하는 책이 없습니다.")
    # 그렇지 않다면 해당 인덱스의 책을 삭제
    del fake_db[foundInd]
    return {"message": "정상적으로 삭제되었습니다."}

def searchBooksFunc(
    title: Optional[str] = None,
    author: Optional[str] = None,
    published_year: Optional[int] = None):
    res = fake_db #fake_db를 계속 순회하면서 조건에 맞지 않는 db는 제거
    if(title):
        tmpRes = []
        for item in res:
            if(title.lower() in item.title.lower()): # 입력한 title이 해당 필드의 제목의 일부인지
                tmpRes.append(item)
        res = tmpRes
    if(author):
        tmpRes = []
        for item in res:
            if(author.lower() in item.author.lower()): # 입력한 author이 해당 필드의 저자의 일부인지
                tmpRes.append(item)
        res = tmpRes
    if(published_year):
        tmpRes = []
        for item in res:
            if(published_year == item.published_year): # 입력한 published_year이 동일한지
                tmpRes.append(item)
        res = tmpRes
    return res
    
@app.get("/books/search", summary="조건에 맞는 도서 검색")
def searchBooks(
    title: Optional[str] = None,
    author: Optional[str] = None,
    published_year: Optional[int] = None 
): # 셋 다 None인 경우는 Client에서 처리
    return searchBooksFunc(title,author,published_year)
    

