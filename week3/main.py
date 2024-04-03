from fastapi import FastAPI
from week3.db.database import engine
from week3.db.models import Base
from week3.routers import book_router, user_router

Base.metadata.create_all(bind=engine)  # 데이터베이스 테이블 생성

app = FastAPI()

# 라우터 등록
app.include_router(user_router.router)
app.include_router(book_router.router)
