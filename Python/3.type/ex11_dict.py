# ex11_dict.py파일 작성

'''
dictt -> 사전형 -> 키:값으로 설정 (ex.사물함)
1. 파이썬 3.7 이후, 순서가 있다.
2. 키 => 조회(검색)
3. 형식) 변수 = dictt(키=값,,,,)
        변수 = {키:값1, 키2:값2,,,,}
'''

mydict = dict(k1=1, k2='abc', k3=3.141592)
print(mydict) # {'k1': 1, 'k2': 'abc', 'k3': 3.141592}

dict = {'파이썬':'뱀', '자바':'커피', '웹':'스프링'}
print(dict, len(dict))   # {'파이썬': '뱀', '자바': '커피', '웹': '스프링'} 3
# print(dict[0])     -> KeyError: 0      -> 인덱싱 안됨
# print(dict['커피']) -> KeyError: '커피' -> 인덱싱 안됨 

dict['데이터베이스'] = '오라클'  # 새로운 항목 추가 -> 객체명[키명] = '값'
print(dict)     # {'파이썬': '뱀', '자바': '커피', '웹': '스프링', '데이터베이스': '오라클'}

del dict['데이터베이스']   # dict의 값을 삭제-> del 객체명[삭제할 데이터의 키명]
print(dict)     # {'파이썬': '뱀', '자바': '커피', '웹': '스프링'}
 
friend = {'body':'테스트','test1':'테스트2','test2':'테스트3'}
print(friend)            # {'body':'테스트','test1':'테스트2','test2':'테스트3'}
print(friend['test1'])   # 테스트2

print(friend.keys())     # dict_keys(['body', 'test1', 'test2']) -> 키명만 출력 -> 객체명.keys()
print(friend.values())   # dict_values(['테스트', '테스트2', '테스트3']) -> 값만 출력 -> 객체명.values()

print('boy' in friend)   # False -> 찾는값 in 객체명
print('test1' in friend) # True  -> 찾는 키명 in 객체명

print()
for k in friend.keys():
    print(k, end=':')    # body:test1:test2: -> 키1:키2:키3:

print()
for k in friend.values():
    print(k, end=',')    # 테스트,테스트2,테스트3, -> 값1,값2,값3,
