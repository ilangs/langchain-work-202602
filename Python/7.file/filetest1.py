# filetest1.py

'''
파일 생성 -> 파일 저장 -> 파일 불러오기 -> file io
예외처리 => 오류가 발생할 가능성이 있는 문장이 있으면 -> try~except 구문 처리
           ㄴ 1.파일출력 2.네트워크 3.DB연동 (예외처리 필수)
'''

import os # 파일의 경로

try:
    # 불러오는 구문, 저장, 조회 (에러발생 가능성있는 구문)...
    
    # 1. 파일객체 = open('경로포함파일명','모드(r,w,rw)',encoding='utf-8') # 모드 생략시 읽기 디폴트
    current_dir = os.path.dirname(os.path.abspath(__file__))
    print('current_dir=>', current_dir) # current_dir=> c:\workAI\work\Python\7.file

    # 2. 운영체제에 맞는 구분자( \ 또는 / )를 사용하여 안전하게 경로를 합친다
    # os.path.join(기본경로, '추가경로1', '추가경로2'...): 폴더명과 파일명을 합쳐 경로로 만들기
    text_path = os.path.join(current_dir, "ftest.txt")
    print('text_path=>', text_path)
    
    f = open(text_path) # r (디폴트)
    print(f.read()) # 파일객체 출력, 라인수를 모를 경우
    f.close()       # 메모리 해제 기능 -> gabage collector
    '''
    My friend!
    Have a good time!
    hello~
    '''

    # 파일저장
    text_path2 = os.path.join(current_dir, "ftest2.txt")
    letter = open(text_path2, mode='w')
    #ascii파일로 저장(순수파일)
    letter.write('My friend2!')
    letter.write('file writing Testing...')
    letter.close()  
    print()         
    
    # 생성된 파일 불러오기
    f2 = open(text_path2)
    print(f2.readline()) # 한줄 읽을 때 -> 여러줄 읽을때 print(f2.read())
    f2.close()
    print()
    '''
    My friend2!file writing Testing...
    '''
    
    f = open(text_path)
    for a in range(3):  # 0,1,2 -> 3줄을 한줄씩 읽어서 출력
        line = f.readline()
        print(line)
    f.close()
    '''
    My friend!
    
    Have a good time!
    
    hello~
    '''
    
    # 파일의 일부분만 읽기
    print('== 부분행 읽기-슬라이싱 ==')
    f = open(text_path)
    lines = f.readlines() # readlines -> list 타입으로 읽기
    print(lines)
    '''
    == 부분행 읽기-슬라이싱 ==
    ['My friend!\n', 'Have a good time!\n', 'hello~']
    '''
    
    import sys
    #sys.stdout(출력객체)->writelines(행수)
    sys.stdout.writelines(lines[:2])#2행(0,1)
    print('=='*10)
    sys.stdout.writelines(lines[1:4])#1,2,3행
    f.close()
    '''
    My friend!
    Have a good time!
    ====================
    Have a good time!
    hello~
    '''
    
    #파일 목록 보기(경로,특정한 파일지정)
    print('\n파일 목록보기')
    import glob
    import os.path

    files = glob.glob('*') # 모든 파일의 경로
    # files = glob.glob('*.txt') # txt파일만
    # files = glob.glob('?????.txt') # 5자리파일명 가져올때 ?
    for k in files:
        print(k)
        #폴더가 존재한다면
        if os.path.isdir(k):
            print('end')
    '''
    파일 목록보기
    LangChain
    end
    memory_cached_index
    end
    Python
    end
    README.md
    requirements-e.txt
    requirements.txt
    '''

except Exception as e:      # except 예외처리클래스 as 예외객체명:
    print('파일 처리 에러 발생:',e)
