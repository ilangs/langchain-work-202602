// react-board2/src/components/Pagination.jsx
// 게시글 목록 하단에 표시되는 페이지네이션 컴포넌트
// - 현재 페이지 강조 표시
// - 이전/다음 페이지 버튼 제공

export default function Pagination({ currentPage, totalPages, onPageChange }) {
  /**
   * @param {number}   currentPage  - 현재 페이지 번호 (1부터 시작)
   * @param {number}   totalPages   - 전체 페이지 수
   * @param {Function} onPageChange - 페이지 변경 시 호출할 함수 (page 번호 전달)
   */

  // 전체 페이지가 1페이지 이하면 페이지네이션 렌더링 불필요
  if (totalPages <= 1) return null;

  // 페이지 번호 배열 생성 [1, 2, 3, ..., totalPages]
  const pages = Array.from({ length: totalPages }, (_, i) => i + 1);

  return (
    <div className="flex items-center justify-center gap-2 mt-6">

      {/* 이전 페이지 버튼 */}
      <button
        className="px-3 py-1 rounded border text-sm text-gray-600
                   hover:bg-gray-100 disabled:opacity-40 disabled:cursor-not-allowed"
        onClick={() => onPageChange(currentPage - 1)}
        disabled={currentPage === 1}  // 첫 페이지면 비활성화
      >
        ◀ 이전
      </button>

      {/* 페이지 번호 버튼 목록 */}
      {pages.map((page) => (
        <button
          key={page}
          className={`px-3 py-1 rounded border text-sm transition
            ${page === currentPage
              ? "bg-blue-500 text-white border-blue-500"   // 현재 페이지 강조
              : "text-gray-600 hover:bg-gray-100"          // 비활성 페이지
            }`}
          onClick={() => onPageChange(page)}
        >
          {page}
        </button>
      ))}

      {/* 다음 페이지 버튼 */}
      <button
        className="px-3 py-1 rounded border text-sm text-gray-600
                   hover:bg-gray-100 disabled:opacity-40 disabled:cursor-not-allowed"
        onClick={() => onPageChange(currentPage + 1)}
        disabled={currentPage === totalPages}  // 마지막 페이지면 비활성화
      >
        다음 ▶
      </button>

    </div>
  );
}
