import streamlit as st
import pandas as pd
import plotly.express as px
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils.naver_api import NaverAPI
from utils.sidebar import render_sidebar

st.set_page_config(page_title="쇼핑 트렌드", page_icon="🛒", layout="wide")
render_sidebar()

st.title("🛒 네이버 쇼핑 카테고리/키워드 트렌드 (Shopping Insight)")

if not st.session_state.get("client_id") or not st.session_state.get("client_secret"):
    st.stop()

keywords = st.session_state.get("keywords", [])
if not keywords:
    st.info("ℹ️ 사이드바에서 분석할 키워드를 입력해 주세요.")
    st.stop()

start_date = st.session_state.get("start_date").strftime("%Y-%m-%d")
end_date = st.session_state.get("end_date").strftime("%Y-%m-%d")

api = NaverAPI(st.session_state["client_id"], st.session_state["client_secret"])

st.markdown("""
> **안내**: 쇼핑 인사이트 API는 기준이 되는 **분야(카테고리 코드)**가 필수입니다.  
> 대시보드에서는 편의상 광범위한 카테고리인 **'디지털/가전(50000003)'** 또는 **'패션의류(50000000)'** 카테고리로 테스트합니다.
""")

category_map = {
    "패션의류 (50000000)": "50000000",
    "패션잡화 (50000001)": "50000001",
    "화장품/미용 (50000002)": "50000002",
    "디지털/가전 (50000003)": "50000003",
    "가구/인테리어 (50000004)": "50000004",
    "출산/육아 (50000005)": "50000005",
    "식품 (50000006)": "50000006",
    "스포츠/레저 (50000007)": "50000007",
    "생활/건강 (50000008)": "50000008",
    "여가/생활편의 (50000009)": "50000009",
    "면세점 (50000010)": "50000010",
    "도서 (50005542)": "50005542"
}
selected_cat_name = st.selectbox("기본 카테고리 선택", list(category_map.keys()))
selected_cat_code = category_map[selected_cat_name]

if st.button("트렌드 분석 시작"):
    with st.spinner("쇼핑 트렌드 데이터를 불러오는 중..."):
        if len(keywords) > 5:
            st.warning("⚠️ 쇼핑 인사이트 API도 한 번에 최대 5개 키워드까지만 허용됩니다.")
            keywords = keywords[:5]
            
        result = api.get_shopping_trend(keywords, start_date, end_date, category=selected_cat_code)

        if result and "results" in result:
            df_list = []
            for group in result["results"]:
                group_name = group["title"]
                for data in group["data"]:
                    df_list.append({
                        "Date": data["period"],
                        "Click Ratio": data["ratio"],
                        "Keyword": group_name
                    })
            
            if df_list:
                df = pd.DataFrame(df_list)
                
                # Plotly 라인 차트
                fig = px.line(df, x="Date", y="Click Ratio", color="Keyword", 
                              title=f"쇼핑 트렌드 클릭 비율 ({start_date} ~ {end_date})",
                              labels={"Click Ratio": "클릭량 비율", "Date": "날짜"},
                              markers=True)
                st.plotly_chart(fig, use_container_width=True)
                
                # 데이터 테이블
                st.subheader("Raw Data")
                df_pivot = df.pivot(index='Date', columns='Keyword', values='Click Ratio').fillna(0)
                st.dataframe(df_pivot)
            else:
                st.warning("해당 기간 및 카테고리에 대한 쇼핑 클릭 데이터가 없습니다. 카테고리가 일치하는지 확인해 주세요.")
        elif result and "error" in result:
            st.error(f"API 에러 발생 (HTTP {result['error']})")
            st.code(result['message'])
            st.info("해결 힌트: \n1. 검색어가 선택한 카테고리와 전혀 연관이 없으면 에러가 날 수 있습니다.\n2. 네이버 개발자 센터의 [내 애플리케이션] - [API 설정] 메뉴에서 '데이터랩(쇼핑)'이 활성화되어 있는지 확인하세요.")
        else:
            st.error("쇼핑 인사이트 검색 결과를 불러오지 못했습니다. 디버그를 위해 아래 응답을 확인하세요.")
            st.write(result)
