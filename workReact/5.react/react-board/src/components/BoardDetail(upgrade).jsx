import React, { useState } from "react";

//추가2
// [내부 컴포넌트] 댓글 입력 폼: 사용자의 입력을 받아 부모에게 전달하는 역할

function CommentForm({ onAdd }) {
   //작성자,본문내용
  const [author,setAuthor] = useState("")
  const [text,setText] = useState("")

  //등록버튼 클릭시 실행되는 핸들러
  const handleSubmit = (e) =>{ //전송버튼의 기본기능을 X(데이터를 서버로 전송X)
    e.preventDefault() //새로고침 방지하기위해서
    if(!author.trim() || !text.trim()) return;//빈값 입력방지->유효성 검사(올바른값 입력확인)

    //부모로부터 받은 onAdd를 이용해서 데이터 전달->부모함수 호출
    //{author,text,date:new Date().toLocaleDateString()}=>comment
    onAdd({author,text,date:new Date().toLocaleDateString()})//localStorage(문자열만 저장)
    //입력 초기화
    setAuthor("")
    setText("")
  };

  return (
    // Tailwind CSS를 활용한 스타일링: Glassmorphism 느낌의 배경과 테두리 적용
    <form onSubmit={handleSubmit} className="mt-8 space-y-4 bg-gray-50/50 p-6 rounded-2xl border border-gray-100">
      <div className="flex gap-4">
        <input
          className="flex-1 px-4 py-2 bg-white border border-gray-200 rounded-xl text-sm focus:ring-2 focus:ring-blue-500 outline-none transition-all"
          placeholder="작성자 이름"
          value={author}
          onChange={(e) => setAuthor(e.target.value)} // 실시간 입력값 상태 반영
        />
      </div>
      <div className="flex gap-2">
        <textarea
          className="flex-[4] px-4 py-2 bg-white border border-gray-200 rounded-xl text-sm focus:ring-2 focus:ring-blue-500 outline-none transition-all resize-none h-20"
          placeholder="댓글을 남겨보세요..."
          value={text}
          onChange={(e) => setText(e.target.value)}
        />
        <button
          type="submit"
          className="flex-1 bg-blue-600 text-white rounded-xl font-bold text-sm hover:bg-blue-700 transition-all active:scale-95 shadow-lg shadow-blue-100 h-20"
        >
          등록
        </button>
      </div>
    </form>
  );
}

