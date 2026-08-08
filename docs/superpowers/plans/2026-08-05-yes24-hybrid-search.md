# YES24 RRF 하이브리드 검색 및 검색 제어 UI 구현 계획서

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** YES24 베스트셀러 챗봇 시스템에 Okapi BM25 키워드 검색과 SBERT/ChromaDB 코사인 유사도 검색을 결합한 RRF 하이브리드 검색 엔진을 추가하고, Streamlit UI에서 유사도 컷오프, 결과 개수(Top-K), 검색 모드를 조정할 수 있도록 구현합니다.

**Architecture:** 
- `bm25_manager.py`: 한국어 어절/N-gram 토큰화 기반 Okapi BM25 인덱서 및 검색기
- `hybrid_search.py`: Reciprocal Rank Fusion (RRF, $k=60$) 기반 검색 결과 통합 및 유사도 threshold 필터링
- `app.py` & `groq_bot.py`: Streamlit 사이드바 컨트롤러(검색 모드, Top-K, Min Similarity %) 연동 및 챗봇 답변 Expander 표기

**Tech Stack:** Python 3.10+, pandas, numpy, chromadb, sentence-transformers, streamlit, groq

## Global Constraints
- 파이썬 실행 환경: `.\.venv\Scripts\python.exe`
- BM25 파라미터: $k_1 = 1.5, b = 0.75$
- RRF 파라미터: $k = 60$
- 신규 의존성 패키지 설치 없이 numpy/standard library로 100% 자급적 BM25 구현

---

### Task 1: BM25 키워드 검색 엔진 (`yes24/bm25_manager.py`) 구현 및 단위 테스트

**Files:**
- Create: `yes24/bm25_manager.py`
- Create: `yes24/test_bm25_manager.py`

**Interfaces:**
- Consumes: pandas DataFrame (`goods_name`, `goods_sub_name`, `author`, `publisher`, `features`, `tags`, `document`)
- Produces: `BM25Searcher` class with `search(query: str, top_k: int = 10) -> List[Dict]`

- [ ] **Step 1: Write failing unit test for BM25Searcher**

```python
# yes24/test_bm25_manager.py
import pandas as pd
from bm25_manager import BM25Searcher

def test_bm25_searcher_basic():
    data = [
        {"goods_name": "파이썬 머신러닝 완벽 가이드", "author": "권철민", "publisher": "위키북스", "features": "파이썬 데이터 분석"},
        {"goods_name": "모두의 딥러닝", "author": "조태호", "publisher": "길벗", "features": "딥러닝 입문"},
        {"goods_name": "파이썬 웹 스크래핑", "author": "Ryan Mitchell", "publisher": "한빛미디어", "features": "크롤링 스크래핑"}
    ]
    df = pd.DataFrame(data)
    searcher = BM25Searcher(df)
    results = searcher.search("파이썬", top_k=2)
    assert len(results) == 2
    assert "파이썬" in results[0]["goods_name"] or "파이썬" in results[1]["goods_name"]

def test_bm25_searcher_empty():
    df = pd.DataFrame([{"goods_name": "테스트 도서"}])
    searcher = BM25Searcher(df)
    results = searcher.search("", top_k=5)
    assert results == []
```

- [ ] **Step 2: Run test to verify it fails**

Run: `.\.venv\Scripts\python.exe -m pytest yes24/test_bm25_manager.py -v`
Expected: FAIL (ModuleNotFoundError: No module named 'bm25_manager')

- [ ] **Step 3: Implement BM25Searcher in `yes24/bm25_manager.py`**

```python
# yes24/bm25_manager.py
import re
import math
from collections import Counter
import pandas as pd

def tokenize_korean(text):
    if not text or pd.isna(text):
        return []
    text_clean = re.sub(r'[^가-힣a-zA-Z0-9\s]', ' ', str(text)).lower()
    words = text_clean.split()
    tokens = set(words)
    for word in words:
        if len(word) >= 2:
            for i in range(len(word) - 1):
                tokens.add(word[i:i+2])
    return list(tokens)

class BM25Searcher:
    def __init__(self, df, k1=1.5, b=0.75):
        self.df = df.copy()
        self.k1 = k1
        self.b = b
        self.corpus_size = len(df)
        self.doc_tokens = []
        self.doc_lens = []
        self.df_counts = Counter()

        for idx, row in df.iterrows():
            parts = [
                str(row.get('goods_name', '')),
                str(row.get('goods_sub_name', '')),
                str(row.get('author_clean', row.get('author', ''))),
                str(row.get('publisher', '')),
                str(row.get('features', '')),
                str(row.get('tags', ''))
            ]
            full_text = " ".join([p for p in parts if p and p != 'nan'])
            tokens = tokenize_korean(full_text)
            self.doc_tokens.append(tokens)
            self.doc_lens.append(len(tokens))
            for t in set(tokens):
                self.df_counts[t] += 1

        self.avgdl = sum(self.doc_lens) / self.corpus_size if self.corpus_size > 0 else 1.0

    def get_idf(self, q_elem):
        n_q = self.df_counts.get(q_elem, 0)
        return math.log((self.corpus_size - n_q + 0.5) / (n_q + 0.5) + 1.0)

    def search(self, query, top_k=10):
        query_tokens = tokenize_korean(query)
        if not query_tokens or self.corpus_size == 0:
            return []

        scores = []
        for idx in range(self.corpus_size):
            doc_toks = self.doc_tokens[idx]
            doc_len = self.doc_lens[idx]
            tf_counter = Counter(doc_toks)
            score = 0.0

            for q_tok in query_tokens:
                if q_tok in tf_counter:
                    tf = tf_counter[q_tok]
                    idf = self.get_idf(q_tok)
                    numerator = tf * (self.k1 + 1)
                    denominator = tf + self.k1 * (1 - self.b + self.b * (doc_len / self.avgdl))
                    score += idf * (numerator / denominator)

            if score > 0:
                item = self.df.iloc[idx].to_dict()
                item['bm25_score'] = round(score, 4)
                item['df_index'] = idx
                scores.append(item)

        scores.sort(key=lambda x: x['bm25_score'], reverse=True)
        return scores[:top_k]
```

