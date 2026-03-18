# func3.py파일 작성

'''
함수의 전역변수, 지역변수의 범위
'''

player = '전국대표' # 함수 밖에 선언 (전역변수)

def FuncSoccer():
    name = '홍길동' # 함수 안에 선언 (지역변수)
    player='지역선수'
    print(name, player) # 동일변수명이면 지역변수를 먼저 찾는다.

print('player=', player) # player= 전국대표
FuncSoccer() # 홍길동 지역선수

def FuncSoccer():
    name = '홍길동' # 함수 안에 선언 (지역변수)
    # player='지역선수'
    print(name, player) # 지역변수를 먼저 찾고, 없으면 전역변수를 찾아서 출력

print('player=', player) # player= 전국대표
FuncSoccer() # 홍길동 전국대표