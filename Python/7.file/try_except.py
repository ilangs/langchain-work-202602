'''
예외처리->파일처리,네트워크,DB,키보드로 입력받기(입출력)

'''
def devide(a,b):
    return a/b

print('프로그램 시작')
try:
    #예외가 나올 가능성이 있는 구문
    print('작업중')
    #c=devide(5,0)
    #파일객체=open(경로포함해서 불러올 파일명)
    f=open('c:/week/aa.txt')

#except 예외처리 클래스명:
except ZeroDivisionError:#0으로 나눈경우
    print("두번째값은 0으로 나누면 안됩니다.")

except FileNotFoundError:
    print('불러올 파일이 없습니다.')
#except Exception as 예외처리객체명:
except Exception as e:#catch(Exception e){}
    print('에러가 발생',e)#System.out.println(e)
finally:
    #DB연결해제하는 구문
    print('에러유무와 상관없이 무조건 수행')
print('프로그램 종료')
'''
프로그램 시작
작업중
불러올 파일이 없습니다.
에러유무와 상관없이 무조건 수행
프로그램 종료
'''