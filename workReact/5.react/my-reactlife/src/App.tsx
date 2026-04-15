// React에서 상태(state)와 lifecycle을 관리하기 위한 Hook import
import { useState, useEffect } from "react";
import UserList from "./UserList.tsx";   // ✅ 추가1
import Timer from "./Timer.tsx";         // ✅ 추가2

// 메인 컴포넌트(App) 정의
function App() {
  // count라는 상태 변수 선언 (숫자 타입, 초기값 0) typescript
  const [count, setCount] = useState<number>(0);  // 형식) useState<자료형>(초기값)
  // show라는 상태 변수 선언 (boolean 타입, 초기값 true)
  const [show, setShow] = useState<boolean>(true);

  // ==========================
  // [1] Mount + Unmount 영역
  // ==========================

  // useEffect는 컴포넌트의 lifecycle을 제어하는 Hook, 
  // 화면에 변화가 생길때마다 자동으로 호출되는 내부함수
  useEffect(() => {
    // 컴포넌트가 처음 화면에 생성될 때 실행됨 (Mount)
    console.log("Mount");
    // return 함수는 컴포넌트가 사라질 때 실행됨 (unMount)
    return () => {
      console.log("unMount");
    };
  }, []); // [] → 의존성 배열이 비어있으면 "처음 1번만 실행"

  // ==========================
  // [2] Update 영역
  // ==========================

  // count 값이 변경될 때마다 실행되는 useEffect
  useEffect(() => {
    // 상태가 변경될 때마다 콘솔 출력
    console.log("Update:", count);
  }, [count]); // count가 바뀔 때만 실행됨

  // ==========================
  // [3] 화면(UI) 구성
  // ==========================

  return (
    // ✅ 전체 배경 + 중앙 정렬
    <div className="min-h-screen">
      
      {/* 제목 출력 */}
      <h1 >React 19 Lifecycle</h1>
        <div className="bg-blue-500 text-white text-center py-3 font-bold">
          Tailwind Working
        </div>

        {/* 현재 count 값 화면에 표시 */}
        <p>Count: {count}</p>

        {/* 버튼 클릭 시 count 증가 → 상태 변경 → Update 발생 */}
        <button onClick={() => setCount(count + 1)}>Increase /</button>
        
        {/* 버튼 클릭 시 show 값 true/false 토글 */}
        <button onClick={() => setShow(!show)}>/ Toggle</button>

        {/* show가 true일 때만 Child 컴포넌트 렌더링 */}
        {/* false가 되면 Child는 제거됨 → Unmount 발생 */}
        {show && <Child />}
        
        {/* ✅ Timer 추가 */}
        <Timer />
        <hr />
        {/* ✅ UserList 추가 */}
        <UserList />
        
    </div>
  );
}

// =====================================
// 자식 컴포넌트 정의 (Child)   <Child />
// =====================================
function Child() {

  // Child 컴포넌트의 lifecycle 관리
  useEffect(() => {
    // Child가 처음 생성될 때 실행 (Mount)
    console.log("Child Mount");
    // Child가 제거될 때 실행 (unMount)
    return () => {
      console.log("Child unMount");
    };
  }, []); // 최초 1회 실행

  // 화면에 표시될 UI
  return <div>Child Component<hr /></div>;
}

// App 컴포넌트를 외부에서 사용할 수 있도록 export
export default App;
