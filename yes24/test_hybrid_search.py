import pandas as pd
from hybrid_search import compute_rrf_fusion

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
    assert fused[0]["bm25_rank"] == 2
    assert fused[0]["vector_rank"] == 1
