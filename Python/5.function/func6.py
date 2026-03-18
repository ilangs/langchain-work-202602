# func6.py파일 작성

# 클로저 함수 => 중첩함수(함수 내부에 또 다른 함수)
'''
함수내부의 변수값을 계속해서 참조(외부에서 불러서 사용)하고 싶을때 사용
-> 한번 불러오고 끝이 아니라 계속해서 누적해서 값을 불러오고 싶을때 사용

1.중첩함수를 작성
2.안쪽함수에서 계산식을 사용
3. 안쪽 함수의 결과값을 밖에서 참조할 수 있도록 바깥 함수에서 결과값(=안쪽함수의 이름)
'''

# def out():
#     count = 0  # 지역변수
#     def inn():
#     #안쪽 함수에서는 밖의 함수의 지역변수값을 가져올수 없다.
#         count+=1 #count = count+1
#         return count
#     print(inn())
# out()
# UnboundLocalError: cannot access local variable 'count' where it is ~

print('===== nonlocal 선언 ======')
def out():
    count = 0  # 지역변수
    def inn():
        # nonlocal 부모의 변수를 선언해야 가져올 수 있다.
        nonlocal count  # 부모함수의 count=0을 가리킨다.
        count+=1 #count = count+1
        return count
    print(inn())
out() # 1
out() # 1 -> 새로 함수를 호출해도 count=0 초기화

print('===== nonlocal + 클로저 ======')
def outer():
    count=0
    def inner():
        #nonlocal키워드를 사용해서 변수선언
        nonlocal count 
        count+=1
        return count
    #print(inner()) -> return inner (클로저->내부함수 반환)
    return inner  #클로저->count가 저장된 주소값를 알고 있는 함수를 반환
add1 = outer() # 주소값을 전달
print('add1()=>',add1()) # 1 # add1() = inner()를 호출하는 것과 동일
print('add1()=>',add1()) # 2
print('add1()=>',add1()) # 3
print('add1()=>',add1()) # 4


#새로운 객체가 되기때문에 처음부터 다시 초기화
add2 = outer()
print('add2()=>',add2())#1

print('수량*단가 세금 결과 출력')
def outer2(tax):
    def inner2(su,dan):
        amount=su*dan*tax
        return amount
    return inner2 #내부 함수를 리턴=>클로저 함수

r = outer2(0.1)#세율 0.1
re = r(3,25000)#r->inner2를 가리킨다. 수량3,단가 25000전달
print('re=',re)#re= 7500.0 

r2 = outer2(0.05)#세율 0.05
re2 = r2(1,50000)
print('re2=',re2)#re2= 2500.0
#closure->함수형 언어에만 있다
# 람다함수, 재귀함수
