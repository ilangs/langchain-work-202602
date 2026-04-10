// ========================================================
// App.jsx - 영화 심리 처방 에이전트 (프론트엔드 메인 파일)
//
// 【전체 구조 요약】
//  1. MovieCard    : 영화 1편을 카드로 보여주는 컴포넌트
//  2. ChatMessage  : 채팅 말풍선(유저/봇/영화카드)을 처리하는 컴포넌트
//  3. LoadingDots  : AI 응답 대기 중 애니메이션 컴포넌트
//  4. App (default): 전체 앱을 조립하는 최상위 컴포넌트
//
// 【백엔드 연결 방식】
//  - SSE(Server-Sent Events) : 서버가 데이터를 실시간으로 밀어주는 단방향 스트리밍
//  - EventSource API를 사용해 /chat_stream 엔드포인트에 연결
// ========================================================

// React 핵심 훅 3가지 import
// - useState  : 컴포넌트 내부 상태(데이터) 관리
// - useRef    : DOM 요소에 직접 접근 (스크롤, input 포커스 등)
// - useEffect : 상태 변화 시 자동 실행되는 사이드이펙트 처리
import { useState, useRef, useEffect } from "react";

// ─── 상수 정의 ──────────────────────────────────────────
// 백엔드 FastAPI 서버 주소
// 개발환경에서는 localhost:8000 고정 (배포 시 실제 서버 주소로 변경)
const API_BASE = "http://localhost:8000";


// ================================================================
// 【컴포넌트 1】 MovieCard
// 역할 : 영화 1편의 정보를 카드 형태로 렌더링
// props: movie (영화 데이터 객체), index (카드 순서 - 애니메이션 딜레이용)
// ================================================================
function MovieCard({ movie, index }) {

  // 추천 사유(reason)를 '/' 기준으로 분리해서 배열로 만들기
  // 예) "힐링 영화 / 가족과 함께" → ["힐링 영화 ", " 가족과 함께"]
  // movie.reason이 없을 경우 빈 배열로 처리 (옵셔널 체이닝 ?.)
  const reasons = movie.reason ? movie.reason.split("/") : [];

  return (
    // 카드 컨테이너 - CSS 클래스로 스타일 적용
    // style 속성으로 카드마다 등장 애니메이션 시작 시간을 다르게 설정
    // index * 120ms → 0번 카드는 0ms, 1번은 120ms, 2번은 240ms 후 등장
    <div
      className="movie-card"
      style={{ animationDelay: `${index * 120}ms` }}
    >
      {/* ── 포스터 영역 ── */}
      <div className="poster-wrap">
        {/* 포스터 이미지가 있으면 img 태그, 없으면 이모지로 대체 */}
        {movie.poster ? (
          <img src={movie.poster} alt={movie.title} className="poster-img" />
        ) : (
          <div className="poster-placeholder">🎬</div>
        )}
        {/* 평점 배지 - 포스터 우하단에 절대 위치로 표시 */}
        <span className="rating-badge">⭐ {movie.rating}</span>
      </div>

      {/* ── 카드 텍스트 내용 영역 ── */}
      <div className="card-body">

        {/* 추천 사유 목록: 배열을 map()으로 순회하며 각 줄을 <p>로 출력 */}
        {/* key={i} : React가 목록 항목을 구분하기 위해 필요한 고유값 */}
        <div className="reason-box">
          {reasons.map((line, i) => (
            <p key={i} className="reason-line">
              {line.trim()} {/* trim() : 앞뒤 공백 제거 */}
            </p>
          ))}
        </div>

        {/* 구분선 */}
        <div className="divider" />

        {/* 영화 제목 */}
        <h3 className="movie-title">{movie.title}</h3>

        {/* 줄거리 요약 (백엔드에서 60자로 잘라서 전달) */}
        <p className="movie-desc">{movie.desc}</p>
      </div>
    </div>
  );
}


