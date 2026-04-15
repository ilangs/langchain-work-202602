// 5.map.js파일 작성 

// map(메서드): 배열의 모든 요소를 '가공(변형)'해서 같은 길이의 배열을 만듭니다.(인덱스 순서대로)

const prices = [100, 200, 300];

// 함수(함수를 전달(매개변수)=>콜백함수)  .map(()=>~)
const doubledPrices = prices.map(price => price * 2);

console.log(doubledPrices);  
/* 
[ 200, 400, 600 ]
*/

//추가
const users = [
    { name: "Tom", age: 20 },  // 익명 객체 1: user = { name: "Tom", age: 20 }
    { name: "Jane", age: 30 }  // 익명 객체 2: user = { name: "Jane", age: 30 }
];

// user -> 익명 객체를 지칭하는 임시 이름
const newUsers = users.map(user => ({ ...user, isAdult: user.age >= 20 }));
console.log('newUsers=>',newUsers);
/*
newUsers=> [
  { name: 'Tom', age: 20, isAdult: true },
  { name: 'Jane', age: 30, isAdult: true }
]
*/