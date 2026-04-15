// react-board2/src/components/CommentForm.jsx
// 게시글 상세 페이지(PostDetail.jsx) 하단의 댓글 입력 폼 컴포넌트
// - 로그인 상태에서만 입력 가능
// - 비로그인 상태에서는 안내 메시지 표시

import { useState } from "react";
import { useNavigate } from "react-router-dom";
import api from "../api/axios";  // 인터셉터가 적용된 axios 인스턴스

export default function CommentForm({ postId, currentUser, onRefresh }) {
  /**
   * @param {number}      postId      - 댓글을 달 게시글 ID
   * @param {Object|null} currentUser - 현재 로그인 사용자 (null이면 비로그인)
   * @param {Function}    onRefresh   - 댓글 작성 후 목록 새로고침 함수
   */

  const [text, setText] = useState("");        // 댓글 입력 내용
  const [loading, setLoading] = useState(false); // 요청 중 버튼 비활성화용
  const navigate = useNavigate();

  // =========================
  // 댓글 제출 처리
  // =========================
  const handleSubmit = async () => {
    if (!text.trim()) return;  // 빈 내용 제출 방지

    setLoading(true);

    try {
      // POST /posts/:postId/comments → 댓글 생성 요청
      // Authorization 헤더는 axios 인터셉터에서 자동 첨부
      await api.post(`/posts/${postId}/comments`, { text });
      setText("");      // 입력창 초기화
      onRefresh();      // 부모 컴포넌트 댓글 목록 새로고침
    } catch (err) {
      alert(err.response?.data?.detail || "댓글 작성에 실패했습니다.");
    } finally {
      setLoading(false);
    }
  };

  // =========================
  // 렌더링
  // =========================
  return (
    <div className="mt-4">
      {currentUser ? (
        // 로그인 상태: 댓글 입력 폼 표시
        <div className="flex flex-col gap-2">
          <textarea
            className="w-full border rounded-lg p-3 text-sm resize-none
                       focus:outline-none focus:ring-2 focus:ring-blue-400"
            rows={3}
            placeholder="댓글을 입력하세요..."
            value={text}
            onChange={(e) => setText(e.target.value)}
          />
          <div className="flex justify-end">
            <button
              className={`px-4 py-2 text-sm text-white rounded-lg transition
                ${loading
                  ? "bg-blue-300 cursor-not-allowed"
                  : "bg-blue-500 hover:bg-blue-600"
                }`}
              onClick={handleSubmit}
              disabled={loading}
            >
              {loading ? "등록 중..." : "댓글 등록"}
            </button>
          </div>
        </div>
      ) : (
        // 비로그인 상태: 로그인 유도 메시지 표시
        <div className="text-center py-4 bg-gray-50 rounded-lg border border-dashed">
          <p className="text-sm text-gray-500 mb-2">
            댓글을 작성하려면 로그인이 필요합니다.
          </p>
          <button
            className="text-sm text-blue-500 underline hover:text-blue-600"
            onClick={() => navigate("/login")}
          >
            로그인하러 가기
          </button>
        </div>
      )}
    </div>
  );
}
