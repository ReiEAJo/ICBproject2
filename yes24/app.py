# -*- coding: utf-8 -*-
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import re
import os
from sklearn.decomposition import PCA

try:
    from embedding_manager import (
        load_or_create_embeddings,
        search_similar_by_query,
        search_similar_by_book_idx
    )
    from chroma_manager import get_or_create_chroma, query_chroma_rag
    from groq_bot import get_groq_api_key, generate_rag_answer, generate_rag_answer_with_eval
    from bm25_manager import BM25Searcher
    from hybrid_search import search_hybrid
    from ragas_evaluator import evaluate_rag_response, run_batch_ragas_evaluation
except ImportError:
    from yes24.embedding_manager import (
        load_or_create_embeddings,
        search_similar_by_query,
        search_similar_by_book_idx
    )
    from yes24.chroma_manager import get_or_create_chroma, query_chroma_rag
    from yes24.groq_bot import get_groq_api_key, generate_rag_answer, generate_rag_answer_with_eval
    from yes24.bm25_manager import BM25Searcher
    from yes24.hybrid_search import search_hybrid
    from yes24.ragas_evaluator import evaluate_rag_response, run_batch_ragas_evaluation



@st.cache_resource
def get_cached_bm25(_df):
    return BM25Searcher(_df)


# 페이지 기본 설정
st.set_page_config(
    page_title="YES24 베스트셀러 검색 & AI 챗봇 대시보드",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# matplotlib 한글 폰트 설정 (Windows 기준 Malgun Gothic)
plt.rc('font', family='Malgun Gothic')
plt.rc('axes', unicode_minus=False)
sns.set_theme(style="whitegrid", font="Malgun Gothic")


@st.cache_data
def load_and_preprocess_data(csv_path):
    if not os.path.exists(csv_path):
        return None

    df = pd.read_csv(csv_path)
    df = df.copy()

    # 1. 가격 컬럼 숫자 변환
    def clean_price(val):
        if pd.isna(val):
            return np.nan
        cleaned = re.sub(r'[^\d.]', '', str(val))
        return float(cleaned) if cleaned else np.nan

    df['price_original_num'] = df['opt_shopPrice'].fillna(df['price_original'].apply(clean_price))
    df['price_sale_num'] = df['opt_salePrice'].fillna(df['price_sale'].apply(clean_price))

    # 2. 할인율 변환
    def clean_discount(val):
        if pd.isna(val):
            return 0.0
        cleaned = re.sub(r'[^\d.]', '', str(val))
        return float(cleaned) if cleaned else 0.0

    df['discount_rate_num'] = df['discount_rate'].apply(clean_discount)

    # 3. 숫자 타입 변환
    df['sale_index_num'] = pd.to_numeric(df['sale_index'], errors='coerce').fillna(0).astype(int)
    df['review_count_num'] = pd.to_numeric(df['review_count'], errors='coerce').fillna(0).astype(int)
    df['rating_num'] = pd.to_numeric(df['rating'], errors='coerce').fillna(0.0)

    # 4. 출판일 연도 추출
    def extract_year(val):
        if pd.isna(val):
            return np.nan
        match = re.search(r'(\d{4})년', str(val))
        return int(match.group(1)) if match else np.nan
    df['publish_year'] = df['publish_date'].apply(extract_year)

    # 5. 저자명 정제
    def clean_author(val):
        if pd.isna(val):
            return "저자 미상"
        author = str(val).strip()
        author = re.sub(r'[<>\s]', '', author)
        if author.endswith("저"):
            author = author[:-1].strip()
        return author

    df['author_clean'] = df['opt_goodsAuth'].fillna(df['author']).apply(clean_author)

    return df


@st.cache_resource
def get_cached_embeddings(_df, npy_path, vec_tsv, meta_tsv):
    return load_or_create_embeddings(_df, npy_path, vec_tsv, meta_tsv, model_name="jhgan/ko-sbert-sts")


@st.cache_resource
def get_cached_chroma(_df, _embeddings, chroma_path):
    return get_or_create_chroma(_df, _embeddings, chroma_path)


# 데이터 경로 및 로드
base_dir = os.path.dirname(os.path.abspath(__file__))
csv_file = os.path.join(base_dir, "yes24_bestsellers.csv")
npy_file = os.path.join(base_dir, "yes24_embeddings.npy")
vec_tsv_file = os.path.join(base_dir, "vectors.tsv")
meta_tsv_file = os.path.join(base_dir, "metadata.tsv")
chroma_dir = os.path.join(base_dir, "chroma_db")

df = load_and_preprocess_data(csv_file)

if df is None:
    st.error("데이터 파일(yes24_bestsellers.csv)을 찾을 수 없습니다.")
else:
    # 임베딩 모델 및 ChromaDB 벡터 로드 (캐싱)
    with st.spinner("SBERT 임베딩 및 ChromaDB 벡터 데이터베이스를 로딩 중입니다..."):
        model, embeddings = get_cached_embeddings(df, npy_file, vec_tsv_file, meta_tsv_file)
        chroma_collection = get_cached_chroma(df, embeddings, chroma_dir)
        bm25_searcher = get_cached_bm25(df)

    # --- 사이드바 설정 및 필터 ---
    st.sidebar.header("⚙️ 대시보드 및 Groq 설정")

    # Groq API Key 입력 로직 (.env 및 UI 입력 지원)
    env_groq_key = get_groq_api_key()
    if env_groq_key:
        st.sidebar.success("🔑 Groq API Key: `.env` 감지됨")
        user_groq_key = st.sidebar.text_input("Groq API Key (재정의)", value="", type="password", help=".env 키를 변경하려면 입력하세요")
        groq_key = user_groq_key.strip() if user_groq_key.strip() else env_groq_key
    else:
        st.sidebar.warning("🔑 Groq API Key가 `.env`에 설정되지 않았습니다.")
        user_groq_key = st.sidebar.text_input("Groq API Key 입력", value="", type="password", help="Groq API Key를 입력하세요")
        groq_key = user_groq_key.strip() if user_groq_key.strip() else None

    st.sidebar.markdown("---")
    st.sidebar.header("🎛️ Groq LLM 하이퍼파라미터")
    temperature_select = st.sidebar.slider(
        "Temperature (창의성)",
        min_value=0.0,
        max_value=1.0,
        value=0.2,
        step=0.05,
        help="답변 생성을 조절합니다. (0.0: 일관됨, 1.0: 높은 창의성)"
    )
    top_p_select = st.sidebar.slider(
        "Top-P (샘플링)",
        min_value=0.0,
        max_value=1.0,
        value=1.0,
        step=0.05,
        help="누적 확률 샘플링 임계값을 조절합니다."
    )
    do_eval_select = st.sidebar.checkbox(
        "실시간 RAGAS 품질 평가 수행",
        value=True,
        help="챗봇 답변 생성 후 RAGAS 지표(Faithfulness, Answer Relevance, Context Precision, Context Recall)를 자동 측정합니다."
    )

    st.sidebar.markdown("---")
    st.sidebar.header("🤖 RAG 하이브리드 검색 옵션")
    search_mode = st.sidebar.selectbox(
        "검색 방식 선택",
        ["하이브리드 (BM25 + Vector)", "벡터 유사도 전용", "키워드(BM25) 전용"],
        index=0,
        help="BM25 키워드 검색과 SBERT 벡터 유사도 검색의 조합 방식을 선택합니다."
    )
    top_k_select = st.sidebar.slider(
        "추출 도서 개수 (Top-K)",
        min_value=1,
        max_value=20,
        value=5,
        help="챗봇이 답변 작성 시 참조할 베스트셀러 도서 개수"
    )
    min_sim_cutoff = st.sidebar.slider(
        "최소 유사도 임계값 (%)",
        min_value=0,
        max_value=100,
        value=0,
        help="설정한 유사도 수치 이상의 도서만 챗봇 답변 컨텍스트로 전달합니다."
    )

    st.sidebar.markdown("---")
    st.sidebar.header("🔍 대시보드 도서 필터 옵션")

    all_publishers = ["전체"] + sorted(list(df['publisher'].dropna().unique()))
    selected_pub = st.sidebar.selectbox("출판사 선택", all_publishers)

    max_price = int(df['price_original_num'].max()) if not df['price_original_num'].isnull().all() else 100000
    price_range = st.sidebar.slider(
        "도서 정가 범위 (원)",
        min_value=0,
        max_value=max_price,
        value=(0, max_price),
        step=5000
    )

    spring_option = st.sidebar.radio("분철 서비스 지원 여부", ["전체", "가능 도서만", "미지원 도서만"])

    # 공통 데이터 필터링 적용
    filtered_df = df.copy()
    if selected_pub != "전체":
        filtered_df = filtered_df[filtered_df['publisher'] == selected_pub]

    filtered_df = filtered_df[
        (filtered_df['price_original_num'] >= price_range[0]) &
        (filtered_df['price_original_num'] <= price_range[1])
    ]

    if spring_option == "가능 도서만":
        filtered_df = filtered_df[filtered_df['is_spring_service'] == "Y"]
    elif spring_option == "미지원 도서만":
        filtered_df = filtered_df[filtered_df['is_spring_service'] == "N"]

    # --- 메인 대시보드 헤더 ---
    st.title("📚 YES24 베스트셀러 AI 대시보드 & Groq 챗봇")
    st.markdown("SBERT 의미론적 유사도 검색, ChromaDB 벡터 DB, Groq LLM 기반 RAG 챗봇 & RAGAS 품질 평가 대시보드입니다.")

    # 핵심 요약 메트릭
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("전체 도서 수", f"{len(df):,} 권", delta=f"필터 적용 {len(filtered_df):,} 권")
    with col2:
        avg_price = filtered_df['price_sale_num'].mean() if len(filtered_df) > 0 else 0
        st.metric("평균 판매가", f"{avg_price:,.0f} 원")
    with col3:
        avg_disc = filtered_df['discount_rate_num'].mean() if len(filtered_df) > 0 else 0
        st.metric("평균 할인율", f"{avg_disc:.1f} %")
    with col4:
        avg_rating = filtered_df[filtered_df['rating_num'] > 0]['rating_num'].mean() if len(filtered_df) > 0 else 0
        st.metric("평균 평점", f"{avg_rating:.2f} / 10")

    st.markdown("---")

    # 6개 메인 탭 구성
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "🔍 키워드 검색",
        "🧬 코사인 유사도 검색",
        "📊 임베딩 시각화 & TSV",
        "🏆 하이라이트 & 데이터",
        "🤖 AI 도서 추천 챗봇 (Groq RAG)",
        "📈 RAG 품질 평가 (RAGAS Dashboard)"
    ])

    # ----------------------------------------------------
    # TAB 1: 키워드 검색
    # ----------------------------------------------------
    with tab1:
        st.subheader("🔍 키워드 기반 도서 검색")
        st.markdown("도서명, 저자, 출판사, 소개 특징(features), 태그에서 입력한 키워드를 검색합니다.")

        kw_query = st.text_input("검색어를 입력하세요 (예: 파이썬, 엑셀, 클로드, 에이전트, AI)", value="", key="kw_input")

        kw_df = filtered_df.copy()
        if kw_query.strip():
            query_str = kw_query.strip().lower()
            mask = (
                kw_df['goods_name'].astype(str).str.lower().str.contains(query_str, na=False) |
                kw_df['goods_sub_name'].astype(str).str.lower().str.contains(query_str, na=False) |
                kw_df['author_clean'].astype(str).str.lower().str.contains(query_str, na=False) |
                kw_df['publisher'].astype(str).str.lower().str.contains(query_str, na=False) |
                kw_df['features'].astype(str).str.lower().str.contains(query_str, na=False) |
                kw_df['tags'].astype(str).str.lower().str.contains(query_str, na=False)
            )
            kw_df = kw_df[mask]

        st.markdown(f"**검색 결과:** 총 **{len(kw_df)}** 건")

        if len(kw_df) > 0:
            display_cols = [
                'rank', 'goods_name', 'author_clean', 'publisher', 'publish_date',
                'price_original_num', 'price_sale_num', 'discount_rate_num',
                'sale_index_num', 'rating_num', 'review_count_num', 'detail_url'
            ]
            renamed_kw = kw_df[display_cols].rename(columns={
                'rank': '순위',
                'goods_name': '도서명',
                'author_clean': '저자',
                'publisher': '출판사',
                'publish_date': '출판일',
                'price_original_num': '정가(원)',
                'price_sale_num': '판매가(원)',
                'discount_rate_num': '할인율(%)',
                'sale_index_num': '판매지수',
                'rating_num': '평점',
                'review_count_num': '리뷰 수',
                'detail_url': '상세링크'
            })
            st.dataframe(
                renamed_kw,
                use_container_width=True,
                column_config={
                    "상세링크": st.column_config.LinkColumn("상세링크", display_text="YES24 이동")
                }
            )
        else:
            st.info("검색 조건에 일치하는 도서가 없습니다.")

    # ----------------------------------------------------
    # TAB 2: 코사인 유사도 검색
    # ----------------------------------------------------
    with tab2:
        st.subheader("🧬 SBERT 기반 코사인 유사도 검색")
        st.markdown("자연어 질문/원하는 주제를 입력하거나 특정 도서를 선택하여 AI 의미적 유사도(Semantic Similarity)가 높은 도서를 검색합니다.")

        sim_mode = st.radio(
            "유사도 검색 방식 선택",
            ["자연어 문장/검색어 직접 입력", "도서 목록에서 기준 도서 선택"],
            horizontal=True
        )

        ctrl_col1, ctrl_col2 = st.columns(2)
        with ctrl_col1:
            min_sim_val = st.slider(
                "🎯 최소 유사도 임계값 (Min Similarity)",
                min_value=0.00,
                max_value=1.00,
                value=0.30,
                step=0.05
            )
        with ctrl_col2:
            top_k_val = st.slider(
                "🔢 출력 도서 개수 (Top-K)",
                min_value=1,
                max_value=50,
                value=10,
                step=1
            )

        sim_results = pd.DataFrame()

        if sim_mode == "자연어 문장/검색어 직접 입력":
            user_query = st.text_input(
                "원하는 도서 주제나 대화형 질문을 입력하세요",
                value="클로드 코드로 1인 창업하고 AI 에이전틱 코딩 배우기",
                key="sim_query_input"
            )
            if user_query.strip():
                sim_results = search_similar_by_query(
                    user_query.strip(),
                    filtered_df,
                    embeddings[filtered_df.index.values],
                    model,
                    top_k=top_k_val,
                    min_similarity=min_sim_val
                )
        else:
            book_titles = filtered_df['goods_name'].tolist()
            if len(book_titles) > 0:
                selected_title = st.selectbox("기준 도서를 선택하세요", book_titles)
                selected_pos = filtered_df[filtered_df['goods_name'] == selected_title].index[0]
                pos_in_df = df.index.get_loc(selected_pos)

                sim_results = search_similar_by_book_idx(
                    pos_in_df,
                    filtered_df,
                    embeddings[filtered_df.index.values],
                    top_k=top_k_val,
                    min_similarity=min_sim_val
                )

        st.markdown("---")
        st.subheader("📋 유사 도서 목록 (표 형태 출력)")

        if len(sim_results) > 0:
            sim_display_cols = [
                'similarity_pct', 'rank', 'goods_name', 'author_clean', 'publisher',
                'price_sale_num', 'sale_index_num', 'rating_num', 'review_count_num', 'detail_url'
            ]
            renamed_sim = sim_results[sim_display_cols].rename(columns={
                'similarity_pct': '유사도 (%)',
                'rank': '순위',
                'goods_name': '도서명',
                'author_clean': '저자',
                'publisher': '출판사',
                'price_sale_num': '판매가(원)',
                'sale_index_num': '판매지수',
                'rating_num': '평점',
                'review_count_num': '리뷰 수',
                'detail_url': '상세링크'
            })
            st.dataframe(
                renamed_sim,
                use_container_width=True,
                column_config={
                    "유사도 (%)": st.column_config.NumberColumn("유사도 (%)", format="%.2f %%"),
                    "상세링크": st.column_config.LinkColumn("상세링크", display_text="YES24 이동")
                }
            )
        else:
            st.warning("선택한 유사도 임계값 조건을 만족하는 유사 도서가 없습니다.")

    # ----------------------------------------------------
    # TAB 3: 임베딩 시각화 & TSV
    # ----------------------------------------------------
    with tab3:
        st.subheader("📊 임베딩 시각화 & TensorFlow Projector TSV 다운로드")
        st.markdown("768차원 도서 벡터를 2D 공간으로 주성분 분석(PCA)하여 분포를 시각화합니다.")

        if len(df) > 0:
            pca = PCA(n_components=2)
            coords_2d = pca.fit_transform(embeddings)

            pca_df = pd.DataFrame({
                'PC1': coords_2d[:, 0],
                'PC2': coords_2d[:, 1],
                '도서명': df['goods_name'],
                '출판사': df['publisher'],
                '판매지수': df['sale_index_num']
            })

            fig, ax = plt.subplots(figsize=(10, 5))
            sns.scatterplot(
                data=pca_df,
                x='PC1',
                y='PC2',
                size='판매지수',
                sizes=(20, 200),
                alpha=0.6,
                palette="viridis",
                ax=ax
            )
            ax.set_title("YES24 도서 임베딩 2D PCA 공간 분포", fontsize=14)
            ax.set_xlabel("주성분 1 (PC1)")
            ax.set_ylabel("주성분 2 (PC2)")
            st.pyplot(fig)

        st.markdown("---")
        st.subheader("📥 TensorFlow Embedding Projector TSV 다운로드")

        tsv_col1, tsv_col2 = st.columns(2)

        if os.path.exists(vec_tsv_file):
            with open(vec_tsv_file, "r", encoding="utf-8") as f:
                vec_data = f.read()
            with tsv_col1:
                st.download_button(
                    label="📥 vectors.tsv 다운로드",
                    data=vec_data,
                    file_name="vectors.tsv",
                    mime="text/tab-separated-values"
                )

        if os.path.exists(meta_tsv_file):
            with open(meta_tsv_file, "r", encoding="utf-8") as f:
                meta_data = f.read()
            with tsv_col2:
                st.download_button(
                    label="📥 metadata.tsv 다운로드",
                    data=meta_data,
                    file_name="metadata.tsv",
                    mime="text/tab-separated-values"
                )

    # ----------------------------------------------------
    # TAB 4: 하이라이트 & 데이터 브라우저
    # ----------------------------------------------------
    with tab4:
        st.subheader("🏆 베스트셀러 하이라이트 & 데이터 브라우저")

        if len(filtered_df) > 0:
            st.write("### 🔥 인기 판매지수 TOP 3 도서")
            top_sales = filtered_df.sort_values(by='sale_index_num', ascending=False).head(3)

            cols = st.columns(3)
            for i, (_, book) in enumerate(top_sales.iterrows()):
                with cols[i]:
                    st.image(book['image_url'], width=130)
                    st.markdown(f"**{i+1}위. {book['goods_name']}**")
                    st.write(f"✍️ 저자: {book['author_clean']} | 🏢 출판사: {book['publisher']}")
                    st.write(f"📈 판매지수: **{book['sale_index_num']:,}**")
                    st.write(f"💰 가격: {book['price_sale_num']:,.0f}원")
                    st.write(f"⭐ 평점: {book['rating_num']}점 ({book['review_count_num']}건)")
                    st.markdown(f"[상세 정보 바로가기]({book['detail_url']})")

            st.markdown("---")
            st.write("### 📋 전체 필터링 데이터 테이블")
            st.dataframe(filtered_df, use_container_width=True)

            csv_data = filtered_df.to_csv(index=False, encoding='utf-8-sig')
            st.download_button(
                label="💾 필터링된 데이터 CSV 다운로드",
                data=csv_data,
                file_name="yes24_filtered_bestsellers.csv",
                mime="text/csv"
            )
        else:
            st.info("조건에 일치하는 도서가 없습니다.")

    # ----------------------------------------------------
    # TAB 5: AI 도서 추천 챗봇 (Groq RAG + ChromaDB)
    # ----------------------------------------------------
    with tab5:
        st.subheader("🤖 AI 도서 추천 챗봇 (Groq RAG + ChromaDB)")
        st.markdown("ChromaDB에 저장된 YES24 베스트셀러 임베딩 벡터를 검색하여 Groq LLM이 엄격히 베스트셀러 목록 내에서만 추천 및 상세 추천 이유를 설명합니다.")

        # API Key 경고/안내
        if not groq_key:
            st.warning("⚠️ Groq API Key가 필요합니다. 사이드바에 API Key를 입력하시거나 `.env` 파일에 `GROQ_API_KEY=your_key`를 등록해 주세요.")

        # 대화 세션 상태 초기화
        if "messages" not in st.session_state:
            st.session_state.messages = [
                {
                    "role": "assistant",
                    "content": "친절한 도서 검색 도우미입니다! YES24 IT/모바일 베스트셀러 목록 중에서 원하시는 주제나 기술에 맞는 최고의 도서와 추천 이유를 설명해 드릴게요. 무엇이 궁금하신가요?"
                }
            ]

        # 이전 대화 출력 및 실시간 RAGAS 평가 표시
        for msg in st.session_state.messages:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])
                if msg["role"] == "assistant" and "eval_res" in msg and msg["eval_res"]:
                    eval_res = msg["eval_res"]
                    with st.expander("🧪 [RAGAS] 실시간 RAG 품질 평가 측정 결과"):
                        e1, e2, e3, e4, e5 = st.columns(5)
                        e1.metric("종합 RAGAS", f"{eval_res.get('ragas_score', 0):.1f} 점")
                        e2.metric("Faithfulness", f"{eval_res.get('faithfulness', 0)*100:.1f} %")
                        e3.metric("Answer Relevance", f"{eval_res.get('answer_relevance', 0)*100:.1f} %")
                        e4.metric("Context Precision", f"{eval_res.get('context_precision', 0)*100:.1f} %")
                        e5.metric("Context Recall", f"{eval_res.get('context_recall', 0)*100:.1f} %")

                        st.progress(min(1.0, max(0.0, eval_res.get('ragas_score', 0) / 100.0)))
                        st.info(f"💡 **평가 사유**: {eval_res.get('reasoning', '')}")

        # 사용자 입력 및 챗봇 처리
        if prompt := st.chat_input("질문을 입력하세요 (예: 클로드 코드나 프롬프트 엔지니어링 추천도서와 추천이유 알려줘)"):
            if not groq_key:
                st.error("Groq API Key를 먼저 입력해 주세요!")
            else:
                # 사용자 메시지 표시 및 세션 추가
                st.session_state.messages.append({"role": "user", "content": prompt})
                with st.chat_message("user"):
                    st.markdown(prompt)

                # 1. RAG 하이브리드 검색 (BM25 + Vector RRF)
                with st.spinner(f"[{search_mode}] 방식으로 관련 베스트셀러 도서를 검색 중입니다..."):
                    retrieved_books = search_hybrid(
                        query_text=prompt,
                        df=df,
                        chroma_collection=chroma_collection,
                        model=model,
                        bm25_searcher=bm25_searcher,
                        top_k=top_k_select,
                        min_sim_pct=min_sim_cutoff,
                        search_mode=search_mode
                    )

                # 2. Groq LLM 응답 생성 및 RAGAS 평가
                with st.chat_message("assistant"):
                    with st.spinner(f"Groq AI 도서 추천 도우미가 답변을 작성 중입니다... (Temp: {temperature_select}, Top-P: {top_p_select})"):
                        answer, eval_res = generate_rag_answer_with_eval(
                            user_query=prompt,
                            chat_history=st.session_state.messages[:-1],
                            retrieved_books=retrieved_books,
                            api_key=groq_key,
                            temperature=temperature_select,
                            top_p=top_p_select,
                            do_eval=do_eval_select
                        )
                        st.markdown(answer)

                        if eval_res:
                            with st.expander("🧪 [RAGAS] 실시간 RAG 품질 평가 측정 결과"):
                                e1, e2, e3, e4, e5 = st.columns(5)
                                e1.metric("종합 RAGAS", f"{eval_res.get('ragas_score', 0):.1f} 점")
                                e2.metric("Faithfulness", f"{eval_res.get('faithfulness', 0)*100:.1f} %")
                                e3.metric("Answer Relevance", f"{eval_res.get('answer_relevance', 0)*100:.1f} %")
                                e4.metric("Context Precision", f"{eval_res.get('context_precision', 0)*100:.1f} %")
                                e5.metric("Context Recall", f"{eval_res.get('context_recall', 0)*100:.1f} %")

                                st.progress(min(1.0, max(0.0, eval_res.get('ragas_score', 0) / 100.0)))
                                st.info(f"💡 **평가 사유**: {eval_res.get('reasoning', '')}")

                st.session_state.messages.append({
                    "role": "assistant",
                    "content": answer,
                    "eval_res": eval_res
                })

                # 하단에 참조된 RAG 검색 도서 정보 펼치기 (투명성 제공)
                if retrieved_books:
                    with st.expander(f"🔍 [{search_mode}] 참조된 Top {len(retrieved_books)} 베스트셀러 도서 목록"):
                        for idx, b in enumerate(retrieved_books, 1):
                            sim_str = f"{b.get('similarity_pct', 0.0)}%"
                            bm25_str = f"순위 {b.get('bm25_rank', '-')}"
                            rrf_str = f"{b.get('rrf_score', 0.0)}"
                            price_val = float(b.get('price_sale', 0))
                            st.markdown(
                                f"**{idx}. {b.get('goods_name', '')}** | 저자: {b.get('author', '')} | 출판사: {b.get('publisher', '')} | {price_val:,.0f}원\n"
                                f"   - 📊 **유사도**: `{sim_str}` | **BM25 순위**: `{bm25_str}` | **RRF 점수**: `{rrf_str}`"
                            )

    # ----------------------------------------------------
    # TAB 6: RAG 품질 평가 (RAGAS Evaluation Dashboard)
    # ----------------------------------------------------
    with tab6:
        st.subheader("📈 RAGAS 기반 RAG 챗봇 품질 평가 대시보드")
        st.markdown("""
        Groq API(`llama-3.3-70b-versatile`) LLM-as-a-Judge 및 SBERT 유사도를 기반으로 **RAGAS 4대 핵심 품질 지표**를 정밀 분석합니다.
        - **Faithfulness (충실도)**: 챗봇 답변이 검색된 도서 문맥에 엄격히 근거했는지 환각(Hallucination) 측정
        - **Answer Relevance (답변 관련성)**: 생성 답변이 사용자 질문 의도에 부합하는지 측정
        - **Context Precision (맥락 정밀도)**: 상위 K개 검색 도서의 유용한 정보 랭킹 순위 측정
        - **Context Recall (맥락 완결성)**: 정답(Ground Truth) 및 필수 정보가 검색된 문맥에 포함되었는지 측정
        """)

        subtab1, subtab2, subtab3 = st.tabs([
            "🎯 단일 질의 실시간 평가",
            "📊 배치 벤치마크 평가",
            "⚔️ 검색 모드별 품질 비교"
        ])

        # Subtab 6-1: 단일 질의 실시간 평가
        with subtab1:
            st.write("### 🎯 사용자 정의 질의 RAGAS 평가")
            eval_query = st.text_input(
                "평가할 질문 입력",
                value="클로드 코드로 1인 창업하고 AI 에이전틱 코딩 배우기 추천도서 알려줘",
                key="eval_query_input"
            )
            eval_gt = st.text_input(
                "기준 정답 (Ground Truth - 선택 사항)",
                value="Do it! 지피티 서비스 개발, 파이썬 프로그래밍",
                key="eval_gt_input"
            )

            ec1, ec2, ec3 = st.columns(3)
            with ec1:
                eval_search_mode = st.selectbox(
                    "검색 방식",
                    ["하이브리드 (BM25 + Vector)", "벡터 유사도 전용", "키워드(BM25) 전용"],
                    key="eval_sm"
                )
            with ec2:
                eval_top_k = st.slider("Top-K 추출 개수", 1, 15, 5, key="eval_tk")
            with ec3:
                eval_min_sim = st.slider("최소 유사도 임계값 (%)", 0, 100, 0, key="eval_ms")

            if st.button("🚀 RAG 답변 생성 및 RAGAS 평가 실행", key="btn_run_single_eval"):
                with st.spinner("1. RAG 하이브리드 검색 수행 중..."):
                    eval_retrieved = search_hybrid(
                        query_text=eval_query,
                        df=df,
                        chroma_collection=chroma_collection,
                        model=model,
                        bm25_searcher=bm25_searcher,
                        top_k=eval_top_k,
                        min_sim_pct=eval_min_sim,
                        search_mode=eval_search_mode
                    )

                with st.spinner("2. Groq LLM 답변 생성 및 RAGAS 지표 계산 중..."):
                    ans_text, single_eval = generate_rag_answer_with_eval(
                        user_query=eval_query,
                        chat_history=[],
                        retrieved_books=eval_retrieved,
                        api_key=groq_key,
                        temperature=temperature_select,
                        top_p=top_p_select,
                        ground_truth=eval_gt,
                        do_eval=True
                    )

                st.markdown("---")
                st.write("#### 💬 생성된 RAG 답변")
                st.info(ans_text)

                if single_eval:
                    st.write("#### 📊 RAGAS 4대 평가 지표 측정 결과")
                    m1, m2, m3, m4, m5 = st.columns(5)
                    m1.metric("🏆 종합 RAGAS", f"{single_eval['ragas_score']:.1f} 점")
                    m2.metric("📌 Faithfulness", f"{single_eval['faithfulness']*100:.1f} %")
                    m3.metric("🎯 Answer Relevance", f"{single_eval['answer_relevance']*100:.1f} %")
                    m4.metric("🔍 Context Precision", f"{single_eval['context_precision']*100:.1f} %")
                    m5.metric("📚 Context Recall", f"{single_eval['context_recall']*100:.1f} %")

                    # 레이더 차트 시각화
                    chart_col1, chart_col2 = st.columns([1, 1])
                    with chart_col1:
                        categories = ['Faithfulness', 'Answer Relevance', 'Context Precision', 'Context Recall']
                        scores = [
                            single_eval['faithfulness'] * 100,
                            single_eval['answer_relevance'] * 100,
                            single_eval['context_precision'] * 100,
                            single_eval['context_recall'] * 100
                        ]
                        angles = np.linspace(0, 2 * np.pi, len(categories), endpoint=False).tolist()
                        scores_cycle = scores + [scores[0]]
                        angles_cycle = angles + [angles[0]]

                        fig, ax = plt.subplots(figsize=(5, 4), subplot_kw=dict(polar=True))
                        ax.fill(angles_cycle, scores_cycle, color='#1f77b4', alpha=0.25)
                        ax.plot(angles_cycle, scores_cycle, color='#1f77b4', linewidth=2)
                        ax.set_xticks(angles)
                        ax.set_xticklabels(categories, fontsize=10)
                        ax.set_ylim(0, 100)
                        ax.set_title("RAGAS 품질 레이더 차트", fontsize=12, pad=15)
                        st.pyplot(fig)

                    with chart_col2:
                        st.write("#### 📝 평가 총평 및 사유")
                        st.success(single_eval.get('reasoning', ''))

                        st.write("#### 📚 검색된 도서 문맥 수")
                        st.write(f"총 **{len(eval_retrieved)}** 권 검색됨")
                        for idx, b in enumerate(eval_retrieved, 1):
                            st.write(f"{idx}. {b.get('goods_name')} ({b.get('publisher')}) - 유사도: {b.get('similarity_pct', 0)}%")

        # Subtab 6-2: 배치 벤치마크 평가
        with subtab2:
            st.write("### 📊 벤치마크 데이터셋 일괄 평가")
            st.markdown("대표적인 YES24 IT/모바일 베스트셀러 질의 5개에 대해 RAG 시스템의 품질을 일괄 평가합니다.")

            benchmark_queries = [
                {
                    "question": "파이썬 입문 프로그래밍 추천도서와 저자 알려줘",
                    "ground_truth": "Do it! 점프 투 파이썬, 혼자 공부하는 파이썬"
                },
                {
                    "question": "클로드 코드 1인 창업 AI 에이전트 책 추천해줘",
                    "ground_truth": "클로드 코드 1인 개발 창업 지피티"
                },
                {
                    "question": "데이터 분석 엑셀 실무 서적 추천",
                    "ground_truth": "엑셀 데이터 분석 실무 데이터 시각화"
                },
                {
                    "question": "스프링 웹 프로그래밍 분철 가능한 책",
                    "ground_truth": "스프링 부트 쇼핑몰 개발 분철 가능"
                },
                {
                    "question": "머신러닝 딥러닝 인공지능 기초 서적 추천해줘",
                    "ground_truth": "혼자 공부하는 머신러닝 딥러닝 텐서플로"
                }
            ]

            if st.button("🚀 벤치마크 일괄 평가 실행", key="btn_run_batch_eval"):
                with st.spinner("벤치마크 질의 5건에 대해 하이브리드 검색 및 Groq LLM RAGAS 평가를 진행 중입니다..."):
                    batch_results = run_batch_ragas_evaluation(
                        benchmark_queries=benchmark_queries,
                        df=df,
                        chroma_collection=chroma_collection,
                        model=model,
                        bm25_searcher=bm25_searcher,
                        search_hybrid_func=search_hybrid,
                        generate_answer_func=generate_rag_answer,
                        api_key=groq_key,
                        search_mode=search_mode,
                        top_k=top_k_select,
                        min_sim_pct=min_sim_cutoff,
                        temperature=temperature_select,
                        top_p=top_p_select
                    )

                batch_df = pd.DataFrame(batch_results)

                st.write("#### 🏆 벤치마크 요약 평균 점수")
                b1, b2, b3, b4, b5 = st.columns(5)
                b1.metric("평균 RAGAS 점수", f"{batch_df['RAGAS 점수'].mean():.1f} 점")
                b2.metric("평균 Faithfulness", f"{batch_df['Faithfulness'].mean():.1f} %")
                b3.metric("평균 Answer Relevance", f"{batch_df['Answer Relevance'].mean():.1f} %")
                b4.metric("평균 Context Precision", f"{batch_df['Context Precision'].mean():.1f} %")
                b5.metric("평균 Context Recall", f"{batch_df['Context Recall'].mean():.1f} %")

                st.markdown("---")
                st.write("#### 📋 질의별 세부 RAGAS 평가 결과")
                st.dataframe(batch_df, use_container_width=True)

                csv_batch = batch_df.to_csv(index=False, encoding='utf-8-sig')
                st.download_button(
                    label="💾 벤치마크 평가 결과 CSV 다운로드",
                    data=csv_batch,
                    file_name="ragas_benchmark_results.csv",
                    mime="text/csv"
                )

        # Subtab 6-3: 검색 모드별 품질 비교
        with subtab3:
            st.write("### ⚔️ 검색 방식별 RAGAS 품질 비교 (Hybrid vs Vector vs BM25)")
            st.markdown("검색 엔진 방식(하이브리드, 벡터 전용, BM25 키워드 전용)에 따른 RAGAS 평가 점수 차이를 비교합니다.")

            if st.button("🚀 3가지 검색 방식 비교 평가 실행", key="btn_run_compare_modes"):
                compare_data = []
                modes = ["하이브리드 (BM25 + Vector)", "벡터 유사도 전용", "키워드(BM25) 전용"]

                test_set = [
                    {"question": "파이썬 입문 프로그래밍 추천도서", "ground_truth": "Do it! 점프 투 파이썬"},
                    {"question": "클로드 코드 에이전틱 코딩", "ground_truth": "클로드 개발 AI 에이전트"},
                    {"question": "데이터 분석 엑셀 서적 추천", "ground_truth": "엑셀 데이터 분석"}
                ]

                progress_bar = st.progress(0)
                for idx, mode_name in enumerate(modes):
                    with st.spinner(f"[{mode_name}] 검색 방식 평가 수행 중..."):
                        eval_rows = run_batch_ragas_evaluation(
                            benchmark_queries=test_set,
                            df=df,
                            chroma_collection=chroma_collection,
                            model=model,
                            bm25_searcher=bm25_searcher,
                            search_hybrid_func=search_hybrid,
                            generate_answer_func=generate_rag_answer,
                            api_key=groq_key,
                            search_mode=mode_name,
                            top_k=top_k_select,
                            min_sim_pct=min_sim_cutoff,
                            temperature=temperature_select,
                            top_p=top_p_select
                        )
                        eval_df = pd.DataFrame(eval_rows)
                        compare_data.append({
                            "검색 방식": mode_name,
                            "RAGAS 점수": round(eval_df['RAGAS 점수'].mean(), 1),
                            "Faithfulness": round(eval_df['Faithfulness'].mean(), 1),
                            "Answer Relevance": round(eval_df['Answer Relevance'].mean(), 1),
                            "Context Precision": round(eval_df['Context Precision'].mean(), 1),
                            "Context Recall": round(eval_df['Context Recall'].mean(), 1)
                        })
                    progress_bar.progress((idx + 1) / len(modes))

                comp_df = pd.DataFrame(compare_data)

                st.write("#### 📊 검색 방식별 품질 점수 비교 표")
                st.dataframe(comp_df, use_container_width=True)

                # 막대그래프 시각화
                fig, ax = plt.subplots(figsize=(8, 4))
                sns.barplot(
                    data=comp_df,
                    x="검색 방식",
                    y="RAGAS 점수",
                    palette="crest",
                    ax=ax
                )
                for p in ax.patches:
                    ax.annotate(
                        f"{p.get_height():.1f}점",
                        (p.get_x() + p.get_width() / 2., p.get_height()),
                        ha='center', va='bottom', fontsize=11, fontweight='bold', xytext=(0, 3),
                        textcoords='offset points'
                    )
                ax.set_ylim(0, 105)
                ax.set_title("검색 방식별 RAGAS 종합 점수 비교", fontsize=13)
                st.pyplot(fig)
