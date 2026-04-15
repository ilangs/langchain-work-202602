// 6.filter.js파일 작성 

// filter(메서드): 배열의 요소 중 조건에 맞는 것만 골라내서(추출) 길이가 같거나 짧은 배열을 만듭니다.

const stocks = [
    { name: "삼성", price: 70000 }, // 익명객체들 -> 함수의 매개변수로 전달시 임의의 객체명 지정
    { name: "애플", price: 250000 },
    { name: "엔비디아", price: 150000 }
];

// 조건에 맞는 데이터만 골라내어 새로운 배열을 만듭니다.
const expensiveStocks = stocks.filter(stock => stock.price >= 150000);
console.log(expensiveStocks); // 애플과 엔비디아만 남습니다.
/*
[ { name: '애플', price: 250000 }, { name: '엔비디아', price: 150000 } ]
*/

// map과 filter를 같이 사용=>es6문법에서 함수를 여러개 나열해서 실행=>체이닝 메서드 방법
const result = stocks
               .filter(stock => stock.price >= 150000)
               .map(stock => stock.name);
console.log('result=>',result)
/*
result=> [ '애플', '엔비디아' ]
*/