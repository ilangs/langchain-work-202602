# 5.main.py 작성

from fastapi import FastAPI, Depends, Query  # FastAPI 기본 모듈
from sqlalchemy.orm import Session           # DB 세션
import models, schemas, crud                 # 내부 모듈 import
from database import SessionLocal, engine    # DB 설정
from fastapi.middleware.cors import CORSMiddleware  # DB에 테이블 생성

models.Base.metadata.create_all(bind=engine) # 테이블 없으면 자동 생성

app = FastAPI()   # FastAPI 앱 생성

# React와 연결
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],     # 모든 도메인 허용 (개발용), 실제 운영에서는 제한있음
    allow_credentials=True,  # 쿠키 포함 요청 허용 (보안때문데 (토큰))
    allow_methods=["*"],     # 모든 HTTP 메서드 허용
    allow_headers=["*"],     # 모든 헤더 허용
)

# DB 세션 의존성 함수
def get_db():
    db = SessionLocal()  # 세션 생성
    try:
        yield db         # 세션 반환
    finally:
        db.close()       # 종료 시 닫기

# 게시글 목록 조회 API(검색 기능 통합)
@app.get("/posts", response_model=list[schemas.PostResponse])
def read_posts(q: str = Query(None), db: Session = Depends(get_db)):  
    if q:
        return crud.search_posts(db, keyword=q) # 검색어가 있으면 검색 실행
    return crud.get_posts(db)                   # DB 조회 결과 반환

# 게시글 생성 API
@app.post("/posts", response_model=schemas.PostResponse)
def create(post: schemas.PostCreate, db: Session = Depends(get_db)):
    return crud.create_post(db, post.title, post.content)  

# 게시글 삭제 API
@app.delete("/posts/{post_id}")
def delete(post_id: int, db: Session = Depends(get_db)):
    return crud.delete_post(db, post_id)

# 게시글 수정 API
@app.put("/posts/{post_id}", response_model=schemas.PostResponse)
def update(post_id: int, post: schemas.PostCreate, db: Session = Depends(get_db)):
    return crud.update_post(db, post_id, post.title, post.content)