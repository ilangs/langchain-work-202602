# ex2.py => 자료형 => 데이터의 종류와 크기를 지정해 주는 것

print('변수 선언시 대,소문자 구분')
print('들여쓰기 조심(함수,제어문,클래스 작성시)') # 함수, 메서드의 차이점

# 예약어
import keyword   # 키워드 목록을 읽기 위한 외부 모듈
print('키워드 목록', keyword.kwlist)
'''
키워드 목록 ['False', 'None', 'True', '__peg_parser__', 
            'and', 'as', 'assert', 'async', 'await', 'break', 
            'class', 'continue', 'def', 'del', 'elif', 'else', 'except',
            'finally', 'for', 'from', 'global', 'if', 'import', 'in', 'is',
            'lambda', 'nonlocal', 'not', 'or', 'pass', 'raise', 
            'return', 'try', 'while', 'with', 'yield']
'''

# 자료형=>내부함수=>파이썬을 설치하면 자동적으로 내부적으로 존재하는 함수 <-> 사용자 정의 함수
print('\n\n숫자 진법')
# oct(숫자) 16진수, hex(숫자) 10진수, bin(숫자) 2진수
print(10, oct(10), hex(10), bin(10)) 
print(10, 0o12, 0xa, 0b1010)
'''
숫자 진법
10 0o12 0xa 0b1010
10 10 10 10
'''

print('type(자료형) 확인')
print(7, type(7))
print(7.2 , type(7.2))
print(3 + 4j, type(3 + 4j))
print(True, type(True))
print('a', type('a'))
'''
type(자료형) 확인
7 <class 'int'>
7.2 <class 'float'>
(3+4j) <class 'complex'>
True <class 'bool'>
a <class 'str'>
'''

print('특별한 자료형')
print('list,tuple,set,dict')        # list, dict 자주 사용
print([1], type([1]))               # list
print((1,), type((1,)))             # tuple, (1)=>int
print({1}, type({1}))               # set => set()
print({'key':1}, type({'key':1}))   # dict=> 키값:저장값
'''
(1,) <class 'tuple'>
[1] <class 'list'>
{1} <class 'set'>
{'key': 1} <class 'dict'>
'''
