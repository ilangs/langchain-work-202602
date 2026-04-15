// react-board2/src/api/auth.js

import api, { setAccessToken, getAccessToken } from "./axios";

// =========================
// 회원가입 API
// =========================
export const register = async (userData) => {
  /**
   * @param {Object} userData - { email, password, nickname, name, address, phone }
   * @returns {Object} 생성된 사용자 정보
   */
  const response = await api.post("/register", userData);
  return response.data;
};

// =========================
// 로그인 API
// =========================
export const login = async (email, password) => {
  /**
   * - Access Token → JS 메모리 변수에 저장 (보안 강화)
   * - Refresh Token → 서버가 HttpOnly 쿠키로 자동 설정
   * - 사용자 정보 → UI 렌더링 편의를 위해 localStorage 유지 (민감정보 제외)
   */
  const response = await api.post("/login", { email, password });
  const { access_token, user } = response.data;

  setAccessToken(access_token);
  localStorage.setItem("user", JSON.stringify(user)); 

  return response.data;
};

// =========================
// 로그아웃 API
// =========================
export const logout = async () => {
  /**
   * - 서버: HttpOnly 쿠키(refresh_token) 삭제
   * - 클라이언트: 메모리 토큰 및 로컬 유저 정보 삭제
   */
  try {
    await api.post("/logout");
  } finally {
    // 서버 요청 성공/실패 관계없이 클라이언트 데이터 반드시 삭제
    setAccessToken(null);
    localStorage.removeItem("user");
  }
};

// =========================
// Access Token 재발급 API (Silent Refresh용)
// =========================
export const refreshAccessToken = async () => {
  /**
   * Refresh Token(HttpOnly 쿠키)으로 새 Access Token 발급
   * - 앱 초기 로드 시(새로고침) 세션 복구를 위해 명시적으로 호출됨
   */
  try {
    const response = await api.post("/refresh");
    const { access_token, user } = response.data;

    setAccessToken(access_token);
    if (user) {
      localStorage.setItem("user", JSON.stringify(user));
    }
    return response.data;
  } catch (error) {
    setAccessToken(null);
    localStorage.removeItem("user");
    throw error;
  }
};

// =========================
// 현재 로그인 사용자 정보 조회 (로컬)
// =========================
export const getCurrentUser = () => {
  /**
   * localStorage의 유저 정보 반환 (서버 요청 없이 즉시 반환)
   * @returns {Object|null}
   */
  const user = localStorage.getItem("user");
  return user ? JSON.parse(user) : null;
};

// =========================
// 로그인 여부 확인
// =========================
export const isLoggedIn = () => {
  /**
   * 메모리에 Access Token 존재 여부로 로그인 상태 확인
   * - PrivateRoute, 조건부 UI 렌더링에 사용
   * @returns {boolean}
   */
  return !!getAccessToken();
};
