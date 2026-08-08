# -*- coding: utf-8 -*-
import json
import os
import re
import streamlit as st
import numpy as np
from groq import Groq
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer

# Load .env from local directory or parent
env_path = os.path.join(os.path.dirname(__file__), ".env")
if os.path.exists(env_path):
    load_dotenv(dotenv_path=env_path)
load_dotenv()

# Page config
st.set_page_config(
    page_title="삼성화재 애니카 자동차보험 AI 도우미",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="expanded"
)


@st.cache_resource
def load_data_and_embeddings():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    json_path = os.path.join(base_dir, "chunks.json")
    npy_path = os.path.join(base_dir, "embeddings.npy")

    if not os.path.exists(json_path) or not os.path.exists(npy_path):
        st.error("데이터 파일(chunks.json, embeddings.npy)이 없습니다. pdf_processor.py를 먼저 실행해 주세요.")
        st.stop()

    with open(json_path, "r", encoding="utf-8") as f:
        chunks = json.load(f)

    embeddings = np.load(npy_path)
    model = SentenceTransformer("jhgan/ko-sbert-sts")
    return chunks, embeddings, model


def search_hybrid_samsungfire(query, chunks, embeddings, model, top_k=5):
    q_emb = model.encode([query], normalize_embeddings=True)[0]
    sims = np.dot(embeddings, q_emb)

    q_tokens = set(re.findall(r'\w+', query.lower()))
    bm25_scores = []
    for c in chunks:
        c_tokens = set(re.findall(r'\w+', c["text"].lower()))
        score = len(q_tokens.intersection(c_tokens))
        bm25_scores.append(score)

    vector_ranks = np.argsort(-sims)
    bm25_ranks = np.argsort(-np.array(bm25_scores))

    rrf_dict = {}
    k = 60
    for r, idx in enumerate(vector_ranks[:50]):
        rrf_dict[idx] = rrf_dict.get(idx, 0.0) + (1.0 / (k + r + 1))
    for r, idx in enumerate(bm25_ranks[:50]):
        rrf_dict[idx] = rrf_dict.get(idx, 0.0) + (1.0 / (k + r + 1))

    sorted_indices = sorted(rrf_dict.keys(), key=lambda i: rrf_dict[i], reverse=True)[:top_k]

    results = []
    for idx in sorted_indices:
        res_chunk = chunks[idx].copy()
        res_chunk["similarity_pct"] = round(float(sims[idx]) * 100, 1)
        res_chunk["rrf_score"] = round(float(rrf_dict[idx]), 4)
        results.append(res_chunk)

    return results


SYSTEM_PROMPT = """친절하고 신뢰받는 삼성화재 애니카 자동차보험 전문 AI 상담원입니다.

[답변 엄격 규칙]
1. 반드시 아래에 제공되는 [삼성화재 약관 및 가이드북 검색 결과] 정보에 실제 존재하는 내용만을 기반으로 친절하게 답변하세요.
2. 약관 및 가이드북 정보에 기반하여 답변할 때, 관련된 약관/가이드북 페이지 번호(예: Page 57)를 함께 안내해 주세요.
3. 조건에 맞는 내용이 없거나 명확하지 않다면 외부 정보를 추측하여 답변하지 말고 "죄송합니다. 제공된 삼성화재 약관/가이드북 문서에서 해당 내용을 찾을 수 없습니다."라고 안내해 주세요.
"""


def generate_samsungfire_answer(query, chat_history, retrieved_chunks, api_key, temperature=0.2, top_p=1.0):
    if not api_key:
        return "❌ Groq API Key가 설정되지 않았습니다. 사이드바에서 API Key를 입력하거나 .env 파일에 GROQ_API_KEY를 등록해 주세요."

    client = Groq(api_key=api_key)

    context_str = "[삼성화재 약관 및 가이드북 검색 결과]\n"
    if retrieved_chunks:
        for idx, c in enumerate(retrieved_chunks, 1):
            context_str += f"{idx}. [Page {c['page']}] {c['text']}\n\n"
    else:
        context_str += "(관련 약관 정보 없음)\n"

    messages = [{"role": "system", "content": SYSTEM_PROMPT + "\n\n" + context_str}]
    for msg in chat_history[-6:]:
        messages.append({"role": msg["role"], "content": msg["content"]})
    if not chat_history or chat_history[-1]["content"] != query:
        messages.append({"role": "user", "content": query})

    try:
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=messages,
            temperature=float(temperature),
            top_p=float(top_p),
            max_tokens=1024
        )
        return completion.choices[0].message.content
    except Exception as e:
        return f"❌ Groq API 호출 중 오류가 발생했습니다: {str(e)}"


