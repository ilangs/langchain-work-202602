# ex8_listcopy

'''
파이썬에서 리스트를 복사하는 방법은 크게 
할당(Assignment), 얕은 복사(Shallow Copy), 깊은 복사(Deep Copy)
로 나눌 수 있으며, 복사된 리스트가 원본과 메모리를 공유하는지에 따라 특징이 다릅니다.

1. 할당 (Assignment, =)
리스트 객체를 새로운 변수에 대입하는 방식입니다. 
실제 데이터를 복사하지 않고, 같은 객체의 참조(주소값)만 공유합니다. 
특징: b = a 형태. a가 변경되면 b도 변경됩니다. (같은 객체 참조)
장점: 속도가 가장 빠름.
단점: 한쪽을 변경하면 다른 쪽도 변경되는 부작용 발생. 

2. 얕은 복사 (Shallow Copy) 
리스트의 껍데기만 복사하고, 내부의 요소는 원본 리스트의 요소를 참조합니다. 
중첩 리스트(리스트 안에 리스트)가 아니라면 완전한 복사본처럼 동작합니다.
방법:
슬라이싱 ([:]): b = a[:]
copy() 메소드: b = a.copy()
list() 함수: b = list(a)
특징: 1차원 리스트는 완전 복사되지만, 2차원 이상의 중첩 리스트 내부 요소는 
참조를 공유하여 원본 수정 시 복사본도 바뀔 수 있습니다. 

3. 깊은 복사 (Deep Copy)
리스트 내부에 있는 모든 객체를 새로운 객체로 복사합니다. 
중첩 리스트 구조까지 완벽하게 분리된 복사본을 생성합니다. 
'''

import copy

# 원본 데이터 (중첩 리스트 포함: 1차원 요소와 2차원 리스트)
original = ['톰', ['제임스', '찰스']]
print(f"원본 초기 상태: {original} (ID: {id(original)})")
print("-" * 50)
'''
원본 초기 상태: ['톰', ['제임스', '찰스']] (ID: 2480210630784)
'''

# 1. 할당 (Assignment)
# 실제 복사가 일어나지 않고, 'original'과 'assignment'가 같은 메모리 주소를 가리킵니다.
assignment = original
print(f"[할당] ID 비교: {id(original)} == {id(assignment)} -> {id(original) == id(assignment)}")
'''
[할당] ID 비교: 2480210630784 == 2480210630784 -> True
'''

# 2. 얕은 복사 (Shallow Copy)
# 새로운 리스트 객체를 생성합니다. (1차원 요소는 별도, 하지만 내부 리스트는 공유)
shallow = original[:]  # 또는 original.copy()
print(f"[얕은 복사] ID 비교: {id(original)} != {id(shallow)} -> {id(original) != id(shallow)}")
print(f"[얕은 복사] 내부 리스트 ID 비교: {id(original[1])} == {id(shallow[1])} -> {id(original[1]) == id(shallow[1])}")
'''
[얕은 복사] ID 비교: 2480210630784 != 2480212262720 -> True
[얕은 복사] 내부 리스트 ID 비교: 2480210628864 == 2480210628864 -> True
'''

# 3. 깊은 복사 (Deep Copy)
# 리스트 뿐만 아니라 그 내부의 모든 객체까지 새롭게 복사합니다.
deep = copy.deepcopy(original)
print(f"[깊은 복사] ID 비교: {id(original)} != {id(deep)} -> {id(original) != id(deep)}")
print(f"[깊은 복사] 내부 리스트 ID 비교: {id(original[1])} != {id(deep[1])} -> {id(original[1]) != id(deep[1])}")
'''
[깊은 복사] ID 비교: 2480210630784 != 2480212262592 -> True
[깊은 복사] 내부 리스트 ID 비교: 2480210628864 != 2480212262656 -> True
'''

print("-" * 50)
print("데이터 변경 후 결과:")

# 원본의 1차원 요소 변경
original[0] = '수잔'
# 원본의 2차원 요소(내부 리스트) 변경
original[1][0] = '마이클'

print(f"원본(Modified): {original}")
print(f"할당(Assignment): {assignment}  <- 전부 바뀜 (완전 동기화)")
print(f"얕은 복사(Shallow): {shallow}  <- 1차원은 유지되나, 내부 리스트는 바뀜")
print(f"깊은 복사(Deep):    {deep}     <- 원본 변경에 전혀 영향받지 않음 (완전 독립)")
'''
데이터 변경 후 결과:
원본(Modified): ['수잔', ['마이클', '찰스']]
할당(Assignment): ['수잔', ['마이클', '찰스']]  <- 전부 바뀜 (완전 동기화)
얕은 복사(Shallow): ['톰', ['마이클', '찰스']]  <- 1차원은 유지되나, 내부 리스트는 바뀜
깊은 복사(Deep):    ['톰', ['제임스', '찰스']]     <- 원본 변경에 전혀 영향받지 않음 (완전 독립)
'''


print('\nList로 stack(LIFO)처리') #stack -> 한쪽은 막혀있고 반대쪽은 열려있는 상태
sbs = [10,20,30]

sbs.append(40)
print(sbs) #[10, 20, 30, 40]

sbs.pop()
print(sbs) #[10, 20, 30]

sbs.pop()
print(sbs) #[10, 20]

sbs.pop(0) #인덱스번호에 해당하는 데이터 빼낼 때
print(sbs) #[20]
