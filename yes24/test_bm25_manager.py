import pandas as pd
from bm25_manager import BM25Searcher, tokenize_korean

def test_tokenize_korean():
    tokens = tokenize_korean("파이썬 데이터 분석!")
    assert "파이썬" in tokens
    assert "데이터" in tokens

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
    names = [r["goods_name"] for r in results]
    assert "파이썬 머신러닝 완벽 가이드" in names or "파이썬 웹 스크래핑" in names

def test_bm25_searcher_empty():
    df = pd.DataFrame([{"goods_name": "테스트 도서"}])
    searcher = BM25Searcher(df)
    results = searcher.search("", top_k=5)
    assert results == []
