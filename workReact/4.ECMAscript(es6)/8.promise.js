// 8.promise.js 파일

// react,vue에서 많이 사용 (비동기 방식을 처리해주는 객체)
// Promise(생성자): 미래에 올 데이터를 약속하는 객체 (대기, 성공, 실패 상태가 있음)
// 예외 처리 (Try-Catch): 네트워크 오류나 서버 에러가 발생했을 때 프로그램이 죽지 않게 관리

const analyzeStock = new Promise((resolve, reject) => {
    const success = true;  // 서버 상황 가정
    
    if (success) {
        resolve("분석 완료!");       // 성공 시 호출=>성공시 결과 받음(json데이터)
    } else {
        reject("서버 연결 실패...");  // 실패 시 호출
    }
})

analyzeStock
    .then(res => console.log(res))  // resolve 호출 시 실행
    .catch(err => console.log(err)) // reject 호출 시 실행

/*
분석 완료!
*/