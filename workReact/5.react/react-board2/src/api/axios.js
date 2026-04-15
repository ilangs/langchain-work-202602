// react-board2/src/api/axios.js

import axios from "axios";

// =========================
// Access Token 메모리 저장소
// =========================
/**
 * XSS 방지를 위해 localStorage 대신 모듈 내 프라이빗 변수에 토큰을 보관합니다.
 * 브라우저 새로고침 시 초기화되므로, App 최상단에서 Silent Refresh 처리가 필요합니다.
 */
let memoryAccessToken = null;

export const setAccessToken = (token) => {
  memoryAccessToken = token;
};

export const getAccessToken = () => {
  return memoryAccessToken;
};

// =========================
// 기본 API 인스턴스 생성
// =========================
const api = axios.create({
  baseURL: "http://localhost:8000",  // FastAPI 서버 주소 (환경에 맞게 수정)
  withCredentials: true,             // HttpOnly 쿠키(refresh_token) 자동 전송 허용
  timeout: 10000,                    // 10초 지나면 에러 발생, 무한대기 방지 
});

// =========================
// 요청 인터셉터 (Request Interceptor)
// =========================
api.interceptors.request.use(
  (config) => {
    // localStorage 대신 JS 메모리 변수에서 Access Token을 가져옴
    const token = getAccessToken();
    if (token) {
      // Bearer 방식으로 Authorization 헤더 설정
      config.headers["Authorization"] = `Bearer ${token}`;
    }
    return config;  // 수정된 요청 설정 반환
  },
  (error) => {
    // 요청 자체가 실패한 경우 (네트워크 오류 등)
    return Promise.reject(error);
  }
);

// =========================
// 응답 인터셉터 (Response Interceptor)
// =========================
api.interceptors.response.use(
  (response) => {
    // 응답이 정상(2xx)인 경우 그대로 반환
    return response;
  },
  async (error) => {
    const originalRequest = error.config;  // 실패한 원본 요청 정보 저장

    // Access Token 만료(401) 이고, 아직 재시도 하지 않은 요청인 경우
    // _retry 플래그: 무한 루프 방지 (재발급 실패 시 반복 요청 차단)
    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;  // 재시도 플래그 설정 (중복 재시도 방지)

      try {
        // Refresh Token(HttpOnly 쿠키)으로 새 Access Token 요청
        // withCredentials: true 이므로 쿠키가 자동으로 함께 전송됨
        const res = await api.post("/refresh");

        const newAccessToken = res.data.access_token;

        // 새 Access Token을 메모리(변수)에 안전하게 저장
        setAccessToken(newAccessToken);

        // 실패했던 원본 요청의 헤더를 새 토큰으로 교체 후 재시도
        originalRequest.headers["Authorization"] = `Bearer ${newAccessToken}`;
        return api(originalRequest);  // 원본 요청 재전송

      } catch (refreshError) {
        // Refresh Token도 만료되었거나 없는 경우 → 완전 로그아웃 처리
        setAccessToken(null);                      // 메모리 토큰 삭제
        localStorage.removeItem("user");           // 저장된 유저 정보 삭제
        window.location.href = "/login";           // 로그인 페이지로 강제 이동
        return Promise.reject(refreshError);
      }
    }

    // 401 외 다른 에러는 그대로 호출부로 전달
    return Promise.reject(error);
  }
);

export default api;
