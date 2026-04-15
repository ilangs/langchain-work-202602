import React from 'react'
//rafc(자식)
//<RandomNumber number={value} onUpdate={updateValue} onTest={test} /> 
export const RandomNumber = (props) => {
    //부모의 함수를 호출해야 되는데 매개변수가 있는 경우=>자식컴포넌트에서 따로 처리해주는 함수 작성
    const handleRandomClick = () => {
       // 자신이 이벤트를 발생시켜서 자기가 작성한 함수를 통해서 부모함수를 호출
       const randomValue = Math.round(Math.random()*100) // 0~100 랜덤 정수
       props.onUpdate(randomValue)
    }

  return (
    <div>
        <h2>Random값:{props.number}</h2>
        <button onClick={handleRandomClick}>랜덤값 출력</button>
        <button onClick={props.onTest}>매개변수 없는 부모함수 호출</button>
    </div>
  )
}