// ================================================================
// 【컴포넌트 2】 ChatMessage
// 역할 : 메시지 종류에 따라 다른 UI를 렌더링
//        - sender === "user"      → 오른쪽 파란 말풍선
//        - type === "empathy"     → 왼쪽 봇 공감 말풍선
//        - type === "movies"      → 영화 카드 5장 그리드
// props: msg (메시지 객체)
// ================================================================
function ChatMessage({ msg }) {

  // ① 유저 메시지 : 오른쪽 정렬 말풍선
  if (msg.sender === "user") {
    return (
      // justify-end : Flexbox에서 오른쪽 정렬 (Tailwind 클래스)
      <div className="flex justify-end mb-4">
        <div className="user-bubble">{msg.text}</div>
      </div>
    );
  }

  // ② 봇 공감 멘트 : 왼쪽 정렬 말풍선 (금색 텍스트)
  if (msg.type === "empathy") {
    return (
      <div className="mb-3">
        <div className="empathy-bubble">
          <span className="bot-avatar">🎭</span>
          {/* white-space: pre-line → '\n' 줄바꿈 문자를 실제 줄바꿈으로 처리 */}
          <p className="empathy-text">{msg.text}</p>
        </div>
      </div>
    );
  }

  // ③ 영화 카드 목록 : 5장을 그리드로 출력
  if (msg.type === "movies") {
    return (
      <div className="mb-6">
        <div className="cards-grid">
          {/* msg.movies 배열을 순회하며 MovieCard 컴포넌트 생성 */}
          {/* index(i)를 전달해 카드별 애니메이션 딜레이 적용 */}
          {msg.movies.map((m, i) => (
            <MovieCard key={i} movie={m} index={i} />
          ))}
        </div>
      </div>
    );
  }

  // 위 조건에 모두 해당하지 않으면 아무것도 렌더링하지 않음
  return null;
}


// ================================================================
// 【컴포넌트 3】 LoadingDots
// 역할 : AI 응답 대기 중 점 3개가 깜빡이는 애니메이션 표시
// ================================================================
function LoadingDots() {
  return (
    <div className="flex justify-start mb-4">
      <div className="loading-bubble">
        <span className="bot-avatar">🎭</span>
        {/* dots 안의 span 3개가 CSS animation(pulse)으로 순차적으로 깜빡임 */}
        <div className="dots">
          <span /><span /><span />
        </div>
      </div>
    </div>
  );
}


