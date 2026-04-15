import { useState } from "react";

function BoardForm({ fetchPosts }) {
  // 입력 상태
  const [title, setTitle] = useState("");
  const [content, setContent] = useState("");

  // 등록 함수
  const handleSubmit = async () => {
    // [보완] 간단한 유효성 검사
    if (!title.trim() || !content.trim()) {
      alert("제목과 내용을 모두 입력해주세요.");
      return;
    }

    try {
      const res = await fetch("http://localhost:8000/posts", {
        method: "POST", 
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ title, content }),
      });

      if (res.ok) {
        alert("글이 등록되었습니다.");
        // 입력 초기화
        setTitle("");
        setContent("");
        // 목록 갱신
        fetchPosts(); 
      } else {
        throw new Error("등록 실패");
      }
    } catch (err) {
      console.error("등록 중 오류 발생:", err);
      alert("서버와 통신 중 오류가 발생했습니다.");
    }
  };

  return (
    <div className="bg-white shadow-md rounded p-6 mb-6 w-3/4 mx-auto">
      <h2 className="text-xl font-semibold mb-4">글 작성</h2>

      {/* 제목 */}
      <input
        className="w-full border px-4 py-2 mb-3 rounded focus:outline-blue-400"
        placeholder="제목 입력"
        value={title}
        onChange={(e) => setTitle(e.target.value)}
      />

      {/* 내용 */}
      <textarea
        className="w-full border px-4 py-2 mb-3 rounded focus:outline-blue-400 h-32"
        placeholder="내용 입력"
        value={content}
        onChange={(e) => setContent(e.target.value)}
      />

      {/* 버튼 */}
      <button
        className="bg-green-500 text-white px-6 py-2 rounded font-bold hover:bg-green-600 transition-colors w-full md:w-auto"
        onClick={handleSubmit}
      >
        등록하기
      </button>
    </div>
  );
}

export default BoardForm;