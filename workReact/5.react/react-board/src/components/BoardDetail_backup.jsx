// 1.BoardDetail.jsx 파일 작성

import React from "react"; // React 라이브러리 임포트

/**
 * [BoardDetail 컴포넌트]
 * props 설명:
 *  ㄴ post: 현재 화면에 보여줄 게시글 객체
 *  ㄴ onEdit: 수정 버튼 클릭 시 실행될 함수 (App.jsx의 모드 변경 로직과 연결)
 *  ㄴ onDelete: 삭제 버튼 클릭 시 실행될 함수 (App.jsx의 데이터 삭제 로직과 연결)
 *  ㄴ onBack: 목록으로 돌아가기 버튼 클릭 시 실행될 함수
 */
export default function BoardDetail({ post, onEdit, onDelete, onBack }) {
  
  // 데이터가 정상적으로 전달되지 않았을 경우를 대비한 예외 처리 (방어 코드)
  if (!post) {
    return (
      <div className="p-10 text-center text-gray-400 bg-white rounded-3xl shadow-sm">
        게시글 내용을 불러올 수 없습니다.
      </div>
    );
  }

  return (
    // 전체 상세 보기 카드 컨테이너: 최대 너비 제한 및 중앙 정렬
    <div className="max-w-3xl mx-auto space-y-8 animate-in fade-in duration-500"> 
      
      {/* ──────────────────────────────────────────────────
          [상단 영역] 게시글 헤더 및 본문 카드
      ────────────────────────────────────────────────── */}
      <div className="bg-white rounded-[2.5rem] shadow-2xl shadow-blue-500/5 border border-gray-100 overflow-hidden">
        
        {/* 상단 그라데이션 헤더 섹션: 제목과 작성자 정보 표시 */}
        <div className="bg-gradient-to-br from-blue-600 to-indigo-700 p-10 text-white">
          <div className="flex justify-between items-start mb-8">
            
            {/* [뒤로가기 버튼]: 목록 화면으로 돌아가는 액션 실행 */}
            <button 
              onClick={onBack} 
              className="bg-white/10 hover:bg-white/20 p-3 rounded-2xl transition-all active:scale-90"
              title="목록으로 돌아가기"
            >
              <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2.5" d="M15 19l-7-7 7-7"/>
              </svg>
            </button>

            {/* [관리 버튼 그룹]: 수정 및 삭제 버튼 배치 */}
            <div className="flex gap-3">
              {/* 수정 버튼: 클릭 시 App.jsx의 모드를 'form'으로 변경하고 현재 post를 전달함 */}
              <button 
                onClick={onEdit} 
                className="bg-white/10 hover:bg-white/20 px-6 py-2.5 rounded-xl text-sm font-black transition-all active:scale-95 border border-white/10"
              >
                수정하기
              </button>
              
              {/* 삭제 버튼: 클릭 시 App.jsx의 handleDelete 함수를 통해 데이터 배열에서 제거함 */}
              <button 
                onClick={onDelete} 
                className="bg-red-500/20 hover:bg-red-500/40 px-6 py-2.5 rounded-xl text-sm font-black transition-all text-red-100 active:scale-95 border border-red-500/20"
              >
                글 삭제
              </button>
            </div>
          </div>

          {/* 게시글 제목: 굵고 큰 글씨로 강조 */}
          <h2 className="text-4xl font-black mb-6 leading-tight tracking-tight">
            {post.title}
          </h2>

          {/* 작성자 정보 및 게시글 고유 ID 표시 */}
          <div className="flex items-center gap-4 opacity-90 text-sm font-bold">
            <span className="bg-white/20 px-4 py-1.5 rounded-full flex items-center gap-2">
              <span className="text-lg">✍️</span> {post.author}
            </span>
            <span className="font-mono text-xs opacity-50 tracking-widest">NO. {post.id}</span>
          </div>
        </div>

        {/* ──────────────────────────────────────────────────
            [본문 영역] 게시글 내용 출력
        ────────────────────────────────────────────────── */}
        {/* whitespace-pre-wrap: 작성 시 입력한 줄바꿈과 공백을 그대로 화면에 유지함 */}
        <div className="p-14 min-h-[400px] text-gray-700 text-xl leading-relaxed whitespace-pre-wrap font-medium selection:bg-blue-100">
          {post.content || "이 게시글에는 작성된 본문 내용이 존재하지 않습니다."}
        </div>

        {/* 하단 장식 또는 정보 영역 (필요 시 활용) */}
        <div className="px-14 py-8 bg-gray-50/50 border-t border-gray-50 flex justify-between items-center text-gray-400 text-sm">
          <span>게시글 상세 정보 모드</span>
          <span className="italic font-mono">React CRUD System v1.0</span>
        </div>
      </div>
    </div>
  );
}
