import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
// react, react-dom/client -> react 개발 사용하기 위해 필요한 라이브러리
import './index.css'  // App(메인컴포넌트)의 css 파일 불러오기
import App from './App.jsx' // App(메인컴포넌트)을 불러온다.

// createRoot 함수 (id가 root인 위치를 찾아서 App(메인컴포넌트)를 부착시켜주는 역할)
// 환경설정=> package.json파일에 설치 기록
createRoot(document.getElementById('root')).render(  // 화면에 보여주는 것(렌더링)
  <StrictMode>
    <App />
  </StrictMode>,
)
