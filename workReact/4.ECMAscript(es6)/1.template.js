// 1.template.js -> node 이용 (html 없이 실행)

// ES6+ 핵심 문법

// 템플릿 리터럴(백틱문자열): + 대신 백틱(`)을 사용해 문자열과 변수를 우아하게 합칩니다.
// 화살표 함수 (Arrow Function): function 키워드 대신 =>를 사용하여 간결하게 함수를 만듭니다.
// 구조 분해 할당 (Destructuring): 객체나 배열의 값을 한 번에 쏙쏙 뽑아냅니다.
// 스프레드 연산자 (Spread): ...을 사용하여 데이터를 복사하거나 합칩니다.
// 배열 고차 함수 (map, filter): 반복문(for) 대신 사용하는 리액트의 필수 문법입니다

const company = "나노테크"
const state = "상승"

// 백틱(`)과 ${}를 사용하면 줄바꿈도 자유롭고 변수 삽입도 쉽습니다.
const report = `현재 ${company}의 주가는 
시장 분석 결과 '${state}'세입니다.`

// document.write(출력문) => html에서만 사용
console.log(report) // 훨씬 읽기 편한 코드가 됩니다.

// node 1.template.js
// 현재 나노테크의 주가는 
// 시장 분석 결과 '상승'세입니다.

// LLM 실습 => 새로운 예제 만들어 줘 -> 복습