// ──────────────────────────────────────────────────
// [내부 컴포넌트] 댓글 리스트 (수정 로직 및 UI가 추가됨)
// ──────────────────────────────────────────────────
function CommentList({ comments,onDelete,onEdit}) {  //comments(댓글들)
  
 //추가 (현재 수정중인 댓글의 id를 찾아서 설정)
 const [editingId,setEditingId] = useState(null)// null=>보기 상태=>수정상태(X)

 //추가2 (수정중인 텍스트를 임시로 저장하는 상태)
 const [editText,setEditText] = useState("")

  // 댓글이 없을 경우 예외 처리
  if (!comments || comments.length === 0) {
    return (
      <div className="text-center py-10 text-gray-400 text-sm">
        첫 번째 댓글을 남겨보세요!
      </div>
    );
  } 
  //추가3 수정버튼클릭시 호출=>해당 댓글을 수정모드로 전환
  const handleStartEdit = (comment) =>{
      setEditingId(comment.id) //수정할 id 세팅
      setEditText(comment.text) //기존 내용을 입력창에 미리 채워놓음
  }
  //추가4 수정완료 버튼 클릭시 호출
  const handleSaveEdit = (commentId) =>{
     if(!editText.trim()) return //내용이 없으면 중단
     onEdit(commentId,editText) //부모(App.jsx)의 데이터 수정함수 실행
     setEditingId(null)//수정 완료후 다시 보기모드로 전환
  }
  /*  글목록보기 먼저 연습
  return (
    <div className="space-y-4">
       
        {
          comments.map((comment)=>(
            <div key={comment.id} className="p-4 rounded-xl border-gray-100 bg-white">
              
               <div className="flex item-center gap-2 mb-1">
                  <span className="font-bold text-gray-800 text-sm">
                    {comment.author}
                  </span>
                  <span className="text-[10px] text-gray-400">
                    {comment.date}
                  </span>
               </div>
                <p className="text-gray-600 text-sm leading-relaxed">
                  {comment.text}
                </p>
            </div>
          ))
        }
    </div>
  )
}
*/

  return (
    <div className="space-y-4">
      {/* map함수를 이용(댓글 배열을 하나씩 꺼내옴) */}
      {comments.map((comment) => (
        <div key={comment.id} className="group p-4 hover:bg-gray-50 rounded-xl transition-all border border-transparent hover:border-gray-100">
          {/* 수정상태 여부에 따라 조건부 화면 전환 */}
          {editingId === comment.id ? (
            // ──────────────────────────────────────────────────
            // [수정 모드 UI]: 텍스트 입력창과 저장/취소 버튼 노출
            // ──────────────────────────────────────────────────
            <div className="space-y-3">
               {/* bg-white text-gray-800 (textarea가 검게 나온다) */}
              <textarea
                className="w-full p-3 border-2 border-blue-200 rounded-xl text-sm focus:border-blue-500 outline-none transition-all resize-none bg-white text-gray-800"
                value={editText}
                onChange={(e) => setEditText(e.target.value)}
              />
              <div className="flex justify-end gap-2">
                <button 
                  onClick={()=>setEditingId(null)}
                  className="px-3 py-1 text-xs font-bold text-gray-400 hover:text-gray-600"
                >
                  취소
                </button>
                <button 
                   onClick={()=>handleSaveEdit(comment.id)}
                  className="px-4 py-1 text-xs font-bold bg-blue-600 text-white rounded-lg hover:bg-blue-700 shadow-md shadow-blue-100"
                >
                  수정 완료
                </button>
              </div>
            </div>
          ) : (
            // ──────────────────────────────────────────────────
            // [일반 보기 모드 UI]: 댓글 내용과 수정/삭제 아이콘 노출
            // ──────────────────────────────────────────────────
            <div className="flex justify-between items-start">
              <div className="space-y-1">
                <div className="flex items-center gap-2">
                  <span className="font-bold text-gray-800 text-sm">{comment.author}</span>
                  <span className="text-[10px] text-gray-400 font-mono">{comment.date}</span>
                </div>
                <p className="text-gray-600 text-sm leading-relaxed">{comment.text}</p>
              </div>
              {/* 버튼그룹: group-hover를 사용하여 마우스를 갖다대면 보이도록 설정 */}
              <div className="flex gap-1 opacity-0 group-hover:opacity-100 transition-all">
                {/* 수정 아이콘 버튼 */}
                <button 
                  onClick={() => handleStartEdit(comment)}
                  className="text-gray-300 hover:text-blue-500 p-1 transition-colors"
                  title="댓글 수정"
                >
                  <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M15.232 5.232l3.536 3.536m-2.036-5.036a2.5 2.5 0 113.536 3.536L6.5 21.036H3v-3.572L16.732 3.732z"/></svg>
                </button>
            
                <button 
                  onClick={() =>onDelete(comment.id)}
                  className="text-gray-300 hover:text-red-500 p-1 transition-colors"
                  title="댓글 삭제"
                >
                  <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"/></svg>
                </button>
              </div>
            </div>
          )}
        </div>
      ))}
    </div>
  );
}

/**
 * [BoardDetail 컴포넌트]
 * props 설명:
 * - post: 현재 화면에 보여줄 게시글 객체
 * - onEdit: 수정 버튼 클릭 시 실행될 함수 (App.jsx의 모드 변경 로직과 연결)
 * - onDelete: 삭제 버튼 클릭 시 실행될 함수 (App.jsx의 데이터 삭제 로직과 연결)
 * - onBack: 목록으로 돌아가기 버튼 클릭 시 실행될 함수
 */
export default function BoardDetail({ post, onEdit, onDelete, onBack,onAddComment,onDeleteComment,onEditComment}) {
  
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
        
         {/* 하단 댓글 관리 영역 */}
      <div className="bg-white rounded-[2rem] shadow-xl shadow-gray-200/50 border border-gray-100 p-10">
        <h3 className="font-extrabold text-xl text-gray-800 mb-8 flex items-center gap-3">
          <span className="p-2 bg-blue-50 text-blue-600 rounded-xl">💬</span>
          {/* post.comments(댓글들)이 있는지 없는지 체크 */}
          댓글 <span className="text-blue-600 ml-1">{post.comments?.length || 0}</span>
        </h3>
        
        {/* 댓글 목록 컴포넌트 호출(App.jsx->post ->BoardDetail(post.comment)-> CommendList) */}
        <CommentList comments={post.comments} 
                     onDelete={(commentId) => onDeleteComment(post.id,commentId)}
                     onEdit={(commentId,newText)=> onEditComment(post.id,commentId,newText)} />
        
        
        {/* 댓글 작성 폼 컴포넌트 호출 (comment(댓글폼에서 입력한 댓글데이터) */}
        <CommentForm onAdd={(comment) => onAddComment(post.id,comment)} />
        
      </div>  
      </div>
        {/* 하단 장식 또는 정보 영역 (필요 시 활용) */}
        {/* <div className="px-14 py-8 bg-gray-50/50 border-t border-gray-50 flex justify-between items-center text-gray-400 text-sm">
          <span>게시글 상세 정보 모드</span>
          <span className="italic font-mono">React CRUD System v1.0</span>
        </div>
      </div> */}
      {/*  */}
    </div>
  );
}