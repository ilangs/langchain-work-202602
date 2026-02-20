# _02_dataBase.py

import sqlite3, os

BASE_DIR = os.path.dirname(os.path.abspath(__file__)) # c:\workAI\work\LangChain\7.FastAPI
DB_PATH = os.path.join(BASE_DIR, "test.db") 


# 연결(공통 모듈로 작성) => 함수로 작성하여 외부에서 호츨 사용
def get_db_connection(): # DB 연결 공통 함수
    conn = sqlite3.connect("test.db") #필드 구성: id, name, email
    
    # [기본값] 데이터를 튜플 형태로 반환: t=(1, "홍길동", "hong@abc.com") 
    # -> 호출 시 t[1] 처럼 인덱스를 써야 해서 필드 파악이 어렵고 불편함
    
    # [설정] row_factory를 sqlite3.Row로 설정하면 행 데이터를 딕셔너리(dict)처럼 반환
    # -> t["name"] 형식으로 컬럼명을 직접 사용하여 호출 가능하므로 가독성이 비약적으로 향상됨
    conn.row_factory = sqlite3.Row
    
    return conn 


#★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★
# 기본적으로 conn.row_factory가 지정되어 있지 않으면, 
# row["name"] 같은 접근은 불가능하고 row[0]처럼 인덱스로만 접근 가능
#★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★★

