// 2.src/components/Pagination.jsx

// Pagination 컴포넌트 정의
// props:
//  ㄴ total: 전체 레코드(데이터) 개수
//  ㄴ pageSize: 한 페이지당 레코드(데이터) 개수
//  ㄴ current: 현재 페이지 번호
//  ㄴ onChange: 페이지 변경 함수
export default function Pagination({ total, pageSize, current, onChange }) {

  // 전체 페이지 수 계산
  // Math.ceil: 나누어 떨어지지 않으면 올림 처리
  // Math.max(1, ...): 최소 1페이지는 유지 (데이터가 0개여도 UI 깨짐 방지)
  const totalPages = Math.max(1, Math.ceil(total / pageSize)); //122/10=12.2=>13 -> max(1,13)=>13

  return (
    // 페이지 버튼들을 가로로 정렬하는 컨테이너, flex: 가로 정렬, gap-2: 버튼 간 간격, mt-4: 위쪽 여백
    <div className="flex gap-2 mt-4">

      {/* =============================== */}
      {/*  이전 버튼  */}
      {/* =============================== */}
      <button
        // 현재 페이지가 1이면 이전 페이지가 없으므로 버튼 비활성화
        disabled={current === 1}
        // Tailwind 스타일, disabled 상태일 때 opacity(투명도) 낮춰서 비활성 느낌 표시
        className="px-3 py-1 border rounded disabled:opacity-50"
        // 클릭 시 현재 페이지 -1 -> Math.max(1, ...)로 1보다 작아지지 않도록 방어 코드
        onClick={() => onChange(Math.max(1, current - 1))}
      >이전</button>

      {/* totalPages 만큼 반복해서 페이지 버튼 생성
        Array(totalPages): 길이만 있는 배열 생성 (비어있음)
        [...Array(totalPages)]: 실제 값이 있는 배열로 변환 → map 사용 가능 */}

      {[...Array(totalPages)].map((_, i) => (

        //===============================
        //   각 페이지 버튼
        //===============================
        <button
          // React 리스트 렌더링 시 필수 key -> 문자열로 명확하게 지정 (충돌 방지)
          key={`page-${i}`}
          // Tailwind 스타일, 현재 페이지이면 파란색 강조 아니면 기본 흰색
          className={`px-3 py-1 border rounded ${current === i + 1 ? "bg-blue-500 text-white":"bg-white"}`}
          // 클릭 시 해당 페이지로 이동, i는 0부터 시작하므로 실제 페이지는 i+1
          onClick={() => onChange(i + 1)} 
        >{i + 1}</button>
      ))}

      {/* =============================== */}
      {/*   다음 버튼   */}
      {/* =============================== */}
      <button
        // 현재 페이지가 마지막 페이지이면 더 이상 다음 없음 → 비활성화
        disabled={current === totalPages}
        // Tailwind 스타일 (이전 버튼과 동일)
        className="px-3 py-1 border rounded disabled:opacity-50"
        // 클릭 시 현재 페이지 +1 -> Math.min으로 마지막 페이지 초과 방지
        onClick={() => onChange(Math.min(totalPages, current + 1))}
      >다음</button>

    </div>
  );
}
