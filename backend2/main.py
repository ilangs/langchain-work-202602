# main.py

# =========================
# FastAPI 및 필수 모듈 import
# =========================
from fastapi import FastAPI, Depends, HTTPException, Query, Header, Response, Cookie
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from jose import jwt
import os

from database import SessionLocal, engine
import models, schemas, crud
from auth import (
    create_access_token,
    create_refresh_token,   # Refresh Token 생성
    verify_password,        # 비밀번호 검증
    get_user_id_from_token, # 토큰에서 user_id 추출
    decode_token            # 토큰 디코딩/검증
)
from models import User

# =========================
# DB 테이블 자동 생성
# =========================
models.Base.metadata.create_all(bind=engine)
# models.py에 정의된 모든 테이블을 DB에 자동으로 생성 (없을 경우에만)

# =========================
# FastAPI 앱 생성
# =========================
app = FastAPI()

# =========================
# CORS 설정
# =========================
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # React 개발 서버 주소
    allow_credentials=True,                   # 쿠키 포함 요청 허용 (refresh_token 쿠키 전송에 필요)
    allow_methods=["*"],                      # GET, POST, PUT, DELETE 등 모든 HTTP 메서드 허용
    allow_headers=["*"],                      # Authorization 헤더 등 모든 헤더 허용
    expose_headers=["*"],                     # 응답 헤더 노츨
)

# =========================
# DB 세션 의존성 주입
# =========================
def get_db():
    """
    FastAPI 요청마다 독립적인 DB 세션 생성 후 사용
    - yield 방식으로 요청 완료 후 자동으로 세션 close
    """
    db = SessionLocal()
    try:
        yield db  # 요청 처리 동안 세션 제공
    finally:
        db.close()  # 요청 종료 후 세션 반환 (커넥션 풀로 반납)

# =========================
# 현재 사용자 추출 (JWT 인증 의존성) <-- ★리액트에서 코딩(heder값을 붙여서 전송)
# 게시판,댓글 공통 메서드
# =========================
def get_current_user(authorization: str = Header(None)) -> int:
    """
    Authorization 헤더에서 Bearer 토큰을 추출하여 user_id 반환
    - 헤더 형식: 'Authorization: Bearer <access_token>'
    - 토큰이 없거나 유효하지 않으면 401 에러 발생
    - 인증이 필요한 모든 엔드포인트에서 Depends(get_current_user)로 사용
    """
    if not authorization:
        raise HTTPException(status_code=401, detail="인증 토큰이 없습니다.")

    # "Bearer <token>" 형식에서 토큰 부분만 추출
    parts = authorization.split(" ")
    if len(parts) != 2 or parts[0].lower() != "bearer":
        raise HTTPException(status_code=401, detail="토큰 형식이 올바르지 않습니다. (Bearer <token>)")

    token = parts[1]
    return get_user_id_from_token(token)  # 디코딩 후 user_id 반환

# =========================
# Refresh Token 검증
# =========================
def verify_refresh_token(token: str) -> int:
    """
    Refresh Token 유효성 검증 후 user_id 반환
    - 타입이 'refresh'인지 추가 확인 (access token으로 refresh 요청 방지)
    """
    payload = decode_token(token)  # 서명/만료 검증

    # 토큰 타입 확인 (access token을 refresh endpoint에 사용하는 것 방지)
    if payload.get("type") != "refresh":
        raise HTTPException(status_code=401, detail="Refresh Token이 아닙니다.")

    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(status_code=401, detail="토큰에서 사용자 정보를 찾을 수 없습니다.")

    return int(user_id)

# =========================
# REGISTER (회원가입)
# =========================
@app.post("/register", response_model=schemas.UserResponse)
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    """
    신규 사용자 등록
    - 이메일/닉네임 중복 시 400 에러 반환
    - 비밀번호는 crud.create_user → auth.hash_password에서 자동 암호화
    """
    # 이메일 중복 확인
    existing_email = crud.get_user_by_email(db, user.email)
    if existing_email:
        raise HTTPException(status_code=400, detail="이미 사용 중인 이메일입니다.")

    # 닉네임 중복 확인
    existing_nickname = db.query(User).filter(User.nickname == user.nickname).first()
    if existing_nickname:
        raise HTTPException(status_code=400, detail="이미 사용 중인 닉네임입니다.")

    return crud.create_user(db, user)

