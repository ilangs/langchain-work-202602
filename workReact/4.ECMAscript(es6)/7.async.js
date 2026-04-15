// 7.async.js파일 작성

// 비동기 처리 (Async/Await) => 축약문법
// 비동기(Asynchronous): 서버에 요청을 보내고 응답을 기다리는 동안 멈추지 않고 다음 코드를 실행하는 방식
// Async/Await: 복잡한 비동기 코드를 마치 일반 코드처럼 위에서 아래로 읽기 쉽게 만들어주는 현대적인 문법

console.log("1. AI에게 분석 요청 전송");

// setTimeout()은 대표적인 비동기 함수 (2초 뒤에 실행)
//  -> 남발하면 속도 저하 단점 (LLM 호출 줄이기 위해 memory caching 기법 병행 필요)
setTimeout(() => {
    console.log("2. AI 에이전트의 답변 도착!"); // 실행할 문장
}, 2000);                                    // 2초뒤 실행

console.log("3. 다른 화면UI 먼저 그리기 (기다리지 않음)");
// 결과 출력 순서: 1->3->2(비동기 방식), 1->2->3(동기 방식)
/*
1. AI에게 분석 요청 전송
3. 다른 화면UI 먼저 그리기 (기다리지 않음)
2. AI 에이전트의 답변 도착!
*/

// 메모리 캐싱 예시
const cache = {}; // 결과를 저장할 객체

async function getLLMResponse(prompt) {
  // 1. 캐시에 이미 데이터가 있는지 확인
  if (cache[prompt]) {
    console.log("캐시된 결과 반환:", cache[prompt]);
    return cache[prompt];
  }

  // 2. 캐시에 없다면 실제 비동기 호출 수행
  const response = await callActualLLM(prompt); 
  
  // 3. 결과를 캐시에 저장
  cache[prompt] = response;
  return response;
}

// 메모리 캐싱보다 더 나은 대안들 (혼합 사용)

// Debounce	    : 짧은 시간 동안 연이어 발생한 이벤트를 하나로 묶어, 마지막 호출만 실행 (예: 검색어 입력)
// Throttle	    : 일정 시간 간격으로 최대 한 번만 실행되도록 제한 (예: 스크롤 이벤트)
// Local Storage: 브라우저를 껐다 켜도 유지되어야 하는 캐시 데이터 저장
// Redis        : 서버 사이드에서 대규모 캐시 데이터를 관리할 때 사용하는 고속 저장소
