# models.py 파일 작성
# LLM 실습 =>
# ERD 모델을 보고  1:다 관계설정에 대한 소스코드를 작성하시오.(화면캡처 참조)
# 1:다 관계 설정에 대한 소스코드를 통해서 ERD 관계에 대한 이미지를 생성하시오.(model.py첨부)
# 각 줄에 주석을 달아 주세요.

# =========================
# DB 테이블 모델 정의
# =========================
from sqlalchemy import Column, Integer, String, ForeignKey, Text, DateTime  
# Column → 테이블의 컬럼(필드)을 정의, ForeignKey → 다른 테이블과 연결(외래키)
from sqlalchemy.orm import relationship  # relationship → 테이블 간 관계(연관관계)를 ORM 레벨에서 정의
from sqlalchemy.sql import func  # func.now() → DB의 현재 시간 함수 사용 (created_at 자동 입력)
from database import Base  # 모든 모델이 상속받을 Base 클래스

# =========================
# 사용자 테이블
# =========================
class User(Base):                                        # Base를 상속받아 ORM 테이블로 등록됨
    __tablename__ = "users"                              # 실제 DB에 생성될 테이블 이름
    id = Column(Integer, primary_key=True, index=True)   # 기본키(PK),자동 증가,인덱스 설정(조회성능)
    # 이메일(로그인 ID 역할), unique=True 중복 불가, index=True 검색 속도 향상, nullable=False 값 필수
    email = Column(String(255), unique=True, index=True, nullable=False)  
    nickname = Column(String(100), unique=True, nullable=False) # 사용자 표시용 닉네임 (중복 불가)
    password = Column(String(255), nullable=False)       # 암호화된 비밀번호 저장 (평문 절대 금지)
    name = Column(String(100))                           # 사용자 실제 이름 (선택 입력 가능)
    address = Column(String(255))                        # 주소
    phone = Column(String(50))                           # 전화번호
    created_at = Column(DateTime(timezone=True), server_default=func.now()) # 등록시간(자동생성)
    posts = relationship(
        "Post",                                          # 연결할 모델 이름
        back_populates="author",                         # Post.author와 양방향 연결(=user_id)
        cascade="all, delete"                            # 유저 삭제 시 게시글도 같이 삭제
    )
    comments = relationship(
        "Comment",
        back_populates="author",
        cascade="all, delete"                            # 유저 삭제 시 댓글도 같이 삭제
    )

# =========================
# 게시글 테이블
# =========================
class Post(Base):
    __tablename__ = "posts"                              # 게시글 테이블 이름
    id = Column(Integer, primary_key=True, index=True)   # 게시글 고유 ID
    title = Column(String(255))                          # 게시글 제목
    content = Column(Text)                               # 게시글 내용 (긴 텍스트 저장 가능)
    user_id = Column(Integer, ForeignKey("users.id"))    # 작성자 ID (users 테이블의 id를 참조)
    created_at = Column(DateTime(timezone=True), server_default=func.now()) # 게시글 생성 시간
    author = relationship(                               # author → 이 게시글을 작성한 사용자 객체
        "User",
        back_populates="posts"                           # User.posts와 연결
    )
    comments = relationship(                             # comments → 이 게시글에 달린 댓글 목록
        "Comment",
        back_populates="post",
        cascade="all, delete"                            # 게시글 삭제 시 댓글도 같이 삭제
    )

# =========================
# 댓글 테이블
# =========================
class Comment(Base):
    __tablename__ = "comments"                           # 댓글 테이블 이름
    id = Column(Integer, primary_key=True, index=True)   # 댓글 고유 ID
    text = Column(Text)                                  # 댓글 내용
    user_id = Column(Integer, ForeignKey("users.id"))    # 댓글 작성자 (users.id 참조)
    post_id = Column(Integer, ForeignKey("posts.id"))    # 어떤 게시글에 달린 댓글인지 (posts.id 참조)
    created_at = Column(DateTime(timezone=True), server_default=func.now()) # 댓글 생성 시간
    author = relationship(                               # author → 댓글 작성자(User 객체)
        "User",
        back_populates="comments") 
    post = relationship(                                 # post → 이 댓글이 속한 게시글(Post 객체)
        "Post",
        back_populates="comments")   