# Main App UI
chunks, embeddings, model = load_data_and_embeddings()

st.sidebar.header("⚙️ 삼성화재 챗봇 & Groq 설정")
env_key = os.getenv("GROQ_API_KEY", "").strip()
if env_key:
    st.sidebar.success("🔑 Groq API Key: `.env` 감지됨")
    user_key = st.sidebar.text_input("Groq API Key (재정의)", value="", type="password")
    api_key = user_key.strip() if user_key.strip() else env_key
else:
    st.sidebar.warning("🔑 Groq API Key 미설정")
    user_key = st.sidebar.text_input("Groq API Key 입력", value="", type="password")
    api_key = user_key.strip() if user_key.strip() else None

st.sidebar.markdown("---")
st.sidebar.header("🎛️ 검색 및 LLM 옵션")
top_k_val = st.sidebar.slider("약관 참조 개수 (Top-K)", 1, 10, 4)
temp_val = st.sidebar.slider("Temperature (창의성)", 0.0, 1.0, 0.2, 0.05)
top_p_val = st.sidebar.slider("Top-P (샘플링)", 0.0, 1.0, 1.0, 0.05)

st.title("🚗 삼성화재 애니카 자동차보험 AI 도우미")
st.markdown("삼성화재 약관 및 가이드북(276페이지)을 바탕으로 정확하고 빠른 보상/가입 안내를 제공합니다. *(저사양 노트북 초고속 하이브리드 검색 적용)*")

col1, col2, col3 = st.columns(3)
col1.metric("총 참조 약관 페이지", "276 페이지")
col2.metric("약관 청크 수", f"{len(chunks):,} 개")
col3.metric("검색 반응 속도", "< 0.05 초 (CPU)")

st.markdown("---")

if "samsungfire_messages" not in st.session_state:
    st.session_state.samsungfire_messages = [
        {
            "role": "assistant",
            "content": "안녕하세요! 삼성화재 애니카 자동차보험 전문 AI 상담원입니다. 자동차보험 보상 범위, 사고 처리 절차, 특약 가입 문의 등 궁금하신 점을 말씀해 주세요!"
        }
    ]

for msg in st.session_state.samsungfire_messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        if "retrieved_chunks" in msg and msg["retrieved_chunks"]:
            with st.expander("🔍 참조된 삼성화재 약관/가이드북 출처 보기"):
                for idx, c in enumerate(msg["retrieved_chunks"], 1):
                    st.markdown(f"**{idx}. [Page {c['page']}]** (유사도: `{c['similarity_pct']}%`)\n- {c['text']}")

if prompt := st.chat_input("질문을 입력하세요 (예: 사고 시 대처 방법 및 대물배상 보상 한도 알려줘)"):
    if not api_key:
        st.error("Groq API Key를 먼저 입력해 주세요!")
    else:
        st.session_state.samsungfire_messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.spinner("삼성화재 약관/가이드북 문서를 검색 중입니다..."):
            retrieved = search_hybrid_samsungfire(prompt, chunks, embeddings, model, top_k=top_k_val)

        with st.chat_message("assistant"):
            with st.spinner("Groq AI 상담원이 약관을 확인 후 답변을 작성하고 있습니다..."):
                ans_text = generate_samsungfire_answer(
                    query=prompt,
                    chat_history=st.session_state.samsungfire_messages[:-1],
                    retrieved_chunks=retrieved,
                    api_key=api_key,
                    temperature=temp_val,
                    top_p=top_p_val
                )
                st.markdown(ans_text)

                if retrieved:
                    with st.expander("🔍 참조된 삼성화재 약관/가이드북 출처 보기"):
                        for idx, c in enumerate(retrieved, 1):
                            st.markdown(f"**{idx}. [Page {c['page']}]** (유사도: `{c['similarity_pct']}%`)\n- {c['text']}")

        st.session_state.samsungfire_messages.append({
            "role": "assistant",
            "content": ans_text,
            "retrieved_chunks": retrieved
        })
