// 3.src/components/BoardList.jsx  작성(글목록 보기)

import { useState } from "react";
// 별도의 페이징 컴포넌트 호출
import Pagination3 from "./Pagination3";  // blocksize가 적용된 경우

// index.html=>main.jsx->App.jsx->BoardList.jsx<-Pagination
export default function BoardList({ posts, onSelect }) { // onSelect=>글상세보기

  // 1.사용자의 입력 검색어 상태
  const [search, setSearch] = useState("");

  // 2.현재 보고 있는 페이지 번호
  const [currentPage, setCurrentPage] = useState(1); // 디폴트 1 페이지

  // 3.한 페이지에 보여줄 게시글 개수
  const pageSize = 5; // 통상 10개
  // pagePerBlock(=blockSize)도 통상 10개

  // 4.검색어에 따른 필터링 로직 (제목 기준)
  const filtered = (posts || []).filter((post) =>
    post.title.toLowerCase().includes(search.toLowerCase())
  );

  // 5.현재 페이지의 시작 인덱스 번호
  const start = (currentPage - 1) * pageSize;
  
  // 6.전체 데이터 중 현재 페이지에 해당하는 부분만 추출
  // 1,11=>(1,10)개 출력
  const currentPosts = filtered.slice(start, start + pageSize);  // 1,6 = (1,2,3,4,5)

  return (
    // 목록을 감싸는 카드 컨테이너
    <div className="w-full bg-white shadow-2xl shadow-gray-200/50 rounded-[2.5rem] border border-gray-100 overflow-hidden">
      
      {/* 상단 컨트롤러: 제목 및 검색바 */}
      <div className="p-10 border-b border-gray-50 flex flex-col sm:flex-row justify-between items-center gap-6 bg-gradient-to-r from-white to-gray-50/50">
        <div>
          <h3 className="text-xl font-extrabold text-gray-800">게시글 목록</h3>
          <p className="text-sm text-gray-400 font-medium">총 <span className="text-blue-600">{filtered.length}</span>개의 게시글이 있습니다.</p>
        </div>
        <div className="relative w-full sm:w-80">
          <input
            type="text"
            placeholder="제목으로 검색..."
            className="w-full pl-12 pr-6 py-4 bg-gray-100/50 border-2 border-transparent rounded-2xl text-sm font-medium focus:ring-2 focus:ring-blue-500 focus:bg-white focus:border-blue-500 outline-none transition-all shadow-inner"
            value={search}
            onChange={(e) => { setSearch(e.target.value); setCurrentPage(1); }}
          />
          <svg className="w-5 h-5 absolute left-4 top-1/2 -translate-y-1/2 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2.5" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"/></svg>
        </div>
      </div>

      {/* 게시글 테이블 */}
      <div className="overflow-x-auto">
        <table className="w-full border-collapse">
          <thead>
            <tr className="bg-gray-50/50">
              <th className="px-8 py-5 text-[10px] font-black text-gray-400 text-center w-24 uppercase tracking-widest">No.</th>
              <th className="px-8 py-5 text-[10px] font-black text-gray-400 text-left uppercase tracking-widest">Subject</th>
              <th className="px-8 py-5 text-[10px] font-black text-gray-400 text-center w-40 uppercase tracking-widest">Author</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-gray-50">
            {currentPosts.length === 0 ? (
              <tr><td colSpan="3" className="py-32 text-center text-gray-300 font-bold italic">표시할 내용이 없습니다.</td></tr>
            ) : (
              currentPosts.map((post, index) => (
                <tr 
                  key={post.id} 
                  className="hover:bg-blue-50/40 cursor-pointer transition-all group relative"
                  onClick={() => onSelect(post)} 
                >
                  <td className="px-8 py-6 text-center text-sm font-bold text-gray-300 font-mono group-hover:text-blue-400 transition-colors">{(currentPage - 1) * pageSize + index + 1}</td>
                  <td className="px-8 py-6">
                    <div className="flex flex-col">
                      <span className="text-base font-bold text-gray-700 group-hover:text-blue-600 group-hover:translate-x-1 transition-all">
                        {post.title}
                      </span>
                      {/* 댓글수까지 출력 */}
                      <span className="text-[10px] text-gray-400 mt-1 flex items-center gap-1">
                        <svg className="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z"/></svg>
                        {/* 없으면 0 comments, 있으면 갯수 comments */}
                        {post.comments?.length || 0} Comments
                      </span>
                    </div>
                  </td>
                  <td className="px-8 py-6 text-center">
                    <span className="inline-flex items-center px-4 py-1.5 rounded-full text-xs font-bold bg-blue-50 text-blue-600 group-hover:bg-blue-600 group-hover:text-white transition-all shadow-sm">
                      {/* 작성자 */}
                      {post.author}
                    </span>
                  </td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>

      {/* 하단 페이지네이션 섹션 */}
      <div className="p-6 flex justify-center border-t border-gray-50 bg-gray-50/30">
        <Pagination3 total={filtered.length} pageSize={pageSize} current={currentPage} onChange={setCurrentPage} />
      </div>
    </div>
  );
}
