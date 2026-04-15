// Pagination 컴포넌트
// props:
//  ㄴ total: 전체 데이터 개수
//  ㄴ pageSize: 한 페이지당 데이터 개수
//  ㄴ current: 현재 페이지
//  ㄴ onChange: 페이지 변경 함수

export default function Pagination({ total, pageSize, current, onChange }) {

  // ==========================
  // [1] 전체 페이지 수 계산
  // ==========================
  const totalPages = Math.max(1, Math.ceil(total / pageSize));

  // ==========================
  // [2] 블럭 설정 (핵심)
  // ==========================
  const blockSize = 5; //  여기 숫자 바꾸면 "페이지 개수" 변경됨

  const currentBlock = Math.ceil(current / blockSize);             // 현재 블럭
  const startPage = (currentBlock - 1) * blockSize + 1;            // 시작 페이지
  const endPage = Math.min(startPage + blockSize - 1, totalPages); // 끝 페이지

  return (
    <div className="flex gap-2 mt-4 items-center">

      {/* =============================== */}
      {/* [3] 처음 페이지 이동 */}
      {/* =============================== */}
      <button
        disabled={current === 1}
        className="px-3 py-1 border rounded disabled:opacity-50"
        onClick={() => onChange(1)}
      >
        {"<<"}
      </button>

      {/* =============================== */}
      {/* [4] 이전 블럭 이동 */}
      {/* =============================== */}
      <button
        disabled={startPage === 1}
        className="px-3 py-1 border rounded disabled:opacity-50"
        onClick={() => onChange(startPage - 1)}
      >
        {"<"}
      </button>

      {/* =============================== */}
      {/* [5] 이전 페이지 */}
      {/* =============================== */}
      {/* <button
        disabled={current === 1}
        className="px-3 py-1 border rounded disabled:opacity-50"
        onClick={() => onChange(Math.max(1, current - 1))}
      >
        이전
      </button> */}

      {/* =============================== */}
      {/* [6] 페이지 번호 목록 (핵심) */}
      {/* =============================== */}
      {[...Array(endPage - startPage + 1)].map((_, i) => {
        const page = startPage + i;

        return (
          <button
            key={`page-${page}`}
            className={`px-3 py-1 border rounded ${
              current === page
                ? "bg-blue-500 text-white"
                : "bg-white"
            }`}
            onClick={() => onChange(page)}
          >
            {page}
          </button>
        );
      })}

      {/* =============================== */}
      {/* [7] 다음 페이지 */}
      {/* =============================== */}
      {/* <button
        disabled={current === totalPages}
        className="px-3 py-1 border rounded disabled:opacity-50"
        onClick={() => onChange(Math.min(totalPages, current + 1))}
      >
        다음
      </button> */}

      {/* ========================== */}
      {/* [8] 다음 블럭 이동 */}
      {/* ========================== */}
      <button
        disabled={endPage === totalPages}
        className="px-3 py-1 border rounded disabled:opacity-50"
        onClick={() => onChange(endPage + 1)}
      >
        {">"}
      </button>

      {/* ========================== */}
      {/* [9] 마지막 페이지 이동 */}
      {/* ========================== */}
      <button
        disabled={current === totalPages}
        className="px-3 py-1 border rounded disabled:opacity-50"
        onClick={() => onChange(totalPages)}
      >
        {">>"}
      </button>

    </div>
  );
}