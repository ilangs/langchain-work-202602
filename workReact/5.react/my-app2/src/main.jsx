import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
// react, react-dom/client -> react 개발 사용하기 위해 필요한 라이브러리
import './index.css'  // App(메인컴포넌트)의 css 파일 불러오기
import App from './components/App' // App(메인컴포넌트)을 불러온다.
//추가
import App2 from './components/App2'

// createRoot 함수 (id가 root인 위치를 찾아서 App(메인컴포넌트)를 부착시켜주는 역할)
// 환경설정=> package.json파일에 설치 기록
createRoot(document.getElementById('root')).render(  // 화면에 보여주는 것(렌더링)
  <StrictMode>
    <App />
    {/* <컴포넌트명 전달할 매개변수명=전달할 값 /> */}
    {/* <App2 headerTitle="전달연습" 
          contentTitle="전달연습2" 
          contentBody="부모에서 자식으로 전달" /> */}
    <App2 />
  </StrictMode>,
)
