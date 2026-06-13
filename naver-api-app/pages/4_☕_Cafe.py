import streamlit as st
import pandas as pd
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils.naver_api import NaverAPI
from utils.sidebar import render_sidebar

st.set_page_config(page_title="카페글 검색", page_icon="☕", layout="wide")
render_sidebar()

st.title("☕ 네이버 카페글 검색")

if not st.session_state.get("client_id") or not st.session_state.get("client_secret"):
    st.stop()

keywords = st.session_state.get("keywords", [])
if not keywords:
    st.info("ℹ️ 사이드바에서 분석할 검색어를 입력해 주세요.")
    st.stop()

api = NaverAPI(st.session_state["client_id"], st.session_state["client_secret"])

tabs = st.tabs(keywords)

for i, kw in enumerate(keywords):
    with tabs[i]:
        with st.spinner(f"'{kw}' 카페글 검색 결과를 불러오는 중..."):
            result = api.search_general("cafearticle", kw, display=100)
            
            if result and "items" in result:
                items = result["items"]
                if not items:
                    st.info("검색 결과가 없습니다.")
                    continue
                
                df = pd.DataFrame(items)
                
                df['title'] = df['title'].str.replace(r'<[^<>]*>', '', regex=True)
                df['description'] = df['description'].str.replace(r'<[^<>]*>', '', regex=True)
                
                display_df = df[['cafename', 'title', 'description', 'link']]
                display_df.columns = ['카페명', '제목', '요약', '링크']
                
                col1, col2 = st.columns([1, 2])
                with col1:
                    st.subheader("활성 카페 순위")
                    cafe_counts = display_df['카페명'].value_counts().reset_index()
                    cafe_counts.columns = ['카페명', '글 수']
                    st.dataframe(cafe_counts, use_container_width=True)
                
                with col2:
                    st.subheader("카페글 목록")
                    st.dataframe(
                        display_df,
                        column_config={"링크": st.column_config.LinkColumn("원문 링크")},
                        use_container_width=True
                    )
            else:
                st.error("결과를 불러오지 못했습니다.")
