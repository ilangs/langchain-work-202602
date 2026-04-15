import React from 'react'
// rafc (자식)
export const Content = (props) => {  // 1.인자로 props를 받는다.
  return (
    <div>
        {/* <h2>Content</h2>
        <p>Hey!</p> */}
        {/* 2.this없이 props.전달받은 매개변수명으로 접근 */}
        <h2>{props.title}</h2>
        <p>{props.body}</p>
    </div>
  )
}
