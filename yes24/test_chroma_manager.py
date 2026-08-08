# yes24/test_chroma_manager.py
import os
import pandas as pd
from app import load_and_preprocess_data
from embedding_manager import load_or_create_embeddings
from chroma_manager import get_or_create_chroma, query_chroma_rag

base_dir = os.path.dirname(os.path.abspath(__file__))
csv_file = os.path.join(base_dir, "yes24_bestsellers.csv")
npy_file = os.path.join(base_dir, "yes24_embeddings.npy")
vec_tsv = os.path.join(base_dir, "vectors.tsv")
meta_tsv = os.path.join(base_dir, "metadata.tsv")
chroma_dir = os.path.join(base_dir, "chroma_db")

print("--- Step 1: Loading Data & Embeddings ---")
df = load_and_preprocess_data(csv_file)
model, embeddings = load_or_create_embeddings(df, npy_file, vec_tsv, meta_tsv)

print("--- Step 2: Populating ChromaDB Collection ---")
collection = get_or_create_chroma(df, embeddings, chroma_dir)
print(f"ChromaDB Collection count: {collection.count()} items")

print("\n--- Step 3: Testing ChromaDB RAG Vector Query ---")
query_text = "AI 챗봇과 프롬프트 엔지니어링 교재 추천해줘"
results = query_chroma_rag(query_text, collection, model, top_k=3)

for idx, book in enumerate(results, 1):
    print(f"{idx}. [{book['similarity_pct']}%] {book['goods_name']} - {book['author']} ({book['publisher']}) | {book['price_sale']}원")

print("\n[SUCCESS] ChromaDB test verified.")
