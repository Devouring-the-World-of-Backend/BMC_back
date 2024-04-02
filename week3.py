import os
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker

#환경 변수에서 데이터베이스 연결 문자열 읽기
database_url = os.getenv('DATABASE_URL', 'sqlite:///week3.db')

#engine 생성
engine = create_engine(database_url, echo=True)

#declarative_base 인스턴스 생성
Base = declarative_base()

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

#session 구성
Session = sessionmaker(bind=engine)
session = Session()

#테이블 생성
Base.metadata.create_all(engine)