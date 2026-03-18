# func7.py => 람다함수,재귀함수

#람다함수=익명함수 -> 코드 간소화, 메모리 절감 용도
print('축약함수(Lambda-이름이 없는 한줄짜리')
#형식 lambda 인자:표현식(구문)(값1,값2,,,)
def Hap(x,y):
    return x+y

print(Hap(3,4))#7
print('람다로 표현하면')
print((lambda x,y:x+y)(3,4))#7
print('\n람다도 가변인수 부여 가능')

#람다함수=>이름있는 함수로 변경가능, kbs=함수의 주소값(치환)
kbs=lambda a,su=10:a+su #su=10은 두번째 인수 입력이 없을때 디폴트값
print(kbs(5))#15
print(kbs(5,6))#11

sbs=lambda a,*tu,**di:print(a,tu,di)
sbs(1,2,3,m=4,n=5) #매개변수명=전달할값,,,->{'매개변수명':'값'}(X)
#1 (2, 3) {'m': 4, 'n': 5}

print('\n다른함수에서 람다 사용하기')
#filter(함수,시퀀스 자료형(=순서가 있는 자료형))
#0~9까지 중에서 조건에 만족하는 데이터를 리스트로 출력
print(list(filter(lambda a:a<5,range(10))))#[0, 1, 2, 3, 4]
print(list(filter(lambda a:a%2,range(10))))#false만 출력 [1, 3, 5, 7, 9]

#재귀함수->자기가 자기자신을 호출 -> 일반적으로 함수(caller->worker)별도 
print('\n재귀함수(팩토리얼계산)') #5!=>5*4*3*2*1
def fsum(n):
    if n==1: return 1
    return n+fsum(n-1)
print(fsum(10))#55->10+9+8+...1=55

def CountDown(n):
    if n==0:  # 종료조건을 반드시 부여 (무한루프 방지)
        print('완료')
    else:
        print(n,end=' ')
        CountDown(n-1)
CountDown(5)#5 4 3 2 1 완료
