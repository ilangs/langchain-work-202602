# auth.py

from datetime import datetime, timedelta   # 토큰 만료 시간 계산용
from jose import jwt, JWTError             # JWT 생성/검증, 에러 처리
from fastapi import HTTPException          # API 에러 응답용
import os                                  # 환경변수 접근
from passlib.context import CryptContext   # bcrypt 비밀번호 해싱

# =========================
# 비밀번호 암호화 설정
# =========================
pwd_context = CryptContext(
    schemes=["bcrypt"],   # bcrypt 알고리즘 사용 (단방향 해시, 복호화 불가)
    deprecated="auto"     # 구버전 방식은 자동 비활성화
)

# =========================
# JWT 설정값
# =========================
from dotenv import load_dotenv
# __file__ → 현재 파일(auth.py)의 절대경로
# os.path.dirname() → 현재 파일이 속한 폴더 (backend2/)
# os.path.join(..., "..") → 한 단계 위 폴더 (work/)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) # BASE_DIR = /절대경로/work/
load_dotenv(os.path.join(BASE_DIR, ".env"))                            # work/.env을 명시적으로 지정

JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "dev-secret-key")  # 운영 환경에서는 반드시 환경변수로 관리
ALGORITHM = "HS256"                                             # 대칭키 서명 알고리즘
ACCESS_TOKEN_EXPIRE_MINUTES = 30                                # Access Token 유효 시간: 30분
REFRESH_TOKEN_EXPIRE_DAYS = 7                                   # Refresh Token 유효 시간: 7일

# =========================
# 비밀번호 해시 (회원가입 시 사용)
# =========================
def hash_password(password: str) -> str:
    """평문 비밀번호 → bcrypt 해시값으로 변환 (DB 저장용)"""
    return pwd_context.hash(password)

# =========================
# 비밀번호 검증 (로그인 시 사용)
# =========================
def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    입력된 평문 비밀번호와 DB에 저장된 해시값을 비교하여 일치 여부 반환
    - plain_password: 사용자가 로그인 폼에서 입력한 비밀번호
    - hashed_password: DB에 저장된 bcrypt 해시값
    """
    return pwd_context.verify(plain_password, hashed_password)

# =========================
# Access Token 생성
# =========================
def create_access_token(user_id: int) -> str:
    """
    사용자 ID를 payload에 담아 단기 Access Token(JWT) 생성
    - 유효 시간: ACCESS_TOKEN_EXPIRE_MINUTES (기본 30분)
    - 클라이언트는 이 토큰을 Authorization 헤더에 담아 API 요청
    """
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    payload = {
        "sub": str(user_id),  # subject: 사용자 식별자 (문자열로 저장)
        "exp": expire,         # 만료 시간
        "type": "access"       # 토큰 종류 구분 (access / refresh 혼용 방지)
    }
    return jwt.encode(payload, JWT_SECRET_KEY, algorithm=ALGORITHM)

# =========================
# Refresh Token 생성
# =========================
def create_refresh_token(user_id: int) -> str:
    """
    장기 Refresh Token 생성 (Access Token 재발급용)
    - 유효 시간: REFRESH_TOKEN_EXPIRE_DAYS (기본 7일)
    - 클라이언트는 HttpOnly 쿠키에 저장하여 XSS 공격 방어
    """
    expire = datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    payload = {
        "sub": str(user_id),
        "exp": expire,
        "type": "refresh"      # access token과 구분하기 위한 타입 필드
    }
    return jwt.encode(payload, JWT_SECRET_KEY, algorithm=ALGORITHM)

# =========================
# 토큰 디코드 (검증)
# =========================
def decode_token(token: str) -> dict:
    """
    JWT 토큰을 디코딩하여 payload(dict) 반환
    - 서명 검증, 만료 시간 검증 자동 수행
    - 유효하지 않으면 401 HTTPException 발생
    """
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        # 서명 불일치, 만료, 형식 오류 등 모든 JWT 에러를 401로 통일
        raise HTTPException(status_code=401, detail="토큰이 유효하지 않습니다.")

# =========================
# 사용자 ID 추출
# =========================
def get_user_id_from_token(token: str) -> int:
    """
    디코딩된 토큰의 'sub' 필드에서 사용자 ID(int) 추출
    - sub 필드가 없으면 401 에러 반환
    """
    payload = decode_token(token)
    user_id = payload.get("sub")  # 토큰 생성 시 str로 저장했으므로 int 변환 필요
    if user_id is None:
        raise HTTPException(status_code=401, detail="토큰에서 사용자 정보를 찾을 수 없습니다.")
    return int(user_id)
