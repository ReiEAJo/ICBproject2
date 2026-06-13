# 🟢 Naver API 통합 분석 대시보드

네이버 오픈 API를 활용하여 검색 트렌드, 쇼핑, 블로그, 카페, 뉴스 등 다양한 검색 데이터와 트렌드를 수집하고 시각화하는 Streamlit 기반의 분석 대시보드 프로젝트입니다.

---

## 🚀 Streamlit 접속 정보

- **배포 접속 주소**: [https://icbproject2-jfmiypxymt4azyaxyatp2q.streamlit.app/Shopping_Trend](https://icbproject2-jfmiypxymt4azyaxyatp2q.streamlit.app/Shopping_Trend)
- **로컬 접속 주소**: [http://localhost:8501](http://localhost:8501)

---

## 📊 주요 분석 기능

프로젝트의 `naver-api-app` 웹 애플리케이션은 다음과 같은 상세 분석 페이지를 제공합니다:

1. **📈 검색어 트렌드 ([1_📈_Search_Trend.py](file:///C:/Users/Rei%20EA%20Jo/Downloads/icb10proj2/naver-api-app/pages/1_%F0%9F%93%88_Search_Trend.py))**
   - 특정 키워드의 기간별 네이버 검색량 추이 분석
2. **🛍️ 쇼핑 검색 ([2_🛍️_Shopping.py](file:///C:/Users/Rei%20EA%20Jo/Downloads/icb10proj2/naver-api-app/pages/2_%F0%9F%9B%8D%EF%B8%8F_Shopping.py))**
   - 네이버 쇼핑 상품 검색 결과 조회 및 가격비교 정보 연동
3. **📝 블로그 검색 ([3_📝_Blog.py](file:///C:/Users/Rei%20EA%20Jo/Downloads/icb10proj2/naver-api-app/pages/3_%F0%9F%93%9D_Blog.py))**
   - 입력 키워드 기반의 최신 및 관련도 순 블로그 포스트 검색
4. **☕ 카페글 검색 ([4_☕_Cafe.py](file:///C:/Users/Rei%20EA%20Jo/Downloads/icb10proj2/naver-api-app/pages/4_%E2%98%95_Cafe.py))**
   - 네이버 카페 내 다양한 게시글 검색 및 정보 연동
5. **📰 뉴스 검색 ([5_📰_News.py](file:///C:/Users/Rei%20EA%20Jo/Downloads/icb10proj2/naver-api-app/pages/5_%F0%9F%93%B0_News.py))**
   - 실시간 주요 이슈 및 검색 키워드 기반 뉴스 기사 검색
6. **🛒 쇼핑 트렌드 ([6_🛒_Shopping_Trend.py](file:///C:/Users/Rei%20EA%20Jo/Downloads/icb10proj2/naver-api-app/pages/6_%F0%9F%9B%92_Shopping_Trend.py))**
   - 네이버 쇼핑 분야별 검색어 클릭 추이 및 카테고리별 트렌드 분석

---

## ⚙️ 설정 및 실행 방법

### 1. 환경 변수 설정
`naver-api-app/.env` 파일 또는 Streamlit Secrets에 발급받은 네이버 오픈 API Key를 입력합니다:
```env
NAVER_CLIENT_ID="YOUR_CLIENT_ID"
NAVER_CLIENT_SECRET="YOUR_CLIENT_SECRET"
```

### 2. 가상환경 및 패키지 설치
로컬 개발 가상환경은 `uv`를 사용해 `.venv` 폴더에 구축되어 있습니다. 의존성 패키지를 설치하려면 다음 명령어를 실행합니다:
```bash
pip install -r naver-api-app/requirements.txt
```

### 3. 애플리케이션 실행
```bash
streamlit run naver-api-app/app.py
```
실행 후 브라우저에서 [http://localhost:8501](http://localhost:8501)로 접속합니다.

---

## 🛠️ 프로젝트 작업 내역

### 1. 대시보드 범용성 개선 및 공통 사이드바 리팩토링 (최근 작업)
- **내용**: 여러 사용자가 자신의 네이버 API Key(Client ID, Client Secret)를 입력해 즉시 사용할 수 있도록 UI와 세션 구조 개선.
- **적용**: [`utils/sidebar.py`](file:///C:/Users/Rei%20EA%20Jo/Downloads/icb10proj2/naver-api-app/utils/sidebar.py)로 공통 사이드바 컴포넌트를 분리하였으며, 메인 페이지와 모든 서브 페이지에서 동일하게 사이드바 폼을 제공하여 페이지 전환 중에도 실시간 설정 변경이 유지되도록 적용했습니다.

### 2. Git 자동 Push Hooks 구축
- **대상**: [`.git/hooks/post-commit`](file:///C:/Users/Rei%20EA%20Jo/Downloads/icb10proj2/.git/hooks/post-commit) 훅 설정
- **내용**: 변경사항이 발생하여 로컬에서 `git commit`을 완료하면, 현재 활성화된 브랜치 명을 감지하여 자동으로 원격 저장소(`origin`)에 `git push`를 실행하도록 구현 및 적용 완료.

### 3. Streamlit 배포 환경 설정
- **내용**: 배포 환경에서 API Key를 안전하게 로드할 수 있도록 `st.secrets` 및 `.env` 파일 연동 설정을 적용하여 Streamlit Cloud 배포 진행.
- **배포 주소**: [https://icbproject2-jfmiypxymt4azyaxyatp2q.streamlit.app/Shopping_Trend](https://icbproject2-jfmiypxymt4azyaxyatp2q.streamlit.app/Shopping_Trend)

### 4. Naver API 통합 분석 대시보드 구축
- **내용**: 네이버 오픈 API(검색, 데이터랩 트렌드 등)를 활용하여 다중 페이지 대시보드 구조 개발.
- **대상 파일**: [`app.py`](file:///C:/Users/Rei%20EA%20Jo/Downloads/icb10proj2/naver-api-app/app.py) 및 `pages/` 폴더 내 다중 분석 스크립트.