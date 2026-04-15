# crud.py

# =========================
# DB 세션 및 SQL 함수 import
# =========================
from sqlalchemy.orm import Session
from sqlalchemy import or_, func

# =========================
# 모델 import
# =========================
from models import User, Post, Comment

# =========================
# 비밀번호 암호화 함수
# =========================
from auth import hash_password

# =========================
# 회원가입 (UserForm.jsx)에서 입력한 값 전달
# =========================
def create_user(db: Session, user):
    """
    새 사용자를 DB에 저장
    - 비밀번호는 hash_password()로 암호화 후 저장 (평문 저장 절대 금지)
    - db.refresh()로 DB에서 최신 상태(id, created_at 등) 재조회
    """
    db_user = User(                             # id 자동 부여(pk)
        email=user.email,
        nickname=user.nickname,
        password=hash_password(user.password),  # bcrypt 해시 변환 후 저장
        name=user.name,
        address=user.address,
        phone=user.phone
    )
    db.add(db_user)      # INSERT 준비 (아직 DB 반영 전)
    db.commit()          # 트랜잭션 커밋 → DB 실제 저장
    db.refresh(db_user)  # DB에서 최신 데이터 재로드 (auto increment id 등 반영)
    
    return db_user

# =========================
# 로그인 (이메일 조회) <--- /login 요청시
# =========================
def get_user_by_email(db: Session, email: str):
    """
    이메일로 사용자 단건 조회
    - 로그인 시 이메일 존재 여부 확인 및 비밀번호 검증에 사용
    - 없으면 None 반환 (호출부에서 404 처리)
    """
    return db.query(User).filter(User.email == email).first()

# =========================
# 게시글 생성
# =========================
def create_post(db: Session, user_id: int, post):
    """새 게시글 저장, JWT에서 추출한 user_id를 작성자로 등록"""
    new_post = Post(
        title=post.title,
        content=post.content,
        user_id=user_id   # 로그인된 사용자 ID를 작성자로 설정
    )
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

# =========================
# 게시글 목록 + 검색 + Pagination + author join
# =========================
def get_posts(db: Session, keyword: str = None, skip: int = 0, limit: int = 10):
    """
    게시글 목록 조회 (검색 + 페이지네이션 + 댓글 수 포함)
    - keyword: 제목/내용 부분 일치 검색 (ilike → 대소문자 무시)
    - skip/limit: 페이지네이션 오프셋 방식
    - outerjoin(Comment): 댓글 없는 게시글도 포함하여 댓글 수 집계
    """
    query = db.query(Post)

    if keyword:
        # 제목 또는 내용에 keyword가 포함된 게시글 필터링
        query = query.filter(
            or_(
                Post.title.ilike(f"%{keyword}%"),
                Post.content.ilike(f"%{keyword}%")
            )
        )

    total = query.count()  # 전체 건수 (페이지 계산에 필요)

    # 댓글 수 포함 LEFT OUTER JOIN (댓글이 0개인 게시글도 포함)
    results = (
        db.query(Post, func.count(Comment.id).label("comment_count"))
        .outerjoin(Comment)
        .group_by(Post.id)
        .order_by(Post.id.desc())   # 최신 게시글 우선
        .offset(skip)
        .limit(limit)
        .all()
    )

    items = []
    for p, count in results:
        items.append({
            "id": p.id,
            "title": p.title,
            "content": p.content,
            "user_id": p.user_id,
            "nickname": p.author.nickname if p.author else None,  # relationship 통해 작성자 닉네임 조회
            "comment_count": count
        })

    return {"total": total, "items": items}

# =========================
# 게시글 수정
# =========================
def update_post(db: Session, post_id: int, user_id: int, post):
    """
    게시글 수정 (작성자 본인만 가능)
    - user_id 불일치 시 None 반환 → 호출부에서 403 처리
    """
    p = db.query(Post).filter(Post.id == post_id).first()
    if not p or p.user_id != user_id:  # 게시글 없거나 작성자 불일치
        return None
    p.title = post.title
    p.content = post.content
    db.commit()
    db.refresh(p)
    return p

# =========================
# 게시글 삭제
# =========================
def delete_post(db: Session, post_id: int, user_id: int):
    """
    게시글 삭제 (작성자 본인만 가능)
    - cascade="all, delete" 설정으로 연결된 댓글도 자동 삭제 (models.py 참조)
    """
    p = db.query(Post).filter(Post.id == post_id).first()
    if not p or p.user_id != user_id:
        return False
    db.delete(p)
    db.commit()
    return True

# =========================
# 댓글 생성
# =========================
def create_comment(db: Session, user_id: int, post_id: int, comment):
    """새 댓글 저장, 로그인 사용자 ID와 대상 게시글 ID를 함께 등록"""
    c = Comment(
        text=comment.text,
        user_id=user_id,  # JWT에서 추출한 작성자 ID
        post_id=post_id   # 어떤 게시글의 댓글인지
    )
    db.add(c)
    db.commit()
    db.refresh(c)
    return c

# =========================
# 댓글 조회
# =========================
def get_comments(db: Session, post_id: int):
    """특정 게시글의 댓글 목록 조회 (최신순)"""
    return db.query(Comment)\
        .filter(Comment.post_id == post_id)\
        .order_by(Comment.id.desc())\
        .all()

# =========================
# 댓글 수정
# =========================
def update_comment(db: Session, comment_id: int, user_id: int, comment):
    """
    댓글 수정 (작성자 본인만 가능)
    - user_id 불일치 시 None 반환 → 호출부에서 403 처리
    """
    c = db.query(Comment).filter(Comment.id == comment_id).first()
    if not c or c.user_id != user_id:
        return None
    c.text = comment.text
    db.commit()
    db.refresh(c)
    return c

# =========================
# 댓글 삭제
# =========================
def delete_comment(db: Session, comment_id: int, user_id: int):
    """댓글 삭제 (작성자 본인만 가능)"""
    c = db.query(Comment).filter(Comment.id == comment_id).first()
    if not c or c.user_id != user_id:
        return False
    db.delete(c)
    db.commit()
    return True
