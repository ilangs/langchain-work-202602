# ex12_if.py

'''
1.순차문 - 작성 순서대로 실행하는 구문 - 변수선언, 연산자계산, 출력문
2.제어문 - 특정 조건에 따라서 실행 O or 실행 X 구문 
    ㄴ if문 (둘 중 하나 선택), for문, while문

형식) if 조건식(관계,산술,,,) :
        명령1
        명령2
      명령3
'''
var = 2
if var >= 3:
    print('크다')
    print('참일때 수행')
print('계속')   
'''
계속
'''

var = 5
if var >= 3:
    print('참일때 수행')
    print('계속')
    print('3보다 크다')
'''
참일때 수행
계속
3보다 크다
'''

if var >= 3:
    print('참인 경우 실행')
else:
    print('거짓인 경우 실행 숫자가 적음')
print('end1')
'''
참인경우 실행
end1
'''

# 여러개의 if문 -> if문내의 또다른 if문(ex 로그인 처리)
money = 1000
age = 23
msg = '' # 조건식이 거짓일때 에러 유발 -> 변수선언 (전역)

if money >= 200:
    item = 'apple' # 지역변수
    if age >= 30:
        msg = 'young'
# 제어문 안에서 선언된 지역변수는 제어문 밖에서 참조할 수 없다.
print('item,msg=',item,msg)  # item,msg= apple 

# 다중 if문
'''
 if 조건식:
    명령어1
elif 조건식2: (elif => else if의 약어 표현)
    명령어2
else:
    명령어3
'''
jumsu = 95
if jumsu >= 90:
    print('우수')
else:
    if jumsu >= 70:
        print('보통')
    else:
        print('저조')
print('end2')
'''
우수
end2
'''

if jumsu >= 90:
    print('우수')
elif jumsu >= 70: # else: if -> elif 사용 가능
        print('보통')
else:
        print('저조')
print('end3')
'''
우수
end3
'''

jum = int(input('점수입력?'))
# print(jum) # >=, <= (&& ||->and,or)로 바뀜
# if jum >= 90 and jum <= 100: 정석방법 >>> if 90 <= jum <= 100: 응용방법
if 90 <= jum <= 100:
    grade = '우수3'
elif 70 <= jum < 90:
    grade = '보통3'
else:
    grade = '저조3'
print('결과=' + str(jum) + ',등급=' + grade)
# jum -> TypeError: can only concatenate str (not "int") to str

'''
점수입력? 97
결과=97,등급=우수3
'''

#삼항연산자->변수=(조건식)?참:거짓
print('\n삼항 연산자')
a = 3
if a > 5:
    re = a*2
else:
    re = a+2
print('re=',re)
'''
삼항 연산자
re= 5
'''

# 변수 = 참인 경우 실행문 if 조건식 else 거짓인 경우 실행문
re = a*2 if a > 5 else a+2
print(re) # 5

# 변형 삼항연산자(튜플)->()
# (0번째요소,1번째요소)[조건식] -> 조건식이 참이면 1번째요소 반환, 거짓이면 0번째요소 반환
print((a+2,a*2)[a>5]) # 5
