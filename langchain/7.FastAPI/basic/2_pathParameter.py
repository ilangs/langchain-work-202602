#웹프로그래밍 -> 파라미터값을 어떻게 전달하고 전달받는지에 대한 개념 
#1.FastAPI 클래스를 가져 온다.
from fastapi import FastAPI 

#2.FastAPI 객체를 생성 
app = FastAPI()  

#3.접속 => 상품구매(items) 

# 파라미터 값을 넘기는 방법 

#(1)Path Parameter(대분류 검색): /items/3 => 상품의 item_id가 3번인 데이터 => {전달할 변수명}
@app.get("/items/{item_id}") #URL 경로에 변수를 지정
def read_item(item_id: int): #변수명:자료형 => 타입힌트로 int 지정 -> 자동 검증
    return {"item_id": item_id} #요청경로의 숫자를 그대로 반환

#(2)Query Parameter(중,소분류 검색): /items?skip=5&limit=20
# =>  ~?매개변수=전달값&매개변수2=전달값2&...
# => 페이지 데이터 공유 목적: A페이지에서 B페이지로 이동하면 A페이지 정보는 사라지므로...
# async def 함수명 => 비동기 처리하는 함수라는 의미 (JavaScript 교육시 추가 교육 예정)
@app.get("/items") #함수에서 매개변수를 전달 받지 못한 경우 => default값(=기본값) 전달
async def read_item(skip: int = 0, limit: int = 10): #FastAPI=>접속=>결과물 반환(json(key,value))
    #skip,limit는 URL 경로에 없지만 ?skip=0&limit=10 형식으로 전달받을 수 있다.
    return {"skip": skip, "limit": limit}

# uvicorn 2_pathParameter:app --reload