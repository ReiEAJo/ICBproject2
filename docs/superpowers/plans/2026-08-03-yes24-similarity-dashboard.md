# YES24 Keyword & Similarity Search Streamlit Dashboard Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a comprehensive Streamlit dashboard for YES24 bestsellers data with keyword search, SBERT-based vector similarity search, precomputed embedding caching, and TensorFlow Embedding Projector TSV file generation.

**Architecture:** Model `jhgan/ko-sbert-sts` generates embeddings for book texts (`goods_name` + `goods_sub_name` + `author_clean` + `publisher` + `features` + `tags`) and caches them as `yes24_embeddings.npy`. `embedding_manager.py` handles model loading, embedding generation, caching, TSV export, and cosine similarity scoring. `app.py` exposes 4 interactive Streamlit tabs with keyword filtering, similarity sliders, 2D PCA embedding visualization, and tabular data views.

**Tech Stack:** Python 3.12+, Streamlit, pandas, numpy, scikit-learn, sentence-transformers, torch, matplotlib, seaborn.

## Global Constraints

- **Embedding Model**: `jhgan/ko-sbert-sts`
- **Embedding Storage**: `yes24/yes24_embeddings.npy`
- **Projector Files**: `yes24/vectors.tsv`, `yes24/metadata.tsv`
- **Table Display**: All book search results MUST be displayed as tables (`st.dataframe`), NOT dropdown selectboxes.

---

### Task 1: Create `embedding_manager.py` for Embedding & Similarity Logic

**Files:**
- Create: `yes24/embedding_manager.py`
- Test/Verification: `yes24/test_embedding_manager.py`

**Interfaces:**
- Produces:
  - `load_or_create_embeddings(df, csv_path, npy_path, vectors_tsv_path, metadata_tsv_path, model_name="jhgan/ko-sbert-sts") -> np.ndarray`
  - `search_similar_by_query(query_text, df, embeddings, model, top_k=10, min_similarity=0.3) -> pd.DataFrame`
  - `search_similar_by_book_idx(book_idx, df, embeddings, top_k=10, min_similarity=0.3) -> pd.DataFrame`
  - `export_projector_tsv(df, embeddings, vectors_path, metadata_path) -> (str, str)`

- [ ] **Step 1: Write `yes24/embedding_manager.py` implementation**

```python
# yes24/embedding_manager.py
import os
import numpy as np
import pandas as pd

def get_combined_text(row):
    title = str(row.get('goods_name', ''))
    sub = str(row.get('goods_sub_name', '')) if pd.notna(row.get('goods_sub_name')) else ''
    author = str(row.get('author_clean', row.get('author', '')))
    publisher = str(row.get('publisher', ''))
    features = str(row.get('features', '')) if pd.notna(row.get('features')) else ''
    tags = str(row.get('tags', '')) if pd.notna(row.get('tags')) else ''
    return f"{title} {sub} {author} {publisher} {features} {tags}".strip()

def export_projector_tsv(df, embeddings, vectors_path, metadata_path):
    os.makedirs(os.path.dirname(vectors_path), exist_ok=True)
    
    # Save vectors.tsv
    np.savetxt(vectors_path, embeddings, delimiter='\t', fmt='%.6f')
    
    # Save metadata.tsv
    with open(metadata_path, 'w', encoding='utf-8') as f:
        f.write("goods_name\tauthor\tpublisher\tprice_sale\tsale_index\trating\n")
        for _, row in df.iterrows():
            name = str(row.get('goods_name', '')).replace('\t', ' ').replace('\n', ' ')
            author = str(row.get('author_clean', '')).replace('\t', ' ').replace('\n', ' ')
            pub = str(row.get('publisher', '')).replace('\t', ' ').replace('\n', ' ')
            price = str(row.get('price_sale_num', 0))
            sale_idx = str(row.get('sale_index_num', 0))
            rating = str(row.get('rating_num', 0))
            f.write(f"{name}\t{author}\t{pub}\t{price}\t{sale_idx}\t{rating}\n")
            
    return vectors_path, metadata_path

def load_or_create_embeddings(df, npy_path, vectors_path, metadata_path, model_name="jhgan/ko-sbert-sts"):
    from sentence_transformers import SentenceTransformer
    
    model = SentenceTransformer(model_name)
    
    if os.path.exists(npy_path):
        embeddings = np.load(npy_path)
        if len(embeddings) == len(df):
            if not os.path.exists(vectors_path) or not os.path.exists(metadata_path):
                export_projector_tsv(df, embeddings, vectors_path, metadata_path)
            return model, embeddings
            
    texts = [get_combined_text(row) for _, row in df.iterrows()]
    embeddings = model.encode(texts, show_progress_bar=False, normalize_embeddings=True)
    
    os.makedirs(os.path.dirname(npy_path), exist_ok=True)
    np.save(npy_path, embeddings)
    export_projector_tsv(df, embeddings, vectors_path, metadata_path)
    
    return model, embeddings

def search_similar_by_query(query_text, df, embeddings, model, top_k=10, min_similarity=0.3):
    if not query_text or len(query_text.strip()) == 0:
        return pd.DataFrame()
        
    query_vec = model.encode([query_text], normalize_embeddings=True)[0]
    sims = np.dot(embeddings, query_vec)
    
    result_df = df.copy()
    result_df['similarity'] = sims
    result_df['similarity_pct'] = (sims * 100).round(2)
    
    filtered = result_df[result_df['similarity'] >= min_similarity]
    filtered = filtered.sort_values(by='similarity', ascending=False).head(top_k)
    return filtered

def search_similar_by_book_idx(book_idx, df, embeddings, top_k=10, min_similarity=0.3):
    if book_idx < 0 or book_idx >= len(embeddings):
        return pd.DataFrame()
        
    target_vec = embeddings[book_idx]
    sims = np.dot(embeddings, target_vec)
    
    result_df = df.copy()
    result_df['similarity'] = sims
    result_df['similarity_pct'] = (sims * 100).round(2)
    
    # Exclude self
    result_df = result_df.drop(index=book_idx, errors='ignore')
    
    filtered = result_df[result_df['similarity'] >= min_similarity]
    filtered = filtered.sort_values(by='similarity', ascending=False).head(top_k)
    return filtered
```

