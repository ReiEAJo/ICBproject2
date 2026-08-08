# yes24/chroma_manager.py
import os
import chromadb
import pandas as pd
import numpy as np
from embedding_manager import get_combined_text


def get_or_create_chroma(df, embeddings, chroma_path="yes24/chroma_db"):
    """
    Creates or loads a persistent ChromaDB vector store for YES24 bestsellers.
    Stores precomputed SBERT embeddings along with metadata.
    """
    os.makedirs(chroma_path, exist_ok=True)
    client = chromadb.PersistentClient(path=chroma_path)
    collection = client.get_or_create_collection(
        name="yes24_bestsellers",
        metadata={"hnsw:space": "cosine"}
    )

    # Check if already populated
    if collection.count() == len(df):
        return collection

    # If count mismatch or empty, clear and rebuild
    if collection.count() > 0:
        client.delete_collection("yes24_bestsellers")
        collection = client.create_collection(
            name="yes24_bestsellers",
            metadata={"hnsw:space": "cosine"}
        )

    # Prepare data for ChromaDB
    ids = [str(i) for i in range(len(df))]
    embed_list = embeddings.tolist()
    documents = [get_combined_text(row) for _, row in df.iterrows()]

    metadatas = []
    for _, row in df.iterrows():
        metadatas.append({
            "goods_name": str(row.get('goods_name', '')) if pd.notna(row.get('goods_name')) else '',
            "author": str(row.get('author_clean', row.get('author', ''))) if pd.notna(row.get('author_clean')) else '',
            "publisher": str(row.get('publisher', '')) if pd.notna(row.get('publisher')) else '',
            "price_sale": float(row.get('price_sale_num', 0)),
            "sale_index": int(row.get('sale_index_num', 0)),
            "rating": float(row.get('rating_num', 0)),
            "detail_url": str(row.get('detail_url', '')) if pd.notna(row.get('detail_url')) else ''
        })

    # Add in batches of 200
    batch_size = 200
    for i in range(0, len(df), batch_size):
        batch_ids = ids[i:i + batch_size]
        batch_embeds = embed_list[i:i + batch_size]
        batch_docs = documents[i:i + batch_size]
        batch_metas = metadatas[i:i + batch_size]

        collection.add(
            ids=batch_ids,
            embeddings=batch_embeds,
            documents=batch_docs,
            metadatas=batch_metas
        )

    return collection


def query_chroma_rag(query_text, collection, model, top_k=5):
    """
    Queries ChromaDB vector database using model embedding of query_text.
    Returns list of matched book metadata dictionaries with similarity scores.
    """
    if not query_text or not query_text.strip():
        return []

    query_vec = model.encode([query_text], normalize_embeddings=True)[0].tolist()
    results = collection.query(
        query_embeddings=[query_vec],
        n_results=top_k
    )

    items = []
    if results and 'metadatas' in results and len(results['metadatas']) > 0:
        metas = results['metadatas'][0]
        distances = results['distances'][0] if 'distances' in results and len(results['distances']) > 0 else [0]*len(metas)
        docs = results['documents'][0] if 'documents' in results and len(results['documents']) > 0 else ['']*len(metas)

        for meta, dist, doc in zip(metas, distances, docs):
            # Cosine distance to similarity percentage
            sim_score = max(0.0, 1.0 - dist)
            meta_copy = dict(meta)
            meta_copy['similarity_pct'] = round(sim_score * 100, 2)
            meta_copy['document'] = doc
            items.append(meta_copy)

    return items
