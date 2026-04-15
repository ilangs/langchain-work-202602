# 1.database.py - DB 설정, DB 세션 셜정

from sqlalchemy import create_engine                     # DB 연결 엔진 생성
from sqlalchemy.ext.declarative import declarative_base  # ORM 모델 기본 클래스
from sqlalchemy.orm import sessionmaker                  # DB 세션 생성

# MariaDB 연결 URL (아이디:비밀번호@호스트:포트/DB명)
DATABASE_URL = "mysql+pymysql://root:1234@localhost:3307/board_db"

# DB 엔진 생성함수
engine = create_engine(DATABASE_URL)

# DB 세션 생성기 (안전장치 설정: 자동 커밋 X (rollback 사용 가능), flush X)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)  

# declarative_base()를 통해 ORM 모델의 부모 클래스 생성
Base = declarative_base()  