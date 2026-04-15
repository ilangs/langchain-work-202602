// import { useState } from 'react'
// import reactLogo from './assets/react.svg'
// import viteLogo from './assets/vite.svg'
// import heroImg from './assets/hero.png'
import '../App.css' // App.jsx에서 css 파일을 불러오기 위해서 경로 재설정

// 컴포넌트 작성 -> 1.클래스 상속(구식)  2.함수로 작성(업계 표준)

function App() {
  
  // 규칙2.변수는 함수 내부에 선언, 화면디자인 태그 내부에 {변수명} 형식으로 사용
  let text = "react 환경설정 연습 중..."
  // 규칙3.스타일 적용(camelCase), 화면디자인 태그 내부에 style={객체명} 형식으로 사용
  let pStyle = {
    color: 'aqua',
    backgroundColor: 'black'
  }
  // 규칙4.복잡한 디자인은 ~.css파일 만들어서 className="클래스명" 호출
  // 규칙5.if조건식 사용불가->삼항연산자, 태그 내부에 형식)조건식?'True값':'False값' 사용
  const num = 1
  // 규칙6.주석 ctrl+/ -> 화면디자인 태그 내부는 {/* ... */} or { 줄바꿈 //... 줄바꿈 } 형식
  // 규칙7.이벤트 처리 -> 화면디자인 태그 내부는 {함수명} 형식 호출, 함수명 뒤 ()는 자동호출(삭제)
  // sayHello(){...}
  const sayHello = () => {
    alert('이벤트 연습중...')
  } 
  return ( // 규칙1.화면디자인은 하나의 부모 태그로 묶어줄 것. ex.<div>...</div>, <span>...</span>
   <div>
      {/* JSX 주석 */}
      {
      // 한줄 주석
      }
      <h2 className="App">첫번째 방식으로 react 예제를 작성중, {text}</h2>
      <h2 className="App-title">리액트 문법 연습 중 ...</h2>
      <p style={pStyle}>스타일 적용연습1</p>
      {/* <p style={pStyle}>{1===1?'True':'False'}</p> */}
      <p style={pStyle}>{num===1?'True':'False'}</p>
      {/* <button onclick={sayHello()}>버튼 클릭</button>-> onClick 카멜타입,함수명 뒤 ()삭제 */}
      <button onClick={sayHello}>버튼 클릭</button>
   </div>
  )
}
// return (화면 디자인)
export default App
// export default App => export default 컴포넌트명 => main.jsx에서 import x