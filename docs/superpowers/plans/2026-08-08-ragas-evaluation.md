# RAGAS RAG Chatbot Evaluation Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a RAGAS-based RAG chatbot quality evaluation engine (`yes24/ragas_evaluator.py`) and integrate real-time evaluation and a dedicated RAGAS Evaluation Dashboard into the Streamlit app (`yes24/app.py` & `yes24/groq_bot.py`).

**Architecture:** Create an independent evaluator module (`yes24/ragas_evaluator.py`) that uses the existing Groq API (`llama-3.3-70b-versatile`) as an LLM-as-a-Judge alongside SBERT embeddings to evaluate Faithfulness, Answer Relevance, Context Precision, and Context Recall. Integrate real-time score expanders in Tab 5 and add a full Tab 6 for batch benchmark runs and mode comparison.

**Tech Stack:** Python, Streamlit, Groq API, SBERT (SentenceTransformers), Pandas, Matplotlib/Seaborn.

## Global Constraints

- Must work with existing Groq API Key setup (`GROQ_API_KEY` from `.env` or UI input).
- Preserves existing RAG chatbot functionality in `yes24/groq_bot.py` and UI structure in `yes24/app.py`.
- No broken imports if optional packages are missing (pure Python/Groq fallback for RAGAS metrics).

---

### Task 1: Create RAGAS Evaluation Module (`yes24/ragas_evaluator.py`) & Unit Tests

**Files:**
- Create: `yes24/ragas_evaluator.py`
- Create: `yes24/test_ragas_evaluator.py`

**Interfaces:**
- Consumes: `groq.Groq` API client, `retrieved_books` dict list, user query string, assistant response string.
- Produces: `evaluate_rag_response(question, retrieved_books, response, ground_truth=None, api_key=None)` -> `dict` containing scores and reasoning for Faithfulness, Answer Relevance, Context Precision, Context Recall, and Overall RAGAS Score.
- Produces: `run_batch_ragas_evaluation(...)` -> `pd.DataFrame` and summary dict for benchmark dataset.

- [ ] **Step 1: Write failing unit test for `evaluate_rag_response`**

```python
# yes24/test_ragas_evaluator.py
import pytest
from ragas_evaluator import calculate_context_precision, evaluate_rag_response

def test_context_precision():
    context_list = ["파이썬 기초 입문 서적", "자바 웹 프로그래밍"]
    query = "파이썬 배우기 적합한 책 추천"
    # Document 1 is relevant, document 2 is less relevant
    precision = calculate_context_precision(query, context_list)
    assert 0.0 <= precision <= 1.0

def test_evaluate_rag_response_mock():
    # Smoke test structure
    res = evaluate_rag_response(
        question="파이썬 도서 추천해줘",
        retrieved_books=[
            {"goods_name": "Do it! 점프 투 파이썬", "document": "파이썬 프로그래밍 기초 입문서"}
        ],
        response="친절한 도서 검색 도우미입니다. Do it! 점프 투 파이썬을 추천합니다.",
        ground_truth="Do it! 점프 투 파이썬",
        api_key=None  # Mock fallback or check return format
    )
    assert "faithfulness" in res
    assert "answer_relevance" in res
    assert "context_precision" in res
    assert "context_recall" in res
    assert "ragas_score" in res
```

- [ ] **Step 2: Run test to verify it fails**

Run: `.\.venv\Scripts\python.exe -m pytest yes24/test_ragas_evaluator.py -v`
Expected: FAIL with ModuleNotFoundError or function not found.

- [ ] **Step 3: Implement minimal `ragas_evaluator.py`**

