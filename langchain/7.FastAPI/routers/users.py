# users.py => db 접속하여 users 테이블에 CRUD 관리

from fastapi import APIRouter, HTTPException  # 공통경로 관리, 예외처리
from pydantic import BaseModel                # 데이터 검증 모델
from typing import List                       # 리스트 타입()= 데이터 여러개(select)
from dataBase import get_db_connection        # DB 연결함수 import

#RestAPI -> 경로가 겹치는 경우 -> 공통 경로를 지정
# prefix="공통경로 지정", tags=프로젝트내의 문서분류 기준
router = APIRouter(prefix="/users", tags=["Users"])
# router = APIRouter(prefix="/items", tags=["Items"])
# router = APIRouter(prefix="/payments", tags=["payments"])

# pydantic 모델 정의 (=다른 랭귀지(java) DTO(=Data Transfer Object)=>데이터 전송 목적(직렬화)

class UserCreate(BaseModel):    #생성용 모델(insert)
    name: str
    email: str
    
class UserUpdate(BaseModel):    #수정용 모델(update) -> id 수정X
    name: str
    email: str

class UserResponse(BaseModel):  #검색(=응답) 모델 -> id 필요 (동명이인 구분)
    id: int
    name: str
    email: str

#1.Create(insert)
#요청경로("/")->/users/ ->insert->select=>json형으로 반환 (RestAPI)
@router.post("/", response_model=UserResponse)
def create_user(user: UserCreate):  #(name:str, email:str, ,,,)
    conn = get_db_connection()   # DB 연결
    cursor = conn.cursor()   # 커서 생성 =>SQL구문 실행
    cursor.execute(   
        #"INSERT INTO users (name, email) VALUES ('Hong','Hong@abc.com')", -> 정적 입력           
        "INSERT INTO users (name, email) VALUES (?, ?)",  #? 동적 입력
        (user.name, user.email)
    )

    conn.commit()   # 변경사항 저장
    user_id = cursor.lastrowid   # cursor.excute시 생성된 ID 가져오기
    conn.close()   # 연결 종료 (= 메모리 해제)
    return {"id": user_id, "name": user.name, "email": user.email}

#2.Read (Select ALL) Get /users/
@router.get("/", response_model=List[UserResponse]) #데이터 여러개, list형태(id,name,email) 
def get_users():  # DB 전체 가져오기
    conn = get_db_connection()   # DB 연결
    # cursor = conn.cursor()   # 커서 생성 =>SQL구문 실행
    # select 구문에서는 conn.execute 약어형 사용
    users = conn.execute("SELECT * FROM users").fetchall()  # fetchall()=>모든 행
    
    # conn.commit() #commit: insert,update,delete 등 DB 테이블에 변화가 발생하는 경우에 사용
    # commit()을 하면 복구(x) -> rollback 불가
    conn.close()
    return [dict(user) for user in users] #for문
    # user리스트 객체에서 하나씩 user 객체를 꺼내어 웹에 출력하기 위해 dict형으로 변환
    # dict형으로 변환 (RestAPI을 사용하고 있기 때문에)
    # for 담을객체명 in 리스트객체(배열)

#3.Read (Select ONE) Get /users/2
@router.get("/{user_id}", response_model=UserResponse) #데이터 1개
def get_user(user_id: int):  
    conn = get_db_connection()   
    user = conn.execute(
        "SELECT * FROM users WHERE id = ?", 
        (user_id,)).fetchone()   #fetchone() => 1개 데이터, (user_id,) = [user_id]
    
    conn.close()

    # 찾는 데이터가 없는 경우 예외 처리
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return dict(user)  # 키, value형태로 반환

#4.Update put /users/2 -> id가 2번인 데이터를 찾아서 수정
@router.put("/{user_id}", response_model=UserResponse) #최종 출력용(id,name,email)
def update_user(user_id: int, updated_user: UserUpdate): #수정된 데이터만 확인
    conn = get_db_connection() #DB연결
    cursor = conn.cursor() #insert,update,delete경우  conn.excute()->주로 select구문 경우
    cursor.execute(
        "UPDATE users SET name=?, email=? WHERE id=?", 
        (updated_user.name, updated_user.email, user_id) # updated_user_id는 수정불가
        )
    
    # 수정 대상 데이터가 없다면 예외 처리 (회원탈퇴 등)
    if cursor.rowcount == 0:
        conn.close() 
        raise HTTPException(status_code=404, detail="User not found")
    
    # 정상 수정된 경우
    conn.commit() #변경 저장 반영 -> 테이블에 그대로 저장
    conn.close()
    return  {"id": user_id, "name": updated_user.name, "email": updated_user.email} 

#5.Delete
@router.delete("/{user_id}") # 데이터가 없기 때문에 출력x
def delete_user(user_id: int): 
    conn = get_db_connection() 
    cursor = conn.cursor() 
    cursor.execute("DELETE FROM users WHERE id=?", (user_id,))   # (user_id,) = [user_id]
    
    # 수정 대상 데이터가 없다면 예외 처리 (회원탈퇴 등)
    if cursor.rowcount == 0:
        conn.close() 
        raise HTTPException(status_code=404, detail="User not found")
    
    # 정상 수정된 경우
    conn.commit() #변경 저장 반영 -> 테이블에 그대로 저장
    conn.close()
    return  {"message":f"User {user_id} is deleted successfully"}

