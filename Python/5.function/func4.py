# func4.py파일 작성

'''
함수명을 호출->인수
만일 매개변수값을 전달받지 않으면->에러 유발->디폴트 매개변수를 설정으로 에러방지
'''

#1.함수선언시 초기값 부여
def ShowGugudan(start,end=5): 
    #range(2,4)->(2,3)
    for dan in range(start,end+1):
        print(str(dan)+'단 출력')
        for i in range(1,10):#(1,2,,,,9)
            print(str(dan)+"*"+str(i)+"="+str(dan*i),end=' ')
        print()

ShowGugudan(2,3) # 2단,3단 출력
print('=='*20)
ShowGugudan(3) # 3단,4단,5단 출력
print('=='*20)

#2.함수호출할때 변수를 이용해서 전달 가능 => 매개변수명=전달할값
ShowGugudan(start=6,end=8) # 6단,7단,8단 출력
print('=='*20)
#3.매개변수명=전달할값의 순서를 변경 가능
ShowGugudan(end=4,start=3) # 3단,4단 출력
print('='*20)
#4.매개변수중에서 원하는 것만 매개변수명=값
ShowGugudan(5,end=6)       # 5단,6단 출력
print('='*10)
#주의할 점
#매개변수명 -> 첫번째는 생략 가능, 두번째는 생략 불가
#ShowGugudan(start=2,3) # error 

#6.가변 인수 처리
def Func1(*ar): # *(매개변수 갯수X,list,set,tuple)
    print(ar)
    # 입력받은 데이터값을 하나씩 변수에 담아 출력
    for i in ar:
        print('food:'+i)

Func1('ham','egg','spam') 
'''
('ham', 'egg', 'spam')
food:ham
food:egg
food:spam
'''
#주의할 점
#def Func2(*ar,a) 
# ->TypeError: Func2() missing 1 required keyword-only argument: 'a'
# ->가변인수는 맨 뒤에 위치해야 한다.
# ->가변인수가 앞에 있으면 앞에서 모두 받아 처리하므로 뒤의 인수에는 할당 안되어 에러
def Func2(a,*ar): 
    print(a)  # ham
    print(ar) # ('egg', 'spam')
    for i in ar:
        print('food:'+i)

Func2('ham','egg','spam')
'''
ham
('egg', 'spam')
food:egg
food:spam
'''
print("-----------")
#앞의 매개변수에 따라서 뒤의 값을 +,*해주는 함수를 작성
def SelProcess(choice,*ar):
    if choice=='sum':
        re=0
        for i in ar:
            re+=i
    elif choice=='mul':
        re=1
        for i in ar:
            re*=i
    return re

print(SelProcess('sum',100,90,70)) # 260
print(SelProcess('mul',100,90,78)) # 702000