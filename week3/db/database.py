import os
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

#환경 변수에서 데이터베이스 연결 문자열 읽기
database_url = os.getenv('DATABASE_URL', 'sqlite:///week3.db')

#engine 생성
engine = create_engine(database_url, echo=True)

#session 구성
Session = sessionmaker(bind=engine)

#declarative_base 인스턴스 생성
Base = declarative_base()