- [ ] **Step 4: Run unit test to verify it passes**

Run: `.\.venv\Scripts\python.exe -m pytest yes24/test_bm25_manager.py -v`
Expected: PASS

- [ ] **Step 5: Commit Task 1**

```bash
git add yes24/bm25_manager.py yes24/test_bm25_manager.py
git commit -m "feat: add Okapi BM25 keyword search engine for YES24 dataset"
```

---

### Task 2: RRF 하이브리드 통합 검색 엔진 (`yes24/hybrid_search.py`) 구현 및 단위 테스트

**Files:**
- Create: `yes24/hybrid_search.py`
- Create: `yes24/test_hybrid_search.py`

**Interfaces:**
- Consumes: `BM25Searcher` from `bm25_manager.py`, `query_chroma_rag` from `chroma_manager.py`
- Produces: `search_hybrid(query_text, df, chroma_collection, model, bm25_searcher, top_k=5, min_sim_pct=0.0, search_mode="하이브리드 (BM25 + Vector)") -> List[Dict]`

- [ ] **Step 1: Write failing unit test for `search_hybrid`**

```python
# yes24/test_hybrid_search.py
import pandas as pd
from hybrid_search import search_hybrid, compute_rrf_fusion

def test_rrf_fusion_basic():
    bm25_results = [
        {"goods_name": "책A", "df_index": 0, "bm25_score": 10.0},
        {"goods_name": "책B", "df_index": 1, "bm25_score": 5.0}
    ]
    vector_results = [
        {"goods_name": "책B", "similarity_pct": 85.0, "df_index": 1},
        {"goods_name": "책C", "similarity_pct": 70.0, "df_index": 2}
    ]
    fused = compute_rrf_fusion(bm25_results, vector_results, k=60)
    assert len(fused) == 3
    # 책B should have highest RRF score because it appeared in both
    assert fused[0]["goods_name"] == "책B"
```

- [ ] **Step 2: Run test to verify it fails**

Run: `.\.venv\Scripts\python.exe -m pytest yes24/test_hybrid_search.py -v`
Expected: FAIL (ModuleNotFoundError: No module named 'hybrid_search')

- [ ] **Step 3: Implement `hybrid_search.py`**

```python
# yes24/hybrid_search.py
import pandas as pd

def compute_rrf_fusion(bm25_results, vector_results, k=60):
    """
    Computes Reciprocal Rank Fusion score for BM25 and Vector Search results.
    RRF_score(d) = 1 / (k + rank_bm25) + 1 / (k + rank_vector)
    """
    scores = {}
    item_map = {}

    for rank, item in enumerate(bm25_results, 1):
        idx = item.get('df_index', item.get('goods_name'))
        scores[idx] = scores.get(idx, 0.0) + (1.0 / (k + rank))
        item_map[idx] = dict(item)
        item_map[idx]['bm25_rank'] = rank

    for rank, item in enumerate(vector_results, 1):
        idx = item.get('df_index', item.get('goods_name'))
        scores[idx] = scores.get(idx, 0.0) + (1.0 / (k + rank))
        if idx not in item_map:
            item_map[idx] = dict(item)
        else:
            item_map[idx].update(item)
        item_map[idx]['vector_rank'] = rank

    fused_items = []
    for idx, rrf_score in scores.items():
        entry = item_map[idx]
        entry['rrf_score'] = round(rrf_score, 6)
        if 'similarity_pct' not in entry:
            entry['similarity_pct'] = 0.0
        if 'bm25_rank' not in entry:
            entry['bm25_rank'] = "-"
        if 'vector_rank' not in entry:
            entry['vector_rank'] = "-"
        fused_items.append(entry)

    fused_items.sort(key=lambda x: x['rrf_score'], reverse=True)
    return fused_items

def search_hybrid(query_text, df, chroma_collection, model, bm25_searcher, top_k=5, min_sim_pct=0.0, search_mode="하이브리드 (BM25 + Vector)"):
    if not query_text or not query_text.strip():
        return []

    fetch_k = max(top_k * 3, 20)

    if search_mode == "키워드(BM25) 전용":
        bm25_res = bm25_searcher.search(query_text, top_k=fetch_k)
        results = bm25_res
        for rank, r in enumerate(results, 1):
            r['bm25_rank'] = rank
            r['similarity_pct'] = 0.0
            r['rrf_score'] = round(r.get('bm25_score', 0), 2)
    elif search_mode == "벡터 유사도 전용":
        from chroma_manager import query_chroma_rag
        vec_res = query_chroma_rag(query_text, chroma_collection, model, top_k=fetch_k)
        results = vec_res
        for rank, r in enumerate(results, 1):
            r['vector_rank'] = rank
            r['bm25_rank'] = "-"
            r['rrf_score'] = round(r.get('similarity_pct', 0), 2)
    else: # 하이브리드 (BM25 + Vector)
        from chroma_manager import query_chroma_rag
        bm25_res = bm25_searcher.search(query_text, top_k=fetch_k)
        vec_res = query_chroma_rag(query_text, chroma_collection, model, top_k=fetch_k)
        results = compute_rrf_fusion(bm25_res, vec_res, k=60)

    # Filter by minimum similarity / threshold if applicable
    filtered = []
    for r in results:
        sim = r.get('similarity_pct', 0.0)
        if search_mode == "키워드(BM25) 전용" or sim >= min_sim_pct:
            filtered.append(r)

    return filtered[:top_k]
```

