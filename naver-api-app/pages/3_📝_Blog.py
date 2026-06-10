import streamlit as st
import pandas as pd
import sys
import os
import plotly.express as px

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils.naver_api import NaverAPI

st.set_page_config(page_title="블로그 검색", page_icon="📝", layout="wide")
st.title("📝 네이버 블로그 검색")

if not st.session_state.get("client_id") or not st.session_state.get("client_secret"):
    st.error("⚠️ 사이드바에서 API Key를 입력해 주세요.")
    st.stop()

keywords = st.session_state.get("keywords", [])
if not keywords:
    st.info("ℹ️ 사이드바에서 분석할 검색어를 입력해 주세요.")
    st.stop()

api = NaverAPI(st.session_state["client_id"], st.session_state["client_secret"])

st.write("선택한 키워드에 대한 최신 블로그 포스팅 결과를 보여줍니다. (정확도순 100건)")

tabs = st.tabs(keywords)

for i, kw in enumerate(keywords):
    with tabs[i]:
        with st.spinner(f"'{kw}' 블로그 검색 결과를 불러오는 중..."):
            result = api.search_general("blog", kw, display=100)
            
            if result and "items" in result:
                items = result["items"]
                if not items:
                    st.info("검색 결과가 없습니다.")
                    continue
                
                df = pd.DataFrame(items)
                
                # HTML 태그 제거 및 날짜 변환
                df['title'] = df['title'].str.replace(r'<[^<>]*>', '', regex=True)
                df['description'] = df['description'].str.replace(r'<[^<>]*>', '', regex=True)
                df['postdate'] = pd.to_datetime(df['postdate'], format='%Y%m%d', errors='coerce')
                
                display_df = df[['postdate', 'title', 'bloggername', 'description', 'link']]
                display_df.columns = ['작성일', '제목', '블로거명', '요약', '링크']
                display_df = display_df.sort_values(by='작성일', ascending=False)
                
                # 작성일 기준 포스팅 건수 차트
                st.subheader("일별 포스팅 발행 건수 (최신 검색 결과 내)")
                date_counts = display_df['작성일'].value_counts().reset_index()
                date_counts.columns = ['작성일', '건수']
                date_counts = date_counts.sort_values('작성일')
                
                if not date_counts.empty:
                    fig = px.bar(date_counts, x='작성일', y='건수', text='건수', title=f"'{kw}' 검색 결과 중 일별 포스팅 빈도")
                    st.plotly_chart(fig, use_container_width=True)
                
                st.subheader("검색 결과 데이터")
                st.dataframe(
                    display_df,
                    column_config={"링크": st.column_config.LinkColumn("원문 링크")},
                    use_container_width=True
                )
            else:
                st.error("결과를 불러오지 못했습니다.")
