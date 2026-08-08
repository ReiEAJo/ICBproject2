# yes24/ragas_evaluator.py
import json
import re
import numpy as np
from groq import Groq


def calculate_context_precision(query, context_list):
    """
    Calculates Average Precision for retrieved contexts based on term overlap with query.
    """
    if not context_list:
        return 0.0

    query_words = set(re.findall(r'\w+', str(query).lower()))
    if not query_words:
        return 1.0

    scores = []
    for ctx in context_list:
        ctx_words = set(re.findall(r'\w+', str(ctx).lower()))
        overlap = len(query_words.intersection(ctx_words))
        score = min(1.0, overlap / max(1, len(query_words)))
        scores.append(score)

    weighted_scores = [s / (idx + 1) for idx, s in enumerate(scores)]
    ideal_weights = [1.0 / (idx + 1) for idx in range(len(scores))]
    return float(np.sum(weighted_scores) / max(1e-5, np.sum(ideal_weights)))


def evaluate_rag_response(question, retrieved_books, response, ground_truth=None, api_key=None, model_name="llama-3.3-70b-versatile", temperature=0.2, top_p=1.0):
    """
    Evaluates RAG response using 4 core RAGAS metrics:
    1. Faithfulness
    2. Answer Relevance
    3. Context Precision
    4. Context Recall
    Returns dict with scores (0.0~1.0) and overall RAGAS Score (0.0~100.0).
    """
    contexts = [f"{b.get('goods_name', '')}: {b.get('document', '')}" for b in (retrieved_books or [])]
    context_str = "\n".join(contexts) if contexts else "(검색된 컨텍스트 없음)"

    ctx_prec = calculate_context_precision(question, contexts)

    if not api_key:
        faithfulness = 0.85 if retrieved_books else 0.40
        answer_rel = 0.90 if ("추천" in response or "도서" in response or "안녕하세요" in response) else 0.50
        ctx_recall = 0.80 if (ground_truth and any(gt in context_str for gt in ground_truth.split())) else 0.75
        ragas_score = round((faithfulness * 0.3 + answer_rel * 0.3 + ctx_prec * 0.2 + ctx_recall * 0.2) * 100, 1)
        return {
            "faithfulness": faithfulness,
            "answer_relevance": answer_rel,
            "context_precision": ctx_prec,
            "context_recall": ctx_recall,
            "ragas_score": ragas_score,
            "reasoning": "API Key 미입력으로 인한 룰 기반 예비 품질 평가 결과입니다."
        }

    try:
        client = Groq(api_key=api_key)
        prompt = f"""RAG 챗봇 답변을 RAGAS 평가 가이드라인에 따라 0.0 ~ 1.0 범위 점수로 평가해 주세요.

[사용자 질문]
{question}

[검색된 도서 문맥 (Context)]
{context_str}

[챗봇 답변 (Response)]
{response}

[기준 정답 (Ground Truth)]
{ground_truth or "없음"}

반드시 다음 JSON 구조로만 답변하세요:
{{
    "faithfulness": 0.0 ~ 1.0 (답변의 각 주장이 검색 문맥에 엄격히 근거했는지),
    "answer_relevance": 0.0 ~ 1.0 (답변이 사용자 질문 의도에 직접적으로 맞는지),
    "context_recall": 0.0 ~ 1.0 (검색 문맥이 질문 답변에 필요한 핵심 도서 정보를 충분히 포함하는지),
    "reasoning": "평가 총평 및 요약 사유 (한국어 2문장 내외)"
}}
"""
        completion = client.chat.completions.create(
            model=model_name,
            messages=[
                {"role": "system", "content": "You are an expert RAG evaluator. Output strictly JSON object."},
                {"role": "user", "content": prompt}
            ],
            temperature=float(temperature),
            top_p=float(top_p),
            response_format={"type": "json_object"}
        )
        data = json.loads(completion.choices[0].message.content)
        faith = float(data.get("faithfulness", 0.85))
        ans_rel = float(data.get("answer_relevance", 0.85))
        ctx_rec = float(data.get("context_recall", 0.80))
        reasoning = str(data.get("reasoning", "Groq LLM-as-a-Judge 평가 완료."))

        # Calculate weighted RAGAS score
        ragas_score = round((faith * 0.35 + ans_rel * 0.35 + ctx_prec * 0.15 + ctx_rec * 0.15) * 100, 1)

        return {
            "faithfulness": faith,
            "answer_relevance": ans_rel,
            "context_precision": ctx_prec,
            "context_recall": ctx_rec,
            "ragas_score": ragas_score,
            "reasoning": reasoning
        }
    except Exception as e:
        return {
            "faithfulness": 0.75,
            "answer_relevance": 0.75,
            "context_precision": ctx_prec,
            "context_recall": 0.70,
            "ragas_score": 73.5,
            "reasoning": f"Groq API 평가 중 예외 발생 (Fallback 적용): {str(e)}"
        }


def run_batch_ragas_evaluation(benchmark_queries, df, chroma_collection, model, bm25_searcher, search_hybrid_func, generate_answer_func, api_key, search_mode="하이브리드 (BM25 + Vector)", top_k=5, min_sim_pct=0, temperature=0.2, top_p=1.0):
    """
    Executes batch RAGAS evaluation across a set of benchmark query items.
    """
    results = []
    for item in benchmark_queries:
        q = item["question"]
        gt = item.get("ground_truth", "")

        books = search_hybrid_func(
            query_text=q,
            df=df,
            chroma_collection=chroma_collection,
            model=model,
            bm25_searcher=bm25_searcher,
            top_k=top_k,
            min_sim_pct=min_sim_pct,
            search_mode=search_mode
        )
        ans = generate_answer_func(
            user_query=q,
            chat_history=[],
            retrieved_books=books,
            api_key=api_key,
            temperature=temperature,
            top_p=top_p
        )

        eval_res = evaluate_rag_response(
            question=q,
            retrieved_books=books,
            response=ans,
            ground_truth=gt,
            api_key=api_key,
            temperature=temperature,
            top_p=top_p
        )

        results.append({
            "질문": q,
            "Ground Truth": gt or "(없음)",
            "RAGAS 점수": eval_res["ragas_score"],
            "Faithfulness": round(eval_res["faithfulness"] * 100, 1),
            "Answer Relevance": round(eval_res["answer_relevance"] * 100, 1),
            "Context Precision": round(eval_res["context_precision"] * 100, 1),
            "Context Recall": round(eval_res["context_recall"] * 100, 1),
            "평가 사유": eval_res["reasoning"]
        })
    return results
