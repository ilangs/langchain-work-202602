# main.py

from fastapi import FastAPI
from routers import users #라우터
# from routers import items 

app = FastAPI()  # FastAPI 어플리케이션 객체 생성 (형식) 객체명 = 클래스명()

#서버 접속
@app.get("/") 
def read_root(): #FastAPI => 접속 => 결과물을 반환(json형태(key,value))
    return {"message":"FastAPI Server Running"}  # 서버 동작 확인

# 라우터 연결
app.include_router(users.router) #users 라우터 등록
# app.include_router(items.router) 

# uvicorn main:app --reload