// ================================================================
// 【컴포넌트 4】 App (최상위 / 기본 export)
// 역할 : 전체 앱 상태 관리 + UI 조립
// ================================================================
export default function App() {

  // ── 상태(State) 정의 ──────────────────────────────────
  // useState(초기값) → [현재값, 값을 바꾸는 함수] 반환

  // 채팅 메시지 전체 목록 (배열에 메시지 객체를 순서대로 추가)
  const [messages, setMessages] = useState([]);

  // 입력창에 타이핑 중인 텍스트
  const [input, setInput] = useState("");

  // AI 응답 대기 중 여부 (true면 입력 비활성화 + 로딩 표시)
  const [loading, setLoading] = useState(false);

  // ── Ref 정의 ──────────────────────────────────────────
  // useRef : 렌더링과 무관하게 DOM 요소에 직접 접근할 때 사용

  // 채팅창 맨 아래 빈 div를 가리킴 → scrollIntoView()로 자동 스크롤
  const chatEndRef = useRef(null);

  // textarea 요소를 가리킴 (포커스 제어 등 확장 가능)
  const inputRef = useRef(null);

  // ── 사이드이펙트 : 자동 스크롤 ────────────────────────
  // messages 또는 loading 상태가 바뀔 때마다 자동 실행
  // 새 메시지가 추가될 때마다 채팅창을 맨 아래로 부드럽게 스크롤
  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, loading]); // 의존성 배열 : 이 값이 바뀔 때만 실행

  // ── 메시지 추가 헬퍼 함수 ─────────────────────────────
  // prev(이전 배열)에 새 msg를 추가한 새 배열을 반환
  // React 상태는 불변성(immutability)을 지켜야 해서 [...prev, msg] 방식 사용
  function addMessage(msg) {
    setMessages((prev) => [...prev, msg]);
  }

  // ── 메시지 전송 함수 (핵심 로직) ──────────────────────
  async function sendMessage() {
    const text = input.trim(); // 앞뒤 공백 제거

    // 빈 입력이거나 이미 로딩 중이면 실행 안 함
    if (!text || loading) return;

    setInput("");                          // 입력창 초기화
    addMessage({ sender: "user", text }); // 유저 메시지 즉시 화면에 추가
    setLoading(true);                     // 로딩 시작 (점 애니메이션 표시)

    try {
      // ── SSE(Server-Sent Events) 연결 ──────────────────
      // EventSource : 서버에서 실시간으로 데이터를 받는 브라우저 내장 API
      // HTTP GET 방식으로 연결 유지하면서 서버가 데이터를 push
      // encodeURIComponent : 한글 등 특수문자를 URL 안전 형식으로 인코딩
      const source = new EventSource(
        `${API_BASE}/chat_stream?prompt=${encodeURIComponent(text)}`
      );

      // ── 서버에서 메시지가 올 때마다 실행 ──────────────
      source.onmessage = (e) => {
        // e.data : 서버가 보낸 문자열 → JSON.parse로 객체로 변환
        const res = JSON.parse(e.data);

        if (res.status === "processing") {
          // 공감 멘트가 있으면 봇 말풍선으로 추가
          if (res.message) {
            addMessage({ sender: "bot", type: "empathy", text: res.message });
          }
          // 영화 데이터가 있으면 카드 목록으로 추가
          if (res.data?.length) {
            addMessage({ sender: "bot", type: "movies", movies: res.data });
          }
          setLoading(false); // 로딩 종료
        } else if (res.status === "complete") {
          // 서버가 스트리밍 완료 신호를 보내면 SSE 연결 종료
          source.close();
        }
      };

      // ── 연결 오류 처리 ─────────────────────────────────
      // 백엔드 서버가 꺼져있거나 네트워크 오류 시 실행
      source.onerror = () => {
        addMessage({
          sender: "bot",
          type: "empathy",
          text: "서버와 연결이 끊겼습니다. 잠시 후 다시 시도해 주세요.",
        });
        setLoading(false);
        source.close();
      };

    } catch (err) {
      // EventSource 생성 자체가 실패한 경우 (거의 발생 안 하지만 안전장치)
      console.error("SSE 오류:", err); // 개발자 도구 콘솔에 오류 출력
      addMessage({
        sender: "bot",
        type: "empathy",
        text: "오류가 발생했습니다. 백엔드 서버가 실행 중인지 확인해 주세요.",
      });
      setLoading(false);
    }
  }

  // ── 키보드 이벤트 : Enter 전송 ────────────────────────
  // Shift+Enter는 줄바꿈, Enter만 누르면 전송
  function handleKeyDown(e) {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault(); // Enter의 기본 동작(줄바꿈) 방지
      sendMessage();
    }
  }

  // ── JSX 렌더링 ────────────────────────────────────────
  // React 컴포넌트는 JSX(HTML과 유사한 문법)를 반환
  // <> </> : Fragment - 불필요한 div 없이 여러 요소를 묶는 방법
  return (
    <>
      {/* ══════════════════════════════════════════════════
          전역 CSS 스타일 정의
          - <style> 태그를 JSX 안에 직접 삽입 (CSS-in-JS 방식)
          - Tailwind로 표현하기 어려운 복잡한 스타일을 여기서 처리
          - CSS 변수(--변수명)로 색상 등 공통값을 한 곳에서 관리
      ══════════════════════════════════════════════════ */}
      <style>{`
        /* Google Fonts 불러오기 - 한국어(Noto Serif KR) + 영문(DM Sans) */
        @import url('https://fonts.googleapis.com/css2?family=Noto+Serif+KR:wght@400;600;700&family=DM+Sans:wght@400;500&display=swap');

        /* 모든 요소의 box-sizing을 border-box로 통일 (padding이 너비에 포함) */
        *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

        /* CSS 변수 : 색상 팔레트를 한 곳에서 관리 (다크 시네마 테마) */
        :root {
          --bg:        #0c0d10;   /* 배경색 (매우 어두운 검정) */
          --surface:   #14161c;   /* 카드/입력창 배경 */
          --border:    #2a2d38;   /* 테두리 색 */
          --accent:    #e8b84b;   /* 강조색 (금색) - 추천사유, 공감멘트 */
          --accent2:   #c47c2b;   /* 강조색2 (진한 금색) - 호버, 포커스 */
          --text:      #e8e4dc;   /* 기본 텍스트 색 */
          --muted:     #7a7d8a;   /* 보조 텍스트 색 (연한 회색) */
          --user-bg:   #1e2133;   /* 유저 말풍선 배경 */
          --bot-bg:    #181a22;   /* 봇 말풍선 배경 */
          --card-bg:   #181a22;   /* 영화 카드 배경 */
          --radius:    14px;      /* 공통 모서리 둥글기 */
        }

        body {
          background: var(--bg);
          color: var(--text);
          font-family: 'DM Sans', 'Noto Serif KR', sans-serif;
          min-height: 100vh; /* 화면 전체 높이 보장 */
        }

        /* ── 헤더 : 상단 고정 + 반투명 블러 효과 ── */
        .app-header {
          position: sticky; top: 0; z-index: 50; /* 스크롤해도 상단 고정 */
          background: rgba(12,13,16,0.85);        /* 85% 불투명 */
          backdrop-filter: blur(18px);            /* 배경 흐림 효과 */
          border-bottom: 1px solid var(--border);
          padding: 18px 24px;
          display: flex; align-items: center; gap: 12px;
        }
        .header-icon { font-size: 2rem; }
        .header-title {
          font-family: 'Noto Serif KR', serif;
          font-size: 1.5rem; font-weight: 700;
          letter-spacing: -0.02em;
          /* 텍스트에 그라디언트 색상 적용 (금색→흰색) */
          background: linear-gradient(135deg, var(--accent), #fff8e7);
          -webkit-background-clip: text;
          -webkit-text-fill-color: transparent;
        }
        .header-sub {
          font-size: 1.0rem; color: var(--muted);
          margin-left: auto; /* 오른쪽 끝으로 밀기 */
          letter-spacing: 0.06em; text-transform: uppercase;
        }

        /* ── 채팅 영역 : 중앙 정렬 + 하단 여백(입력창 높이만큼) ── */
        .chat-area {
          max-width: 1800px; margin: 0 auto;
          padding: 32px 8px 160px; /* 하단 160px = 입력창이 내용을 가리지 않게 */
          min-height: 80vh;
        }

        /* ── 초기 안내 문구 (메시지 없을 때만 표시) ── */
        .welcome {
          text-align: center; padding: 80px 0 40px;
          opacity: 0.55; /* 살짝 투명하게 */
        }
        .welcome-icon { font-size: 3.5rem; margin-bottom: 16px; }
        .welcome-text {
          font-family: 'Noto Serif KR', serif;
          font-size: 1.05rem; line-height: 1.9; color: var(--muted);
        }

        /* ── 유저 말풍선 : 오른쪽 파란 계열 ── */
        .user-bubble {
          background: var(--user-bg);
          border: 1px solid #2e3347;
          /* 오른쪽 하단 모서리만 뾰족하게 → 말풍선 꼬리 효과 */
          border-radius: var(--radius) var(--radius) 4px var(--radius);
          padding: 12px 18px;
          max-width: 60%; font-size: 0.95rem; line-height: 1.6;
          color: #d6d2ff; /* 연보라 텍스트 */
        }

        /* ── 봇 공감 말풍선 : 왼쪽 어두운 배경 ── */
        .empathy-bubble {
          display: flex; align-items: flex-start; gap: 10px;
          background: var(--bot-bg);
          border: 1px solid var(--border);
          /* 왼쪽 상단 모서리만 뾰족하게 → 말풍선 꼬리 효과 */
          border-radius: 4px var(--radius) var(--radius) var(--radius);
          padding: 14px 18px;
          width: 100%; /* 전체 너비 사용 */
        }
        .bot-avatar {
          font-size: 1.4rem; flex-shrink: 0; /* 아이콘 크기 고정 */
          margin-top: 2px;
        }
        .empathy-text {
          font-family: 'Noto Serif KR', serif;
          font-size: 0.92rem; line-height: 1.85;
          color: var(--accent);
          white-space: pre-line; /* \n을 실제 줄바꿈으로 처리 */
        }

        /* ── 로딩 점 애니메이션 ── */
        .loading-bubble {
          display: flex; align-items: center; gap: 10px;
          background: var(--bot-bg); border: 1px solid var(--border);
          border-radius: 4px var(--radius) var(--radius) var(--radius);
          padding: 14px 20px;
        }
        .dots { display: flex; gap: 5px; }
        .dots span {
          width: 7px; height: 7px; border-radius: 50%;
          background: var(--accent); opacity: 0.6;
          animation: pulse 1.2s infinite ease-in-out;
        }
        /* nth-child로 각 점의 애니메이션 시작 시간을 다르게 → 물결 효과 */
        .dots span:nth-child(2) { animation-delay: 0.2s; }
        .dots span:nth-child(3) { animation-delay: 0.4s; }
        @keyframes pulse {
          0%,100% { transform: scale(0.8); opacity: 0.4; }
          50%      { transform: scale(1.2); opacity: 1; }
        }

        /* ── 영화 카드 그리드 : 5열 균등 분할 ── */
        .cards-grid {
          display: grid;
          grid-template-columns: repeat(5, 1fr); /* 5칸 균등 분할 */
          gap: 16px; /* 카드 간격 */
        }

        /* ── 영화 카드 ── */
        .movie-card {
          background: var(--card-bg);
          border: 1px solid var(--border);
          border-radius: var(--radius);
          overflow: hidden; /* 포스터 이미지가 모서리 밖으로 나가지 않게 */
          display: flex; flex-direction: column; /* 세로 방향 배치 */
          transition: transform 0.25s ease, box-shadow 0.25s ease;
          animation: cardIn 0.45s ease both; /* 등장 애니메이션 */
        }
        /* 호버 시 위로 살짝 떠오르는 효과 */
        .movie-card:hover {
          transform: translateY(-5px);
          box-shadow: 0 16px 40px rgba(0,0,0,0.55);
          border-color: var(--accent2);
        }
        /* 카드 등장 애니메이션 : 아래에서 위로 페이드인 */
        @keyframes cardIn {
          from { opacity: 0; transform: translateY(24px); }
          to   { opacity: 1; transform: translateY(0); }
        }

        /* 포스터 비율 고정 (세로형 2:3 비율 유지) */
        .poster-wrap { position: relative; aspect-ratio: 2/3; overflow: hidden; }
        .poster-img { width: 100%; height: 100%; object-fit: cover; display: block; }
        .poster-placeholder {
          width: 100%; height: 100%;
          display: flex; align-items: center; justify-content: center;
          font-size: 3rem;
          background: linear-gradient(160deg, #1a1d28, #0c0d10);
        }
        /* 평점 배지 : 포스터 우하단에 절대 위치로 겹치기 */
        .rating-badge {
          position: absolute; bottom: 8px; right: 8px;
          background: rgba(0,0,0,0.78); color: var(--accent);
          font-size: 0.72rem; font-weight: 600;
          padding: 3px 8px; border-radius: 20px;
          border: 1px solid rgba(232,184,75,0.3);
        }

        /* 카드 텍스트 영역 */
        .card-body {
          padding: 14px; flex: 1; /* 남은 공간 모두 차지 */
          display: flex; flex-direction: column; gap: 8px;
        }
        .reason-box { display: flex; flex-direction: column; gap: 3px; }
        .reason-line {
          font-family: 'Noto Serif KR', serif;
          font-size: 0.78rem; line-height: 1.65;
          color: var(--accent); font-weight: 600;
        }
        .divider { height: 1px; background: var(--border); margin: 4px 0; }
        .movie-title {
          font-family: 'Noto Serif KR', serif;
          font-size: 0.95rem; font-weight: 700;
          color: var(--text); line-height: 1.3;
        }
        .movie-desc {
          font-size: 0.78rem; color: var(--muted);
          line-height: 1.6; flex: 1;
        }

        /* ── 입력창 : 하단 고정 바 ── */
        .input-bar {
          position: fixed; bottom: 0; left: 0; right: 0; /* 화면 하단 고정 */
          background: rgba(12,13,16,0.92);
          backdrop-filter: blur(18px);
          border-top: 1px solid var(--border);
          padding: 16px 20px 20px;
        }
        .input-inner {
          max-width: 1800px; margin: 0 auto;
          display: flex; gap: 10px; align-items: flex-end;
        }
        .input-field {
          flex: 1; /* 버튼 제외한 나머지 공간 모두 차지 */
          background: var(--surface);
          border: 1px solid var(--border);
          border-radius: 12px;
          padding: 13px 18px;
          color: var(--text);
          font-size: 0.95rem;
          font-family: 'DM Sans', sans-serif;
          outline: none; resize: none; /* 크기 조절 핸들 숨김 */
          line-height: 1.5;
          transition: border-color 0.2s;
          min-height: 48px; max-height: 120px; /* 최소/최대 높이 제한 */
        }
        .input-field::placeholder { color: var(--muted); }
        .input-field:focus { border-color: var(--accent2); } /* 포커스 시 테두리 강조 */

        /* 전송 버튼 : 금색 그라디언트 정사각형 */
        .send-btn {
          background: linear-gradient(135deg, var(--accent), var(--accent2));
          color: #0c0d10;
          border: none; border-radius: 12px;
          width: 48px; height: 48px;
          display: flex; align-items: center; justify-content: center;
          font-size: 1.3rem;
          cursor: pointer; flex-shrink: 0; /* 버튼 크기 고정 */
          transition: opacity 0.2s, transform 0.15s;
        }
        .send-btn:hover:not(:disabled) { transform: scale(1.07); }
        .send-btn:disabled { opacity: 0.35; cursor: not-allowed; } /* 로딩 중 비활성화 */
      `}</style>

      {/* ══════════════════════════════════════════
          헤더 영역
      ══════════════════════════════════════════ */}
      <header className="app-header">
        <span className="header-icon">🎬</span>
        <h1 className="header-title">영화별 맞춤 심리 처방 에이전트</h1>
        <span className="header-sub">Cinema Therapist</span>
      </header>

      {/* ══════════════════════════════════════════
          채팅 본문 영역
      ══════════════════════════════════════════ */}
      <main className="chat-area">

        {/* 메시지가 하나도 없을 때만 초기 안내 문구 표시 */}
        {messages.length === 0 && (
          <div className="welcome">
            <div className="welcome-icon">🎭</div>
            <p className="welcome-text">
              지금 어떤 기분인지 자유롭게 이야기해 주세요.<br />
              당신의 감정에 꼭 맞는 영화를 처방해 드립니다.
            </p>
          </div>
        )}

        {/* messages 배열을 순회하며 ChatMessage 컴포넌트 렌더링 */}
        {messages.map((msg, i) => (
          <ChatMessage key={i} msg={msg} />
        ))}

        {/* loading이 true일 때만 로딩 애니메이션 표시 */}
        {loading && <LoadingDots />}

        {/* 자동 스크롤 타겟 : 항상 화면 맨 아래에 위치 */}
        <div ref={chatEndRef} />
      </main>

      {/* ══════════════════════════════════════════
          하단 고정 입력 바
      ══════════════════════════════════════════ */}
      <div className="input-bar">
        <div className="input-inner">
          {/* textarea : 여러 줄 입력 가능한 텍스트 입력창 */}
          <textarea
            ref={inputRef}
            className="input-field"
            rows={1}
            value={input}                              // 상태와 연결 (제어 컴포넌트)
            onChange={(e) => setInput(e.target.value)} // 타이핑할 때마다 상태 업데이트
            onKeyDown={handleKeyDown}                  // Enter 키 감지
            placeholder="지금 기분은 어떤가요?..."
            disabled={loading}                         // 로딩 중 입력 비활성화
          />

          {/* 전송 버튼 : 로딩 중이거나 입력값 없으면 비활성화 */}
          <button
            className="send-btn"
            onClick={sendMessage}
            disabled={loading || !input.trim()}
            title="처방받기"
          >
            {/* 로딩 중이면 모래시계, 아니면 편지 이모지 */}
            {loading ? "⏳" : "✉️"}
          </button>
        </div>
      </div>
    </>
  );
}