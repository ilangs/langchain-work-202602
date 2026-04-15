
import { useState, useEffect } from "react";

// onsave(저장함수) editingPost(모드=>list(글목록보기폼) or form(글쓰기폼=>신규글 or 수정글)) onCancel(취소 함수)
export default function BoardForm({ onSave, editingPost, onCancel }) {
  
  const [title,setTitle] = useState("")     // 글제목
  const [author,setAuthor] = useState("")   // 작성자
  const [content,setContent] = useState("") // 본문 내용
  // const [hobby, setHobby] = useState("")

  // 수정 폼 or 새글 작성폼
  useEffect(() => {
    if (editingPost) {
      setTitle(editingPost.title || "");
      setAuthor(editingPost.author || "");
      setContent(editingPost.content || "");
      // setHobby(editingPost.hobby || "");
    } else {
      setTitle(""); 
      setAuthor(""); 
      setContent(""); // 작성 모드 시 초기화
      //setHobby("");
    }
  }, [editingPost]);

  // 전송폼(데이터 전송) event객체(매개변수)
  const handleSubmit = (e) => {
    e.preventDefault();  // <a href="#">회원가입</a> 링크의 기본기능(이동하기)을 방해한다.
    // preventDefault 서버로 데이터 전송을 하지 못하게 하기 위해서 
    if (!title.trim() || !author.trim() || !content.trim()) {
      alert("모든 필드를 입력해 주세요.");
      return;  // 탈출문
    }

    onSave({
      id: editingPost ? editingPost.id : Date.now(), // 작성날짜
      title: title.trim(),
      author: author.trim(),
      content: content.trim(),
      //hobby: hobby.trim(),
      // 신규 작성 시 댓글 배열을 빈 상태로 생성 (댓글 기능용)
      comments: editingPost ? editingPost.comments : [] 
    });
  };

  return (
    <div className="w-full max-w-2xl mx-auto bg-white shadow-2xl shadow-gray-200/50 rounded-[2.5rem] border border-gray-100 overflow-hidden animate-in fade-in slide-in-from-bottom-8 duration-700">
      <div className="bg-gradient-to-r from-gray-50 to-white border-b border-gray-100 px-10 py-8">
        <h2 className="text-2xl font-black text-gray-800 flex items-center gap-3">
          <span className="p-2 bg-blue-100 text-blue-600 rounded-xl">
            {editingPost ? (
              <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2.5" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"/></svg>
            ) : (
              <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2.5" d="M12 4v16m8-8H4"/></svg>
            )}
          </span>
          {editingPost ? "게시글 수정하기" : "새 게시글 작성하기"}
        </h2>
        <p className="text-gray-400 text-sm mt-2 ml-14 font-medium italic">당신의 생각을 자유롭게 공유해 주세요.</p>
      </div>

      <form onSubmit={handleSubmit} className="p-10 space-y-8">
        <div className="space-y-6">
          <div className="space-y-2">
            <label className="text-[10px] font-black text-blue-500 uppercase tracking-[0.2em] ml-2 mb-2 block">Subject</label>
            <input
              className="w-full px-6 py-4 bg-gray-50 border-2 border-transparent rounded-2xl focus:border-blue-500 focus:bg-white outline-none transition-all shadow-inner font-bold text-gray-700 placeholder:text-gray-300 placeholder:font-normal"
              placeholder="멋진 제목을 지어주세요"
              value={title}
              // e.target=>현재 당신이 입력하는 입력박스
              onChange={(e) => setTitle(e.target.value)}  // 입력하고 있는 글
            />
          </div>

          <div className="space-y-2">
            <label className="text-[10px] font-black text-blue-500 uppercase tracking-[0.2em] ml-2 mb-2 block">Writer</label>
            <input
              className="w-full px-6 py-4 bg-gray-50 border-2 border-transparent rounded-2xl focus:border-blue-500 focus:bg-white outline-none transition-all shadow-inner font-bold text-gray-700 placeholder:text-gray-300 placeholder:font-normal"
              placeholder="작성자 성함"
              value={author}
              onChange={(e) => setAuthor(e.target.value)}
            />
          </div>

          <div className="space-y-2">
            <label className="text-[10px] font-black text-blue-500 uppercase tracking-[0.2em] ml-2 mb-2 block">Content</label>
            <textarea
              className="w-full px-6 py-5 bg-gray-50 border-2 border-transparent rounded-2xl focus:border-blue-500 focus:bg-white outline-none transition-all shadow-inner min-h-[250px] resize-none font-medium text-gray-700 leading-relaxed placeholder:text-gray-300 placeholder:font-normal"
              placeholder="마음을 담은 내용을 상세히 적어주세요..."
              value={content}
              onChange={(e) => setContent(e.target.value)}
            />
          </div>

            {/* <div className="space-y-2">
            <label className="text-[10px] font-black text-blue-500 uppercase tracking-[0.2em] ml-2 mb-2 block">Content</label>
            <textarea
              className="w-full px-6 py-5 bg-gray-50 border-2 border-transparent rounded-2xl focus:border-blue-500 focus:bg-white outline-none transition-all shadow-inner min-h-[250px] resize-none font-medium text-gray-700 leading-relaxed placeholder:text-gray-300 placeholder:font-normal"
              placeholder="취미를 알려 주세요..."
              value={hobby}
              onChange={(e) => setHobby(e.target.value)}
            />
          </div> */}

        </div>

        <div className="flex gap-4 pt-4">
          <button 
            type="button" 
            onClick={onCancel} 
            className="flex-1 px-8 py-4 bg-gray-100 text-gray-400 rounded-2xl font-black hover:bg-gray-200 hover:text-gray-600 transition-all active:scale-95"
          >취소하기</button>

          <button 
            type="submit" 
            className="flex-[2] bg-blue-600 text-white py-4 rounded-2xl font-black shadow-xl shadow-blue-200 hover:bg-blue-700 hover:-translate-y-1 transition-all active:scale-95"
          >{editingPost ? "수정사항 저장하기" : "지금 바로 게시하기"}</button>
        </div>
      </form>
    </div>
  );
}
