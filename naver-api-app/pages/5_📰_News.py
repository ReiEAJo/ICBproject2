import streamlit as st
import pandas as pd
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils.naver_api import NaverAPI
from utils.sidebar import render_sidebar

st.set_page_config(page_title="뉴스 검색", page_icon="📰", layout="wide")
render_sidebar()

st.title("📰 네이버 뉴스 검색")

if not st.session_state.get("client_id") or not st.session_state.get("client_secret"):
    st.stop()

keywords = st.session_state.get("keywords", [])
if not keywords:
    st.info("ℹ️ 사이드바에서 분석할 검색어를 입력해 주세요.")
    st.stop()

api = NaverAPI(st.session_state["client_id"], st.session_state["client_secret"])

st.write("선택한 키워드에 대한 최신 관련 뉴스를 제공합니다.")

# 키워드별 뉴스를 한 화면에 정리해서 보여주기
for kw in keywords:
    st.subheader(f"🔹 '{kw}' 관련 최신 뉴스 (Top 10)")
    with st.spinner(f"'{kw}' 뉴스 검색 중..."):
        # 뉴스는 정확도순보다는 시간순 최신 소식이 중요할 수 있으므로, 기본 sim 대신 date 정렬 옵션을 추가 제공 가능
        # 여기서는 기본적으로 정확도(sim) 10개를 표시
        result = api.search_general("news", kw, display=10, sort="sim")
        
        if result and "items" in result:
            items = result["items"]
            if not items:
                st.info("검색 결과가 없습니다.")
                continue
            
            for item in items:
                title = item['title'].replace("<b>", "").replace("</b>", "")
                desc = item['description'].replace("<b>", "").replace("</b>", "")
                pub_date = item['pubDate']
                link = item['link']
                
                with st.expander(f"[{pub_date}] {title}"):
                    st.write(desc)
                    st.markdown(f"[뉴스 원문 보기]({link})")
        else:
            st.error("뉴스 결과를 불러오지 못했습니다.")
    st.markdown("---")
