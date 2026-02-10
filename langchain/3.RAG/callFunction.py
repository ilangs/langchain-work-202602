"""
공통 import 및 환경 설정 모듈
 이 파일을 import 하시면 
 1) .env 파일 자동 로드
 2) 공통 라이브러리 import: 필요한 클래스들을 함께 가져올 수 있음
"""

# ===== 환경 변수 로드 =====
from dotenv import load_dotenv
load_dotenv()

# ===== 공통 라이브러리 import =====
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, PromptTemplate
from langchain_core.output_parsers import StrOutputParser
