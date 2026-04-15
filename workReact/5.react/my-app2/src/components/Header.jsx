import React from 'react'

// 외부에서 불러올때 {Header}를 사용해야 한다.
// 전달 받는 방법1 => export const Header = ({title}) => { 
// 전달 받는 방법2 => 여러개를 동시에 전달 => props에서 구분해서 출력한다.

export const Header = (props) => {
  return (
    <div>
        {/* <h1>Header</h1> */}
        <h1>{props.title}</h1>
    </div>
  )
}
