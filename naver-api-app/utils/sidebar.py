import streamlit as st
from datetime import date, timedelta
import os

def render_sidebar():
    st.sidebar.title("⚙️ 설정 (Settings)")
    
    # 1. API Key 세션 기본값 및 동기화 (백업본을 활용한 멀티페이지 위젯 소멸 방지)
    st.sidebar.subheader("🔑 API 인증")
    
    if "client_id" not in st.session_state:
        st.session_state["client_id"] = st.secrets.get("NAVER_CLIENT_ID", os.getenv("NAVER_CLIENT_ID", ""))
    if "client_secret" not in st.session_state:
        st.session_state["client_secret"] = st.secrets.get("NAVER_CLIENT_SECRET", os.getenv("NAVER_CLIENT_SECRET", ""))
        
    if "client_id_backup" not in st.session_state:
        st.session_state["client_id_backup"] = st.session_state["client_id"]
    if "client_secret_backup" not in st.session_state:
        st.session_state["client_secret_backup"] = st.session_state["client_secret"]

    def sync_credentials():
        st.session_state["client_id"] = st.session_state["temp_client_id"]
        st.session_state["client_id_backup"] = st.session_state["temp_client_id"]
        
    def sync_secret():
        st.session_state["client_secret"] = st.session_state["temp_client_secret"]
        st.session_state["client_secret_backup"] = st.session_state["temp_client_secret"]

    st.sidebar.text_input(
        "네이버 Client ID", 
        value=st.session_state["client_id_backup"],
        key="temp_client_id",
        on_change=sync_credentials,
        placeholder="Client ID를 입력하세요"
    )
    st.sidebar.text_input(
        "네이버 Client Secret", 
        value=st.session_state["client_secret_backup"],
        key="temp_client_secret",
        type="password",
        on_change=sync_secret,
        placeholder="Client Secret을 입력하세요"
    )
    
    # 2. 검색어 설정 (백업본을 활용한 멀티페이지 위젯 소멸 방지)
    st.sidebar.subheader("1. 검색어 (Keywords)")
    
    if "keywords" not in st.session_state:
        st.session_state["keywords"] = []
        
    if "keywords_backup" not in st.session_state:
        # keywords 리스트 기반 초기화
        st.session_state["keywords_backup"] = ", ".join(st.session_state["keywords"])

    def sync_keywords():
        val = st.session_state["temp_keywords_input"]
        st.session_state["keywords_backup"] = val
        if val:
            st.session_state["keywords"] = [k.strip() for k in val.split(",") if k.strip()]
        else:
            st.session_state["keywords"] = []

    st.sidebar.text_input(
        "검색어 입력 (쉼표로 구분)",
        value=st.session_state["keywords_backup"],
        key="temp_keywords_input",
        on_change=sync_keywords,
        placeholder="예: 스마트폰, 노트북, 태블릿"
    )
        
    # 3. 검색 기간 설정 (백업본을 활용한 멀티페이지 위젯 소멸 방지)
    st.sidebar.subheader("2. 검색 기간 (Date Range)")
    st.sidebar.caption("데이터랩 트렌드 API에 주로 적용됩니다.")
    
    if "start_date" not in st.session_state:
        st.session_state["start_date"] = date.today() - timedelta(days=30)
    if "end_date" not in st.session_state:
        st.session_state["end_date"] = date.today()
        
    if "start_date_backup" not in st.session_state:
        st.session_state["start_date_backup"] = st.session_state["start_date"]
    if "end_date_backup" not in st.session_state:
        st.session_state["end_date_backup"] = st.session_state["end_date"]

    def sync_start_date():
        st.session_state["start_date"] = st.session_state["temp_start_date"]
        st.session_state["start_date_backup"] = st.session_state["temp_start_date"]

    def sync_end_date():
        st.session_state["end_date"] = st.session_state["temp_end_date"]
        st.session_state["end_date_backup"] = st.session_state["temp_end_date"]

    start_date = st.sidebar.date_input(
        "시작일", 
        value=st.session_state["start_date_backup"], 
        key="temp_start_date", 
        on_change=sync_start_date
    )
    end_date = st.sidebar.date_input(
        "종료일", 
        value=st.session_state["end_date_backup"], 
        key="temp_end_date", 
        on_change=sync_end_date
    )
    
    if start_date > end_date:
        st.sidebar.error("에러: 종료일이 시작일보다 빠를 수 없습니다.")
        
    # 하단 상태 표시
    if not st.session_state["client_id"] or not st.session_state["client_secret"]:
        st.sidebar.warning("⚠️ 네이버 API Key(Client ID, Client Secret)를 입력해야 서비스가 작동합니다.")
    elif not st.session_state["keywords"]:
        st.sidebar.info("ℹ️ 분석을 시작하려면 검색어를 입력해 주세요.")
