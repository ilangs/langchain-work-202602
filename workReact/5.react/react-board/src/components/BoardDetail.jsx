// ========================================================
// BoardDetail.jsx - 게시글 상세보기 + 댓글 CRUD + 영구 저장
// ========================================================

import { useState } from "react";

export default function BoardDetail({ post, onBack, onEdit, onDelete, onUpdateComments }) {

  const [showConfirm, setShowConfirm] = useState(false);

  // 댓글 목록 (post.comments 기반 초기화)
  const [comments, setComments] = useState(post?.comments ?? []);

  // 댓글 작성
  const [commentAuthor, setCommentAuthor] = useState("");
  const [commentText, setCommentText] = useState("");

  // 댓글 수정 상태
  const [editingId, setEditingId] = useState(null);   // 현재 수정 중인 댓글 id
  const [editingText, setEditingText] = useState(""); // 수정 중인 댓글 내용

  // 댓글 삭제 확인
  const [deleteTargetId, setDeleteTargetId] = useState(null);

  // ── 공통: 댓글 변경 후 App까지 동기화 ──────────────
  function syncComments(next) {
    setComments(next);
    onUpdateComments?.(post.id, next);
  }

  // ── 댓글 등록 ────────────────────────────────────────
  function handleAddComment() {
    const author = commentAuthor.trim();
    const content = commentText.trim();
    if (!author || !content) return;

    const now = new Date();
    const date = `${now.getFullYear()}. ${String(now.getMonth() + 1).padStart(2, "0")}. ${String(now.getDate()).padStart(2, "0")}.`;
    const next = [...comments, { id: Date.now(), author, date, text: content }];

    syncComments(next);
    setCommentAuthor("");
    setCommentText("");
  }

  // ── 댓글 수정 시작 ───────────────────────────────────
  function startEdit(comment) {
    setEditingId(comment.id);
    setEditingText(comment.text);
  }

  // ── 댓글 수정 저장 ───────────────────────────────────
  function handleEditSave(id) {
    const text = editingText.trim();
    if (!text) return;
    const next = comments.map((c) => c.id === id ? { ...c, text } : c);
    syncComments(next);
    setEditingId(null);
    setEditingText("");
  }

  // ── 댓글 삭제 ────────────────────────────────────────
  function handleDeleteComment(id) {
    const next = comments.filter((c) => c.id !== id);
    syncComments(next);
    setDeleteTargetId(null);
  }

  // ── 게시글 삭제 ──────────────────────────────────────
  function handleDeleteConfirm() {
    setShowConfirm(false);
    if (onDelete) onDelete(post.id);
  }

  if (!post) {
    return (
      <div className="p-10 text-center text-gray-400 bg-white rounded-3xl shadow-sm">
        게시글 내용을 불러올 수 없습니다.
      </div>
    );
  }

  return (
    <>
      {/* ── 히어로 카드 ── */}
      <div className="bg-gradient-to-br from-indigo-600 to-violet-600 rounded-t-2xl px-9 pt-8 pb-8">
        <div className="flex justify-between items-center mb-8">
          <button
            onClick={onBack}
            className="w-11 h-11 rounded-full bg-white/20 hover:bg-white/40 text-white text-2xl flex items-center justify-center transition-all duration-200"
          >‹</button>
          <div className="flex gap-3">
            <button
              onClick={() => onEdit?.(post.id)}
              className="bg-white/20 hover:bg-white/35 text-white text-sm font-medium px-5 py-2 rounded-xl transition-all duration-200"
            >수정하기</button>
            <button
              onClick={() => setShowConfirm(true)}
              className="bg-violet-700 hover:bg-violet-800 text-white text-sm font-bold px-5 py-2 rounded-xl transition-all duration-200"
            >글 삭제</button>
          </div>
        </div>

        <h1 className="text-3xl font-black text-white text-center mb-7 leading-snug tracking-tight">
          {post.title}
        </h1>

        <div className="flex items-center gap-4">
          <div className="flex items-center gap-2 bg-white/20 rounded-full px-4 py-1.5">
            <div className="w-7 h-7 rounded-full bg-white/30 flex items-center justify-center text-sm">🔥</div>
            <span className="text-white text-sm font-bold tracking-wide">{post.author}</span>
          </div>
          <span className="text-white/70 text-xs font-medium tracking-widest uppercase">No. {post.id}</span>
        </div>
      </div>

      {/* ── 본문 카드 ── */}
      <div className="bg-white rounded-b-2xl shadow-lg flex flex-col">
        <div className="px-12 py-10 min-h-48">
          <p className="text-slate-700 text-base leading-loose text-center whitespace-pre-line">
            {post.content}
          </p>
        </div>
        <footer className="border-t border-slate-200 px-6 py-4 flex justify-between items-center">
          <span className="text-xs text-slate-400 tracking-wide">게시글 상세 정보 모드</span>
          <span className="text-xs text-slate-400 italic tracking-wide">React CRUD System v1.0</span>
        </footer>
      </div>

      {/* ── 댓글 섹션 ── */}
      <div className="bg-white rounded-2xl shadow-lg mt-5 px-8 py-7">

        {/* 댓글 헤더 */}
        <div className="flex items-center gap-3 mb-6">
          <div className="w-9 h-9 rounded-full bg-indigo-50 flex items-center justify-center text-lg">💬</div>
          <span className="text-lg font-bold text-slate-800">댓글</span>
          <span className="text-lg font-bold text-indigo-500">{comments.length}</span>
        </div>

        {/* 댓글 목록 */}
        <div className="flex flex-col gap-5 mb-7">
          {comments.length === 0 ? (
            <p className="text-center text-slate-400 text-sm py-6">
              아직 댓글이 없습니다. 첫 댓글을 남겨보세요!
            </p>
          ) : (
            comments.map((c) => (
              <div key={c.id} className="border-b border-slate-100 pb-5 last:border-0 last:pb-0">

                {/* 작성자 + 날짜 + 수정/삭제 버튼 */}
                <div className="flex items-center justify-between mb-1.5">
                  <div className="flex items-center gap-2">
                    <span className="text-sm font-bold text-slate-800">{c.author}</span>
                    <span className="text-xs text-slate-400">{c.date}</span>
                  </div>
                  {/* 수정/삭제 버튼 (수정 중이 아닐 때만 표시) */}
                  {editingId !== c.id && (
                    <div className="flex gap-2">
                      <button
                        onClick={() => startEdit(c)}
                        className="text-xs text-slate-400 hover:text-indigo-500 transition-colors px-2 py-1 rounded-lg hover:bg-indigo-50"
                      >수정</button>
                      <button
                        onClick={() => setDeleteTargetId(c.id)}
                        className="text-xs text-slate-400 hover:text-red-500 transition-colors px-2 py-1 rounded-lg hover:bg-red-50"
                      >삭제</button>
                    </div>
                  )}
                </div>

                {/* 댓글 본문 or 수정 폼 */}
                {editingId === c.id ? (
                  <div className="flex flex-col gap-2 mt-2">
                    <textarea
                      value={editingText}
                      onChange={(e) => setEditingText(e.target.value)}
                      rows={2}
                      className="w-full border border-indigo-300 rounded-xl px-4 py-2.5 text-sm text-slate-700 outline-none focus:ring-2 focus:ring-indigo-100 transition-all resize-none"
                    />
                    <div className="flex gap-2 justify-end">
                      <button
                        onClick={() => { setEditingId(null); setEditingText(""); }}
                        className="text-xs px-4 py-1.5 border border-slate-200 rounded-lg text-slate-500 hover:bg-slate-50 transition-all"
                      >취소</button>
                      <button
                        onClick={() => handleEditSave(c.id)}
                        className="text-xs px-4 py-1.5 bg-indigo-600 hover:bg-indigo-700 text-white rounded-lg transition-all"
                      >수정 완료</button>
                    </div>
                  </div>
                ) : (
                  <p className="text-sm text-slate-600 leading-relaxed">{c.text}</p>
                )}
              </div>
            ))
          )}
        </div>

        {/* 댓글 작성 폼 */}
        <div className="flex flex-col gap-3 pt-5 border-t border-slate-100">
          <input
            type="text"
            placeholder="작성자 이름"
            value={commentAuthor}
            onChange={(e) => setCommentAuthor(e.target.value)}
            className="w-full border border-slate-200 rounded-xl px-4 py-3 text-sm text-slate-700 placeholder-slate-400 outline-none focus:border-indigo-400 focus:ring-2 focus:ring-indigo-100 transition-all"
          />
          <div className="flex gap-3">
            <textarea
              placeholder="댓글을 남겨보세요..."
              value={commentText}
              onChange={(e) => setCommentText(e.target.value)}
              rows={3}
              className="flex-1 border border-slate-200 rounded-xl px-4 py-3 text-sm text-slate-700 placeholder-slate-400 outline-none focus:border-indigo-400 focus:ring-2 focus:ring-indigo-100 transition-all resize-none"
            />
            <button
              onClick={handleAddComment}
              className="bg-indigo-600 hover:bg-indigo-700 active:scale-95 text-white font-bold text-sm px-6 rounded-xl transition-all duration-200"
            >등록</button>
          </div>
        </div>
      </div>

      {/* ── 게시글 삭제 확인 모달 ── */}
      {showConfirm && (
        <div className="fixed inset-0 bg-black/45 z-50 flex items-center justify-center">
          <div className="bg-white rounded-2xl px-10 py-9 w-80 text-center shadow-2xl">
            <div className="text-4xl mb-3">🗑️</div>
            <p className="text-slate-800 font-bold text-lg mb-2">글을 삭제하시겠습니까?</p>
            <p className="text-slate-400 text-sm leading-relaxed mb-7">
              삭제된 글은 복구할 수 없습니다.<br />정말 삭제하시겠습니까?
            </p>
            <div className="flex gap-3">
              <button
                onClick={() => setShowConfirm(false)}
                className="flex-1 py-2.5 border border-slate-200 rounded-xl text-sm text-slate-600 hover:bg-slate-50 transition-all duration-200"
              >취소</button>
              <button
                onClick={handleDeleteConfirm}
                className="flex-1 py-2.5 bg-violet-600 hover:bg-violet-700 text-white rounded-xl text-sm font-bold transition-all duration-200"
              >삭제</button>
            </div>
          </div>
        </div>
      )}

      {/* ── 댓글 삭제 확인 모달 ── */}
      {deleteTargetId && (
        <div className="fixed inset-0 bg-black/45 z-50 flex items-center justify-center">
          <div className="bg-white rounded-2xl px-10 py-9 w-80 text-center shadow-2xl">
            <div className="text-4xl mb-3">💬</div>
            <p className="text-slate-800 font-bold text-lg mb-2">댓글을 삭제하시겠습니까?</p>
            <p className="text-slate-400 text-sm leading-relaxed mb-7">
              삭제된 댓글은 복구할 수 없습니다.
            </p>
            <div className="flex gap-3">
              <button
                onClick={() => setDeleteTargetId(null)}
                className="flex-1 py-2.5 border border-slate-200 rounded-xl text-sm text-slate-600 hover:bg-slate-50 transition-all duration-200"
              >취소</button>
              <button
                onClick={() => handleDeleteComment(deleteTargetId)}
                className="flex-1 py-2.5 bg-red-500 hover:bg-red-600 text-white rounded-xl text-sm font-bold transition-all duration-200"
              >삭제</button>
            </div>
          </div>
        </div>
      )}
    </>
  );
}