- [ ] **Step 2: Create unit verification script `yes24/test_embedding_manager.py`**

```python
# yes24/test_embedding_manager.py
import os
import pandas as pd
from app import load_and_preprocess_data
from embedding_manager import load_or_create_embeddings, search_similar_by_query

base_dir = os.path.dirname(os.path.abspath(__file__))
csv_file = os.path.join(base_dir, "yes24_bestsellers.csv")
npy_file = os.path.join(base_dir, "yes24_embeddings.npy")
vec_tsv = os.path.join(base_dir, "vectors.tsv")
meta_tsv = os.path.join(base_dir, "metadata.tsv")

df = load_and_preprocess_data(csv_file)
print(f"Loaded {len(df)} books")

model, embeddings = load_or_create_embeddings(df, npy_file, vec_tsv, meta_tsv)
print(f"Embeddings shape: {embeddings.shape}")
print(f"NPY exists: {os.path.exists(npy_file)}")
print(f"Vectors TSV exists: {os.path.exists(vec_tsv)}")
print(f"Metadata TSV exists: {os.path.exists(meta_tsv)}")

res = search_similar_by_query("파이썬 코딩 입문", df, embeddings, model, top_k=5, min_similarity=0.2)
print("Search results for '파이썬 코딩 입문':")
for _, r in res.iterrows():
    print(f"[{r['similarity_pct']}%] {r['goods_name']} ({r['author_clean']})")
```

- [ ] **Step 3: Run unit verification**

Run: `.\.venv\Scripts\python.exe yes24/test_embedding_manager.py`
Expected: Embedding calculation/loading success, file creation verified, sample query search returns top matched books.

---

### Task 2: Update `yes24/app.py` Streamlit UI with Keyword & Similarity Search, Sliders, and 2D Projection

**Files:**
- Modify: `yes24/app.py`

**Interfaces:**
- Consumes: `load_or_create_embeddings`, `search_similar_by_query`, `search_similar_by_book_idx` from `yes24/embedding_manager.py`

- [ ] **Step 1: Update `yes24/app.py`**
  - Load embeddings and model cached via `@st.cache_resource` / `@st.cache_data`.
  - Reorganize main tabs into:
    1. 🔍 **키워드 검색** (Keyword text search input + filtering options + dataframe table)
    2. 🧬 **코사인 유사도 검색** (Query text search / book selection + min_similarity slider + top_k slider + dataframe table with similarity %)
    3. 📊 **임베딩 시각화 & 프로젝터 TSV** (2D PCA scatter plot of book embeddings + TSV download buttons for vectors.tsv and metadata.tsv + TensorFlow Projector instructions)
    4. 🏆 **하이라이트 & 데이터 브라우저** (Original top 3 highlights, metrics, full data table)

- [ ] **Step 2: Verify `yes24/app.py` syntax and run app**

Run: `.\.venv\Scripts\python.exe -m streamlit run yes24/app.py --server.headless true`

- [ ] **Step 3: Verify search functionality in running dashboard**

Check log and test similarity search, slider interactions, and TSV exports.

---
