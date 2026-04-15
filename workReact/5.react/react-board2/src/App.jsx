// react-board2/src/App.jsx
// 앱 전체 라우팅 및 전역 상태(로그인 유저) 관리

// 실무 권장 방식으로 수정: JS 메모리(변수) + Silent Refresh
// Access Token: JS 모듈 내부 변수나 React State(Zustand, Context 등)에 저장 (XSS로 털리지 않음)
// Refresh Token: 현재 백엔드 설정처럼 HttpOnly 쿠키에 저장 (JS로 접근 불가, CSRF는 SameSite 설정으로 방어)
// 새로고침(F5) 대응 (Silent Refresh): 새로고침하면 JS 메모리가 날아가므로, React 앱이 최상단에서 마운트될 때 백엔드의 /refresh 엔드포인트를 호출하여 Access Token을 다시 받아옴.


import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import { useEffect, useState } from "react";

// 페이지 컴포넌트 import
import Login from "./pages/Login";
import UserForm from "./pages/UserForm";
import PostList from "./pages/PostList";
import PostDetail from "./pages/PostDetail";
import PostForm from "./pages/PostForm";

// 공통 컴포넌트 import
import PrivateRoute from "./components/PrivateRoute";

// API 함수 import
import { refreshAccessToken, logout, getCurrentUser } from "./api/auth";

export default function App() {

  // =========================
  // 전역 상태 관리
  // =========================
  const [user, setUser] = useState(null);        // 로그인 사용자 정보
  const [loading, setLoading] = useState(true);  // 세션 복구 완료 전 로딩 상태

  // =========================
  // 앱 초기 로드 시 세션 복구 (Silent Refresh)
  // =========================
  useEffect(() => {
    const restoreSession = async () => {
      // localStorage 유저 정보로 즉시 UI 복구 (깜빡임 방지)
      const savedUser = getCurrentUser();
      if (savedUser) setUser(savedUser);

      try {
        // Refresh Token(HttpOnly 쿠키)으로 새 Access Token을 발급받아 JS 메모리에 적재
        const data = await refreshAccessToken();
        setUser(data.user);  // 서버의 최신 유저 정보로 업데이트
      } catch {
        // Refresh Token 만료 or 없음 → 비로그인 처리
        setUser(null);
        // access_token은 이제 메모리에서 관리되므로 로컬 스토리지에서 삭제할 필요가 없습니다.
        localStorage.removeItem("user");
      } finally {
        setLoading(false);  // 복구 완료 → 로딩 해제
      }
    };

    restoreSession();
  }, []);  // 최초 마운트 시 1회만 실행

  // =========================
  // 로그인 성공 처리
  // =========================
  const handleLogin = (userData) => {
    // Login.jsx에서 호출 → 전역 user 상태 업데이트
    setUser(userData);
  };

  // =========================
  // 로그아웃 처리
  // =========================
  const handleLogout = async () => {
    try {
      await logout();  // POST /logout → 서버 쿠키 삭제 + 클라이언트 메모리/로컬 초기화
    } finally {
      setUser(null);   // 전역 상태 초기화 (요청 실패해도 반드시 실행)
    }
  };

  // =========================
  // 세션 복구 중 로딩 화면
  // =========================
  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-100">
        <p className="text-gray-400 text-lg">로딩 중...</p>
      </div>
    );
  }

  // =========================
  // 라우팅
  // =========================
  return (
    <BrowserRouter>
      <Routes>

        {/* 루트 → 로그인 상태면 /posts, 아니면 /login */}
        <Route
          path="/"
          element={<Navigate to={user ? "/posts" : "/login"} replace />}
        />

        {/* 로그인 (이미 로그인 상태면 /posts로) */}
        <Route
          path="/login"
          element={
            user
              ? <Navigate to="/posts" replace />
              : <Login onLogin={handleLogin} />
          }
        />

        {/* 회원가입 (이미 로그인 상태면 /posts로) */}
        <Route
          path="/register"
          element={
            user
              ? <Navigate to="/posts" replace />
              : <UserForm />
          }
        />

        {/* 게시글 목록 (비로그인도 열람 가능) */}
        <Route
          path="/posts"
          element={<PostList user={user} onLogout={handleLogout} />}
        />

        {/* 게시글 상세 (비로그인도 열람 가능) */}
        <Route
          path="/posts/:id"
          element={<PostDetail user={user} onLogout={handleLogout} />}
        />

        {/* 게시글 작성 (로그인 필수) */}
        <Route
          path="/posts/new"
          element={
            <PrivateRoute user={user}>
              <PostForm user={user} onLogout={handleLogout} />
            </PrivateRoute>
          }
        />

        {/* 게시글 수정 (로그인 필수) */}
        <Route
          path="/posts/:id/edit"
          element={
            <PrivateRoute user={user}>
              <PostForm user={user} onLogout={handleLogout} />
            </PrivateRoute>
          }
        />

        {/* 정의되지 않은 경로 → 루트로 이동 */}
        <Route path="*" element={<Navigate to="/" replace />} />

      </Routes>
    </BrowserRouter>
  );
}
