from sqlalchemy.orm import Session
from week3.schemas import book,user
from week3.db import models

def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def create_user(db: Session, user: user.UserCreate):
    db_user = models.User(name=user.name, phone=user.phone)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_books(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Book).offset(skip).limit(limit).all()

def create_book(db: Session, book: book.BookCreate):
    db_book = models.Book(**book.dict())
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book

def update_book(db: Session, book_id: int, book: book.BookUpdate):
    db_book = db.query(models.Book).filter(models.Book.id == book_id).first()
    if db_book:
        update_data = book.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_book, key, value)
        db.commit()
        db.refresh(db_book)
        return db_book
    return None

def delete_book(db: Session, book_id: int):
    db_book = db.query(models.Book).filter(models.Book.id == book_id).first()
    if db_book:
        db.delete(db_book)
        db.commit()
        return db_book
    return None

def borrow_book(db: Session, book_id: int, user_id: int):
    db_book = db.query(models.Book).filter(models.Book.id == book_id).first()
    if(db_book): 
        if(not db_book.user_id): # 책이 존재하고 현재 빌려지지 않은 상태여야 함
            db_book.user_id = user_id
            db.commit()
            return db_book
        else:
            return 0 # 책이 빌려진 상태임을 알림
    else:
        return None # 책이 존재하지 않음
    
def return_book(db: Session, book_id: int, user_id: int):
    db_book = db.query(models.Book).filter(models.Book.id == book_id).first()
    if(db_book): 
        if(db_book.user_id): # 책이 존재하고 현재 빌린 상태
            if(db_book.user_id == user_id): # 빌린 사람과 요청인이 같은 경우
                db_book.user_id = None
                db.commit()
                return db_book
            else:
                return -1 # 빌린 사람과 다른 상태임을 알림
        else:
            return 0 # 책이 빌려지지 않은 상태임을 알림
    else:
        return None # 책이 존재하지 않음
