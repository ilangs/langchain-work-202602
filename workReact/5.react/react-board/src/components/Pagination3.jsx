// ==============================================
// Pagination 컴포넌트
//
// Props:
//   total     - 전체 데이터 개수
//   pageSize  - 페이지당 데이터 개수
//   current   - 현재 페이지 번호
//   onChange  - 페이지 변경 콜백 (page: number) => void
// ==============================================

export default function Pagination({ total, pageSize, current, onChange }) {

  // 전체 페이지 수 (최소 1)
  const totalPages = Math.max(1, Math.ceil(total / pageSize));

  // 블럭당 표시할 페이지 수 (변경 시 이 값만 수정)
  const blockSize = 5;

  // 현재 블럭의 시작/끝 페이지 계산
  const currentBlock = Math.ceil(current / blockSize);
  const startPage   = (currentBlock - 1) * blockSize + 1;
  const endPage     = Math.min(startPage + blockSize - 1, totalPages);

  // 공통 버튼 스타일
  const baseBtn     = "px-3 py-1 border rounded disabled:opacity-50";
  const activeBtn   = "bg-blue-500 text-white";
  const inactiveBtn = "bg-white";

  return (
    <div className="flex gap-2 mt-4 items-center">

      {/* 첫 페이지로 이동 */}
      <button
        disabled={current === 1}
        className={baseBtn}
        onClick={() => onChange(1)}
      >
        {"<<"}
      </button>

      {/* 이전 블럭으로 이동 (블럭의 마지막 페이지로) */}
      <button
        disabled={startPage === 1}
        className={baseBtn}
        onClick={() => onChange(startPage - 1)}
      >
        {"<"}
      </button>

      {/* 현재 블럭의 페이지 번호 목록 */}
      {Array.from({ length: endPage - startPage + 1 }, (_, i) => startPage + i).map((page) => (
        <button
          key={page}
          className={`${baseBtn} ${current === page ? activeBtn : inactiveBtn}`}
          onClick={() => onChange(page)}
        >
          {page}
        </button>
      ))}

      {/* 다음 블럭으로 이동 (블럭의 첫 페이지로) */}
      <button
        disabled={endPage === totalPages}
        className={baseBtn}
        onClick={() => onChange(endPage + 1)}
      >
        {">"}
      </button>

      {/* 마지막 페이지로 이동 */}
      <button
        disabled={current === totalPages}
        className={baseBtn}
        onClick={() => onChange(totalPages)}
      >
        {">>"}
      </button>

    </div>
  );
}