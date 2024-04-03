from pydantic import BaseModel
from typing import Optional

# 도서 생성을 위한 Pydantic 모델
class BookCreate(BaseModel):
    title: str
    author: str

# 도서 정보 응답을 위한 Pydantic 모델
class Book(BaseModel):
    id: int
    title: str
    author: str

    class Config:
        orm_mode = True

# 선택적으로 도서 정보를 업데이트하기 위한 Pydantic 모델
class BookUpdate(BaseModel):
    title: Optional[str] = None
    author: Optional[str] = None