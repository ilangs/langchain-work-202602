# 2.models.py 작성=>database.py를 이용->Base를 불러와서 상속받아서 작성(클래스)

from sqlalchemy import Column, Integer, String          # 컬럼 타입 import
from database import Base                               # Base 클래스 import

# 게시판 =>  1:다 

class Post(Base):                                       # 게시글 테이블 정의
    __tablename__ = "posts"                             # 테이블명 지정
    #           1.자료형  2.제약조건  3.인덱스여부(속도향상)        
    id = Column(Integer, primary_key=True, index=True)  # 기본키 (자동 증가)
    title = Column(String(100))                         # 제목
    content = Column(String(500))                       # 내용  
    #addr = Column(String(400))                          # 주소  
