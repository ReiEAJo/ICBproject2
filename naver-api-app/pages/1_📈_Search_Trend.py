import streamlit as st
import pandas as pd
import plotly.express as px
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils.naver_api import NaverAPI

st.set_page_config(page_title="검색어 트렌드", page_icon="📈", layout="wide")
st.title("📈 네이버 통합 검색어 트렌드 (Datalab)")

if not st.session_state.get("client_id") or not st.session_state.get("client_secret"):
    st.error("⚠️ 사이드바에서 API Key를 입력해 주세요.")
    st.stop()

keywords = st.session_state.get("keywords", [])
if not keywords:
    st.info("ℹ️ 사이드바에서 분석할 검색어를 입력해 주세요.")
    st.stop()

start_date = st.session_state.get("start_date").strftime("%Y-%m-%d")
end_date = st.session_state.get("end_date").strftime("%Y-%m-%d")

api = NaverAPI(st.session_state["client_id"], st.session_state["client_secret"])

with st.spinner("트렌드 데이터를 불러오는 중..."):
    # 최대 5개 키워드까지만 허용 (네이버 API 제한)
    if len(keywords) > 5:
        st.warning("⚠️ 검색어는 최대 5개까지만 비교 가능합니다. 첫 5개 키워드만 사용합니다.")
        keywords = keywords[:5]
        
    result = api.get_datalab_search(keywords, start_date, end_date)

    if result and "results" in result:
        df_list = []
        for group in result["results"]:
            group_name = group["title"]
            for data in group["data"]:
                df_list.append({
                    "Date": data["period"],
                    "Ratio": data["ratio"],
                    "Keyword": group_name
                })
        
        if df_list:
            df = pd.DataFrame(df_list)
            
            # Plotly 라인 차트
            fig = px.line(df, x="Date", y="Ratio", color="Keyword", 
                          title=f"통합 검색어 트렌드 ({start_date} ~ {end_date})",
                          labels={"Ratio": "검색량 비율", "Date": "날짜"},
                          markers=True)
            st.plotly_chart(fig, use_container_width=True)
            
            # 데이터 테이블
            st.subheader("Raw Data")
            df_pivot = df.pivot(index='Date', columns='Keyword', values='Ratio').fillna(0)
            st.dataframe(df_pivot)
        else:
            st.warning("해당 기간에 대한 데이터가 없습니다.")
    else:
        st.error("데이터랩 검색 결과를 불러오지 못했습니다. API Key와 할당량을 확인해주세요.")
