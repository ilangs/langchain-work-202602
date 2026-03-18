# ex8_list.py

'''
리스트의 특성->[]

1.순서가 있고, 0부터 시작
2.값 변경이 가능하다.
3.리스트내부에 또 다른 리스트가 들어갈 수있다.
4.중복된 데이터를 허용
5.임의의 데이터(=데이터 타입 무관)를 저장 가능 
'''
a = [1,2,3]
b = [10,a,20.5,True,'문자열']

print(a) # [1, 2, 3]
print(b) # [10, [1, 2, 3], 20.5, True, '문자열']
print(id(a),id(b)) # 주소값 출력 -> 1911973861504 1911973859584
print()

print()
busor = ['개발부', '총무부', '영업부', '관리부']
print('부서 목록 : ', busor)  # 부서 목록 :  ['개발부', '총무부', '영업부', '관리부']
print('부서 목록수 : ', len(busor)) # 부서 목록수 :  4
print(busor[2]) # 영업부

#데이터 CRUD
busor.append('영업2부')    # .append('추가대상')
busor.remove('총무부')     # .remove('삭제대상')
busor.insert(0, '총무2과') # .insert('추가대상') -> 위치 지정하여 추가
busor.extend(['개발2부', '개발3부']) # extend-> 여러 값을 동시에 추가 (리스트로 묶어서)
busor += ['영업3부'] # busor = busor + ['영업3부'] 
print(busor) # ['총무2과','개발부','영업부','관리부','영업2부','개발2부','개발3부','영업3부']

#검색 - 찾고자하는 단어 in 리스트객체명?->True|False
print('영업2부' in busor, '관리3부' in busor) # True False
print(busor.index('개발부')) # index(찾는 단어), 없으면 ValueError Traceback 

#데이터 찾기-> 슬라이싱
print('\n슬라이싱') 
aa=[1,2,3,4,5]
print(aa[1:])   # [2, 3, 4, 5] -> 인덱스번호 1 이상 끝까지 출력
print(aa[:2])   # [1, 2] -> 인덱스번호 2 미만 출력
print(aa[0:2])  # [1, 2] -> 인덱스번호 0 이상 2 미만 출력

#리스트 내부에 데이터 변경
aa=[1,2,3,['a','b','c'],4,5]
aa[0]=100;       # 1->100
print(aa)        # [100, 2, 3, ['a', 'b', 'c'], 4, 5]
print(aa[3])     # ['a','b','c']
print(aa[3][0])  # a
aa[3][0]='good'  # 'a'->'good'

print(aa)          # [100, 2, 3, ['good', 'b', 'c'], 4, 5]
print(aa[0],aa[3]) # 100 ['good','b']
print(aa[3][:2])   # ['good', 'b'] -> 인덱스번호 3번데이터 내에 인덱스번호 0이상 2미만
print(aa[3][2])    # c
