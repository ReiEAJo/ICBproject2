import streamlit as st
import pandas as pd
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils.naver_api import NaverAPI

st.set_page_config(page_title="쇼핑 검색", page_icon="🛍️", layout="wide")
st.title("🛍️ 네이버 쇼핑 검색")

if not st.session_state.get("client_id") or not st.session_state.get("client_secret"):
    st.error("⚠️ 사이드바에서 API Key를 입력해 주세요.")
    st.stop()

keywords = st.session_state.get("keywords", [])
if not keywords:
    st.info("ℹ️ 사이드바에서 분석할 검색어를 입력해 주세요.")
    st.stop()

api = NaverAPI(st.session_state["client_id"], st.session_state["client_secret"])

st.write("선택한 키워드에 대한 최신 쇼핑 검색 결과를 보여줍니다. (정확도순)")

tabs = st.tabs(keywords)

for i, kw in enumerate(keywords):
    with tabs[i]:
        with st.spinner(f"'{kw}' 쇼핑 검색 결과를 불러오는 중..."):
            result = api.search_general("shop", kw, display=100)
            
            if result and "items" in result:
                items = result["items"]
                if not items:
                    st.info("검색 결과가 없습니다.")
                    continue
                
                df = pd.DataFrame(items)
                
                # HTML 태그 제거 및 데이터 정리
                df['title'] = df['title'].str.replace(r'<[^<>]*>', '', regex=True)
                df['lprice'] = pd.to_numeric(df['lprice'], errors='coerce')
                
                # 컬럼 이름 변경 및 필터링
                display_df = df[['title', 'lprice', 'mallName', 'category1', 'category2', 'link']]
                display_df.columns = ['상품명', '최저가(원)', '쇼핑몰', '카테고리1', '카테고리2', '링크']
                
                # 요약 통계
                col1, col2, col3 = st.columns(3)
                col1.metric("검색된 상품 수", len(display_df))
                col2.metric("평균 최저가", f"{display_df['최저가(원)'].mean():,.0f} 원" if not display_df['최저가(원)'].isnull().all() else "N/A")
                col3.metric("가장 많이 노출된 쇼핑몰", display_df['쇼핑몰'].mode()[0] if not display_df.empty else "N/A")
                
                # 데이터프레임
                st.dataframe(
                    display_df,
                    column_config={
                        "링크": st.column_config.LinkColumn("상품 링크")
                    },
                    use_container_width=True
                )
            else:
                st.error("결과를 불러오지 못했습니다.")
