// React Hook import (상태관리, 생명주기)
import { useEffect, useState } from "react";

// 컴포넌트 import
import BoardList from "./components/BoardList";
import BoardForm from "./components/BoardForm";

const API_URL = "http://localhost:8000/posts";

function App() {

  // =========================
  // [1] 상태 관리
  // =========================

  const [posts, setPosts] = useState([]);     // 전체 게시글
  const [keyword, setKeyword] = useState(""); // 검색어
  const [page, setPage] = useState(1);        // 현재 페이지

  const limit = 5; // 한 페이지당 게시글 수

  // =========================
  // [2] 게시글 전체 조회 (select * from posts)
  // =========================
  const fetchPosts = async () => {
    try {
      const res = await fetch(API_URL);  // API 호출
      if (!res.ok) throw new Error("서버 응답 오류");
      const data = await res.json();     // JSON 변환
      setPosts(data);                    // 상태 저장
    } catch (err) {
      console.error("데이터 로딩 실패:", err);
    }
  };

  // =========================
  // [3] 검색 기능
  // =========================
  const handleSearch = async () => {
    // 검색어가 없으면 전체 게시글을 다시 불러옵니다.
    if (!keyword.trim()) {
      fetchPosts();
      return;
    }

    try {
      // json-server 기준 전체 필드 검색 (?q=키워드)
      const res = await fetch(`${API_URL}?q=${keyword}`);
      if (!res.ok) throw new Error("검색 실패");
      
      const data = await res.json();
      setPosts(data);                // 검색 결과로 posts 상태 업데이트
      setPage(1);                    // 검색 후 결과가 줄어드므로 페이지를 1페이지로 리셋
    } catch (error) {
      console.error("Error searching posts:", error);
      alert("검색 중 오류가 발생했습니다.");
    }
  };

  // =========================
  // [4] 페이지네이션 처리
  // =========================
  const start = (page - 1) * limit;                       // 시작 index
  const currentPosts = posts.slice(start, start + limit); // 현재 페이지 데이터

  // =========================
  // [5] 최초 실행
  // =========================
  useEffect(() => {
    fetchPosts(); // 첫 로딩 시 실행
  }, []);

  return (
    <div className="min-h-screen bg-gray-100 p-6">

      {/* 제목 */}
      <h1 className="text-3xl font-bold text-center mb-6">
        📋 게시판
      </h1>

      {/* =========================
          [검색 영역]
      ========================= */}
      <div className="flex justify-center mb-6 space-x-2">
        
        {/* 검색 입력 */}
        <input
          className="border px-4 py-2 rounded w-64"
          value={keyword}
          onChange={(e) => setKeyword(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && handleSearch()} // 엔터키 감지
          placeholder="검색어 입력"
        />

        {/* 검색 버튼 */}
        <button
          className="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600"
          onClick={handleSearch}
        >
          검색
        </button>

        {/* 전체보기 */}
        <button
          className="bg-gray-500 text-white px-4 py-2 rounded hover:bg-gray-600"
          onClick={fetchPosts}
        >
          전체보기
        </button>
      </div>

      {/* 글쓰기 폼 */}
      <BoardForm fetchPosts={fetchPosts} />

      {/* 목록 */}
      {posts.length === 0 ? (
        <div className="text-center py-10 text-gray-500">게시글이 없습니다.</div>
      ) : (
        <BoardList posts={currentPosts} fetchPosts={fetchPosts} />
      )}

      {/* =========================
          [페이지네이션]
      ========================= */}
      <div className="flex justify-center mt-6 space-x-2">
        {Array.from({ length: Math.ceil(posts.length / limit) }).map((_, i) => (
          <button
            key={i}
            onClick={() => setPage(i + 1)}
            className={`px-3 py-1 border rounded 
              ${page === i + 1 ? "bg-blue-500 text-white" : "bg-white"}`}
          >
            {i + 1}
          </button>
        ))}
      </div>

    </div>
  );
}

export default App;