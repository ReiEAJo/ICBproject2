import streamlit as st
from datetime import date, timedelta
import os
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(
    page_title="Naver API Dashboard",
    page_icon="🟢",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize Session State
if "client_id" not in st.session_state:
    st.session_state["client_id"] = st.secrets.get("NAVER_CLIENT_ID", os.getenv("NAVER_CLIENT_ID", ""))
if "client_secret" not in st.session_state:
    st.session_state["client_secret"] = st.secrets.get("NAVER_CLIENT_SECRET", os.getenv("NAVER_CLIENT_SECRET", ""))
if "keywords" not in st.session_state:
    st.session_state["keywords"] = []
if "start_date" not in st.session_state:
    st.session_state["start_date"] = date.today() - timedelta(days=30)
if "end_date" not in st.session_state:
    st.session_state["end_date"] = date.today()

# Sidebar Configuration
st.sidebar.title("⚙️ 설정 (Settings)")

st.sidebar.subheader("1. 검색어 (Keywords)")
keywords_input = st.sidebar.text_input("검색어 입력 (쉼표로 구분)", placeholder="예: 스마트폰, 노트북, 태블릿")
if keywords_input:
    st.session_state["keywords"] = [k.strip() for k in keywords_input.split(",") if k.strip()]

st.sidebar.subheader("2. 검색 기간 (Date Range)")
st.sidebar.caption("데이터랩 트렌드 API에 주로 적용됩니다.")
start_date = st.sidebar.date_input("시작일", value=st.session_state["start_date"])
end_date = st.sidebar.date_input("종료일", value=st.session_state["end_date"])

if start_date <= end_date:
    st.session_state["start_date"] = start_date
    st.session_state["end_date"] = end_date
else:
    st.sidebar.error("에러: 종료일이 시작일보다 빠를 수 없습니다.")

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
