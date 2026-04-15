// ========================================================
// BoardDetail.jsx - 게시글 상세보기 (더미 데이터 내장)
//
// 【props】
//  post     : { id, title, author, content } 게시글 데이터
//  onBack   : 뒤로가기 / 목록으로 이동 함수
//  onEdit   : 수정 페이지로 이동 함수
//  onDelete : 삭제 처리 함수
// ========================================================

import { useState } from "react";

export default function BoardDetail({ post, onBack, onEdit, onDelete }) {

  // 삭제 확인 모달 표시 여부
  const [showConfirm, setShowConfirm] = useState(false);

  // 삭제 확인 처리
  function handleDeleteConfirm() {
    setShowConfirm(false);
    if (onDelete) onDelete(post.id);
  }

  // ── 더미 데이터 ──────────────────────────────────────
  // 부모에서 post props가 전달되면 그 데이터를 사용
  // 전달되지 않으면 아래 더미 데이터로 대체
  if(!post){
    return (
      <div className="p-10 text-center text-gray-400 bg-white rounded-3xl shaddow-sm">
        게시글 내용을 불러올 수 없습니다.</div>
    )
  }

  return (
    <>
      {/* ── 히어로 카드 (파란 그라디언트) ── */}
      <div className="bg-gradient-to-br from-indigo-600 to-violet-600 rounded-t-2xl px-9 pt-8 pb-8">

        {/* 상단: 뒤로가기 + 수정/삭제 버튼 */}
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

        {/* 글 제목 */}
        <h1 className="text-3xl font-black text-white text-center mb-7 leading-snug tracking-tight">
          {post.title}
        </h1>

        {/* 작성자 배지 + 글번호 */}
        <div className="flex items-center gap-4">
          <div className="flex items-center gap-2 bg-white/20 rounded-full px-4 py-1.5">
            <div className="w-7 h-7 rounded-full bg-white/30 flex items-center justify-center text-sm">
              🔥
            </div>
            <span className="text-white text-sm font-bold tracking-wide">
              {post.author}
            </span>
          </div>
          <span className="text-white/70 text-xs font-medium tracking-widest uppercase">
            No. {post.id}
          </span>
        </div>
      </div>

      {/* ── 본문 + 푸터 통합 카드 ── */}
      <div className="bg-white rounded-b-2xl shadow-lg flex flex-col">

        {/* 본문 내용 */}
        <div className="px-12 py-10 min-h-48">
          <p className="text-slate-700 text-base leading-loose text-center whitespace-pre-line">
            {post.content}
          </p>
        </div>

        {/* 푸터 */}
        <footer className="border-t border-slate-200 px-6 py-4 flex justify-between items-center">
          <span className="text-xs text-slate-400 tracking-wide">게시글 상세 정보 모드</span>
          <span className="text-xs text-slate-400 italic tracking-wide">React CRUD System v1.0</span>
        </footer>
      </div>

      {/* ── 삭제 확인 모달 ── */}
      {showConfirm && (
        <div className="fixed inset-0 bg-black/45 z-50 flex items-center justify-center">
          <div className="bg-white rounded-2xl px-10 py-9 w-80 text-center shadow-2xl">
            <div className="text-4xl mb-3">🗑️</div>
            <p className="text-slate-800 font-bold text-lg mb-2">글을 삭제하시겠습니까?</p>
            <p className="text-slate-400 text-sm leading-relaxed mb-7">
              삭제된 글은 복구할 수 없습니다.<br />
              정말 삭제하시겠습니까?
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
    </>
  );
}