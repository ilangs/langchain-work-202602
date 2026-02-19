#웹프로그래밍 -> 파라미터값의 범위를 지정(숫자,문자) -> Query 함수 이용
#1.FastAPI 클래스를 가져 온다.
from fastapi import FastAPI, Query #데이터 제약조건 부여

#2.FastAPI 객체를 생성 
app = FastAPI()  


@app.get("/items/") #URL 경로에 변수를 지정(문자,숫자 입력(제약조건=원하는데이터만 입력))
# Query함수 사용목적 : 1.디폴트값 설정  2.범위해당 옵션...  3.title="사용목적"
# 사용예시: 판매/주문수량 제한, 재고수량 한계, 발주수량/금액 제한
async def read_items(q: str = Query(None,min_length=3,max_length=50,title="검색어"),
                     limit: int = Query(10,gt=0,le=100)): # >0, <=100 (1~100)
    return {"q": q, "limit": limit} 

# uvicorn 3_dataValidation:app --reload