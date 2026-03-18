'''
상속의 장점=>1.부모의 멤버변수와 메서드를 상속받으므로 새로 작성할 필요 없다.(소스코드 절약)
            -> cf.복붙(=>라인수 증가) ex.A 1000라인 코딩 => B 700라인(중복코딩)+신규코딩300라인
            -> 상속 ex.1000라인 그대로 상속 -> 신규 300라인만 코딩
           2.재사용성 때문에 필요 (cf.모듈작성->불러오기)
    ㄴ오버라이딩 기법(자식 입장에서 부모의 메서드의 내용만 수정해서 사용하는 기법)      
'''

class Person:  # 부모클래스 (범위가 넓음, 포괄적)
    name = ''
    age = 17

    def greeting(self):
        print('안녕하세요')
# is a 관계->상속   p(자식)->q(부모)(o)  q(부모)->p(자식)(x) 
# class Employee(직원,부모) -> class Manager(팀장,자식) => 팀장은 직원이다(o) 직원은 팀장이다(x)


class Student(Person):  # 형식) class 자식클래스(부모클래스) 
    def study(self):
        print('열심히 공부하기')

james = Student()
james.name = '제임스'
print(james.name, james.age) # 제임스 17
james.study()    # 열심히 공부하기 => 자기 클래스 호출
james.greeting() # 안녕하세요 => 부모로부터 물려받은 클래스 호출


class Student2(Person):  # 형식) class 자식클래스(부모클래스) 
    # 오버라이딩->부모로부터 상속받은 메서드의 내용을 자식클래스에 맞게 내용을 수정.
    def greeting(self):
        print('반갑습니다. 제임스라고 합니다.')

james = Student2()
james.name = '제임스'
print(james.name, james.age) # 제임스 17
james.greeting() # 반갑습니다. 제임스라고 합니다. => 오버라이딩 자기 클래스 호출
