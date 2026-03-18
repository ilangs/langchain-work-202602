#class4_has.py
'''
프로그램을 작성 => 클래스 한개이상 작성->각 클래스와의 관계설정=>
1.has a 관계(=포함관계) ->한개이상의 클래스들이 연결(=결합)
2.is a 관계 => 상속

요구분석=>냉장고(class)에 음식(class)을 넣고 보관
'''

class Fridge:#주
    #1.공통으로 가질만한 속성,상태를 저장
    isOpened = False #닫혀있는 상태
    foods = [] #음식을 넣을 저장소
    
    #냉장고 문 열기=>단순,반복 매개변수X 반환값X
    def open(self):#매개변수가 없는것으로 간주
        self.isOpened = True #fri.isOpened = True
        print('냉장고 문을 열어놓음!!')
    
    #음식을 넣기->자동으로 지금까지 넣어준 음식 목록 보기(매개변수 O ,반환값X)
    def put(self,thing):
        if self.isOpened: #생략 True
            self.foods.append(thing)
            print('냉장고 속에 음식을 넣었음.')
            self.list()#자기 클래스내의 다른 메서드호출할 경우 self.호출할 메서드명(~)
        else:
            print('냉장고 문이 닫혀서 음식을 넣을수 없는 상태입니다.')
            
    #냉장고 문 닫기->단순,반복
    def close(self):
        self.isOpened = False
        print('냉장고 문을 닫아놓음!!')
        
    #냉장고의 내용을 출력(확인)
    def list(self):# 매개변수X  받아서 전달X ==>반환값 O
        for f in self.foods:# ['a','b',,,]
            print('-',f.irum,f.expiry_date)
        print()#꺼낸음식사이의 줄바꿈(거리를 두자)

class FoodData:#부(음식이름,유통기한,,,)
    def __init__(self,irum,expiry_date):
        self.irum = irum #동적으로 멤버변수 추가
        self.expiry_date=expiry_date
        
#결과
fri = Fridge()
print()
apple = FoodData('사과','2026-3-15')
fri.open()
fri.put(apple)
fri.close()

cola = FoodData('콜라','2026-3-30')
fri.open()
fri.put(cola)
fri.close()
print('\n 음식물 확인')
print(fri.foods)#객체명.속성명=값 <-->객체명.속성명

'''
냉장고 문을 닫아놓음!!
냉장고 문을 열어놓음!!
냉장고 속에 음식을 넣었음.
- 사과 2026-3-15
- 콜라 2026-3-30

냉장고 문을 닫아놓음!!

 음식물 확인
[<__main__.FoodData object at 0x000001F86C4E3BE0>, <__main__.FoodData object at 0x000001F86C4E3B50>]
'''
