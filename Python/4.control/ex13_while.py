# ex13_while.py 파일 작성

'''
반복문 -> 반복해서 수행이 되는 구문들
형식) while 조건식: 조건이 참인 동안에만 계속 실행 -> 거짓이면 한번도 실행이 안될 수도 있다.
          참인 명령어
          참인 명령어2
'''

a = 1
while a <= 5: # 무한 루프 명령어 while True:
    print(a, end=' ')
    a += 1  # 이 부분이 없으면 무한루프
print('\na:',a)

'''
1 2 3 4 5 
a: 6
'''

# 이중 while문 -> 제어문내에 또 다른 제어문 => 중첨 제어문(=이중 제어문)
i = 1
while i <= 3:
    j = 1
    while j <= 4:
        print('i='+str(i)+' | j='+str(j))
        j += 1
    print()  
    i += 1
print('while 구문 종료')

'''
i=1 | j=1
i=1 | j=2
i=1 | j=3
i=1 | j=4

i=2 | j=1
i=2 | j=2
i=2 | j=3
i=2 | j=4

i=3 | j=1
i=3 | j=2
i=3 | j=3
i=3 | j=4

while구문 종료
'''

# 1~100 합계 구하기 => hap(합계), i(반복횟수) -> 2개의 변수 필요
i = 1 ; hap = 0
while i <= 100:
    hap += i  # hap = hap+i = 1+2+3+4+,,,+100
    i += 1
print('합은 '+str(hap))  # 합은 5050

# 1~100사이에서 3의 배수 숫자들의 합 출력
j = 1 ; hap3 = 0
while j <= 100:
    # 3의 배수인 경우에만 합산
    if j%3 == 0:
        hap3 += j  # hap = hap+i = 3+6+9+15+,,,+99
    j += 1
print('3의 배수의 합은 '+str(hap3)) # 3의 배수의 합은 1683

'''
while True,continue,break
continue->skip->조건에 만족->skip
break->특정조건에 만족하면 루프 탈출
'''
a = 0
while a < 10:
    a += 1
    if a == 5: continue  # 하나 skip
    if a == 7: break     # 무조건 탈출
    print(a, end=' ')

'''
1 2 3 4 6 
'''

#짝수,홀수판별->무한루프
while True:
    a=int(input("확인할 숫자를 입력하세요?"))
    if a==0:
        print('프로그램 종료')
        break
    elif a%2==0:
        print('%d는 짝수'%(a))
    print('aaa') 
'''
확인할 숫자를 입력하세요? 34
34는 짝수
aaa
확인할 숫자를 입력하세요? 0
프로그램 종료
'''
