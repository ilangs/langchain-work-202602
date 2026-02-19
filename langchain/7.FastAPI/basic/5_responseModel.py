# 값을 입력을 받아서 검증 => class를 통해서 검증 가능
from pydantic import BaseModel # 입력 데이터 검증 및 스키마 정의(=DB)
#1.FastAPI 클래스를 가져 온다.
from fastapi import FastAPI
# 추가
from typing import Optional


class User(BaseModel):
    username: str
    email: Optional[str] = None # 형식) Optional[입력받는 자료형] = None
                                # => 문자열 또는 None (기본값 None으로 설정)
                                # => 필수입력이 아닌 선택입력 필드

#2.FastAPI 객체를 생성 
app = FastAPI()  

#3.접속
# /users/23 함수뒤에, response=User (사용자 정의 자료형) => 전달받은 객체는 User를 의미
# select username from User
@app.get("/users/{username}", response_model=User) 
def get_user(username: str): 
    return User(username=username) # username(멤버변수)=전달받은 매개변수(익명객체)

# 익명객체 => 이름없는 객체(작자미상)
# 객체명 = 클래스명()  객체명.멤버변수=값
# User(username=username)      => 객체이름 없음
# us = User(username=username) => 객체이름 us
# return us                    => 객체이름 us


# uvicorn 5_responseModel:app --reload