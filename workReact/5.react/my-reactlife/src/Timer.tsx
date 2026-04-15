import { useState, useEffect } from "react";

// 타이머 컴포넌트
function Timer() {

  // seconds 상태 (초단위 저장)
  const [seconds, setSeconds] = useState<number>(0);
  // ✅ 실행 상태 추가
  const [running, setRunning] = useState<boolean>(false);

  // ==========================
  // [1] Mount + unMount
  // ==========================
  useEffect(() => {

    // 실행 중일 때만 interval 생성
    if (!running) return;
    
    const interval = setInterval(() => {
      // seconds 증가 (Update 발생)
      setSeconds((prev) => prev + 1);
    }, 1000);

    // 컴포넌트가 사라질 때 실행
    return () => {
      // interval 제거 (메모리 누수 방지)-> clearInterval(초기화시킬 대상자(정보))
      clearInterval(interval); // 정리(unMount or 재실행시)
    };
  }, [running]); // ✅ running 변경 시 실행


  // ==========================
  // [2] UI 출력
  // ==========================
  return (
   <div className="p-6 mt-6 border border-gray-300 text-center">

      <h2 className="text-xl font-bold mb-2">Timer</h2>

      <p className="text-lg mb-4">Time: {seconds}s</p>

      {/* 버튼 영역 */}
      <div className="flex justify-center gap-2">

        {/* Start */}
        <button
          onClick={() => setRunning(true)}
          className="bg-blue-500 text-white px-4 py-1 rounded">
          Start
        </button>

        {/* Stop */}
        <button
          onClick={() => setRunning(false)}
          className="bg-red-500 text-white px-4 py-1 rounded">
          Stop
        </button>

        {/* Reset */}
        <button
          onClick={() => {
            setSeconds(0);
            setRunning(false);
          }}
          className="bg-gray-400 text-white px-4 py-1 rounded">
          Reset
        </button>

      </div>

    </div>
  );
}

export default Timer;