# =========================
# LOGIN (로그인)
# =========================
@app.post("/login")
def login(user: schemas.UserLogin, response: Response, db: Session = Depends(get_db)):
    """
    로그인 처리
    1. 이메일로 사용자 조회
    2. 비밀번호 bcrypt 검증
    3. Access Token → JSON body 반환
    4. Refresh Token → HttpOnly 쿠키로 설정 (XSS 방어)
    """
    # 이메일로 사용자 조회
    db_user = crud.get_user_by_email(db, user.email)
    if not db_user:
        raise HTTPException(status_code=401, detail="이메일 또는 비밀번호가 일치하지 않습니다.")

    # 비밀번호 검증 (입력값 vs DB 해시값)
    if not verify_password(user.password, db_user.password):
        raise HTTPException(status_code=401, detail="이메일 또는 비밀번호가 일치하지 않습니다.")

    # 토큰 생성
    access_token = create_access_token(db_user.id)    # sessionStorage에 저장
    refresh_token = create_refresh_token(db_user.id)  # 브라우저에 저장

    # Refresh Token을 HttpOnly 쿠키로 설정 (JS에서 접근 불가 → XSS 방어)
    response.set_cookie(
        key="refresh_token",   # 쿠키 이름
        value=refresh_token,   # 쿠키 값
        httponly=True,         # JavaScript에서 document.cookie로 접근 불가(XSS 방어)
        samesite="lax",        # CSRF 방지: 동일 사이트 요청에만 쿠키 전송(외부유출 방지)
        max_age=60*60*24*7,    # 보관기간 7일간 유효 
        # secure=True          # HTTPS 환경에서만 전송 (운영 배포시 활성화 필수)
    )

    return {                               # 리액트가 받아서 저장
        "access_token": access_token,
        "token_type": "bearer",
        "user": {
            "id": db_user.id,
            "email": db_user.email,
            "nickname": db_user.nickname
        }
    }

# =========================
# Refresh Token 생성 (Access Token 재발급)
# =========================
@app.post("/refresh")
def refresh(refresh_token: str = Cookie(None), db: Session = Depends(get_db)):
    """
    쿠키의 Refresh Token을 검증하여 새 Access Token 발급
    - Refresh Token 만료 시 401 반환 → 클라이언트는 재로그인 유도
    """
    if not refresh_token:
        raise HTTPException(status_code=401, detail="Refresh Token이 없습니다.")

    user_id = verify_refresh_token(refresh_token)  # 검증 + user_id 추출

    # 사용자 정보 조회
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=401, detail="사용자를 찾을 수 없습니다.")

    return {
        "access_token": create_access_token(user_id),  # 새 Access Token 발급
        "user": {
            "id": user.id,
            "email": user.email,
            "nickname": user.nickname
        }
    }

# =========================
# LOGOUT (로그아웃)
# =========================
@app.post("/logout")
def logout(response: Response):
    """
    로그아웃: 쿠키의 Refresh Token 삭제
    - Access Token은 만료까지 유효하므로 클라이언트에서 메모리/스토리지에서 삭제 필요
    - 완전한 보안이 필요하다면 Refresh Token을 DB에서 관리하는 Token Blacklist 패턴 사용 권장
    """
    response.delete_cookie(
        key="refresh_token", 
        httponly=True,
        samesite="lax"
    )
    return {"message": "로그아웃 되었습니다."}

# =========================
# POSTS 목록 (페이징 + 검색)
# =========================
@app.get("/posts")
def get_posts(
    keyword: str = Query("", description="검색어"),
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1),
    db: Session = Depends(get_db)
):
    """
    게시글 목록 조회 (인증 불필요 - 비로그인 사용자도 열람 가능)
    - keyword: 제목/내용 검색
    - page/size: 페이지네이션 (page=1부터 시작)
    """
    skip = (page - 1) * size  # offset 계산
    return crud.get_posts(db, keyword=keyword, skip=skip, limit=size)