- [ ] **Step 4: Run unit test to verify it passes**

Run: `.\.venv\Scripts\python.exe -m pytest yes24/test_hybrid_search.py -v`
Expected: PASS

- [ ] **Step 5: Commit Task 2**

```bash
git add yes24/hybrid_search.py yes24/test_hybrid_search.py
git commit -m "feat: add RRF hybrid search algorithm and search_hybrid module"
```

---

### Task 3: Streamlit UI (`yes24/app.py`) & Groq Bot (`yes24/groq_bot.py`) 연동

**Files:**
- Modify: `yes24/app.py:110-140`
- Modify: `yes24/app.py:470-493`
- Modify: `yes24/groq_bot.py:35-65`

**Interfaces:**
- Consumes: `BM25Searcher` from `bm25_manager.py`, `search_hybrid` from `hybrid_search.py`

- [ ] **Step 1: Update `yes24/app.py` to initialize BM25 and add Sidebar Controls**

Add cached loading of `BM25Searcher` in `app.py`:
```python
from bm25_manager import BM25Searcher
from hybrid_search import search_hybrid

@st.cache_resource
def get_cached_bm25(_df):
    return BM25Searcher(_df)

bm25_searcher = get_cached_bm25(df)
```

In Sidebar UI settings:
```python
st.sidebar.subheader("🔍 RAG 검색 모드 & 필터 설정")
search_mode = st.sidebar.selectbox(
    "검색 방식",
    ["하이브리드 (BM25 + Vector)", "벡터 유사도 전용", "키워드(BM25) 전용"],
    index=0
)
top_k_select = st.sidebar.slider("추출 도서 개수 (Top-K)", min_value=1, max_value=20, value=5)
min_sim_cutoff = st.sidebar.slider("최소 유사도 임계값 (%)", min_value=0, max_value=100, value=0)
```

- [ ] **Step 2: Update `query_chroma_rag` call in `app.py` to use `search_hybrid`**

```python
with st.spinner(f"[{search_mode}] 방식으로 관련 베스트셀러 도서를 검색 중입니다..."):
    retrieved_books = search_hybrid(
        query_text=prompt,
        df=df,
        chroma_collection=chroma_collection,
        model=model,
        bm25_searcher=bm25_searcher,
        top_k=top_k_select,
        min_sim_pct=min_sim_cutoff,
        search_mode=search_mode
    )
```

In bottom expander of `app.py`:
```python
if retrieved_books:
    with st.expander(f"🔍 [{search_mode}] 참조 Top {len(retrieved_books)} 베스트셀러 도서 목록"):
        for idx, book in enumerate(retrieved_books, 1):
            st.markdown(
                f"**{idx}. {book.get('goods_name')}** | 저자: {book.get('author')} | 출판사: {book.get('publisher')}\n"
                f"- **유사도**: `{book.get('similarity_pct', 0)}%` | **BM25 순위**: `{book.get('bm25_rank', '-')}` | **RRF 점수**: `{book.get('rrf_score', 0)}`"
            )
```

- [ ] **Step 3: Verify app runs cleanly without error**

Run: `.\.venv\Scripts\python.exe -c "import sys; sys.path.append('yes24'); import app; print('App module loaded successfully')"`
Expected: Clean load without SyntaxError/ImportError.

- [ ] **Step 4: Run full pytest suite**

Run: `.\.venv\Scripts\python.exe -m pytest yes24/ -v`
Expected: ALL PASS.

- [ ] **Step 5: Commit Task 3**

```bash
git add yes24/app.py yes24/groq_bot.py
git commit -m "feat: integrate RRF hybrid search and sidebar controls into Streamlit app"
```
