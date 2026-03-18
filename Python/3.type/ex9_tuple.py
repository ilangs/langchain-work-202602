# ex9_tuple.py

'''
 []->리스트, ()->튜플
 1.리스트와 유사하나,읽기전용(검색)
 2.중복을 허용해준다.
 3.변수명=(값1,값2,,,)
'''
t = ('a','b','c','a')  # ('a', 'b', 'c', 'a')
print(t)
print(t,t*2,len(t))  # ('a', 'b', 'c', 'a') ('a', 'b', 'c', 'a', 'a', 'b', 'c', 'a') 4
print()
# 응용
p = (1,2,3)
print(p[1]) # 2
# p[1] = 10  => TypeError: 'tuple' object does not support item assignment (입력X 저장X)

#list로 만들어주는 함수  -> list(객체명)
#tuple로 만들어주는 함수 -> tuple(객체명)
q = list(p)
print('q의 값:',q)       # [1, 2, 3]
q[1] = 10
print('변경후 q의 값',q)  # [1, 10, 3]
p = tuple(q)            
print('tuple변경후', p)  # (1, 10, 3)
# 설정값,좌표값,함수의 반환값을 여러개 받는 경우, 값을 교환

print('\n슬라이싱')
print(p[1:])       # (10, 3)

print('\n값 교환')
t1 = (10,20) # 튜플
a,b = t1     # a=10, b=20
b,a = a,b    # 교환 (=주소값 교환)
t2 = a,b     # a=20, b=10
print(t2)    # (20, 10)
