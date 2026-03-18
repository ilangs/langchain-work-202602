# ex6_op.py파일 작성

'''
연산자
'''
print('\n산술연산자',end=':')  # 나누기->정밀한값(/) 몫->// 나머지->% , 5*3->5*5*5
print(5+2,5-2,5*2,5/2,5//2,5%2,5**2) # 7 3 10 2.5 2 1 25

print('나누기에서 몫과 나머지를 구하기')
print(divmod(5,2)) #(2,1) 
print('연산자 우선순위:',3+4*5,(3+4)*5) #연산자 우선순위: 23 35

print('\n관계연산자(대소비교)',end=':')
print(5>3,5==3,5!=3,5<=3) # True False True False

print('\n논리연산자',end=':') # ->true,false 리턴값
print(5>3 and 4<3,5>3 or 4<3,not(5>=3)) # False True False

print('\n문자열 더하기',end=':')  # 다른 랭귀지: 단일문자열-홑따옴표, 다중문자열-겹따옴표
print('테'+'스'+"트연습") # 테스트연습
print('테스트,'*10)   # 특정 문자열*반복횟수

print('\n누적(배정연산자)')
#a=a+1 -> a+=1
#a++,++a, a-- 등 파이썬에서는 증감연산자가 없다.
a = 10
a = a+1 # 11 
a+=1    # 12 속도가 빠름
print(a) # => 12

print('\n부호변경', a, a*-1, -a, --a) # 12 -12 -12 12  ->  -(-12)

print('\nboolean처리',bool(0),bool(1),bool(2),bool(3),bool(None),bool(''))  
# => False True True True False False
# 0->False, 0이외에는->True, None->False, 공백->False


