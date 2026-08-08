# YES24 베스트셀러 키워드 & 유사도 검색 대시보드 설계서

- **작성일**: 2026년 8월 3일
- **목적**: `yes24/yes24_bestsellers.csv` 데이터셋을 기반으로 경량 한국어 임베딩 모델(`jhgan/ko-sbert-sts`)을 사용하여 키워드 검색, 벡터 코사인 유사도 검색, 임베딩 캐싱, 임베딩 프로젝터 TSV 파일 생성 및 시각화 대시보드 구축.

---

## 1. 주요 요구사항 및 아키텍처

### 1.1 한국어 임베딩 및 파일 캐싱
- **Embedding Model**: `jhgan/ko-sbert-sts` (Hugging Face / SentenceTransformers, 약 400MB)
- **Embedded Text Context**: `goods_name` + `goods_sub_name` + `author_clean` + `publisher` + `features` + `tags`
- **File Persistence**:
  - `yes24/yes24_embeddings.npy`: 임베딩 행렬 저장 (.npy)
  - `yes24/vectors.tsv`: TensorFlow Embedding Projector용 벡터 데이터
  - `yes24/metadata.tsv`: TensorFlow Embedding Projector용 메타데이터 (Header: `goods_name\tauthor\tpublisher\tprice\tsale_index\trating`)

### 1.2 Streamlit 대시보드 기능 (`yes24/app.py`)
1. **🔍 키워드 검색 탭**:
   - 도서명, 저자, 출판사, 특징 필드 대상 텍스트 매칭
   - 출판사, 가격, 분철 여부 조건 필터링
   - 결과를 `st.dataframe` 표(Table) 형태로 출력
2. **🧬 코사인 유사도 검색 탭**:
   - 입력 모드 2가지: (1) 자연어 쿼리 문장 입력, (2) 목록에서 기준 도서 선택
   - **조정 컨트롤**:
     - `min_similarity` (최소 유사도 임계값): 0.0 ~ 1.0 Slider (기본값 0.3)
     - `top_k` (출력 도서 개수): 1 ~ 50 Slider (기본값 10)
   - 결과 표출: 유사도 점수(%), 랭킹, 도서 정보, 바로가기 링크를 표(Table)로 표출
3. **📊 임베딩 시각화 & 프로젝터 TSV 탭**:
   - PCA 2D 차원 축소 차트 (도서 위치 시각화)
   - `vectors.tsv`, `metadata.tsv` 다운로드 버튼 및 TensorFlow Projector 활용 가이드
4. **🏆 하이라이트 & 데이터 브라우저 탭**:
   - 기존 베스트셀러 TOP3 카드, KPI 메트릭, CSV 다운로드

---

## 2. 모듈 구조

```
yes24/
├── yes24_bestsellers.csv       # 원본 데이터셋
├── embedding_manager.py       # 모델 로드, 임베딩 계산/저장/로드, 코사인 유사도, TSV 생성
├── yes24_embeddings.npy       # 캐싱된 임베딩 행렬
├── vectors.tsv                # embedding projector 벡터 파일
├── metadata.tsv               # embedding projector 메타데이터 파일
└── app.py                     # Streamlit 대시보드 메인 앱
```
