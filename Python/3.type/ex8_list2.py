# ex8_list2.py

'''
리스트를 가지고 계산(제어문 for문을 배우고 나서 실습)
'''
chars = [] #리스트 객체 chars생성됨
seq = '대한 민국은 korea'
#반복문->for문
#->for 출력변수명 in 컬렉션객체(배열):
for k in seq:
    #print(k,end=' ')#중간에 공백을 주면서출력
    chars.append(k)
    #print(chars)
print(chars)

#성적표 출력
print('\n성적표 출력')
tom = [90,85,70]
james = [100,100,100]
charles = [99,98,97]

students = [tom,james,charles]#중첩리스트
name = ['톰','제임스','찰스']

for score in students:
    print(score)

#총점,평균출력
i = 0 #내부적인 인덱스번호
for score in students:#학생 구분
    total = 0
    for s in score:#tome
        total+=s#90,85,70
    ave = total/3
    print('{0}=>총점:{1},평균:{2}'.
          format(name[i],total,round(ave)))
    i+=1

print(tom+james+charles)#합친 리스트가 된다
print(tom*3)#톰의 데이터만 3번 반복해서 저장
    
'''
성적표 출력
[90, 85, 70]
[100, 100, 100]
[99, 98, 97]
톰=>총점:245,평균:82
제임스=>총점:300,평균:100
찰스=>총점:294,평균:98
[90, 85, 70, 100, 100, 100, 99, 98, 97]
[90, 85, 70, 90, 85, 70, 90, 85, 70]
'''

    



    