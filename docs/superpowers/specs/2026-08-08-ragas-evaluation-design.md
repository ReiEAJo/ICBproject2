# RAGAS 기반 RAG 챗봇 품질 평가 기능 설계서

## 1. 개요
YES24 베스트셀러 RAG 챗봇 시스템(`yes24/groq_bot.py` 및 Streamlit 대시보드 `yes24/app.py`)에 RAGAS(Retrieval-Augmented Generation Assessment) 기법을 기반으로 하는 RAG 품질 평가 기능을 추가한다. 

Groq API Key(`llama-3.3-70b-versatile`)를 활용한 **LLM-as-a-Judge** 방식과 SBERT 코사인 유사도를 결합하여 별도의 외부 서비스 비용/설정 없이 4대 핵심 RAG 지표를 실시간 및 대시보드 형태로 측정한다.

---

## 2. 평가 지표 (RAGAS Metrics)

1. **Faithfulness (충실도 / 환각 여부)**
   - 챗봇이 생성한 답변의 각 주장이 검색된 베스트셀러 도서 문맥(Context)에 근거하였는지 평가
   - Score: `(검색 문맥에 근거한 주장 수) / (전체 생성 주장 수)`

2. **Answer Relevance (답변 관련성)**
   - 생성된 답변이 사용자의 질문 의도에 얼마나 직결되는지 평가
   - Score: 생성 답변에서 역으로 도출한 질문들과 원본 질문 간의 SBERT 의미적 유사도 / LLM 평가 점수

3. **Context Precision (맥락 정밀도)**
   - 검색된 Top-K 도서 문서들 중 답변 작성에 실제 도움이 되는 관련 문서가 상위에 잘 랭크되었는지 평가
   - Score: 상위 K개 컨텍스트 문서의 Precision@K 및 AP(Average Precision)

4. **Context Recall (맥락 완결성 / 재현율)**
   - 질문에 답변하기 위해 필요한 핵심 정보/기준 정답(Ground Truth)이 검색된 문맥에 얼마나 포함되어 있는지 평가
   - Score: Ground Truth 항목 중 검색 문맥에 존재하는 비율

5. **종합 RAGAS Score**
   - 4개 지표의 조화 평균(Harmonic Mean) 또는 가중 평균으로 계산되는 종합 챗봇 응답 품질 점수 (0 ~ 100점)

---

## 3. 모듈 아키텍처 및 구현 파일

### 1) `yes24/ragas_evaluator.py` (신규 전용 평가 모듈)
- **`evaluate_rag_response(question, retrieved_books, response, ground_truth, api_key, model_name)`**
  - 단일 Q&A에 대해 4개 RAGAS 지표 산출
  - 세부 사유(Reasoning) 및 지표별 점수 dict 반환
- **`run_batch_ragas_evaluation(df, chroma_collection, model, bm25_searcher, search_mode, top_k, min_sim_pct, api_key)`**
  - 벤치마크 테스트셋(기본 5개 이상 대표 도서 질문)에 대해 RAG 하이브리드 검색 및 Groq LLM 평가 수행
  - 지표별 평균, 요약 데이터프레임, 검색 모델별(Hybrid vs Vector vs BM25) 성능 비교 결과 제공

### 2) `yes24/groq_bot.py` (기존 RAG 로직 확장)
- RAG 답변 생성 시 평가에 필요한 구조화된 컨텍스트 데이터를 동시 제공하는 헬퍼 지원
- RAGAS 평가 모듈과의 연동 인터페이스 정립

### 3) `yes24/app.py` (Streamlit 대시보드 UI 연동)
- **Tab 5 (AI 도서 추천 챗봇)**:
  - 챗봇 답변 하단 `🧪 [RAGAS] 실시간 RAG 품질 평가` Expander 추가
  - Faithfulness, Answer Relevance, Context Precision 실시간 점수 카드, 프로그레스 바, 및 사유 표시
- **Tab 6 (📈 RAG 품질 평가 - RAGAS Dashboard)**:
  - **단일 질의 커스텀 평가**: 사용자 질문, 정답(선택) 입력 후 실시간 RAGAS 평가 및 Plotly/Matplotlib 레이더 차트 시각화
  - **배치 벤치마크 실행**: 벤치마크 테스트셋에 대한 일괄 평가 수행 및 요약 메트릭 카드/테이블
  - **검색 방식(Hybrid vs Vector vs BM25) 비교 분석**: 검색 모드별 RAGAS 4대 지표 비교 막대 그래프

---

## 4. 검증 계획
- `ragas_evaluator.py` 단체/단일 unit test 작성 및 실행
- Streamlit 실행 및 Tab 5 실시간 평가 & Tab 6 대시보드 렌더링 확인
