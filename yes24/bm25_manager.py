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
    """
    Okapi BM25 Keyword Search Engine for YES24 Bestseller Dataset.
    k1 = 1.5, b = 0.75
    """
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

        self.avgdl = (sum(self.doc_lens) / self.corpus_size) if self.corpus_size > 0 else 1.0

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
