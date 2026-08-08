# YES24 베스트셀러 챗봇 RRF 하이브리드 검색 및 검색 제어 기능 설계서

## 1. 개요 (Overview)
본 설계는 YES24 베스트셀러 도서 검색 및 RAG AI 챗봇(`yes24`) 시스템에 키워드 검색(BM25)과 벡터 유사도 검색(SBERT/ChromaDB)을 결합한 **RRF (Reciprocal Rank Fusion) 기반 하이브리드 검색(Hybrid Search)** 엔진을 구축하고, 사용자가 검색 유사도 임계값(Threshold) 및 결과 개수(Top-K), 검색 모드를 직접 조절할 수 있는 UI 컨트롤을 추가하는 것을 목표로 합니다.

---

## 2. 주요 기능 및 변경 사항 (Features & Architecture)

### 2.1 신규 모듈 작성

1. **`yes24/bm25_manager.py` (Okapi BM25 검색 엔진)**
   - **토큰화 (Tokenization)**: 정규식 기반 정제 및 공백/어절/N-gram 토큰화로 한국어 도서명, 저자, 출판사, 설명 키워드 매칭 보장.
   - **BM25Index / BM25Searcher**:
     - 파라미터: $k_1 = 1.5, b = 0.75$
     - 데이터프레임의 결합 텍스트(`goods_name`, `author`, `publisher`, `features`, `tags` 등) 기반 문서 인덱싱.
     - `search(query, top_k)`: 주어진 질의에 대해 BM25 점수 상위 결과 반환.

2. **`yes24/hybrid_search.py` (RRF 하이브리드 통합 검색 엔진)**
   - **Reciprocal Rank Fusion (RRF)** 알고리즘 구현:
     $$\text{RRF Score}(d) = \frac{1}{k + \text{rank}_{\text{bm25}}(d)} + \frac{1}{k + \text{rank}_{\text{vector}}(d)}$$ (상수 $k = 60$)
   - **`search_hybrid()` 메인 함수**:
     - 입력 파라미터: `query_text`, `df`, `chroma_collection`, `model`, `bm25_searcher`, `top_k`, `min_sim_pct`, `search_mode`
     - `search_mode` 처리:
       - `"하이브리드 (BM25 + Vector)"`: BM25와 ChromaDB 검색을 각각 수행 후 RRF 순위 합산.
       - `"벡터 유사도 전용"`: ChromaDB 코사인 유사도 검색만 수행.
       - `"키워드(BM25) 전용"`: BM25 키워드 점수 기반 검색만 수행.
     - `min_sim_pct` (최소 유사도/점수 Threshold) 이하의 결과 자동 필터링.
     - 최종 Top-K 결과를 반환 (유사도 %, BM25 순위, RRF 점수 포함).

### 2.2 기존 모듈 수정 및 UI 연동

1. **`yes24/app.py` (Streamlit 대시보드 및 사이드바 설정)**
   - 사이드바 설정 영역에 검색 컨트롤러 조작 슬라이더/셀렉트박스 추가:
     - **검색 모드**: `하이브리드 (BM25 + Vector)`, `벡터 유사도 전용`, `키워드(BM25) 전용`
     - **추출 도서 개수 (Top-K)**: 슬라이더 `1 ~ 20` (기본값: `5`)
     - **최소 유사도 threshold**: 슬라이더 `0% ~ 100%` (기본값: `0%`)
   - 챗봇 질의 시 `search_hybrid()`를 호출하고, 사용자가 선택한 `top_k` 및 `min_sim_pct` 옵션을 `generate_rag_answer`에 전달.
   - 답변 하단 expander 영역에 Top-K 도서의 **벡터 유사도(%)**, **BM25 순위**, **RRF 점수** 투명하게 시각화.

2. **`yes24/groq_bot.py` (RAG 프롬프트 및 응답 생성기)**
   - `generate_rag_answer()`에 하이브리드 메타데이터(유사도 %, BM25 순위, 검색 조건 정보)를 포함하여 Groq LLM이 관련도 높은 추천 사유를 명확히 제시하도록 프롬프트 구성.

---

## 3. 데이터 흐름 (Data Flow)

```
[사용자 질문 입력]
       │
       ▼
[app.py: 사이드바 검색 옵션 감지]
 (Search Mode, Top-K, Min Sim %)
       │
       ▼
[hybrid_search.py: search_hybrid()]
 ├──▶ [bm25_manager.py] ──▶ BM25 순위 검색
 └──▶ [chroma_manager.py] ──▶ SBERT 코사인 유사도 검색
       │
       ▼
[RRF (Reciprocal Rank Fusion) 순위 통합 & Min Sim % 필터링]
       │
       ▼
[groq_bot.py: generate_rag_answer()] ──▶ Groq Llama-3.3-70B API 호출
       │
       ▼
[Streamlit UI 답변 출력 및 Top-K 상세 Expander 표시]
```

---

## 4. 검증 방안 (Verification)
1. **단체 테스트 script**: Python 스크립트로 BM25 단독 검색, ChromaDB 단독 검색, RRF 하이브리드 검색 결과의 정확도 및 점수 산출 검증.
2. **Streamlit UI 동작 검증**: 사이드바 옵션 조절(Top-K 변경, Min Sim % 변경, 검색 모드 전환) 시 챗봇과 Expander 결과가 즉각 반영되는지 확인.
