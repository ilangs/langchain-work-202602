import { useState } from "react";

// 커스텀 훅: 로컬 스토리지와 상태를 연결하여 브라우저를 닫아도 데이터가 유지됩니다.
import useLocalStorage from "./hooks/useLocalStorage";

// 게시글 목록을 보여주는 컴포넌트
import BoardList from "./components/BoardList";

// 게시글 작성 폼 컴포넌트
import BoardForm from "./components/BoardForm";

// 초기 데이터 (데이터가 없을 때 기본값으로 사용)
import { mockPosts } from "./data/mockPosts";

export default function App() {
  // [데이터 동기화] 'posts'라는 키로 로컬 스토리지와 상태를 연동합니다.
  // setPosts가 호출될 때마다 useLocalStorage.js 내부 로직에 의해 자동으로 저장됩니다.
  const [posts, setPosts] = useLocalStorage("posts", mockPosts);

  // [화면 전환 상태] 'list'는 목록 화면, 'form'은 작성 화면을 의미합니다.
  // 리액트 라우터 대신 사용
  const [mode, setMode] = useState("list");

  /**
   * [글 저장 핸들러]
   * 새로운 게시글 객체를 받아 전체 목록의 맨 앞에 추가합니다.
   */
  const handleSave = (newPost) => {
    // 함수형 업데이트를 통해 이전 상태(prev)에 새 글을 결합합니다.
    setPosts((prev) => [newPost, ...prev]);
    
    // 저장이 완료되면 목록 화면으로 돌아갑니다.
    setMode("list");
  };

  /* [작성 취소 핸들러] */
  const handleCancel = () => {
    setMode("list");
  };

  return (
    <div className="min-h-screen font-sans bg-gray-50/50">
      {/* 헤더 영역: 로고와 상단 버튼 구성 */}
      <header className="fixed top-0 left-0 right-0 z-50 bg-white/80 backdrop-blur-md border-b border-gray-200/50">
        <div className="max-w-6xl mx-auto px-6 py-4 flex justify-between items-center">
          {/* 로고 클릭 시 목록 화면으로 이동 */}
          <h1 
            className="text-2xl font-extrabold text-blue-600 cursor-pointer flex items-center gap-2"
            onClick={() => setMode("list")}
          >
            DASHBOARD
            <span className="text-gray-400 font-medium text-xs bg-gray-100 px-2 py-0.5 rounded-full">v1.1</span>
          </h1>

          {/* 목록 화면일 때만 '새 글 작성' 버튼을 보여줍니다. */}
          {mode === "list" && (
            <button
              className="bg-blue-600 text-white px-6 py-2.5 rounded-xl text-sm font-bold shadow-lg hover:bg-blue-700 transition-all active:scale-95"
              onClick={() => setMode("form")}
            >
              새 글 작성
            </button>
          )}

          {/* 작성 화면일 때는 '목록으로' 버튼을 보여줍니다. */}
          {mode === "form" && (
            <button
              className="text-gray-500 hover:text-blue-600 text-sm font-semibold transition-colors"
              onClick={() => setMode("list")}
            >
              ← 목록으로 돌아가기
            </button>
          )}
        </div>
      </header>

      {/* 메인 컨텐츠 영역 */}
      <main className="max-w-6xl mx-auto px-6 pt-32 pb-20">
        <div className="w-full">
          
          {/* [1. 목록 화면] posts 데이터를 넘겨주어 화면에 리스트를 렌더링합니다. */}
          {mode === "list" && (
            <BoardList posts={posts} onSelect={() => {}} />
          )}

          {/* [2. 작성 폼 화면] 저장(onSave)과 취소(onCancel) 로직을 넘겨줍니다. */}
          {mode === "form" && (
            <BoardForm 
              onSave={handleSave} 
              onCancel={handleCancel}
              editingPost={null} // 신규 작성이므로 null 전달
            />
          )}

        </div>
      </main>

      <footer className="text-center py-10 border-t border-gray-100 mt-20">
        <p className="text-gray-400 text-sm font-medium">© 2026 Board System. Sync with LocalStorage.</p>
      </footer>
    </div>
  );
}