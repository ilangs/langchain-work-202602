import React from 'react'
// 자식은 import로 불러오기
import {Header} from './Header'
import {Content} from './Content'
//추가
import { RandomNumber } from './RandomNumber'
//추가2
import { useState } from 'react'  // 괴거에는 클래스를 이용하여 생성자 함수를 통해 값 초기화
//useState(초기값)함수를 이용해서 초기값 설정

//rafce
// 전달받는 경우 ({headerTitle,,,}) =>
const App2 = ({headerTitle="기본헤더",contentTitle="기본제목",contentBody="기본본문"}) => {
//const App2 = (props) => {}
  // 상태(State)선언: [값,변경함수명] = useState(초기값)
  // 이벤트 발생
  const [count,setCount] = useState(0)  //count=count+1 문법(X)

  //추가3-1(RandomNumber에 값을 전달해서 처리해야 할 값 선언)
  const [value,setValue] = useState(0)  //RandomNumber에서 처리

  //추가3-2 자식에게 넘겨 줄 이벤트 핸들러 함수 정의
  const updateValue = (newValue) => {
    setValue(newValue)  // state 변경=> 화면에 자동으로 리렌더링 (화면에 새로 고침)
  }
  //3-3 자식에게 매개변수 없는 함수 정의
  const test = () => {
    alert("매개변수 없는 부모함수가 호출되었습니다.")
  }

  return (
    <div>
      <h1>{count}</h1>
      <button onClick={()=>setCount(count+1)}>증가</button>
      <hr />
      {/* 자식에게 상태값(number) 함수(onUndate, onTest)를 props로 전달 */}
      <RandomNumber number={value} onUpdate={updateValue} onTest={test} />
      <hr />
      <h2>{headerTitle}</h2>
      <h2>{contentTitle}</h2>
      <h2>{contentBody}</h2>
      {/* <h2>{props.headerTitle}</h2>
      <h2>{props.contentTitle}</h2>
      <h2>{props.contentBody}</h2> */}
      <Header title={headerTitle} />
      <Content title={contentTitle} body={contentBody} />
      {/* <Header title={props.headerTitle} />
      <Content title={props.contentTitle} body={props.contentBody} /> */}
      <hr />
    </div>
  )
}

export default App2































//================================================================
// rafc 
// import React from 'react'

// export const App2 = () => {
//   return (
//     <div>App2</div>
//   )
// }
// ===============================================================
// rafce
// import React from 'react'

// const App2 = () => {
//   return (
//     <div>App2</div>
//   )
// }

// export default App2
//================================================================
// rafcp 
// import React from 'react'
// import PropTypes from 'prop-types'

// const App2 = props => {
//   return (
//     <div>App2</div>
//   )
// }

// App2.propTypes = {}

// export default App2
//=================================================================