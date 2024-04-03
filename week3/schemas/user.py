from pydantic import BaseModel
from typing import Optional

# 유저 생성을 위한 Pydantic 모델
class UserCreate(BaseModel):
    name: str
    phone: str

# 유저 정보 응답을 위한 Pydantic 모델
class User(BaseModel):
    id: int
    name: str
    phone: str

    class Config:
        orm_mode = True

# 선택적으로 유저 정보를 업데이트하기 위한 Pydantic 모델
class UserUpdate(BaseModel):
    name: Optional[str] = None
    phone: Optional[str] = None