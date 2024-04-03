from fastapi import APIRouter, HTTPException
from week3.schemas import user
from week3.db.database import Session
from week3.crud import crud

router = APIRouter()

# 새로운 사용자를 데이터베이스에 추가
@router.post("/users/", response_model=user.User)
def create_user(user: user.UserCreate):
    db = Session()
    db_user = crud.create_user(db=db, user=user)
    db.close()
    return db_user