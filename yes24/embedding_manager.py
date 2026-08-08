# yes24/embedding_manager.py
import os
import numpy as np
import pandas as pd


def get_combined_text(row):
    """
    Combines goods_name, goods_sub_name, author_clean or author, publisher, features, and tags cleanly.
    """
    title = str(row.get('goods_name', '')) if pd.notna(row.get('goods_name')) else ''
    sub = str(row.get('goods_sub_name', '')) if pd.notna(row.get('goods_sub_name')) else ''

    author_val = row.get('author_clean')
    if pd.isna(author_val) or not str(author_val).strip():
        author_val = row.get('author')
    author = str(author_val) if pd.notna(author_val) else ''

    publisher = str(row.get('publisher', '')) if pd.notna(row.get('publisher')) else ''
    features = str(row.get('features', '')) if pd.notna(row.get('features')) else ''
    tags = str(row.get('tags', '')) if pd.notna(row.get('tags')) else ''

    parts = [p.strip() for p in [title, sub, author, publisher, features, tags] if p and str(p).strip()]
    return " ".join(parts)


def export_projector_tsv(df, embeddings, vectors_path, metadata_path):
    """
    Exports vectors.tsv (embedding matrix tab-separated) and metadata.tsv
    (header: goods_name\tauthor\tpublisher\tprice_sale\tsale_index\trating).
    """
    vec_dir = os.path.dirname(os.path.abspath(vectors_path))
    meta_dir = os.path.dirname(os.path.abspath(metadata_path))
    if vec_dir:
        os.makedirs(vec_dir, exist_ok=True)
    if meta_dir:
        os.makedirs(meta_dir, exist_ok=True)

    # Save vectors.tsv
    np.savetxt(vectors_path, embeddings, delimiter='\t', fmt='%.6f')

    # Save metadata.tsv
    with open(metadata_path, 'w', encoding='utf-8') as f:
        f.write("goods_name\tauthor\tpublisher\tprice_sale\tsale_index\trating\n")
        for _, row in df.iterrows():
            name = str(row.get('goods_name', '') if pd.notna(row.get('goods_name')) else '').replace('\t', ' ').replace('\n', ' ')

            author_val = row.get('author_clean')
            if pd.isna(author_val) or not str(author_val).strip():
                author_val = row.get('author')
            author = str(author_val if pd.notna(author_val) else '').replace('\t', ' ').replace('\n', ' ')

            pub = str(row.get('publisher', '') if pd.notna(row.get('publisher')) else '').replace('\t', ' ').replace('\n', ' ')
            price = str(row.get('price_sale_num', 0))
            sale_idx = str(row.get('sale_index_num', 0))
            rating = str(row.get('rating_num', 0))
            f.write(f"{name}\t{author}\t{pub}\t{price}\t{sale_idx}\t{rating}\n")

    return vectors_path, metadata_path


def load_or_create_embeddings(df, npy_path, vectors_path, metadata_path, model_name="jhgan/ko-sbert-sts"):
    """
    Loads model via SentenceTransformer(model_name).
    If npy_path exists and length matches len(df), loads np.load(npy_path) and exports TSVs if missing.
    Else encodes texts using model.encode(texts, normalize_embeddings=True), saves .npy, exports TSVs, and returns (model, embeddings).
    """
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

    npy_dir = os.path.dirname(os.path.abspath(npy_path))
    if npy_dir:
        os.makedirs(npy_dir, exist_ok=True)

    np.save(npy_path, embeddings)
    export_projector_tsv(df, embeddings, vectors_path, metadata_path)

    return model, embeddings


def search_similar_by_query(query_text, df, embeddings, model, top_k=10, min_similarity=0.3):
    """
    Encodes query with normalize_embeddings=True, computes cosine similarity,
    adds similarity and similarity_pct, filters similarity >= min_similarity, sorts descending, and returns top top_k rows.
    """
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
    """
    Computes similarity against embeddings[book_idx], drops self, filters similarity >= min_similarity,
    sorts descending, and returns top top_k rows.
    """
    if book_idx < 0 or book_idx >= len(embeddings):
        return pd.DataFrame()

    target_vec = embeddings[book_idx]
    sims = np.dot(embeddings, target_vec)

    result_df = df.copy()
    result_df['similarity'] = sims
    result_df['similarity_pct'] = (sims * 100).round(2)

    # Exclude self by index label at positional index book_idx
    if book_idx < len(df):
        self_label = df.index[book_idx]
        result_df = result_df.drop(index=self_label, errors='ignore')

    filtered = result_df[result_df['similarity'] >= min_similarity]
    filtered = filtered.sort_values(by='similarity', ascending=False).head(top_k)
    return filtered
