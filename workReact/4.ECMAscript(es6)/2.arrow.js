// 2.arrow.js 파일 작성 => 화살표 함수

// 기존 방식보다 간결하며, 리액트 컴포넌트 만들 때 필수입니다.
// function getStockAlert(price) {  }
const getStockAlert = (price) => {
    return price > 100000 ? "매수알림" : "관망"  // 3항 연산자
} // 여러줄 작성시

// 중괄호와 return도 생략 가능한 더 간결한 버전 
const addTax = (price) => price * 1.1  // 한줄 작성시

console.log(getStockAlert(120000))
console.log(`최종 가격: ${addTax(10000)}원`)
// 매수 알림
// 최종 가격: 11000원

// 추가 예제
