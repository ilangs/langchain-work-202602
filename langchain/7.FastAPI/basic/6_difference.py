# BaseModel을 사용하는 이유 vs TypeDict를 사용하는 이유(차이점)
from pydantic import BaseModel # 입력 데이터 검증 및 스키마 정의(=DB)
from fastapi import FastAPI
# 추가
from typing import TypedDict

# Pydantic Basemodel : 1.런타임 검증, 직렬화(메모리값 -> 파일 저장(USB):이동 가능)
class UserModel(BaseModel):
    username: str
    age: int = 20      # 2.기본값 설정 가능 (멤버 변수에 미리 값을 저장)   3.자료형 변환 O

# TypedDict: 정적 타입을 chcking, 1.런타임 검증 없음 => 문제 있어도 pass 우려
class UserTypedDict(TypedDict):
    username: str      # 값을 저장시킬 때 반드시 자료형에 맞게 데이터를 입력하라.
    age: int #=25(x)   # 2. 기본값 기능이 없음    3.자료형 변환 X


# 테스트 코드
#-----------------------------------------------
print("\n===== BaseModel 객체 생성 예제(1) =====")
try:
    user1 = UserModel(username="alice") # age 기본값 적용
    print("user1:", user1)
    print("dict:", user1.model_dump()) # model_dump() => BaseModel객체를 Python dict로 변환
except Exception as e:
    print("에러 발생(e):", e)

#-----------------------------------------------
print("\n===== BaseModel 객체 생성 예제(2) =====")
try:
    user2 = UserModel(username="jane", age="25")  #문자열 -> 정수형으로 변환 기능
    print("user2:", user2)
    print("dict:", user2.model_dump()) # model_dump() => BaseModel객체를 Python dict로 변환
except Exception as e:
    print("에러 발생(e):", e)

#-----------------------------------------------
print("\n===== TypedDict 객체 생성 예제 =====")
try:
    user3: UserTypedDict = {"username": "bob", "age": "30"}
    print("user3:", user3)  # dict 타입 반환
    print("age타입:", type(user3["age"]))  
except Exception as e:
    print("에러 발생(e):", e)
    
#-----------------------------------------------
print("\n===== TypedDict 객체 생성 예제 =====")
try:
    user3: UserTypedDict = {"username": "bob"}
    print("user3:", user3)  # dict 타입 반환
    print("age타입:", type(user3["age"]))  
except Exception as e:
    print("에러 발생(e):", e)
    

    
"""
===== BaseModel 객체 생성 예제(1) =====
user1: username='alice' age=20
dict: {'username': 'alice', 'age': 20}

===== BaseModel 객체 생성 예제(2) =====
user2: username='jane' age=25
dict: {'username': 'jane', 'age': 25}

===== TypedDict 객체 생성 예제 =====
user3: {'username': 'bob', 'age': '30'}
age타입: <class 'int'>

===== TypedDict 객체 생성 예제 =====
user3: {'username': 'bob'}
에러 발생(e): 'age'
"""