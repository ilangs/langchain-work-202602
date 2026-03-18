# class6_inheritnace.py
'''
다중상속=>동시에 한개 이상의 부모클래스로부터 상속을 받는 경우 (ex.외모+성격)
'''

class Person: #부모(포괄적)
    name = ''
    age = 17

    def greeting(self):
        print('안녕하세요')

# 부모클래스 추가
class University:
    def manage_credit(self):
        print('학점관리')  

    def greeting(self):
        print('반가워요')   

# 형식) class 자식클래스(부모1,부모2)
class Student(Person,University): # 안녕하세요
# class Student(University,Person): # 반가워요 
# -> 다중상속에서 동일 메서드가 있으면 먼저 상속받은 클래스 우선
    def study(self):
        print('열심히 공부하기')

james = Student()
james.name = '제임스'
print(james.name,james.age) # 제임스 17
james.greeting()      # 안녕하세요 => person 클래스 호출 
# -> 다중상속에서 동일 메서드가 있으면 먼저 상속받은 클래스 우선
james.study()         # 열심히 공부하기 => 자기 클래스 호출
james.manage_credit() # 학점 관리 => University 클래스 호출
