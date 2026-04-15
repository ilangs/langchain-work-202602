# 4.crud.py 작성

from sqlalchemy.orm import Session  # DB 세션 타입
from models import Post             # Post 모델 import

# 전체 게시글 조회(select * from posts) where 조건식이 없으면 보통 매개변수 없음
def get_posts(db: Session):     
    return db.query(Post).all() # 모든 데이터 조회

# 새 게시글 생성->insert
def create_post(db: Session, title: str, content: str):  
    new_post = Post(title=title, content=content)  
    db.add(new_post)                               # DB에 추가
    db.commit()                                    # 저장 -> rollback 안 됨
    db.refresh(new_post)                           # 최신 상태 반영, 새로고침
    return new_post                                # 결과 반환

# 게시글 삭제->delete from table명 where 조건식=>매개변수 있음
def delete_post(db: Session, post_id: int):  
    post = db.query(Post).filter(Post.id == post_id).first() # 해당 게시글 찾기
    if post:                                                 # 존재하면
        db.delete(post)                                      # 삭제
        db.commit()                                          # 저장
    return post                                              # 삭제된 데이터 반환

# 게시글 수정
def update_post(db: Session, post_id: int, title: str, content: str):
    post = db.query(Post).filter(Post.id == post_id).first()
    if post:
        post.title = title
        post.content = content
        db.commit()
        db.refresh(post)
    return post

# 게시글 검색
def search_posts(db: Session, keyword: str):
    return db.query(Post).filter(
        (Post.title.contains(keyword)) | (Post.content.contains(keyword))
    ).all()
    