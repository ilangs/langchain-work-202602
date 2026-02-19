'''
7.FastAPI
    └ 협업 시스템 => 유지보수 편리(기능별로 파일을 분리)
    
      DB연동 => 1.init_db.py(테이블생성->데이터를 저장(insert 구문))
               2.database.py => get_db_connection()
               3.routers/users => CRUD 작업
                        /items 
                        ,,,
               4.main.py -> routers/users 연결 구문
               
               프로젝트 구성 => 어디까지 만들 것인가? 업무분석 => 팀원 기능별로 할당
'''

#1.init_db.py

import sqlite3   # SQLite 모듈
import os        # 절대경로를 지정해서 생성된 test.db 위치 지정

# 대문자로 된 변수 => 경로저장(정적변수)
BASE_DIR = os.path.dirname(os.path.abspath(__file__)) # c:\workAI\work\LangChain\7.FastAPI
DB_PATH = os.path.join(BASE_DIR, "test.db") # ~\test.db

#DB작업 => 1.실행시킬 프로그램 가동 => Connection(연결 객체) 얻어오기
conn = sqlite3.connect(DB_PATH) # test.db 파일 이름으로 DB 생성하고 반환
print("conn=>", conn)  #conn=> <sqlite3.Connection object at 0x00000231923F5030>(=주소값)

#2.원하는 SQL 구문을 작성 => cursor 객체를 생성해야 SQL 구문을 사용할 수 있다.
cursor = conn.cursor() # 객체명.호출할 메서드명()
print('cursor=>', cursor)  #cursor=> <sqlite3.Cursor object at 0x000002557AB90C40>

# sql구문 create table 생성할 테이블명=> 제약조건 포함
cursor.execute("""
    CREATE TABLE IF NOT EXISTS users(
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      name TEXT,
      email TEXT
    )
""")

#샘플 데이터 입력
cursor.execute("INSERT INTO users (name,email) VALUES('John','john@test.com')")
cursor.execute("INSERT INTO users (name,email) VALUES('Alice','alice@gmail.com')")
cursor.execute("INSERT INTO users (name,email) VALUES('Bob','bob@msn.com')")

conn.commit()  # 저장
conn.close()   # 종료

print("DB Initialized", DB_PATH)

'''
conn=> <sqlite3.Connection object at 0x000002557A985030>
cursor=> <sqlite3.Cursor object at 0x000002557AB90C40>
DB Initialized c:\workAI\work\LangChain\7.FastAPI\test.db
'''


