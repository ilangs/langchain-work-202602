// 3.objectDestriction.js파일 작성

const agent = {
    modelName: "금융봇",
    version: "2.0",
    skill: "재무분석"
};

// 객체의 키값과 동일한 변수명을 사용하여 데이터를 바로 추출합니다.
// const { 변수명1, 변수명2, 변수명3 } = 객체명

const { modelName, skill } = agent  // 객체의 키값과 동일한 변수명 사용

console.log(`${modelName}의 주특기는 ${skill}입니다.`)
// 금융봇의 주특기는 재무분석입니다.

//추가 => LLM 만들어 준 응용예제
const printAgent = ({ modelName, skill }) => {
    console.log(`${modelName}은 ${skill} 전문가입니다.`)
}

printAgent(agent)
//금융봇은 재무분석 전문가입니다.

