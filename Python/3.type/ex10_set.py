# ex10_set.py

'''
[] -> list , () -> tuple
{}(set()을 이용 생성) -> set -> 순서,중복된 데이터 저장 불가
형식) 변수 = {값1,값2,,,,}
'''
a = {1,2,3,1}
print(a)  # {1, 2, 3}
print(len(a)) # 3 

# 리스트1 + 리스트2 + ,,,
b = {3,4}
print(a.union(b)) # {1, 2, 3, 4} -> 합집합 
print(a.intersection(b)) # {3} -> 교집합

# a-b->차집합, a | b->union, a & b->interseciton
print(a-b, a | b, a & b) # {1, 2} {1, 2, 3, 4} {3}
# print(b[0]) # TypeError: 'set' object is not subscriptable -> set은 indexing 불가

b.update({6,7})  # 형식) set객체명.update(데이터항목)
print(b)         # {3, 4, 6, 7} -> 합집합
b.update([8,9])  # 리스트 형태로 값저장 가능
b.update((8,9))  # 튜플 형태도 가능
print(b)         # {3, 4, 6, 7, 8, 9}

b.add(10)        # 형식) set객체명.add(추가할 항목)
b.discard(7)     # set내 데이터 삭제-> .discard(삭제할 항목) -> 없어도 오류 x
b.remove(6)      # set내 데이터 삭제-> .remove(삭제할 항목) -> 없으면 오류
print(b)         # {3, 4, 8, 9, 10}

# 변수명 = set() => set, 변수명 = {} => dict, 변수명 = [] => list,
c = set()            # {} 대신에 set() -> set 타입
c = b; print(c)      # {3 ,4, 8, 9} c의 주소값 == b의 주소값 공유
c.clear(); print(c)  # 전체 지워짐

# set -> 중복된 데이터가 많은 리스트 객체에서 중복 데이터를 삭제하고자 할 때 주로 사용
li = [1,2,3,4,1,2,1,3,1,1,1,2,2,2,3,3,1,1,2,2,4] # -> [1,2,3,4] 로 만들고 싶을때
# -> set으로 변환하여 데이터 정리 후 다시 리스트로 재변환
s = set(li); print(s)   # {1,2,3,4} 
li = list(s); print(li) # [1,2,3,4]          
