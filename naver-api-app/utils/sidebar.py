import streamlit as st
from datetime import date, timedelta
import os

def render_sidebar():
    st.sidebar.title("⚙️ 설정 (Settings)")
    
    # 1. API Key 세션 기본값 및 동기화
    st.sidebar.subheader("🔑 API 인증")
    
    if "client_id" not in st.session_state:
        st.session_state["client_id"] = st.secrets.get("NAVER_CLIENT_ID", os.getenv("NAVER_CLIENT_ID", ""))
    if "client_secret" not in st.session_state:
        st.session_state["client_secret"] = st.secrets.get("NAVER_CLIENT_SECRET", os.getenv("NAVER_CLIENT_SECRET", ""))
        
    st.sidebar.text_input(
        "네이버 Client ID", 
        key="client_id",
        placeholder="Client ID를 입력하세요"
    )
    st.sidebar.text_input(
        "네이버 Client Secret", 
        key="client_secret",
        type="password",
        placeholder="Client Secret을 입력하세요"
    )
    
    # 2. 검색어 설정
    st.sidebar.subheader("1. 검색어 (Keywords)")
    
    if "keywords" not in st.session_state:
        st.session_state["keywords"] = []
    
    # 입력 폼을 위한 임시 텍스트 세션 상태 관리
    if "keywords_input_val" not in st.session_state:
        st.session_state["keywords_input_val"] = ", ".join(st.session_state["keywords"])
        
    keywords_input = st.sidebar.text_input(
        "검색어 입력 (쉼표로 구분)",
        key="keywords_input_val",
        placeholder="예: 스마트폰, 노트북, 태블릿"
    )
    
    # 파싱하여 실제 리스트 세션 상태 업데이트
    if keywords_input:
        st.session_state["keywords"] = [k.strip() for k in keywords_input.split(",") if k.strip()]
    else:
        st.session_state["keywords"] = []
        
    # 3. 검색 기간 설정
    st.sidebar.subheader("2. 검색 기간 (Date Range)")
    st.sidebar.caption("데이터랩 트렌드 API에 주로 적용됩니다.")
    
    if "start_date" not in st.session_state:
        st.session_state["start_date"] = date.today() - timedelta(days=30)
    if "end_date" not in st.session_state:
        st.session_state["end_date"] = date.today()
        
    start_date = st.sidebar.date_input("시작일", key="start_date")
    end_date = st.sidebar.date_input("종료일", key="end_date")
    
    if start_date > end_date:
        st.sidebar.error("에러: 종료일이 시작일보다 빠를 수 없습니다.")
        
    # 하단 상태 표시
    if not st.session_state["client_id"] or not st.session_state["client_secret"]:
        st.sidebar.warning("⚠️ 네이버 API Key(Client ID, Client Secret)를 입력해야 서비스가 작동합니다.")
    elif not st.session_state["keywords"]:
        st.sidebar.info("ℹ️ 분석을 시작하려면 검색어를 입력해 주세요.")
