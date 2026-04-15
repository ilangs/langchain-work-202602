// react-board2/src/pages/PostForm.jsx
// 게시글 작성 / 수정 페이지 (하나의 컴포넌트로 통합)
// - /posts/new    → 새 게시글 작성 모드
// - /posts/:id/edit → 기존 게시글 수정 모드 (기존 내용 자동 로드)

import { useEffect, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";
import api from "../api/axios";
import Navbar from "../components/Navbar";

export default function PostForm({ user, onLogout }) {
  /**
   * @param {Object|null} user     - 전역 로그인 사용자 정보
   * @param {Function}    onLogout - 로그아웃 처리 함수
   */

  // URL 파라미터에서 id 추출
  // - /posts/new     → id = undefined → 작성 모드
  // - /posts/:id/edit → id = 숫자    → 수정 모드
  const { id } = useParams();
  const isEditMode = !!id;  // id 존재 여부로 작성/수정 모드 구분

  const navigate = useNavigate();

  // =========================
  // 상태 관리
  // =========================
  const [form, setForm] = useState({
    title: "",    // 게시글 제목
    content: "",  // 게시글 내용
  });
  const [loading, setLoading] = useState(false);       // 제출 버튼 로딩
  const [fetching, setFetching] = useState(isEditMode); // 수정 모드일 때 기존 데이터 로딩

  // =========================
  // 수정 모드: 기존 게시글 데이터 로드
  // =========================
  useEffect(() => {
    if (!isEditMode) return;  // 작성 모드면 스킵

    const fetchPost = async () => {
      try {
        // GET /posts/:id → 기존 게시글 내용 조회
        const res = await api.get(`/posts/${id}`);

        // 작성자 본인 확인 (다른 사람의 게시글 수정 시도 방지)
        if (user && res.data.user_id !== user.id) {
          alert("수정 권한이 없습니다.");
          navigate(`/posts/${id}`);
          return;
        }

        // 기존 내용을 폼에 미리 채움
        setForm({
          title: res.data.title,
          content: res.data.content,
        });
      } catch (err) {
        alert("게시글을 불러올 수 없습니다.");
        navigate("/posts");
      } finally {
        setFetching(false);  // 데이터 로딩 완료
      }
    };

    fetchPost();
  }, [id]);  // id가 바뀌면 재조회

  // =========================
  // 입력값 공통 핸들러
  // =========================
  const handleChange = (e) => {
    // name 속성을 key로 사용하여 해당 필드만 업데이트
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  // =========================
  // 폼 제출 (작성 or 수정)
  // =========================
  const handleSubmit = async () => {
    // 제목, 내용 필수 입력 확인
    if (!form.title.trim() || !form.content.trim()) {
      alert("제목과 내용을 모두 입력해주세요.");
      return;
    }

    setLoading(true);

    try {
      if (isEditMode) {
        // 수정 모드: PUT /posts/:id (Authorization 헤더 자동 첨부)
        await api.put(`/posts/${id}`, form);
        alert("게시글이 수정되었습니다.");
        navigate(`/posts/${id}`);  // 수정 후 상세 페이지로 이동
      } else {
        // 작성 모드: POST /posts (Authorization 헤더 자동 첨부)
        const res = await api.post("/posts", form);
        alert("게시글이 작성되었습니다.");
        navigate(`/posts/${res.data.id}`);  // 작성 후 새 게시글 상세 페이지로 이동
      }
    } catch (err) {
      alert(err.response?.data?.detail || "저장에 실패했습니다.");
    } finally {
      setLoading(false);
    }
  };

  // =========================
  // 수정 모드 초기 데이터 로딩 중
  // =========================
  if (fetching) {
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
        <div className="bg-white rounded-xl shadow-md p-6">

          {/* 페이지 타이틀 (작성/수정 모드 구분) */}
          <h1 className="text-2xl font-bold text-gray-800 mb-6">
            {isEditMode ? "✏️ 게시글 수정" : "📝 게시글 작성"}
          </h1>

          {/* 제목 입력 */}
          <input
            type="text"
            name="title"                      // handleChange에서 key로 사용
            placeholder="제목을 입력하세요"
            value={form.title}                // controlled input
            className="w-full border px-3 py-2 rounded-lg mb-4 text-sm
                       focus:outline-none focus:ring-2 focus:ring-blue-400"
            onChange={handleChange}
          />

          {/* 내용 입력 */}
          <textarea
            name="content"
            placeholder="내용을 입력하세요"
            value={form.content}
            rows={12}
            className="w-full border px-3 py-2 rounded-lg mb-4 text-sm
                       resize-none focus:outline-none focus:ring-2 focus:ring-blue-400"
            onChange={handleChange}
          />

          {/* 버튼 영역 */}
          <div className="flex gap-3 justify-end">

            {/* 취소 버튼 */}
            <button
              className="px-5 py-2 text-sm bg-gray-200 text-gray-700
                         rounded-lg hover:bg-gray-300 transition"
              onClick={() => navigate(isEditMode ? `/posts/${id}` : "/posts")}
            >
              취소
            </button>

            {/* 제출 버튼 (작성/수정 모드 텍스트 구분) */}
            <button
              className={`px-5 py-2 text-sm text-white rounded-lg transition
                ${loading
                  ? "bg-blue-300 cursor-not-allowed"
                  : "bg-blue-500 hover:bg-blue-600"
                }`}
              onClick={handleSubmit}
              disabled={loading}
            >
              {loading ? "저장 중..." : isEditMode ? "수정 완료" : "작성 완료"}
            </button>

          </div>
        </div>
      </div>
    </div>
  );
}
