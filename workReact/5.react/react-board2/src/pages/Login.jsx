// react-board2/src/pages/Login.jsx

import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { login } from "../api/auth";

export default function Login({ onLogin }) {

  // =========================
  // 상태 관리
  // =========================
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const [showPassword, setShowPassword] = useState(false); // 비밀번호 표시/숨김 토글

  const navigate = useNavigate();

  // =========================
  // 로그인 처리
  // =========================
  const handleLogin = async () => {
    if (!email || !password) {
      setError("이메일과 비밀번호를 모두 입력해주세요.");
      return;
    }
    setLoading(true);
    setError("");

    try {
      const data = await login(email, password);
      if (onLogin) onLogin(data.user);
      navigate("/posts");
    } catch (err) {
      setError(err.response?.data?.detail || "로그인에 실패했습니다.");
    } finally {
      setLoading(false);
    }
  };

  // Enter 키 로그인
  const handleKeyDown = (e) => {
    if (e.key === "Enter") handleLogin();
  };

  // =========================
  // 렌더링
  // =========================
  return (
    <div className="min-h-screen flex items-center justify-center
                    bg-gradient-to-br from-blue-50 via-white to-indigo-100">

      {/* 카드 컨테이너 */}
      <div className="w-full max-w-md bg-white rounded-2xl shadow-2xl overflow-hidden">

        {/* 상단 헤더 배너 */}
        <div className="bg-gradient-to-r from-blue-500 to-indigo-600 px-8 py-8 text-center">
          <div className="text-5xl mb-2">📋</div>
          <h1 className="text-2xl font-bold text-white tracking-wide">Board</h1>
          <p className="text-blue-100 text-sm mt-1">게시판에 오신 것을 환영합니다</p>
        </div>

        {/* 폼 영역 */}
        <div className="px-8 py-8">

          <h2 className="text-xl font-bold text-gray-700 mb-6 text-center">
            로그인
          </h2>

          {/* 에러 메시지 */}
          {error && (
            <div className="flex items-center gap-2 bg-red-50 border border-red-200
                            text-red-600 text-sm px-4 py-3 rounded-lg mb-5">
              <span>⚠️</span>
              <span>{error}</span>
            </div>
          )}

          {/* 이메일 입력 */}
          <div className="mb-4">
            <label className="block text-sm font-semibold text-gray-600 mb-1">
              이메일
            </label>
            <div className="relative">
              {/* 이메일 아이콘 */}
              <span className="absolute left-3 top-1/2 -translate-y-1/2 text-gray-400">
                ✉️
              </span>
              <input
                type="email"
                placeholder="example@email.com"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                onKeyDown={handleKeyDown}
                className="w-full pl-10 pr-4 py-3 border border-gray-200 rounded-xl
                           text-sm bg-gray-50 focus:bg-white
                           focus:outline-none focus:ring-2 focus:ring-blue-400
                           focus:border-transparent transition"
              />
            </div>
          </div>

          {/* 비밀번호 입력 */}
          <div className="mb-6">
            <label className="block text-sm font-semibold text-gray-600 mb-1">
              비밀번호
            </label>
            <div className="relative">
              {/* 자물쇠 아이콘 */}
              <span className="absolute left-3 top-1/2 -translate-y-1/2 text-gray-400">
                🔒
              </span>
              <input
                type={showPassword ? "text" : "password"}
                placeholder="비밀번호를 입력하세요"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                onKeyDown={handleKeyDown}
                className="w-full pl-10 pr-12 py-3 border border-gray-200 rounded-xl
                           text-sm bg-gray-50 focus:bg-white
                           focus:outline-none focus:ring-2 focus:ring-blue-400
                           focus:border-transparent transition"
              />
              {/* 비밀번호 표시/숨김 토글 버튼 */}
              <button
                type="button"
                className="absolute right-3 top-1/2 -translate-y-1/2
                           text-gray-400 hover:text-gray-600 text-sm"
                onClick={() => setShowPassword(!showPassword)}
              >
                {showPassword ? "🙈" : "👁️"}
              </button>
            </div>
          </div>

          {/* 로그인 버튼 */}
          <button
            onClick={handleLogin}
            disabled={loading}
            className={`w-full py-3 rounded-xl font-semibold text-white text-sm
                        shadow-md transition-all duration-200
                        ${loading
                          ? "bg-blue-300 cursor-not-allowed"
                          : "bg-gradient-to-r from-blue-500 to-indigo-600 hover:from-blue-600 hover:to-indigo-700 hover:shadow-lg active:scale-95"
                        }`}
          >
            {loading ? (
              <span className="flex items-center justify-center gap-2">
                <span className="animate-spin">⏳</span> 로그인 중...
              </span>
            ) : "로그인"}
          </button>

          {/* 구분선 */}
          <div className="flex items-center gap-3 my-5">
            <hr className="flex-1 border-gray-200" />
            <span className="text-xs text-gray-400">또는</span>
            <hr className="flex-1 border-gray-200" />
          </div>

          {/* 회원가입 버튼 */}
          <button
            onClick={() => navigate("/register")}
            className="w-full py-3 rounded-xl font-semibold text-blue-500 text-sm
                       border-2 border-blue-200 bg-blue-50
                       hover:bg-blue-100 hover:border-blue-400
                       transition-all duration-200 active:scale-95"
          >
            회원가입하기
          </button>

        </div>

        {/* 하단 푸터 */}
        <div className="bg-gray-50 px-8 py-4 text-center border-t border-gray-100">
          <p className="text-xs text-gray-400">
            © 2026 Board Service. All rights reserved.
          </p>
        </div>

      </div>
    </div>
  );
}
