## 📊 데이터 흐름도

```mermaid
flowchart TD
    MAIN["main.jsx<br/>앱 진입점"]:::entry
    MOCK["mockPosts.js<br/>초기 더미 데이터"]:::data
    APP["App.jsx<br/>state: posts · mode · selectedPost"]:::controller
    ULS["useLocalStorage<br/>커스텀 훅 (hooks/)"]:::hook
    LS[("localStorage<br/>JSON 영구 저장")]:::storage
    BL["BoardList<br/>목록 · 검색 · 페이지네이션"]:::component
    BD["BoardDetail<br/>상세보기 · 댓글 CRUD"]:::component
    BF["BoardForm<br/>작성 · 수정 폼"]:::component

    MAIN --> APP
    MOCK -->|초기 데이터| APP
    APP <-->|posts 동기화| ULS
    ULS <-->|JSON 저장/로드| LS

    APP -->|"mode='list' · props: posts"| BL
    APP -->|"mode='detail' · props: post"| BD
    APP -->|"mode='form' · props: editingPost"| BF

    BL -->|onSelect| APP
    BD -->|"onBack · onEdit · onDelete"| APP
    BF -->|"onSave · onCancel"| APP

    classDef entry    fill:#f1f0e8,stroke:#888780,color:#2c2c2a
    classDef data     fill:#faeeda,stroke:#854f0b,color:#412402
    classDef controller fill:#eeedfe,stroke:#534ab7,color:#26215c
    classDef hook     fill:#e1f5ee,stroke:#0f6e56,color:#04342c
    classDef storage  fill:#e1f5ee,stroke:#0f6e56,color:#04342c
    classDef component fill:#e6f1fb,stroke:#185fa5,color:#042c53
```

---

## 🗂️ 파일 역할 요약

| 파일 | 역할 |
|------|------|
| `main.jsx` | React 앱 진입점. `<App />`을 DOM에 마운트 |
| `App.jsx` | 화면 전환 컨트롤러. `mode` 상태로 `list / detail / form` 렌더링 결정 |
| `data/mockPosts.js` | `useLocalStorage` 초기값. localStorage가 비어있을 때만 사용 |
| `hooks/useLocalStorage.js` | 상태와 localStorage를 자동 동기화하는 커스텀 훅 |
| `components/BoardList.jsx` | 게시글 목록 출력, 제목 검색, 페이지네이션 |
| `components/BoardDetail.jsx` | 게시글 상세보기, 댓글 목록 및 작성, 삭제 확인 모달 |
| `components/BoardForm.jsx` | 게시글 작성(신규) / 수정(editingPost 전달 시) 폼 |

---

## 🔄 상태 흐름 요약

```
사용자 클릭
  └─ BoardList.onSelect(post)
       └─ App: setSelectedPost(post) + setMode('detail')
            └─ BoardDetail 렌더링

  └─ BoardDetail.onEdit()
       └─ App: setMode('form')  [selectedPost 유지]
            └─ BoardForm 렌더링 (수정 모드)

  └─ BoardForm.onSave(newPost)
       └─ App: handleSave → setPosts → setMode('list')
            └─ useLocalStorage → localStorage 자동 저장
```