// 9.async2.js => 축약형

// 함수앞에 async 붙이면 => 비동기 처리를 요청해주는 함수
const getAgentInfo = async () => {
    console.log("정보를 가져오는 중...")
    // 비동기 방식 async 함수내에 await를 이용해서 서버로부터 값을 가져온다.
    const info = await "에이전트 v2.0"
    console.log(`버젼 확인: ${info}`)
}
getAgentInfo()
/*
정보를 가져오는 중...
버젼 확인: 에이전트 v2.0
*/
