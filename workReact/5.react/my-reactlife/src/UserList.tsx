import { useState, useEffect } from "react";

// 사용자 목록 테이블 컴포넌트
function UserList() {

  // 사용자 데이터 상태 (배열)
  const [users, setUsers] = useState<any[]>([]);

  // 로딩 상태 (true = 로딩 중)
  const [loading, setLoading] = useState<boolean>(true);
  
  // ==========================
  // [추가] 검색 상태
  // ==========================
  const [search, setSearch] = useState<string>(""); // 검색어 상태

  // ==========================
  // [추가] 정렬 상태
  // ==========================
  const [asc, setAsc] = useState<boolean>(true); // 정렬 방향 (true=오름차순)


  // ==========================
  // [1] 데이터 요청 (Mount)
  // ==========================
  useEffect(() => {

    // 비동기 함수 선언
    const fetchData = async () => {

      // API 요청
      const res = await fetch("https://jsonplaceholder.typicode.com/users");

      // JSON 변환
      const data = await res.json();

      // 상태 업데이트
      setUsers(data);

      // 로딩 종료
      setLoading(false);
    };

    // 함수 실행
    fetchData();

  }, []); // 최초 1회 실행

  // =========================================================
  // [추가] 검색 필터 (영문자(대/소문자 구분=>소문자로 변경하여 검색))
  // =========================================================
  const filteredUsers = users.filter((user) => // users 배열 필터링
    user.name.toLowerCase().includes(search.toLowerCase()) // 이름 기준 검색
  ); // 불러온 데이터도 소문자로 변경 == 검색한 데이터도 소문자로 변경
     // toUpperCase()(대문자로 변경)

  // ===============================================================
  // [추가] 정렬 처리 (자바스크립트에서 배열을 변경시킬 때 => 원본배열 복사)
  // ===============================================================
  const sortedUsers = [...filteredUsers].sort((a, b) => // 배열 복사 후 정렬
    asc // 숫자 정렬 5 > 3, 문자열 정렬(a.name > b.name (X) -> localeCompare 함수 사용)
      ? a.name.localeCompare(b.name) // 오름차순 (작은값->큰값) A->Z
      // "apple".localCompare("banana")
      : b.name.localeCompare(a.name) // 내림차순 (큰값->작은값) Z->A
      // "banana".localCompare("apple")
  );

  // ==========================
  // [2] UI (테이블 출력)
  // ==========================
  return (
  // p-6 → padding 1.5rem (전체 여백)
  <div className="p-6">

    {/* text-2xl → 글자 크기 크게
        font-bold → 글자 굵게
        mb-4 → margin-bottom 1rem (아래 여백) */}
    <h2 className="text-2xl font-bold mb-4">User List</h2>

    {/* ==========================
          [추가] 검색 입력창
      ========================== */}
      <input
        className="bg-gray-200 border p-2 mb-4 w-full text-black rounded" // 테두리 + 여백 + 전체 너비
        placeholder="Search name..." // 안내 텍스트
        value={search} // 입력값 상태 연결 value=""
        // onChange이벤트 -> 입력상자의 값이 변동이 있을 때마다 호출되는 이벤트 종류
        // 콤보박스의 항목을 선택하는 경우(=event 객체)
        // event객체(사용자들의 모든 행동(키보드,마우스,터치)정보)
        // e.target=>이벤트가 발생된 객체(input box) value=>검색문자열
        onChange={(e) => setSearch(e.target.value)} // 입력 시 상태 변경
      />

      {/*=======================
          [추가] 정렬 버튼
         =======================*/}
      <button
        className="mb-4 px-4 py-2 bg-green-500 text-white rounded" // 버튼 스타일
        onClick={() => setAsc(!asc)} // 클릭 시 정렬 방향 변경
      >
        Sort ({asc ? "ASC" : "DESC"}) {/* 상태 표시 (삼항연산자) */}
      </button>


    {/* text-gray-500 → 회색 텍스트 */}
    {loading && <p className="text-gray-500">Loading...</p>}

    {!loading && (
      // min-w-full → 최소 너비 100%
      // border → 전체 테두리
      // border-gray-300 → 연한 회색 테두리
      // rounded-lg → 테두리 둥글게
      // overflow-hidden → 넘치는 부분 숨김 (둥근 테두리 유지)
      <table className="min-w-full border border-gray-300 rounded-lg overflow-hidden">

        {/* bg-blue-500 → 파란 배경
            text-white → 흰색 글자 */}
        <thead className="bg-blue-500 text-white">
          <tr>

            {/* py-2 → 위아래 padding 0.5rem
                px-4 → 좌우 padding 1rem
                border → 셀 테두리 */}
            <th className="py-2 px-4 border">ID</th>

            <th className="py-2 px-4 border">Name</th>

            <th className="py-2 px-4 border">Email</th>

            <th className="py-2 px-4 border">City</th>

          </tr>
        </thead>

        <tbody>
          {/* {users.map((user) => ( */}
          {sortedUsers.map((user) => (

            // text-center → 텍스트 가운데 정렬
            // hover:bg-gray-100 → 마우스 올리면 연한 회색 배경
            <tr key={user.id} className="text-center hover:bg-gray-100">

              {/* py-2 → 위아래 여백
                  px-4 → 좌우 여백
                  border → 셀 테두리 */}
              <td className="py-2 px-4 border">
                {user.id}
              </td>

              <td className="py-2 px-4 border">
                {user.name}
              </td>

              <td className="py-2 px-4 border">
                {user.email}
              </td>

              <td className="py-2 px-4 border">
                {user.address.city}
              </td>

            </tr>
          ))}
        </tbody>

      </table>
    )}

  </div>
);
}

export default UserList;