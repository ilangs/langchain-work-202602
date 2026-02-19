
from fastapi import FastAPI, HTTPException

app = FastAPI() 

#3.접속 -> Get 방식(=SQL select에 해당)
@app.get("/error/") 
def raise_error():
    #404 -> 요청한 데이터가 없을 때 발생, 500 -> 문법 에러
    raise HTTPException(status_code=404, detail="Item not found")

#1.서버의 상태코드값, detail="이유"

# uvicorn 7_error:app --reload