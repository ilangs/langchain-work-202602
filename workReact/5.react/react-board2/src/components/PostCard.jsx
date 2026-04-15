// react-board2/src/components/PostCard.jsx
// 게시글 목록(PostList.jsx)에서 각 게시글을 카드 형태로 표시하는 컴포넌트
// - 제목, 작성자 닉네임, 댓글 수 표시
// - 클릭 시 게시글 상세 페이지로 이동

import { useNavigate } from "react-router-dom";

export default function PostCard({ post }) {
  /**
   * @param {Object} post - 게시글 데이터
   *   - id           : 게시글 ID
   *   - title        : 제목
   *   - content      : 내용 (미리보기용)
   *   - nickname     : 작성자 닉네임
   *   - comment_count: 댓글 수
   */
  const navigate = useNavigate();

  return (
    <div
      className="bg-white rounded-xl shadow-sm p-4 mb-3 cursor-pointer
                 hover:shadow-md hover:border-blue-300 border border-transparent transition"
      onClick={() => navigate(`/posts/${post.id}`)}  // 클릭 시 상세 페이지로 이동
    >
      {/* 게시글 제목 */}
      <h2 className="text-lg font-semibold text-gray-800 mb-1 truncate">
        {post.title}
      </h2>

      {/* 게시글 내용 미리보기 (2줄 제한) */}
      <p className="text-sm text-gray-500 mb-3 line-clamp-2">
        {post.content}
      </p>

      {/* 하단 메타 정보: 작성자, 댓글 수 */}
      <div className="flex items-center justify-between text-xs text-gray-400">

        {/* 작성자 닉네임 */}
        <span>✍️ {post.nickname || "알 수 없음"}</span>

        {/* 댓글 수 */}
        <span>💬 댓글 {post.comment_count ?? 0}개</span>

      </div>
    </div>
  );
}
