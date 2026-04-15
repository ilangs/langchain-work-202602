// react-board2/src/components/Navbar.jsx
// 모든 페이지 상단에 표시되는 공통 네비게이션 바
// - 로그인 상태: 닉네임 + 로그아웃 버튼 표시
// - 비로그인 상태: 로그인/회원가입 버튼 표시

import { useNavigate } from "react-router-dom";

export default function Navbar({ user, onLogout }) {
  /**
   * @param {Object|null} user     - 전역 로그인 사용자 정보 (App.jsx에서 전달)
   * @param {Function}    onLogout - 로그아웃 처리 함수 (App.jsx에서 전달)
   */
  const navigate = useNavigate();

  return (
    <nav className="bg-white shadow-md px-6 py-3 flex items-center justify-between">

      {/* 로고 (클릭 시 게시글 목록으로 이동) */}
      <span
        className="text-xl font-bold text-blue-500 cursor-pointer"
        onClick={() => navigate("/posts")}
      >
        📋 Board
      </span>

      {/* 우측 메뉴 */}
      <div className="flex items-center gap-3">
        {user ? (
          // 로그인 상태: 닉네임 + 게시글 작성 + 로그아웃
          <>
            {/* 로그인된 사용자 닉네임 표시 */}
            <span className="text-sm text-gray-600">
              👤 <strong>{user.nickname}</strong> 님
            </span>

            {/* 게시글 작성 버튼 */}
            <button
              className="text-sm bg-blue-500 text-white px-3 py-1 rounded hover:bg-blue-600 transition"
              onClick={() => navigate("/posts/new")}
            >
              글쓰기
            </button>

            {/* 로그아웃 버튼 */}
            <button
              className="text-sm bg-gray-200 text-gray-700 px-3 py-1 rounded hover:bg-gray-300 transition"
              onClick={onLogout}  // App.jsx의 handleLogout 호출
            >
              로그아웃
            </button>
          </>
        ) : (
          // 비로그인 상태: 로그인 + 회원가입 버튼
          <>
            <button
              className="text-sm text-blue-500 hover:underline"
              onClick={() => navigate("/login")}
            >
              로그인
            </button>

            <button
              className="text-sm bg-blue-500 text-white px-3 py-1 rounded hover:bg-blue-600 transition"
              onClick={() => navigate("/register")}
            >
              회원가입
            </button>
          </>
        )}
      </div>
    </nav>
  );
}
