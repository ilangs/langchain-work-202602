# 3.schemas.py 작성

from pydantic import BaseModel  # 데이터 검증용 모델

class PostCreate(BaseModel):    # 게시글 생성 요청 데이터 (insert)
    title: str                  # 제목
    content: str                # 내용

class PostResponse(BaseModel):  # 응답 데이터 구조
    id: int
    title: str
    content: str
    
    # 내부클래스 (클래스 내부에 또 다른 클래스(환경설정))->들여쓰기 필수
    class Config:               
        orm_mode = True         # ORM객체를 JSON으로 변환 허용 (리액트에서 출력 목적)