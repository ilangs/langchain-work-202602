# class3_student.py=>생성자 추가
'''
생성자
1. 파이썬에서 객체를 생성할 때 저동으로 호출되는 특수한 메서드 -> 임의 호츨X
   => ex.카드결재o => 폰(카드내역)o 객체생성x => 호출불가
2. 생성자명=>__init__.py(self)
3. 생성자의 기능=>데이터의 저장을 위한 초기값 설정(=처음에 저장할 값)
'''
class Student:
    old=-1 # 나이=>설계상으로 만든 멤버변수(=속성)
    # name => 정적
    # 생성자
    def __init__(self,name,old=17):#Student(name,old)
        # this.old = old
        self.name=name # 동적으로 멤버변수 추가 가능
        self.old=old
    # 저장된 멤버변수값 가져오기
    def print_name(self):
        # public void print_name()->java
        print(self.name) # s.name

    def print_old(self):
        print(self.old) # self.멤버변수->self생략X
# 객체생성->자동적으로 생성자호출
s = Student("철수")#self->s(현재 생성된 객체)
#원형클래스에서 함수호출(매개변수로 객체 전달)
Student.print_name(s)#unbound method call=>철수
s.print_name()#bound method call->철수

print('철수의 나이는',s.old)#철수의 나이는 17
print('학생의 이름은',s.name)#학생의 이름은 철수

'''
철수
철수
철수의 나이는 17
학생의 이름은 철수
'''
