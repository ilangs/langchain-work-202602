// 4.spread.js파일 작성
// ... -> spread 연산자

const originalSectors = ["IT", "바이오"];
// ...을 사용하면 기존 배열을 그대로 복사하고 새 데이터를 추가하기 쉽습니다.
const newSectors = [...originalSectors, "AI", "로봇"]; // 게시판의 글쓰기 (기존+새데이터)

const [first, second] = newSectors; 
// const first = newSectors[0];
// second = newSectors[1]; => 앞에서부터 순서대로 할당

const [main, ...others] = newSectors;
// main: "IT"
// others: ["바이오", "AI", "로봇"] => 나머지가 다시 배열이 됨

console.log(`주력 섹터: ${first}, ${second}`);
console.log(`전체 섹터:`, newSectors);

// 주력 섹터: IT, 바이오
// 전체 섹터: [ 'IT', '바이오', 'AI', '로봇' ]