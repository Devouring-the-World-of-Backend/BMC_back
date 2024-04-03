from fastapi import FastAPI
from sqlalchemy.ext.asyncio import AsyncSession
from week3.db.database import engine
from week3.db.models import Base
from week3.routers import book_router, user_router

app = FastAPI()

# 데이터베이스 테이블 생성 (비동기 방식)
async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

@app.on_event("startup")
async def startup_event():
    await create_tables()


# 라우터 등록
app.include_router(user_router.router)
app.include_router(book_router.router)
