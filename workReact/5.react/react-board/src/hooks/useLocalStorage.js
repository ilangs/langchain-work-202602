// React에서 상태와 lifecycle을 사용하기 위한 Hook import
import { useState, useEffect } from "react";

// localStorage와 상태를 연동하는 커스텀 훅 정의
// key: localStorage에 저장할 키 이름
// initialValue: 초기값
export default function useLocalStorage(key, initialValue) {

  // ==========================
  // [1] 상태 초기화
  // ==========================
  const [value, setValue] = useState(() => {

    try {
      // localStorage에서 key에 해당하는 값 가져오기 (문자열 형태)
      const stored = localStorage.getItem(key);

      // LocalStorage에는 무조건 문자열로 저장 (<=> 웹상은 배열형태로 저장)
      // 저장된 값이 있으면 JSON.parse로 객체/값으로 변환
      // 없으면 initialValue 사용
      return stored ? JSON.parse(stored) : initialValue;

    } catch (e) {
      // JSON 파싱 에러 또는 접근 에러 발생 시
      console.error(e); // 에러 출력

      // 안전하게 초기값 반환
      return initialValue;
    }
  });

  // ==========================
  // [2] 값이 변경될 때 localStorage 저장
  // ==========================
  useEffect(() => {

    try {
      // value를 문자열(JSON)로 변환해서 localStorage에 저장
      localStorage.setItem(key, JSON.stringify(value));

    } catch (error) {
      // 저장 중 에러 발생 시
      console.error("localStorage 저장 실패", error);
    }

  }, [key, value]); // key 또는 value가 바뀔 때마다 실행


  // ==========================
  // [3] 상태 반환
  // ==========================
  // 배열 형태로 반환 → useState처럼 사용 가능
  // ex) const [data, setData] = useLocalStorage(...)
  return [value, setValue];
}
