// React에서 상태 사용을 위한 Hook import
import { useState } from "react";
// 게시글 목록 컴포넌트 import
import BoardList from "./components/BoardList";
// 테스트용 더미 데이터 import
import { mockPosts } from "./data/mockPosts";

// 메인 App 컴포넌트
export default function App() {

  // ==========================
  // [1] 게시글 상태 (mock 데이터 사용)
  // ==========================
  // mockPosts를 그대로 초기값으로 사용
  const [posts, setPosts] = useState(mockPosts);

  // ==========================
  // [2] 게시글 클릭 시 실행 함수
  // ==========================
  const handleSelect = (post) => {

    // 클릭한 게시글 콘솔 출력 (테스트용)
    console.log("선택된 게시글:", post);
  };

  // ==========================
  // [3] 화면(UI)
  // ==========================
  return (

    // 전체 화면 컨테이너  min-h-screen → 화면 높이 100%  font-sans → 기본 폰트  bg-gray-100 → 배경색
    <div className="min-h-screen font-sans bg-gray-100">

      {/* ==========================
          헤더 영역
      ========================== */}

      {/* 상단 고정 헤더 */}
      {/* fixed → 고정  top-0 left-0 right-0 → 전체 상단  z-50 → 최상단 레이어  bg-white → 흰 배경 */}
      <header className="fixed top-0 left-0 right-0 z-50 bg-white border-b">

        {/* 가운데 정렬 컨테이너 */}
        <div className="max-w-6xl mx-auto px-6 py-4 flex justify-between items-center">

          {/* 로고 */}
          {/* text-2xl → 큰 글자  font-bold → 굵게 */}
          <h1 className="text-2xl font-bold text-blue-600">
            BOARD LIST TEST
          </h1>

        </div>
      </header>

      {/* ==========================
          메인 영역
      ========================== */}
      {/* 컨텐츠 영역 */}
      {/* pt-24 → 헤더 높이만큼 여백 */}
      <main className="max-w-6xl mx-auto px-6 pt-24">

        {/* BoardList 컴포넌트 출력 */}
        <BoardList 
          posts={posts}             // 게시글 데이터 전달
          onSelect={handleSelect}   // 클릭 이벤트 전달
        />
      </main>
      {/* ==========================
          푸터 영역
      ========================== */}
      <footer className="text-center py-10 text-gray-400">
        TEST FOOTER
      </footer>
    </div>
  );
}
