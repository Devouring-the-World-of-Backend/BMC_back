from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from week3.db import models
from week3.schemas import book, user

async def get_user(db: AsyncSession, user_id: int):
    async with db as session:
        result = await session.execute(select(models.User).filter(models.User.id == user_id))
        return result.scalars().first()

async def create_user(db: AsyncSession, user: user.UserCreate):
    db_user = models.User(name=user.name, phone=user.phone)
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user

async def get_books(db: AsyncSession, skip: int = 0, limit: int = 100):
    async with db as session:
        result = await session.execute(select(models.Book).offset(skip).limit(limit))
        return result.scalars().all()

async def create_book(db: AsyncSession, book: book.BookCreate):
    db_book = models.Book(**book.dict())
    db.add(db_book)
    await db.commit()
    await db.refresh(db_book)
    return db_book

async def update_book(db: AsyncSession, book_id: int, book: book.BookUpdate):
    async with db as session:
        result = await session.execute(select(models.Book).filter(models.Book.id == book_id))
        db_book = result.scalars().first()
        if db_book:
            update_data = book.dict(exclude_unset=True)
            for key, value in update_data.items():
                setattr(db_book, key, value)
            await db.commit()
            await db.refresh(db_book)
            return db_book
    return None

async def delete_book(db: AsyncSession, book_id: int):
    async with db as session:
        result = await session.execute(select(models.Book).filter(models.Book.id == book_id))
        db_book = result.scalars().first()
        if db_book:
            await session.delete(db_book)
            await session.commit()
            return db_book
    return None

async def borrow_book(db: AsyncSession, book_id: int, user_id: int):
    result = await db.execute(
        select(models.Book).options(selectinload(models.Book.user)).filter(models.Book.id == book_id)
    )
    db_book = result.scalars().first()
    if db_book:
        if not db_book.user_id:  # 책이 대여되지 않았다면
            db_book.user_id = user_id
            await db.commit()  # 세션을 사용하여 변경 사항을 커밋
            return db_book
        else:  # 책이 이미 대여된 상태
            return 0
    else:
        return None  # 책이 데이터베이스에 존재하지 않음

async def return_book(db: AsyncSession, book_id: int, user_id: int):
    result = await db.execute(
        select(models.Book).options(selectinload(models.Book.user)).filter(models.Book.id == book_id)
    )
    db_book = result.scalars().first()
    if db_book:
        if db_book.user_id and db_book.user_id == user_id:
            db_book.user_id = None
            await db.commit()
            return db_book
        else:
            return 0
    return None
