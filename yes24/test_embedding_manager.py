# yes24/test_embedding_manager.py
import os
import pandas as pd
from app import load_and_preprocess_data
from embedding_manager import load_or_create_embeddings, search_similar_by_query, search_similar_by_book_idx

base_dir = os.path.dirname(os.path.abspath(__file__))
csv_file = os.path.join(base_dir, "yes24_bestsellers.csv")
npy_file = os.path.join(base_dir, "yes24_embeddings.npy")
vec_tsv = os.path.join(base_dir, "vectors.tsv")
meta_tsv = os.path.join(base_dir, "metadata.tsv")

print("--- Step 1: Data Loading & Preprocessing ---")
df = load_and_preprocess_data(csv_file)
print(f"Loaded {len(df)} books from dataset.")

print("\n--- Step 2: Load or Generate Embeddings & TSV Projector Files ---")
model, embeddings = load_or_create_embeddings(df, npy_file, vec_tsv, meta_tsv)
print(f"Embeddings shape: {embeddings.shape}")
print(f"NPY file exists: {os.path.exists(npy_file)} ({os.path.getsize(npy_file) if os.path.exists(npy_file) else 0} bytes)")
print(f"Vectors TSV exists: {os.path.exists(vec_tsv)} ({os.path.getsize(vec_tsv) if os.path.exists(vec_tsv) else 0} bytes)")
print(f"Metadata TSV exists: {os.path.exists(meta_tsv)} ({os.path.getsize(meta_tsv) if os.path.exists(meta_tsv) else 0} bytes)")

print("\n--- Step 3: Test Query Similarity Search ---")
query = "파이썬 코딩 입문"
res_query = search_similar_by_query(query, df, embeddings, model, top_k=5, min_similarity=0.2)
print(f"Top 5 search results for query '{query}':")
for _, r in res_query.iterrows():
    print(f"  [{r['similarity_pct']}%] {r.get('goods_name', '')} ({r.get('author_clean', r.get('author', ''))})")

print("\n--- Step 4: Test Book Index Similarity Search ---")
target_idx = 0
target_book_name = df.iloc[target_idx].get('goods_name', '')
res_book = search_similar_by_book_idx(target_idx, df, embeddings, top_k=5, min_similarity=0.2)
print(f"Top 5 similar books to book index {target_idx} ('{target_book_name}'):")
for _, r in res_book.iterrows():
    print(f"  [{r['similarity_pct']}%] {r.get('goods_name', '')} ({r.get('author_clean', r.get('author', ''))})")

print("\n[SUCCESS] Unit verification completed successfully.")
