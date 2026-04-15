// react-board2/src/pages/PostDetail.jsx
// 게시글 상세 페이지
// - 게시글 내용 표시
// - 작성자 본인에게만 수정/삭제 버튼 표시
// - 댓글 목록 + 댓글 작성 폼

import { useEffect, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";
import api from "../api/axios";
import Navbar from "../components/Navbar";
import CommentList from "../components/CommentList";
import CommentForm from "../components/CommentForm";

export default function PostDetail({ user, onLogout }) {
  /**
   * @param {Object|null} user     - 전역 로그인 사용자 정보
   * @param {Function}    onLogout - 로그아웃 처리 함수
   */

  // URL 파라미터에서 게시글 ID 추출 (/posts/:id)
  const { id } = useParams();
  const navigate = useNavigate();

  // =========================
  // 상태 관리
  // =========================
  const [post, setPost] = useState(null);        // 게시글 상세 데이터
  const [comments, setComments] = useState([]);  // 댓글 목록
  const [loading, setLoading] = useState(true);  // 초기 로딩 상태

  // =========================
  // 게시글 상세 조회
  // =========================
  const fetchPost = async () => {
    try {
      // GET /posts/:id
      const res = await api.get(`/posts/${id}`);
      setPost(res.data);
    } catch (err) {
      // 게시글이 없는 경우 목록으로 이동
      alert("게시글을 찾을 수 없습니다.");
      navigate("/posts");
    } finally {
      setLoading(false);
    }
  };

  // =========================
  // 댓글 목록 조회
  // =========================
  const fetchComments = async () => {
    try {
      // GET /posts/:id/comments
      const res = await api.get(`/posts/${id}/comments`);
      setComments(res.data);
    } catch (err) {
      console.error("댓글 조회 실패:", err);
    }
  };

  // 컴포넌트 마운트 시 게시글 + 댓글 동시 조회
  useEffect(() => {
    fetchPost();
    fetchComments();
  }, [id]);  // id가 바뀌면 재조회

  // =========================
  // 게시글 삭제
  // =========================
  const handleDelete = async () => {
    if (!window.confirm("게시글을 삭제하시겠습니까?")) return;

    try {
      // DELETE /posts/:id (Authorization 헤더 자동 첨부)
      await api.delete(`/posts/${id}`);
      alert("게시글이 삭제되었습니다.");
      navigate("/posts");  // 삭제 후 목록으로 이동
    } catch (err) {
      alert(err.response?.data?.detail || "게시글 삭제에 실패했습니다.");
    }
  };

  // =========================
  // 로딩 화면
  // =========================
  if (loading) {
    return (
      <div className="min-h-screen bg-gray-100">
        <Navbar user={user} onLogout={onLogout} />
        <div className="text-center text-gray-400 py-20">불러오는 중...</div>
      </div>
    );
  }

  // =========================
  // 렌더링
  // =========================
  return (
    <div className="min-h-screen bg-gray-100">

      {/* 공통 네비게이션 바 */}
      <Navbar user={user} onLogout={onLogout} />

      <div className="max-w-2xl mx-auto py-8 px-4">

        {/* 게시글 본문 카드 */}
        <div className="bg-white rounded-xl shadow-md p-6 mb-6">

          {/* 게시글 제목 */}
          <h1 className="text-2xl font-bold text-gray-800 mb-2">
            {post.title}
          </h1>

          {/* 작성자 닉네임 */}
          <p className="text-sm text-gray-400 mb-4">
            ✍️ {post.nickname || "알 수 없음"}
          </p>

          <hr className="mb-4" />

          {/* 게시글 내용 (줄바꿈 유지) */}
          <p className="text-gray-700 whitespace-pre-wrap leading-relaxed">
            {post.content}
          </p>

          {/* 수정/삭제 버튼 (작성자 본인만 표시) */}
          {user && user.id === post.user_id && (
            <div className="flex gap-3 mt-6 justify-end">
              <button
                className="text-sm bg-yellow-400 text-white px-4 py-2
                           rounded-lg hover:bg-yellow-500 transition"
                onClick={() => navigate(`/posts/${id}/edit`)}
              >
                수정
              </button>
              <button
                className="text-sm bg-red-500 text-white px-4 py-2
                           rounded-lg hover:bg-red-600 transition"
                onClick={handleDelete}
              >
                삭제
              </button>
            </div>
          )}
        </div>

        {/* 목록으로 버튼 */}
        <button
          className="text-sm text-gray-500 hover:text-blue-500 mb-6"
          onClick={() => navigate("/posts")}
        >
          ← 목록으로 돌아가기
        </button>

        {/* 댓글 섹션 */}
        <div className="bg-white rounded-xl shadow-md p-6">

          <h2 className="text-lg font-semibold text-gray-700 mb-4">
            💬 댓글 {comments.length}개
          </h2>

          {/* 댓글 작성 폼 */}
          <CommentForm
            postId={id}
            currentUser={user}
            onRefresh={fetchComments}  // 댓글 작성 후 목록 새로고침
          />

          <hr className="my-4" />

          {/* 댓글 목록 */}
          <CommentList
            comments={comments}
            currentUser={user}
            onRefresh={fetchComments}  // 수정/삭제 후 목록 새로고침
          />

        </div>
      </div>
    </div>
  );
}