# =========================
# 게시글 상세 조회
# =========================
@app.get("/posts/{post_id}")
def get_post(post_id: int, db: Session = Depends(get_db)):
    """
    단건 게시글 상세 조회 (인증 불필요)
    - author relationship을 통해 작성자 닉네임 함께 반환
    """
    post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="게시글을 찾을 수 없습니다.")

    return {
        "id": post.id,
        "title": post.title,
        "content": post.content,
        "user_id": post.user_id,
        "nickname": post.author.nickname if post.author else None
    }

# =========================
# POST CREATE (게시글 작성)
# =========================
@app.post("/posts")
def create_post(
    post: schemas.PostCreate,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user)  # JWT 인증 필수
):
    """게시글 작성 (로그인 필수) - user_id는 토큰에서 자동 추출"""
    return crud.create_post(db, user_id, post)

# =========================
# POST UPDATE (게시글 수정)
# =========================
@app.put("/posts/{post_id}")
def update_post(
    post_id: int,
    post: schemas.PostCreate,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user)  # JWT 인증 필수
):
    """
    게시글 수정 (작성자 본인만 가능)
    - crud.update_post에서 user_id 불일치 시 None 반환 → 403 에러
    """
    result = crud.update_post(db, post_id, user_id, post)
    if not result:
        raise HTTPException(status_code=403, detail="수정 권한이 없습니다.")

    return {
        "id": result.id,
        "title": result.title,
        "content": result.content,
        "user_id": result.user_id
    }

# =========================
# POST DELETE (게시글 삭제)
# =========================
@app.delete("/posts/{post_id}")
def delete_post(
    post_id: int,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user)  # JWT 인증 필수
):
    """게시글 삭제 (작성자 본인만 가능) - cascade로 댓글도 자동 삭제"""
    if not crud.delete_post(db, post_id, user_id):
        raise HTTPException(status_code=403, detail="삭제 권한이 없습니다.")
    return {"message": "게시글이 삭제되었습니다."}

# =========================
# 댓글 조회
# =========================
@app.get("/posts/{post_id}/comments")
def get_comments(post_id: int, db: Session = Depends(get_db)):
    """특정 게시글의 댓글 목록 조회 (인증 불필요)"""
    comments = crud.get_comments(db, post_id)
    return [
        {
            "id": c.id,
            "text": c.text,
            "user_id": c.user_id,
            "nickname": c.author.nickname if c.author else None
        }
        for c in comments
    ]

# =========================
# COMMENT CREATE (댓글 작성)
# =========================
@app.post("/posts/{post_id}/comments")
def create_comment(
    post_id: int,
    comment: schemas.CommentCreate,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user)  # JWT 인증 필수
):
    """댓글 작성 (로그인 필수)"""
    return crud.create_comment(db, user_id, post_id, comment)

# =========================
# COMMENT UPDATE (댓글 수정)
# =========================
@app.put("/comments/{comment_id}")
def update_comment(
    comment_id: int,
    comment: schemas.CommentCreate,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user)  # JWT 인증 필수
):
    """댓글 수정 (작성자 본인만 가능)"""
    result = crud.update_comment(db, comment_id, user_id, comment)
    if not result:
        raise HTTPException(status_code=403, detail="수정 권한이 없습니다.")
    return result

# =========================
# COMMENT DELETE (댓글 삭제)
# =========================
@app.delete("/comments/{comment_id}")
def delete_comment(
    comment_id: int,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user)  # JWT 인증 필수
):
    """댓글 삭제 (작성자 본인만 가능)"""
    if not crud.delete_comment(db, comment_id, user_id):
        raise HTTPException(status_code=403, detail="삭제 권한이 없습니다.")
    return {"message": "댓글이 삭제되었습니다."}
