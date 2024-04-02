import os
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

#환경 변수에서 데이터베이스 연결 문자열 읽기
database_url = os.getenv('DATABASE_URL', 'sqlite:///week3.db')

#engine 생성
engine = create_engine(database_url, echo=True)

Base = declarative_base()

#session 구성
Session = sessionmaker(bind=engine)
session = Session()