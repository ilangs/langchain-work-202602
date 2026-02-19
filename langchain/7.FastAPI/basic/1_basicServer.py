# basicServer(1).py

#1.FastAPI 클래스를 가져 온다.
from fastapi import FastAPI
import uvicorn # FastAPI를 사용하게 해주는 클래스

#2.FastAPI 객체를 생성 -> 1.데이터 저장 목적 2. 특정한 메서드를 호출하기 위해
app = FastAPI()  # FastAPI 어플리케이션 객체 생성 (형식) 객체명 = 클래스명()

#3.접속 -> Get 방식(=SQL select에 해당)
@app.get("/") # HTTP GET 요청 명령어 "/"로 요청 => 함수로 만들어서 호출
def read_root(): #FastAPI => 접속 => 결과물을 반환(json형태(key,value))
    return {"message":"Hello FastAPI"}

#FAST API(GET,POST) != REST API(GET,POST+PUT,DELETE)
#@app(어플리케이션 객체명).요청방식명(get()): 데이터 조회
#@app.post(): 데이터 생성할 때 (= insert)
#@app.put(): 데이터 수정할 때 (= update)
#@app.delete(): 데이터 삭제할 때 (= delete)

#서버 가동 방법 -> uvicorn 파일명:app(객체명) --reload (=새로 고침기능) -> 종료는 CTRL+C

# uvicorn 1_basicServer:app --reload