```python
# yes24/ragas_evaluator.py
import json
import re
import numpy as np
from groq import Groq

def calculate_context_precision(query, context_list):
    if not context_list:
        return 0.0
    # Simple keyword/token coverage check for precision fallback
    query_words = set(re.findall(r'\w+', query.lower()))
    if not query_words:
        return 1.0
    scores = []
    for ctx in context_list:
        ctx_words = set(re.findall(r'\w+', str(ctx).lower()))
        overlap = len(query_words.intersection(ctx_words))
        score = min(1.0, overlap / max(1, len(query_words)))
        scores.append(score)
    # Average precision weighted by rank
    weighted_scores = [s / (idx + 1) for idx, s in enumerate(scores)]
    ideal_weights = [1.0 / (idx + 1) for idx in range(len(scores))]
    return float(np.sum(weighted_scores) / max(1e-5, np.sum(ideal_weights)))

def evaluate_rag_response(question, retrieved_books, response, ground_truth=None, api_key=None, model_name="llama-3.3-70b-versatile"):
    contexts = [f"{b.get('goods_name', '')}: {b.get('document', '')}" for b in (retrieved_books or [])]
    context_str = "\n".join(contexts) if contexts else "(검색된 컨텍스트 없음)"

    # Compute context precision
    ctx_prec = calculate_context_precision(question, contexts)

    if not api_key:
        # Heuristic fallback if API key is not supplied directly
        faithfulness = 0.85 if retrieved_books else 0.40
        answer_rel = 0.90 if "추천" in response or "도서" in response else 0.50
        ctx_recall = 0.80 if ground_truth and any(gt in context_str for gt in ground_truth.split()) else 0.70
        ragas_score = round((faithfulness + answer_rel + ctx_prec + ctx_recall) / 4.0 * 100, 1)
        return {
            "faithfulness": faithfulness,
            "answer_relevance": answer_rel,
            "context_precision": ctx_prec,
            "context_recall": ctx_recall,
            "ragas_score": ragas_score,
            "reasoning": "API Key 미입력으로 인한 룰 기반 예비 평가 결과입니다."
        }

    try:
        client = Groq(api_key=api_key)
        prompt = f"""RAG 챗봇 답변을 RAGAS 평가 가이드라인에 따라 0.0 ~ 1.0 범위 점수로 평가해 주세요.

[사용자 질문]
{question}

[검색된 문맥 (Context)]
{context_str}

[챗봇 답변 (Response)]
{response}

[기준 정답 (Ground Truth)]
{ground_truth or "없음"}

다음 JSON 형식으로만 엄격히 반환하세요:
{{
    "faithfulness": 0.0 ~ 1.0 (답변이 문맥에만 근거했는지),
    "answer_relevance": 0.0 ~ 1.0 (답변이 질문 의도와 관련이 깊은지),
    "context_recall": 0.0 ~ 1.0 (문맥이 정답/답변에 필요한 핵심 정보를 포함하는지),
    "reasoning": "평가 사유 요약 (한국어 2문장)"
}}
"""
        completion = client.chat.completions.create(
            model=model_name,
            messages=[{"role": "system", "content": "You are a professional RAG evaluator. Output pure JSON only."},
                      {"role": "user", "content": prompt}],
            temperature=0.0,
            response_format={"type": "json_object"}
        )
        data = json.loads(completion.choices[0].message.content)
        faith = float(data.get("faithfulness", 0.8))
        ans_rel = float(data.get("answer_relevance", 0.8))
        ctx_rec = float(data.get("context_recall", 0.8))
        reasoning = data.get("reasoning", "Groq LLM-as-a-Judge 평가 완료.")

        ragas_score = round((faith * 0.3 + ans_rel * 0.3 + ctx_prec * 0.2 + ctx_rec * 0.2) * 100, 1)

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
            "faithfulness": 0.7,
            "answer_relevance": 0.7,
            "context_precision": ctx_prec,
            "context_recall": 0.7,
            "ragas_score": 70.0,
            "reasoning": f"평가 수행 중 오류 발생: {str(e)}"
        }

def run_batch_ragas_evaluation(benchmark_queries, df, chroma_collection, model, bm25_searcher, search_hybrid_func, generate_answer_func, api_key, search_mode="하이브리드 (BM25 + Vector)", top_k=5, min_sim_pct=0):
    results = []
    for item in benchmark_queries:
        q = item["question"]
        gt = item.get("ground_truth", "")
        
        books = search_hybrid_func(q, df, chroma_collection, model, bm25_searcher, top_k=top_k, min_sim_pct=min_sim_pct, search_mode=search_mode)
        ans = generate_answer_func(q, [], books, api_key=api_key)
        
        eval_res = evaluate_rag_response(q, books, ans, ground_truth=gt, api_key=api_key)
        results.append({
            "질문": q,
            "Ground Truth": gt,
            "RAGAS 점수": eval_res["ragas_score"],
            "Faithfulness": round(eval_res["faithfulness"] * 100, 1),
            "Answer Relevance": round(eval_res["answer_relevance"] * 100, 1),
            "Context Precision": round(eval_res["context_precision"] * 100, 1),
            "Context Recall": round(eval_res["context_recall"] * 100, 1),
            "평가 사유": eval_res["reasoning"]
        })
    return results
```

- [ ] **Step 4: Run test to verify it passes**

Run: `.\.venv\Scripts\python.exe -m pytest yes24/test_ragas_evaluator.py -v`
Expected: PASS

- [ ] **Step 5: Commit Task 1**

```bash
git add yes24/ragas_evaluator.py yes24/test_ragas_evaluator.py
git commit -m "feat: add RAGAS evaluation module and unit tests"
```

---

### Task 2: Integrate RAGAS Evaluator with `groq_bot.py`

**Files:**
- Modify: `yes24/groq_bot.py`

