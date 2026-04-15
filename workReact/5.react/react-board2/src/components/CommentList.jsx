// react-board2/src/components/CommentList.jsx
// 게시글 상세 페이지(PostDetail.jsx)에서 댓글 목록을 표시하는 컴포넌트
// - 작성자 본인 댓글에만 수정/삭제 버튼 표시
// - 수정 클릭 시 인라인 편집 모드 전환

import { useState } from "react";
import api from "../api/axios";  // 인터셉터가 적용된 axios 인스턴스

export default function CommentList({ comments, currentUser, onRefresh }) {
  /**
   * @param {Array}       comments    - 댓글 목록 배열
   * @param {Object|null} currentUser - 현재 로그인 사용자 (null이면 비로그인)
   * @param {Function}    onRefresh   - 수정/삭제 후 댓글 목록 새로고침 함수
   */

  // 현재 수정 중인 댓글 ID (null이면 수정 모드 아님)
  const [editingId, setEditingId] = useState(null);
  // 수정 중인 댓글의 텍스트 상태
  const [editText, setEditText] = useState("");

  // =========================
  // 수정 모드 진입
  // =========================
  const handleEditStart = (comment) => {
    setEditingId(comment.id);      // 수정 대상 ID 저장
    setEditText(comment.text);     // 기존 내용을 입력창에 미리 채움
  };

  // =========================
  // 수정 취소
  // =========================
  const handleEditCancel = () => {
    setEditingId(null);  // 수정 모드 해제
    setEditText("");     // 입력창 초기화
  };

  // =========================
  // 댓글 수정 저장
  // =========================
  const handleEditSave = async (commentId) => {
    if (!editText.trim()) return;  // 빈 내용 저장 방지

    try {
      // PUT /comments/:id → 댓글 수정 요청 (Authorization 헤더 자동 첨부)
      await api.put(`/comments/${commentId}`, { text: editText });
      setEditingId(null);  // 수정 모드 해제
      onRefresh();         // 부모 컴포넌트에서 댓글 목록 새로고침
    } catch (err) {
      alert(err.response?.data?.detail || "댓글 수정에 실패했습니다.");
    }
  };

  // =========================
  // 댓글 삭제
  // =========================
  const handleDelete = async (commentId) => {
    if (!window.confirm("댓글을 삭제하시겠습니까?")) return;  // 삭제 확인 다이얼로그

    try {
      // DELETE /comments/:id → 댓글 삭제 요청
      await api.delete(`/comments/${commentId}`);
      onRefresh();  // 댓글 목록 새로고침
    } catch (err) {
      alert(err.response?.data?.detail || "댓글 삭제에 실패했습니다.");
    }
  };

  // =========================
  // 렌더링
  // =========================
  if (comments.length === 0) {
    return (
      <p className="text-sm text-gray-400 text-center py-4">
        아직 댓글이 없습니다. 첫 댓글을 남겨보세요! 💬
      </p>
    );
  }

  return (
    <ul className="space-y-3">
      {comments.map((comment) => (
        <li
          key={comment.id}
          className="bg-gray-50 rounded-lg p-3 border border-gray-200"
        >
          {editingId === comment.id ? (
            // =========================
            // 인라인 수정 모드
            // =========================
            <div>
              <textarea
                className="w-full border rounded p-2 text-sm resize-none
                           focus:outline-none focus:ring-2 focus:ring-blue-400"
                rows={2}
                value={editText}
                onChange={(e) => setEditText(e.target.value)}
              />
              <div className="flex gap-2 mt-2 justify-end">
                {/* 저장 버튼 */}
                <button
                  className="text-xs bg-blue-500 text-white px-3 py-1 rounded hover:bg-blue-600"
                  onClick={() => handleEditSave(comment.id)}
                >
                  저장
                </button>
                {/* 취소 버튼 */}
                <button
                  className="text-xs bg-gray-300 text-gray-700 px-3 py-1 rounded hover:bg-gray-400"
                  onClick={handleEditCancel}
                >
                  취소
                </button>
              </div>
            </div>
          ) : (
            // =========================
            // 일반 표시 모드
            // =========================
            <div>
              {/* 댓글 작성자 닉네임 */}
              <div className="flex items-center justify-between mb-1">
                <span className="text-xs font-semibold text-blue-500">
                  👤 {comment.nickname || "알 수 없음"}
                </span>

                {/* 본인 댓글에만 수정/삭제 버튼 표시 */}
                {currentUser && currentUser.id === comment.user_id && (
                  <div className="flex gap-2">
                    <button
                      className="text-xs text-gray-500 hover:text-blue-500"
                      onClick={() => handleEditStart(comment)}
                    >
                      수정
                    </button>
                    <button
                      className="text-xs text-gray-500 hover:text-red-500"
                      onClick={() => handleDelete(comment.id)}
                    >
                      삭제
                    </button>
                  </div>
                )}
              </div>

              {/* 댓글 내용 */}
              <p className="text-sm text-gray-700">{comment.text}</p>
            </div>
          )}
        </li>
      ))}
    </ul>
  );
}
