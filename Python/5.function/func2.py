# func2.py파일 작성

'''
사용자정의 함수 => 만들어서 호츨할 목적
  ㄴ 작성 이유 => 필요로 하면 언제든지 사용(=호출)(=재사용성) => 소스코드 줄여주는 효과
'''
print('\n사용자 정의 함수\n')

# 1.매개변수 X, 반환값 X -> 단순반복
def printTest():
    print('테스트1')
    print('테스트1')
    print('테스트1')
    print('테스트1')
    print('테스트1')

printTest() # 호출 -> 함수명()
'''
테스트1
테스트1
테스트1
테스트1
테스트1
'''

def printTest2():
    for i in range(1,6): # 1, 5-1
        print('테스트'+str(i))
        
printTest2()
'''
테스트1
테스트2
테스트3
테스트4
테스트5
'''

# 2.매개변수 O,반환값 X->입력을 받아서 계산,저장,출력,조회 목적
def printTest3(start, end): # -> 반환값
    for i in range(start, end+1): # 5, 15+1=16
        print('테스트'+str(i))

printTest3(5,15)
'''
테스트5
테스트6
테스트7
테스트8
테스트9
테스트10
테스트11
테스트12
테스트13
테스트14
테스트15
'''

# 3.매개변수 O, 반환값 O -> 계산목적,웹프로그래밍에서 많이 사용
def DoFunc(arg1, arg2):
     re = arg1 + arg2
     return re  # 호출한 쪽으로 되돌린다.

# 형식) 반환받는 자료형 = 함수명(=생성자)(매개변수,,,)
cal = DoFunc(10,20)
print('cal(반환)=>', cal) # cal(반환)=> 30
print('===========')     # ===========
print(DoFunc(30,40))     # 70 = print(sum([30,40]))


print('함수명은 객체의 주소이다', DoFunc) # <function DoFunc at 0x000002C975ABD080>

# 함수를 다른 함수가 대신 호출 사용 가능 
otherFunc = DoFunc      # 함수 주소를 변수에 대입하면, (= 주소 공유)
print(otherFunc(90,100)) # 변수가 함수 역할을 한다. -> 190

# 내장함수 globals() => 만즐어진 함수 뿐만 아니라 내장함수의 정보를 출력
print('현재 객체목록:', globals()) # 객체 설명상의 Any => 명확한 자료형이 없는 임의의 자료
'''
현재 객체목록: {'__name__': '__main__', '__doc__': '\n사용자정의 함수 => 만들어서 호츨할 목적\n
ㄴ 작성 이유 => 필요로 하면 언제든지 사용(=호출)(=재사용성) => 소스코드 줄여주는 효과\n', 
'__package__': None, 
'__loader__': <_frozen_importlib_external.SourceFileLoader object at 0x000002783B3871D0>,
'__spec__': None, '__builtins__': <module 'builtins' (built-in)>, '__file__':
'c:\\workAI\\work\\Python\\5.function\\func2.py', '__cached__': None, 
'printTest': <function printTest at 0x000002783B543740>, 
'printTest2': <function printTest2 at 0x000002783B543950>, 
'printTest3': <function printTest3 at 0x000002783B5B3690>, 
'DoFunc': <function DoFunc at 0x000002783B5B3740>, 
'cal': 30, 'otherFunc': <function DoFunc at 0x000002783B5B3740>}
'''

# 5.함수의 매개변수 -> 갯수별로 작성해야 되는가? 일반적으로 Yes
# *매개변수 -> list, set, tuple 형태의 자료를 받아서 처리
# **매개변수 -> dict 형태의 자료를 받아서 처리

def ListHap(*ar):
    print(ar)

list = [1,3,5]; list2 = [1,2,6]
ListHap(list,list2)  # ([1, 3, 5], [1, 2, 6])
