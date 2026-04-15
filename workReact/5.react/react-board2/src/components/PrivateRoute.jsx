// react-board2/src/components/PrivateRoute.jsx
// 로그인이 필요한 페이지를 보호하는 래퍼 컴포넌트
// - App.jsx에서 인라인으로 정의했던 PrivateRoute를 별도 파일로 분리
// - 비로그인 상태에서 접근 시 /login으로 강제 이동

import { Navigate } from "react-router-dom";

export default function PrivateRoute({ user, children }) {
  /**
   * @param {Object|null} user     - 전역 로그인 상태 (null이면 비로그인)
   * @param {ReactNode}   children - 보호할 페이지 컴포넌트
   */

  if (!user) {
    // 비로그인 상태 → 로그인 페이지로 리다이렉트
    // replace: 히스토리 스택에 남기지 않음 (뒤로가기로 보호 페이지 재접근 방지)
    return <Navigate to="/login" replace />;
  }

  // 로그인 상태 → 보호된 페이지 정상 렌더링
  return children;
}
