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
    """
    Hybrid Search dispatcher supporting RRF (Reciprocal Rank Fusion), Vector-only, and BM25-only search.
    Filters results by minimum similarity threshold (min_sim_pct).
    """
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
    else:  # 하이브리드 (BM25 + Vector)
        from chroma_manager import query_chroma_rag
        bm25_res = bm25_searcher.search(query_text, top_k=fetch_k)
        vec_res = query_chroma_rag(query_text, chroma_collection, model, top_k=fetch_k)
        results = compute_rrf_fusion(bm25_res, vec_res, k=60)

    # Filter by minimum similarity / threshold if applicable
    filtered = []
    for r in results:
        sim = float(r.get('similarity_pct', 0.0))
        if search_mode == "키워드(BM25) 전용" or sim >= min_sim_pct:
            filtered.append(r)

    return filtered[:top_k]
