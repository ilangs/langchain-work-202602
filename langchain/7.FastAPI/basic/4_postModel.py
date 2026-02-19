# 값을 입력을 받아서 검증 => class를 통해서 검증 가능
from pydantic import BaseModel # 입력 데이터 검증 및 스키마 정의(=DB)
#1.FastAPI 클래스를 가져 온다.
from fastapi import FastAPI

# Item(상품) => 왜 상속?(멤버 변수(=데이터 저장 목적)와 메서드를 상속받기 위해서(=소유권 이전))
class Item(BaseModel): # 입력 데이터 구조 정의 vs 랭그래프 class ChefState(TypeDict):
    name: str
    price: float
    is_offer: bool = None

#2.FastAPI 객체를 생성 
app = FastAPI()  

#3.접속=>상품구매(items) => json형태로 받아서 반환
# 기술면접 => 용어 질문 (CRUD, 직렬화 등등)
# 직렬화 => 메모리상에서 저장된 변수값을 --> 파일로 저장하는 것 (USB에 담기(이동 목적), 메일로 전송)
# 역직렬화 => USB에 저장된 데이터를 메모리에 Loading(로딩해서 작업)
@app.get("/items/") # 객체명.멤버변수명
def create_item(item: Item): # Item = (item_name:str, item_price:float, is_offer:bool)
    return {"item_name": item.name, 
            "item_price": item.price, 
            "item_is_offer": item.is_offer} 
    

# 웹상에서 입력할때 클래스의 멤버변수로써 입력----------->내부에서 Item객체로 변환되어서 출력
#  {
#  "name": "사과", 
#  "price": 5000,
#  "is_offer":false      =>★postman에서는 False가 아닌 false를 써야 된다.(주의)
#  }


# uvicorn 4_postModel:app --reload