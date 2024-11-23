from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# 데이터베이스 연결 URL 설정
DATABASE_URL = "mysql+pymysql://root:root@localhost:3306/taskdb"

# 데이터베이스 엔진 생성
engine = create_engine(DATABASE_URL)

# 세션 로컬 설정
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base 클래스 정의
Base = declarative_base()

# DB 세션을 생성하고 종료하는 함수
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
