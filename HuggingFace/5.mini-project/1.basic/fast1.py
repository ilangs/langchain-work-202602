# 1.basic\fast1.py파일 작성

from fastapi import FastAPI, Request 
from fastapi.responses import HTMLResponse # 응답(html로 전송)
from fastapi.templating import Jinja2Templates # 서버의 요청을 받아서 html에 전송 해주는 엔진

app = FastAPI()

import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__)) # 절대경로
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates")) #디렉토리 지정

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    # 템플릿에 전달할 데이터
    context = {
        "request": request,                            # 요청 객체
        "name": "홍길동",                               # {{ name }}
        "movies": ["인셉션", "인터스텔라", "다크 나이트"]  # {% for movie in movies %}
    }
    # index.html이 있는 위치 (1.이동할 페이지명, 이동할 페이지에게 전달할 값)
    return templates.TemplateResponse("index.html", context)

# uvicorn으로 자동 실행되도록 추가
if __name__ == "__main__":
    import uvicorn
    # host와 port를 지정해서 실행
    uvicorn.run("fast1:app", host="127.0.0.1", port=8000, reload=True)
