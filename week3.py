import os
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import declarative_base, sessionmaker, relationship

#환경 변수에서 데이터베이스 연결 문자열 읽기
database_url = os.getenv('DATABASE_URL', 'sqlite:///week3.db')

#engine 생성
engine = create_engine(database_url, echo=True)

#declarative_base 인스턴스 생성
Base = declarative_base()

#책과 카테고리 다대다 관계 설정을 위한 테이블 설정
book_category = Table('book_category', Base.metadata,
                      Column('book_id',Integer,ForeignKey('books.id'), primary_key=True),
                      Column('category_id',Integer,ForeignKey('categories.id'),primary_key=True))


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    phone = Column(String, unique=True, nullable=False)

class Book(Base):
    __tablename__ = 'books'
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    author = Column(String, nullable=False)

    #카테고리와 다대다 연결 설정
    categories = relationship("Category", secondary=book_category, back_populates="books")

    

class Category(Base):
    __tablename__ = 'categories'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)

    #책과 다대다 연결 설정
    books = relationship("Book", secondary=book_category, back_populates="categories")




#session 구성
Session = sessionmaker(bind=engine)
session = Session()

#테이블 생성
Base.metadata.create_all(engine)