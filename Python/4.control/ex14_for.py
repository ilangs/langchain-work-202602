# ex14_for.py파일 작성

'''
형식) for 출력변수 in 출력대상객체(list,set,tuple,dict):
         수행문장
'''

for i in [1,2,3,4,5]:
    print(i, end=' ')  # 1 2 3 4 5
else:
    print('for문 종료') # 1 2 3 4 5 for문 종료


# 이중 for문 -> 2,3단
for n in [2,3]:
    print(f"--{n}단--")         # = print('--{}단--'.format(n))
    for i in range(1,10):       # = for i in [1,2,3,4,5,6,7,8,9]:
        print(f"{n}x{i}={n*i}") # = print('{0}*{1}={2}'.format(n,i,n*i))

'''
--2단--
2x1=2
2x2=4
2x3=6
2x4=8
2x5=10
2x6=12
2x7=14
2x8=16
2x9=18
--3단--
3x1=3
3x2=6
3x3=9
3x4=12
3x5=15
3x6=18
3x7=21
3x8=24
3x9=27
'''
