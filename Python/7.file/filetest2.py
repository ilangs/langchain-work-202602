# filetest2.py파일 작성

'''
파일에 복합객체 저장 가능 (리스트,셋,튜플,클래스,,) -> 텍스트+객체도 저장 가능

'''
import os

try:
    #파일객체명=open(경로파일명,모드,encoding정보)
    #with open(경로파일명,모드,encoding정보) as 파일객체명
    current_dir = os.path.dirname(os.path.abspath(__file__)) # ~7.file
    text_path = os.path.join(current_dir, "ftest3.txt") 

    #with open('ftest3.txt',mode='w',encoding='utf-8') as f:
    with open(text_path,mode='w',encoding='utf-8') as f:
        f.write('파이썬 파일 연습중')
        f.write('\n파이썬 파일쓰기1')
        f.write('\n파이썬 읽기연습')
        f.write('\n파이썬 한글연습')
        #f.close()->암묵적으로 실행(자동)
    
    with open(text_path, mode='r', encoding='utf-8') as f2:
        print(f2.read())
    print('\n파일명(복합객체처리)')
    
    import pickle #임의의 객체를 파일로 저장 -> pickle파일이용(ObjectOutputStream)
    #binary형태로 저장(wb)
    pickle_path = os.path.join(current_dir,"test.pickle")
    with open(pickle_path,'wb') as f3:
        phones = {'tom':'02-123-0987','길동':'02-222-2333'}
        li = ['마우스','키보드']
        t = (phones,li) #여러 종류의 객체를 모아놓은 객체(=복합객체)
        #dump(출력대상객체명,파일객체)=>객체를 파일로 저장-> 옮길수 있는 상태(=객체 직렬화)(USB에 저장)
        pickle.dump(t,f3)  #튜플을 f3에 저장(test.pickle)
        pickle.dump(li,f3) #list객체 저장 가능

    print('\n 이진파일 불러오기')
    with open(pickle_path,'rb') as f4:
        a,b = pickle.load(f4) #pickle(모듈명).load(불러올 파일명)
        #a->phones, b->li
        c = pickle.load(f4)
        print(a) #t
        print(b) #li
        print(c) #li만
        '''
        {'tom': '02-123-0987', '길동': '02-222-2333'} -> a
        ['마우스', '키보드']                           -> b
        ['마우스', '키보드']                           -> c
        '''
    
    #파이썬의 클래스를 통해서 만든 객체도 저장 가능? y
    print('\n 작업중인 클래스 객체 저장 가능 ?')
    class Hello:
        irum = 'tom'
    h = Hello()    #데이터 저장 목적
    h.mesg = 'Hi' #동적으로 멤버변수 추가
    #pickle객체생성->저장->불러오기
    pickle_path2 = os.path.join(current_dir, "test2.pickle")
    with open(pickle_path2,'wb') as f5: 
        pickle.dump(h,f5) # 클래스 객체도 저장 가능

    print('\n 클래스의 객체 내용 불러오기')
    with open(pickle_path2,'rb') as f5:
        h1 = pickle.load(f5) #pickle(모듈명).load(불러올 파일명)
    print('h1.irum=>',h1.irum,'h1.mesg=>',h1.mesg)
    '''
     클래스의 객체 내용 불러오기
    h1.irum=> tom h1.mesg=> Hi
    '''

except Exception as e:
    print('실행에러=>',e)
