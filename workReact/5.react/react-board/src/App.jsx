// 2. App.jsx (화면 전환의 컨트롤러)

import { useState } from "react"; // React 상태 관리 훅
import useLocalStorage from "./hooks/useLocalStorage"; // 로컬 스토리지 연동 커스텀 훅
import BoardList from "./components/BoardList"; // 게시글 목록 컴포넌트
import BoardForm from "./components/BoardForm"; // 게시글 작성/수정 폼 컴포넌트
//
import BoardDetail from "./components/BoardDetail"; // [추가] 게시글 상세보기 컴포넌트 임포트
//
import { mockPosts } from "./data/mockPosts"; // 초기 테스트 데이터

export default function App() {
  // 로컬 스토리지와 동기화된 게시글 데이터 상태
  const [posts, setPosts] = useLocalStorage("posts", mockPosts);
  
  // 현재 화면 모드 관리 ('list', 'form', 'detail') -> 화면 전환
  const [mode, setMode] = useState("list");
  
  // [변경] 선택된 게시글 상태 (상세보기 및 수정시 사용)
  const [selectedPost, setSelectedPost] = useState(null); // 객체의 초기화

  // [추가] 게시글 삭제 처리 함수
  const handleDelete = (id) => {
    // if (window.confirm("정말로 삭제하시겠습니까?")) { // 삭제 확인 창
      setPosts((prev) => prev.filter((p) => p.id !== id)); // 해당 ID만 제외하고 필터링
      setMode("list"); // 삭제 후 목록으로 이동
      setSelectedPost(null); // 선택 상태 초기화
    // }
  };

  // 게시글 저장 처리 함수
  const handleSave = (newPost) => {
    setPosts((prev) => {
      // 기존 데이터 수정인지 찾기 (p.id(기존 글의 id)와 newPost.id(신규글의 id) 대조)
      const exists = prev.find((p) => p.id === newPost.id);
      // ID가 존재하면 해당 항목 교체
      if (exists) {
        return prev.map((p) => (p.id === newPost.id ? newPost : p));
      }
      // 배열 맨 앞에 추가
      return [newPost, ...prev]; // 신규글은 맨 앞에 배치
    });

    setMode("list"); // 저장 완료 후 목록화면으로 전환
    setSelectedPost(null); // 수정,신규글 작성 후 상태 초기화
  };

  // 댓글 기능 함수
  const handleUpdateComments = (postId, newComments) => {
    setPosts((prev) =>
      prev.map((p) => (p.id === postId ? { ...p, comments: newComments } : p))
    );
  };

  // 목록으로 돌아가기 (초기화)
  const goToList = () => {
    setMode("list");       // 글쓰기나 글쓰기 취소
    setSelectedPost(null); // 수정,삭제를 취소 -> 글목록으로 가기(= not 글상세보기)
  };

  // 화면(UI)
  return (
    <div className="min-h-screen bg-gray-50 text-gray-800">
      {/* 상단 네비게이션 헤더 */}
      <header className="bg-white border-b border-gray-200 sticky top-0 z-50 shadow-sm">
        <div className="max-w-4xl mx-auto px-6 py-3 flex justify-between items-center">
          <h1 
            className="text-xl font-black text-blue-600 cursor-pointer tracking-tighter"
            // onClick={() => setMode("list")} -> 익명함수형태
            onClick={goToList} // 함수형태
          >
            DASHBOARD<span className="text-gray-400 font-normal ml-1 text-sm">v1.0</span>
          </h1>

          <button
            className={`px-5 py-2 rounded-lg text-sm font-bold transition-all active:scale-95 ${
              mode === "list" 
              ? "bg-blue-600 text-white hover:bg-blue-700 shadow-md shadow-blue-100" 
              : "bg-gray-100 text-gray-600 hover:bg-gray-200"
            }`}
            onClick={() => {
              if (mode === "list") { setMode("form"); setSelectedPost(null); }
              else goToList();
            }}
          >
            {mode === "list" ? "+ 새 글 작성" : "목록으로 돌아가기"}
          </button>
        </div>
      </header>

      {/* 메인 콘텐츠 영역 */}
      <main className="max-w-4xl mx-auto px-4 py-10 flex justify-center">
        <div className="w-full transition-all duration-500">
          
          {/* 1. 목록 화면 모드 - posts 데이터를 넘겨주어 화면에 리스트를 렌더링합니다. */}
          {mode === "list" && (
            <BoardList posts={posts}
                       onSelect={(post) => {
                        setSelectedPost(post); // [추가] 클릭한 게시글 저장
                        setMode("detail");     // [추가] 상세 보기 모드로 전환(list<->detail)
                       }} 
            />
          )}

          {/* [추가] 2. 상세 보기 화면 모드 */}
          {mode === "detail" && (
            <BoardDetail post={selectedPost}  // 현재 선택된 데이터 전달
                         onBack={goToList}    // 뒤로가기 시 목록으로
                         onEdit={() => setMode("form")} // 수정 버튼 클릭시 폼으로 전환
                         onDelete={() => handleDelete(selectedPost.id)} // 삭제 실행
                         onUpdateComments={handleUpdateComments} // 댓글 기능 추가
            />
          )}

          {/* 3. 작성 및 수정 폼 화면 모드 */}
          {mode === "form" && (
            <BoardForm onSave={handleSave}        // 신규글과 수정폼의 공통함수 
                       editingPost={selectedPost} // [변경] 수정폼에 selectedPost를 전달
                       onCancel={goToList} 
            />
          )}

        </div>
      </main>

      <footer className="text-center text-gray-400 text-xs py-10">
        © 2026 Admin Dashboard. All rights reserved.
      </footer>
    </div>
  );
}
