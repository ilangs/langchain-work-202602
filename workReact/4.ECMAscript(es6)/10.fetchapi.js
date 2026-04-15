// 10.fetchapi.js파일 작성

// Fetch API: 백엔드(AI 에이전트 서버)로부터 데이터를 가져오는 표준 방법
// fetch 메서드

// 실제 공개 API를 호출하는 예제
const fetchPost = async () => {
    // 서버에 데이터를 요청하고 응답이 올 때까지 기다린다.
    const response = await fetch('https://jsonplaceholder.typicode.com/posts/1');
    const data = await response.json();      // 응답 데이터를 JSON 형태로 변환
    console.log(data);
    console.log("가져온 데이터:", data.title); // json데이터에서 특정 항목만 출력 
};
fetchPost();
/*
{
  userId: 1,
  id: 1,
  title: 'sunt aut facere repellat provident occaecati excepturi optio reprehenderit',
  body: 'quia et suscipit\n' +
    'suscipit recusandae consequuntur expedita et cum\n' +
    'reprehenderit molestiae ut ut quas totam\n' +
    'nostrum rerum est autem sunt rem eveniet architecto'
}
가져온 데이터: sunt aut facere repellat provident occaecati excepturi optio reprehenderit
*/