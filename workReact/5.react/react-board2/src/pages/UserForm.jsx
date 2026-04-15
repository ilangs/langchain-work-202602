// react-board2/src/pages/UserForm.jsx

import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { register } from "../api/auth";

export default function UserForm() {

  // =========================
  // 상태 관리
  // =========================
  const [form, setForm] = useState({
    email: "",
    password: "",
    nickname: "",
    name: "",
    address: "",
    phone: "",
  });
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");
  const [loading, setLoading] = useState(false);
  const [showPassword, setShowPassword] = useState(false);

  // 각 필드의 아이콘과 라벨 정의 (반복 렌더링에 활용)
  const fields = [
    { key: "email",    label: "이메일",   icon: "✉️",  type: "email",    placeholder: "example@email.com" },
    { key: "password", label: "비밀번호", icon: "🔒",  type: "password", placeholder: "6자 이상 입력하세요" },
    { key: "nickname", label: "닉네임",   icon: "😊",  type: "text",     placeholder: "사용할 닉네임" },
    { key: "name",     label: "이름",     icon: "👤",  type: "text",     placeholder: "실명을 입력하세요" },
    { key: "address",  label: "주소",     icon: "📍",  type: "text",     placeholder: "주소를 입력하세요" },
    { key: "phone",    label: "전화번호", icon: "📱",  type: "tel",      placeholder: "010-0000-0000" },
  ];

  const navigate = useNavigate();

  // =========================
  // 입력값 공통 핸들러
  // =========================
  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  // =========================
  // 유효성 검사
  // =========================
  const validate = () => {
    const { email, password, nickname, name, address, phone } = form;

    if (!email || !password || !nickname || !name || !address || !phone) {
      setError("모든 항목을 입력해주세요.");
      return false;
    }
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(email)) {
      setError("올바른 이메일 형식을 입력해주세요.");
      return false;
    }
    if (password.length < 6) {
      setError("비밀번호는 6자 이상 입력해주세요.");
      return false;
    }
    return true;
  };

  // =========================
  // 회원가입 처리
  // =========================
  const handleRegister = async () => {
    setError("");
    setSuccess("");
    if (!validate()) return;

    setLoading(true);
    try {
      await register(form);
      setSuccess("🎉 회원가입이 완료되었습니다! 로그인 페이지로 이동합니다.");
      setTimeout(() => navigate("/login"), 1500);
    } catch (err) {
      setError(err.response?.data?.detail || "회원가입에 실패했습니다.");
    } finally {
      setLoading(false);
    }
  };

  // =========================
  // 렌더링
  // =========================
  return (
    <div className="min-h-screen flex items-center justify-center
                    bg-gradient-to-br from-indigo-50 via-white to-blue-100
                    py-10 px-4">

      <div className="w-full max-w-md bg-white rounded-2xl shadow-2xl overflow-hidden">

        {/* 상단 헤더 배너 */}
        <div className="bg-gradient-to-r from-indigo-500 to-blue-600 px-8 py-7 text-center">
          <div className="text-4xl mb-2">🙋</div>
          <h1 className="text-xl font-bold text-white tracking-wide">회원가입</h1>
          <p className="text-indigo-100 text-sm mt-1">
            새 계정을 만들고 게시판을 이용하세요
          </p>
        </div>

        {/* 폼 영역 */}
        <div className="px-8 py-7">

          {/* 에러 메시지 */}
          {error && (
            <div className="flex items-center gap-2 bg-red-50 border border-red-200
                            text-red-600 text-sm px-4 py-3 rounded-lg mb-5">
              <span>⚠️</span>
              <span>{error}</span>
            </div>
          )}

          {/* 성공 메시지 */}
          {success && (
            <div className="flex items-center gap-2 bg-green-50 border border-green-200
                            text-green-600 text-sm px-4 py-3 rounded-lg mb-5">
              <span>{success}</span>
            </div>
          )}

          {/* 입력 필드 목록 반복 렌더링 */}
          {fields.map(({ key, label, icon, type, placeholder }) => (
            <div className="mb-4" key={key}>
              <label className="block text-sm font-semibold text-gray-600 mb-1">
                {label}
              </label>
              <div className="relative">
                {/* 필드 아이콘 */}
                <span className="absolute left-3 top-1/2 -translate-y-1/2 text-gray-400 text-sm">
                  {icon}
                </span>
                <input
                  type={
                    // 비밀번호 필드는 showPassword 상태에 따라 타입 변경
                    key === "password"
                      ? (showPassword ? "text" : "password")
                      : type
                  }
                  name={key}               // handleChange에서 key로 사용
                  placeholder={placeholder}
                  value={form[key]}        // controlled input
                  onChange={handleChange}
                  className="w-full pl-10 pr-4 py-2.5 border border-gray-200 rounded-xl
                             text-sm bg-gray-50 focus:bg-white
                             focus:outline-none focus:ring-2 focus:ring-indigo-400
                             focus:border-transparent transition"
                />
                {/* 비밀번호 표시/숨김 토글 */}
                {key === "password" && (
                  <button
                    type="button"
                    className="absolute right-3 top-1/2 -translate-y-1/2
                               text-gray-400 hover:text-gray-600 text-sm"
                    onClick={() => setShowPassword(!showPassword)}
                  >
                    {showPassword ? "🙈" : "👁️"}
                  </button>
                )}
              </div>
            </div>
          ))}

          {/* 회원가입 버튼 */}
          <button
            onClick={handleRegister}
            disabled={loading}
            className={`w-full mt-2 py-3 rounded-xl font-semibold text-white text-sm
                        shadow-md transition-all duration-200
                        ${loading
                          ? "bg-indigo-300 cursor-not-allowed"
                          : "bg-gradient-to-r from-indigo-500 to-blue-600 hover:from-indigo-600 hover:to-blue-700 hover:shadow-lg active:scale-95"
                        }`}
          >
            {loading ? (
              <span className="flex items-center justify-center gap-2">
                <span className="animate-spin">⏳</span> 처리 중...
              </span>
            ) : "회원가입 완료"}
          </button>

          {/* 구분선 */}
          <div className="flex items-center gap-3 my-4">
            <hr className="flex-1 border-gray-200" />
            <span className="text-xs text-gray-400">또는</span>
            <hr className="flex-1 border-gray-200" />
          </div>

          {/* 로그인 이동 버튼 */}
          <button
            onClick={() => navigate("/login")}
            className="w-full py-3 rounded-xl font-semibold text-indigo-500 text-sm
                       border-2 border-indigo-200 bg-indigo-50
                       hover:bg-indigo-100 hover:border-indigo-400
                       transition-all duration-200 active:scale-95"
          >
            이미 계정이 있으신가요? 로그인
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