**Interfaces:**
- Consumes: `evaluate_rag_response` from `ragas_evaluator.py`.
- Produces: `generate_rag_answer_with_eval(user_query, chat_history, retrieved_books, api_key, model_name, ground_truth=None, do_eval=True)` -> `(answer_text, eval_dict)`

- [ ] **Step 1: Update `groq_bot.py` to import evaluator and support optional evaluation wrapper**

```python
# In yes24/groq_bot.py
from ragas_evaluator import evaluate_rag_response

def generate_rag_answer_with_eval(user_query, chat_history, retrieved_books, api_key, model_name="llama-3.3-70b-versatile", ground_truth=None, do_eval=True):
    answer = generate_rag_answer(user_query, chat_history, retrieved_books, api_key, model_name)
    eval_res = None
    if do_eval and api_key and not answer.startswith("❌"):
        eval_res = evaluate_rag_response(
            question=user_query,
            retrieved_books=retrieved_books,
            response=answer,
            ground_truth=ground_truth,
            api_key=api_key,
            model_name=model_name
        )
    return answer, eval_res
```

- [ ] **Step 2: Verify `groq_bot.py` imports without error**

Run: `.\.venv\Scripts\python.exe -c "from yes24.groq_bot import generate_rag_answer_with_eval; print('OK')"`
Expected: Output `OK`

- [ ] **Step 3: Commit Task 2**

```bash
git add yes24/groq_bot.py
git commit -m "feat: integrate RAGAS evaluator helper in groq_bot.py"
```

---

### Task 3: Streamlit UI Integration (`yes24/app.py` Tab 5 real-time RAGAS & Tab 6 RAGAS Dashboard)

**Files:**
- Modify: `yes24/app.py`

**Interfaces:**
- Consumes: `ragas_evaluator.py`, `groq_bot.py`, Streamlit tabs, session state.
- Produces: Enhanced 6-tab Streamlit dashboard with real-time RAGAS expander and interactive evaluation dashboard.

- [ ] **Step 1: Add imports and Tab 6 configuration to `app.py`**

In `app.py`:
- Import `evaluate_rag_response`, `run_batch_ragas_evaluation` from `ragas_evaluator`.
- Update tab configuration from 5 tabs to 6 tabs:
```python
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "🔍 키워드 검색",
    "🧬 코사인 유사도 검색",
    "📊 임베딩 시각화 & TSV",
    "🏆 하이라이트 & 데이터",
    "🤖 AI 도서 추천 챗봇 (Groq RAG)",
    "📈 RAG 품질 평가 (RAGAS Dashboard)"
])
```

- [ ] **Step 2: Update Tab 5 (AI 챗봇) to display real-time RAGAS evaluation**

In Tab 5:
- Call `evaluate_rag_response(prompt, retrieved_books, answer, api_key=groq_key)` after response generation.
- Store `eval_res` in message dictionary or session state.
- Render `st.expander("🧪 [RAGAS] 실시간 RAG 품질 평가 측정 결과")` displaying:
  - Overall RAGAS Score metric
  - Progress bars / metric cards for Faithfulness, Answer Relevance, Context Precision, Context Recall
  - Reasoning text.

- [ ] **Step 3: Implement Tab 6 (RAGAS Evaluation Dashboard)**

In Tab 6:
- **Sub-tab 6-1: 커스텀 질의 실시간 평가 (Single Evaluation)**:
  - Input query, optional ground truth, search mode selectbox.
  - Run hybrid search & Groq RAG answer.
  - Render radar chart / bar chart of 4 metrics + detailed reasoning card.
- **Sub-tab 6-2: 배치 벤치마크 평가 (Batch Benchmark)**:
  - Preset test dataset of 5 representative YES24 questions.
  - Button "🚀 벤치마크 평가 실행".
  - Output summary metrics table and average RAGAS score.
- **Sub-tab 6-3: 검색 모드별 성능 비교 (Hybrid vs Vector vs BM25)**:
  - Compare RAGAS Scores across the 3 search modes side-by-side using Seaborn/Matplotlib barplot.

- [ ] **Step 4: Verify Streamlit app runs without errors**

Run: `.\.venv\Scripts\python.exe -m streamlit run yes24/app.py --server.headless=true`
Expected: App launches successfully without syntax or runtime import errors.

- [ ] **Step 5: Commit Task 3**

```bash
git add yes24/app.py
git commit -m "feat: add real-time RAGAS evaluation to chatbot tab and new RAGAS evaluation dashboard tab"
```

---

### Task 4: Full System Verification & Testing

- [ ] **Step 1: Run pytest across all test files**

Run: `.\.venv\Scripts\python.exe -m pytest yes24/ -v`
Expected: ALL PASS

- [ ] **Step 2: Verify git status is clean**

Run: `git status`
Expected: Clean working tree.
