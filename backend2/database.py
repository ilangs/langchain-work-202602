# =========================
# DB 연결 설정
# =========================
from sqlalchemy import create_engine     
# 엔진은 DB와 실제 통신을 담당하는 핵심 객체
from sqlalchemy.ext.declarative import declarative_base
# ORM 모델 클래스들이 상속받을 Base 클래스 생성 함수,테이블 정의의 기준(부모 클래스 역할)
from sqlalchemy.orm import sessionmaker
# DB 작업(조회, 저장 등)을 수행할 세션(Session)을 생성하는 도구

# =========================
# MariaDB 연결 URL
# =========================
SQLALCHEMY_DATABASE_URL = "mysql+pymysql://root:1234@localhost:3307/board_db2"
# DB 접속 정보 문자열 (URL 형식)
# 형식: mysql+pymysql://아이디:비밀번호@호스트:포트/DB이름,board_db2 → 사용할 데이터베이스 이름

# =========================
# 엔진 생성                   create_engine() → DB와 실제 연결을 담당하는 엔진 객체 생성
# =========================
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,  # 위에서 정의한 DB 접속 URL의 연결이 살아있는지 확인 (끊어진 연결 방지)
    pool_pre_ping=True        # pool_pre_ping=True → 커넥션 풀에서 가져온 연결이 유효한지 검사 (실무 매우 중요)
)                             

# =========================
# 세션 생성
# =========================
SessionLocal = sessionmaker(
    autocommit=False,  # 자동 커밋 비활성화 → 명시적으로 commit() 해야 DB 반영됨
    autoflush=False,   # 자동 flush 비활성화 → 쿼리 실행 전에 자동 반영 방지
    bind=engine        # 위에서 만든 엔진(DB 연결)과 연결
)
# sessionmaker → DB 작업용 세션을 생성하는 "팩토리 함수"
# SessionLocal() 호출 시 실제 세션 객체 생성됨

# =========================
# Base 클래스
# =========================
Base = declarative_base()
# ORM 모델들이 상속받는 기본 클래스 생성
# 이 Base를 상속받아야 SQLAlchemy가 테이블로 인식함
# 예: class User(Base): → 자동으로 users 테이블 생성 대상이 됨