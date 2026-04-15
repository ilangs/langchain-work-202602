// react-board2/src/pages/PostList.jsx
// 게시글 목록 페이지
// - 검색, 페이지네이션, 게시글 카드 목록 표시

import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import api from "../api/axios";
import Navbar from "../components/Navbar";
import PostCard from "../components/PostCard";
import Pagination from "../components/Pagination";

export default function PostList({ user, onLogout }) {
  /**
   * @param {Object|null} user     - 전역 로그인 사용자 정보 (App.jsx에서 전달)
   * @param {Function}    onLogout - 로그아웃 처리 함수 (App.jsx에서 전달)
   */

  // =========================
  // 상태 관리
  // =========================
  const [posts, setPosts] = useState([]);          // 게시글 목록 배열
  const [total, setTotal] = useState(0);           // 전체 게시글 수 (페이지 계산용)
  const [keyword, setKeyword] = useState("");      // 검색어 입력값
  const [search, setSearch] = useState("");        // 실제 API 요청에 사용할 검색어
  const [page, setPage] = useState(1);             // 현재 페이지 번호
  const [loading, setLoading] = useState(false);   // 데이터 로딩 상태

  const SIZE = 10;  // 페이지당 게시글 수
  const totalPages = Math.ceil(total / SIZE);  // 전체 페이지 수 계산

  const navigate = useNavigate();

  // =========================
  // 게시글 목록 조회
  // =========================
  const fetchPosts = async () => {
    setLoading(true);
    try {
      // GET /posts?keyword=...&page=...&size=...
      const res = await api.get("/posts", {
        params: {
          keyword: search,  // 검색어 (빈 문자열이면 전체 조회)
          page,             // 현재 페이지
          size: SIZE        // 페이지당 게시글 수
        }
      });
      setPosts(res.data.items);  // 게시글 목록 업데이트
      setTotal(res.data.total);  // 전체 게시글 수 업데이트
    } catch (err) {
      console.error("게시글 조회 실패:", err);
    } finally {
      setLoading(false);
    }
  };

  // page 또는 search 변경 시 자동으로 목록 재조회
  useEffect(() => {
    fetchPosts();
  }, [page, search]);  // search, page가 바뀔 때마다 API 재호출

  // =========================
  // 검색 처리
  // =========================
  const handleSearch = () => {
    setPage(1);          // 검색 시 첫 페이지로 초기화
    setSearch(keyword);  // 검색어 확정 → useEffect 트리거
  };

  // Enter 키로 검색 실행
  const handleKeyDown = (e) => {
    if (e.key === "Enter") handleSearch();
  };

  // =========================
  // 렌더링
  // =========================
  return (
    <div className="min-h-screen bg-gray-100">

      {/* 공통 네비게이션 바 */}
      <Navbar user={user} onLogout={onLogout} />

      <div className="max-w-2xl mx-auto py-8 px-4">

        {/* 페이지 타이틀 */}
        <h1 className="text-2xl font-bold text-gray-800 mb-6">
          📋 게시글 목록
        </h1>

        {/* 검색 바 */}
        <div className="flex gap-2 mb-5">
          <input
            className="flex-1 border px-3 py-2 rounded-lg text-sm
                       focus:outline-none focus:ring-2 focus:ring-blue-400"
            placeholder="제목 또는 내용으로 검색..."
            value={keyword}
            onChange={(e) => setKeyword(e.target.value)}
            onKeyDown={handleKeyDown}
          />
          <button
            className="bg-blue-500 text-white px-4 py-2 rounded-lg text-sm
                       hover:bg-blue-600 transition"
            onClick={handleSearch}
          >
            검색
          </button>
          {/* 검색어 초기화 버튼 */}
          {search && (
            <button
              className="bg-gray-300 text-gray-700 px-4 py-2 rounded-lg text-sm
                         hover:bg-gray-400 transition"
              onClick={() => {
                setKeyword("");   // 입력창 초기화
                setSearch("");    // 검색어 초기화 → useEffect 트리거
                setPage(1);
              }}
            >
              초기화
            </button>
          )}
        </div>

        {/* 전체 게시글 수 표시 */}
        <p className="text-sm text-gray-400 mb-3">
          전체 <strong>{total}</strong>개의 게시글
        </p>

        {/* 게시글 목록 */}
        {loading ? (
          // 로딩 중 표시
          <div className="text-center text-gray-400 py-10">
            불러오는 중...
          </div>
        ) : posts.length === 0 ? (
          // 게시글 없음 표시
          <div className="text-center text-gray-400 py-10">
            게시글이 없습니다.
          </div>
        ) : (
          // PostCard 컴포넌트로 각 게시글 렌더링
          posts.map((post) => (
            <PostCard key={post.id} post={post} />
          ))
        )}

        {/* 페이지네이션 */}
        <Pagination
          currentPage={page}
          totalPages={totalPages}
          onPageChange={(p) => setPage(p)}  // 페이지 변경 → useEffect 트리거
        />

      </div>
    </div>
  );
}
