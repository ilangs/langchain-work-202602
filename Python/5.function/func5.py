# func5.py파일 작성

'''
함수의 매개변수전달2(*,**)
'''
print('\ndict타입의 자료형')
def Func3(w,h,**other):
    print(f'몸무게 {w},키 {h}') # 몸무게 65,키 175
    print(other) # {'irum': '홍길동', 'nai': 23, 'gender': '남', 'addr': '대전'} -> dic형 출력

#입력할때에는 매개변수명=값,매개변수2=값
Func3(65,175,irum='홍길동',nai=23,gender='남',addr='대전')
'''
몸무게 65,키 175
{'irum': '홍길동', 'nai': 23, 'gender': '남', 'addr': '대전'}
'''

#Func3(65,175,{'irum':'홍길동2','nai':23}) 
# -> TypeError: Func3() takes 2 positional arguments but 3 were given
# -> **매개변수 => dict형태로 출력을 하지만, dict형으로 입력(전달)하면 안됨.
Func3(75,185,irum='김길수')
'''
몸무게 75,키 185
{'irum': '김길수'}
'''

print('\n종합')
def Func4(a,b,*v1,**v2):
    print(a)
    print(b)
    print(v1) # *V1 -> () list 자료형을 받는다.
    print(v2) # **v2 -> {} dict 자료형을 받는다.

Func4(1,2)
'''
1
2
()
{}
'''
Func4(1,2,3,4,5)
'''
1
2
(3, 4, 5)
{}
'''
Func4(1,2,3,4,5,m=6,n=7)
'''
1
2
(3, 4, 5)
{'m': 6, 'n': 7}
'''
