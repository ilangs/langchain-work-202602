import { useState } from "react";

function BoardList({ posts, fetchPosts }) {
  // 수정 상태 관리
  const [editId, setEditId] = useState(null); // 현재 수정 중인 게시글의 ID
  const [editTitle, setEditTitle] = useState(""); // 수정할 제목 입력값
  const [editContent, setEditContent] = useState(""); // 수정할 내용 입력값

  const API_URL = "http://localhost:8000/posts";

  // =========================
  // [1] 삭제 기능
  // =========================
  const handleDelete = async (id) => {
    if (!window.confirm("정말 삭제하시겠습니까?")) return;

    try {
      const res = await fetch(`${API_URL}/${id}`, {
        method: "DELETE",
      });

      if (res.ok) {
        alert("삭제되었습니다.");
        fetchPosts(); // 삭제 후 목록 새로고침
      } else {
        throw new Error("삭제 실패");
      }
    } catch (err) {
      console.error(err);
      alert("삭제 중 오류가 발생했습니다.");
    }
  };

  // =========================
  // [2] 수정 시작 (모드 전환)
  // =========================
  const handleEdit = (post) => {
    setEditId(post.id); // 해당 행을 수정 모드로 전환
    setEditTitle(post.title); // 기존 제목을 input에 세팅
    setEditContent(post.content); // 기존 내용을 input에 세팅
  };

  // =========================
  // [3] 수정 저장 (PUT 요청)
  // =========================
  const handleUpdate = async () => {
    try {
      const res = await fetch(`${API_URL}/${editId}`, {
        method: "PUT",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          title: editTitle,     // 수정된 제목
          content: editContent, // 수정된 내용
        }),
      });

      if (res.ok) {
        alert("수정되었습니다.");
        setEditId(null);        // 수정 모드 종료
        fetchPosts();           // 수정 후 목록 새로고침
      } else {
        throw new Error("수정 실패");
      }
    } catch (err) {
      console.error(err);
      alert("수정 중 오류가 발생했습니다.");
    }
  };

  return (
    <div className="w-3/4 mx-auto bg-white shadow-md rounded overflow-hidden mt-6">
      <table className="w-full text-center border">
        {/* 헤더 */}
        <thead className="bg-gray-100">
          <tr>
            <th className="p-3 border">ID</th>
            <th className="p-3 border">제목</th>
            <th className="p-3 border">내용</th>
            <th className="p-3 border">수정</th>
            <th className="p-3 border">삭제</th>
          </tr>
        </thead>

        {/* 본문 */}
        <tbody>
          {posts.map((post) => (
            <tr key={post.id} className="hover:bg-gray-50 transition">
              <td className="p-3 border">{post.id}</td>

              {/* 제목 영역 */}
              <td className="p-3 border">
                {editId === post.id ? (
                  <input
                    className="border px-2 py-1 w-full"
                    value={editTitle}
                    onChange={(e) => setEditTitle(e.target.value)}
                  />
                ) : (
                  post.title
                )}
              </td>

              {/* 내용 영역 */}
              <td className="p-3 border">
                {editId === post.id ? (
                  <input
                    className="border px-2 py-1 w-full"
                    value={editContent}
                    onChange={(e) => setEditContent(e.target.value)}
                  />
                ) : (
                  post.content
                )}
              </td>

              {/* 수정/저장 버튼 */}
              <td className="p-3 border">
                {editId === post.id ? (
                  <button
                    className="bg-blue-500 text-white px-3 py-1 rounded hover:bg-blue-600"
                    onClick={handleUpdate}
                  >
                    저장
                  </button>
                ) : (
                  <button
                    className="bg-yellow-500 text-white px-3 py-1 rounded hover:bg-yellow-600"
                    onClick={() => handleEdit(post)}
                  >
                    수정
                  </button>
                )}
              </td>

              {/* 삭제 버튼 */}
              <td className="p-3 border">
                <button
                  className="bg-red-500 text-white px-3 py-1 rounded hover:bg-red-600"
                  onClick={() => handleDelete(post.id)}
                >
                  삭제
                </button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default BoardList;