import streamlit as st
from datetime import date, timedelta
import os
from dotenv import load_dotenv
from utils.sidebar import render_sidebar

load_dotenv()

st.set_page_config(
    page_title="Naver API Dashboard",
    page_icon="🟢",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 공통 사이드바 렌더링
render_sidebar()


# Main Page Content
st.title("🟢 Naver API 통합 분석 대시보드")
st.markdown("""
이 대시보드는 네이버 오픈 API를 활용하여 다양한 검색 결과 및 트렌드를 수집하고 분석합니다.

### 🚀 사용 방법
1. **Streamlit Secrets** (또는 **`.env` 파일**)에 발급받은 네이버 API **Client ID**와 **Client Secret**을 설정해 주세요.
2. 분석하고자 하는 **검색어**를 쉼표(`,`)로 구분하여 입력해 주세요.
3. 데이터랩(트렌드) 분석을 위한 **검색 기간**을 설정해 주세요.
4. 좌측 메뉴의 **각 카테고리(페이지)**를 클릭하여 상세 분석 결과를 확인하세요.

---

### 📊 지원하는 분석 기능
- **📈 검색어 트렌드 (Datalab)**: 특정 검색어의 기간별 검색량 추이 분석
- **🛍️ 쇼핑 검색**: 네이버 쇼핑 상품 검색 결과
- **🛒 쇼핑 트렌드 (Datalab)**: 쇼핑 카테고리별 검색 클릭 추이
- **📝 블로그 검색**: 네이버 블로그 포스트 검색
- **☕ 카페글 검색**: 네이버 카페 게시글 검색
- **📰 뉴스 검색**: 최신 뉴스 기사 검색
""")

if not st.session_state["client_id"] or not st.session_state["client_secret"]:
    st.warning("⚠️ Streamlit 설정(Secrets) 또는 `.env` 파일에 네이버 API Key(NAVER_CLIENT_ID, NAVER_CLIENT_SECRET)를 입력해야 정상적으로 작동합니다.")
elif not st.session_state["keywords"]:
    st.info("ℹ️ 분석을 시작하려면 검색어를 입력해 주세요.")
else:
    st.success(f"✅ 준비 완료! 현재 설정된 검색어: {', '.join(st.session_state['keywords'])}")
