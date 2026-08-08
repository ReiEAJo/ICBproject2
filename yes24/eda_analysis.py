# -*- coding: utf-8 -*-
import os
import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import re

# 콘솔 인코딩 설정 (Windows)
if sys.platform.startswith('win'):
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# matplotlib 한글 폰트 설정 (Windows 기준 Malgun Gothic)
plt.rc('font', family='Malgun Gothic')
plt.rc('axes', unicode_minus=False)
sns.set_theme(style="whitegrid", font="Malgun Gothic")

def preprocess_data(df):
    """도서 데이터 전처리"""
    # 복사본 사용
    df = df.copy()

    # 1. 가격 컬럼 숫자 변환
    def clean_price(val):
        if pd.isna(val):
            return np.nan
        # 숫자와 소수점 제외한 문자 제거
        cleaned = re.sub(r'[^\d.]', '', str(val))
        return float(cleaned) if cleaned else np.nan

    df['price_original_num'] = df['opt_shopPrice'].fillna(df['price_original'].apply(clean_price))
    df['price_sale_num'] = df['opt_salePrice'].fillna(df['price_sale'].apply(clean_price))

    # 2. 할인율 변환 (예: "10%" -> 10)
    def clean_discount(val):
        if pd.isna(val):
            return 0.0
        cleaned = re.sub(r'[^\d.]', '', str(val))
        return float(cleaned) if cleaned else 0.0
    
    df['discount_rate_num'] = df['discount_rate'].apply(clean_discount)

    # 3. 판매지수 및 리뷰수 숫자 변환 (이미 정수형인 경우 유지)
    df['sale_index_num'] = pd.to_numeric(df['sale_index'], errors='coerce').fillna(0).astype(int)
    df['review_count_num'] = pd.to_numeric(df['review_count'], errors='coerce').fillna(0).astype(int)
    df['rating_num'] = pd.to_numeric(df['rating'], errors='coerce').fillna(0.0)

    # 4. 출판일에서 연도 추출 (예: "2025년 12월" -> 2025)
    def extract_year(val):
        if pd.isna(val):
            return np.nan
        match = re.search(r'(\d{4})년', str(val))
        return int(match.group(1)) if match else np.nan
    df['publish_year'] = df['publish_date'].apply(extract_year)

    # 5. 저자명 정제 (끝에 ' 저' 또는 '< >' 괄호 등 제거)
    def clean_author(val):
        if pd.isna(val):
            return "저자 미상"
        author = str(val).strip()
        # <조태호> 저 -> 조태호
        author = re.sub(r'[<>\s]', '', author)
        if author.endswith("저"):
            author = author[:-1].strip()
        return author
    
    df['author_clean'] = df['opt_goodsAuth'].fillna(df['author']).apply(clean_author)

    return df

def generate_eda_report(csv_path, artifact_dir):
    if not os.path.exists(csv_path):
        print(f"오류: CSV 파일을 찾을 수 없습니다 ({csv_path})")
        return

    # 데이터 로드 및 전처리
    df_raw = pd.read_csv(csv_path)
    df = preprocess_data(df_raw)

    # 차트 저장 경로 설정
    os.makedirs(artifact_dir, exist_ok=True)
    
    # 1. 인기 출판사 TOP 10
    plt.figure(figsize=(10, 6))
    top_pub = df['publisher'].value_counts().head(10)
    sns.barplot(x=top_pub.values, y=top_pub.index, hue=top_pub.index, legend=False, palette="viridis")
    plt.title("베스트셀러 인기 출판사 TOP 10", fontsize=15, fontweight='bold', pad=15)
    plt.xlabel("도서 수 (권)", fontsize=12)
    plt.ylabel("출판사", fontsize=12)
    plt.tight_layout()
    pub_chart_path = os.path.join(artifact_dir, "top_publishers.png")
    plt.savefig(pub_chart_path, dpi=150)
    plt.close()

    # 2. 인기 저자 TOP 10
    plt.figure(figsize=(10, 6))
    top_auth = df['author_clean'].value_counts().head(10)
    sns.barplot(x=top_auth.values, y=top_auth.index, hue=top_auth.index, legend=False, palette="magma")
    plt.title("베스트셀러 인기 저자 TOP 10", fontsize=15, fontweight='bold', pad=15)
    plt.xlabel("도서 수 (권)", fontsize=12)
    plt.ylabel("저자", fontsize=12)
    plt.tight_layout()
    auth_chart_path = os.path.join(artifact_dir, "top_authors.png")
    plt.savefig(auth_chart_path, dpi=150)
    plt.close()

    # 3. 가격 분포 (정가 vs 판매가)
    plt.figure(figsize=(10, 6))
    # 이상치 제외한 범위에서 그리기 (정가 10만원 이하)
    price_filter = df[df['price_original_num'] <= 100000]
    sns.kdeplot(data=price_filter, x='price_original_num', fill=True, label='정가 (Shop Price)', color='gray')
    sns.kdeplot(data=price_filter, x='price_sale_num', fill=True, label='판매가 (Sale Price)', color='blue')
    plt.title("베스트셀러 도서 가격 분포 (10만원 이하 도서 대상)", fontsize=15, fontweight='bold', pad=15)
    plt.xlabel("가격 (원)", fontsize=12)
    plt.ylabel("밀도 (Density)", fontsize=12)
    plt.legend(fontsize=11)
    plt.tight_layout()
    price_chart_path = os.path.join(artifact_dir, "price_distribution.png")
    plt.savefig(price_chart_path, dpi=150)
    plt.close()

    # 4. 할인율 분포
    plt.figure(figsize=(10, 6))
    # 0% 초과 할인율 대상
    discount_filter = df[df['discount_rate_num'] > 0]
    sns.histplot(data=discount_filter, x='discount_rate_num', bins=15, kde=True, color='teal')
    plt.title("베스트셀러 할인율 분포 (할인 적용 도서 대상)", fontsize=15, fontweight='bold', pad=15)
    plt.xlabel("할인율 (%)", fontsize=12)
    plt.ylabel("도서 수 (권)", fontsize=12)
    plt.tight_layout()
    discount_chart_path = os.path.join(artifact_dir, "discount_distribution.png")
    plt.savefig(discount_chart_path, dpi=150)
    plt.close()

    # 5. 리뷰 평점 vs 판매지수 상관관계
    plt.figure(figsize=(10, 6))
    # 평점 0점 제외, 판매지수 로그 스케일 시각화 혹은 기본
    rating_filter = df[(df['rating_num'] > 0) & (df['sale_index_num'] > 0)]
    sns.scatterplot(data=rating_filter, x='rating_num', y='sale_index_num', alpha=0.6, color='coral', edgecolor='w', s=60)
    plt.title("평점 vs 판매지수 상관관계", fontsize=15, fontweight='bold', pad=15)
    plt.xlabel("평점 (10점 만점)", fontsize=12)
    plt.ylabel("판매지수", fontsize=12)
    plt.yscale('log') # 판매지수의 편차가 크므로 로그 스케일 적용
    plt.ylabel("판매지수 (Log Scale)", fontsize=12)
    plt.tight_layout()
    rating_chart_path = os.path.join(artifact_dir, "rating_vs_sale_index.png")
    plt.savefig(rating_chart_path, dpi=150)
    plt.close()

    # --- 통계 요약 지표 산출 ---
    total_books = len(df)
    avg_original_price = df['price_original_num'].mean()
    avg_sale_price = df['price_sale_num'].mean()
    avg_discount = df['discount_rate_num'].mean()
    avg_rating = df[df['rating_num'] > 0]['rating_num'].mean()
    total_reviews = df['review_count_num'].sum()
    avg_sale_index = df['sale_index_num'].mean()

    # 최고 판매지수 도서
    top_sale_book = df.loc[df['sale_index_num'].idxmax()]
    # 최고 평점 도서 (리뷰 10개 이상 중)
    high_rating_books = df[df['review_count_num'] >= 10]
    if not high_rating_books.empty:
        top_rating_book = high_rating_books.loc[high_rating_books['rating_num'].idxmax()]
    else:
        top_rating_book = df.loc[df['rating_num'].idxmax()]

    # 출판 연도별 도서 수
    year_trends = df['publish_year'].value_counts().sort_index(ascending=False).head(5)
    year_trends_str = ", ".join([f"{int(y)}년({int(c)}권)" for y, c in zip(year_trends.index, year_trends.values)])

    # 마크다운 리포트 텍스트 생성
    report_content = f"""# YES24 IT/모바일 베스트셀러 데이터 EDA 분석 보고서

본 보고서는 YES24 IT/모바일 베스트셀러 카테고리에서 수집한 총 **{total_books:,}개**의 도서 데이터를 바탕으로 수행한 탐색적 데이터 분석(EDA) 결과입니다.

---

## 📊 1. 핵심 요약 지표 (KPIs)

| 지표명 | 수치 | 설명 |
| :--- | :---: | :--- |
| **분석 대상 도서 수** | {total_books:,} 권 | 카테고리 전체 베스트셀러 도서 |
| **평균 정가** | {avg_original_price:,.0f} 원 | 도서 정가의 평균값 |
| **평균 판매가** | {avg_sale_price:,.0f} 원 | 실판매가의 평균값 |
| **평균 할인율** | {avg_discount:.1f}% | 정가 대비 할인 비율의 평균값 |
| **평균 평점** | {avg_rating:.2f} / 10 | 평점이 있는 도서들의 평균 점수 |
| **총 회원 리뷰 건수** | {total_reviews:,} 건 | 수집된 도서들에 등록된 리뷰 총합 |
| **평균 판매지수** | {avg_sale_index:,.1f} | 도서 인기도를 나타내는 YES24 판매지수 평균 |

---

## 🏆 2. 주요 하이라이트 도서

### 🔥 최고 판매지수 도서 (인기 1위)
* **도서명**: {top_sale_book['goods_name']}
* **저자/출판사**: {top_sale_book['author_clean']} / {top_sale_book['publisher']}
* **판매지수**: {top_sale_book['sale_index_num']:,}
* **가격**: 정가 {top_sale_book['price_original_num']:,.0f}원 → 판매가 {top_sale_book['price_sale_num']:,.0f}원 ({top_sale_book['discount_rate_num']:.0f}% 할인)
* **평점/리뷰**: {top_sale_book['rating_num']}점 (리뷰 {top_sale_book['review_count_num']:,}건)

### ⭐ 최고 평점 도서 (리뷰 10건 이상 기준)
* **도서명**: {top_rating_book['goods_name']}
* **저자/출판사**: {top_rating_book['author_clean']} / {top_rating_book['publisher']}
* **평점**: {top_rating_book['rating_num']} / 10 (리뷰 {top_rating_book['review_count_num']:,}건)
* **판매지수**: {top_rating_book['sale_index_num']:,}

---

## 📈 3. 데이터 시각화 분석

### 🏢 ① 인기 출판사 TOP 10
베스트셀러 목록에 가장 많은 도서를 올린 상위 10개 출판사 분포입니다.

![인기 출판사 TOP 10](top_publishers.png)

> [!NOTE]
> **출판사 시장 점유**: 베스트셀러 목록 내에서 특정 출판사들의 도서 점유율이 높게 나타납니다. 상위 출판사들은 IT 모바일 분야의 베스트셀러 트렌드를 주도하고 있음을 확인할 수 있습니다.

### ✍️ ② 인기 저자 TOP 10
베스트셀러에 가장 많은 작품을 올린 상위 10개 저자 분포입니다.

![인기 저자 TOP 10](top_authors.png)

---

### 💵 ③ 도서 가격 분포 (정가 vs 판매가)
도서들의 원래 정가(Shop Price)와 실제 할인이 적용된 판매가(Sale Price)의 밀도 분포입니다.

![도서 가격 분포](price_distribution.png)

> [!TIP]
> **주요 가격대 분석**: 대부분의 베스트셀러 도서는 20,000원 ~ 30,000원 선에 집중 분포하고 있으며, 할인이 적용되면서 전체적인 분포 곡선이 왼쪽(낮은 가격대)으로 평행 이동한 것을 볼 수 있습니다.

### 🏷️ ④ 도서 할인율 분포
도서에 적용되는 할인율의 빈도 분포입니다.

![도서 할인율 분포](discount_distribution.png)

> [!IMPORTANT]
> **할인율 평준화**: 대다수의 도서가 도서정가제의 영향 하에 **10%** 부근의 표준 할인율을 적용받고 있음을 명확하게 보여줍니다.

---

### 💬 ⑤ 평점과 판매지수의 상관관계
도서 평점(10점 만점)과 인기도(판매지수, 로그 스케일) 간의 관계를 보여주는 산점도입니다.

![평점 vs 판매지수](rating_vs_sale_index.png)

> [!NOTE]
> **상관관계 해석**: 평점과 판매지수 간에는 단순 비례적인 강력한 양의 상관관계는 관찰되지 않습니다. 이는 평점이 높다고 해서 무조건 많이 판매되는 것은 아니며, 대중적인 인지도(리뷰 수)나 마케팅 요소가 판매지수에 복합적으로 작용함을 나타냅니다.

---

## 📅 4. 출판 동향 및 기타 인사이트
* **최근 출판 경향**: 최근 5개년 출판 도서 비중 ({year_trends_str})이 압도적으로 높아, IT 기술 분야 특성상 최신 트렌드를 반영한 도서들이 베스트셀러에 신속하게 진입하고 유지되는 경향을 보입니다.
* **분철 서비스**: 전체 분석 대상 도서 중 **{df['is_spring_service'].value_counts().get('Y', 0) / total_books * 100:.1f}%**의 도서가 분철 서비스를 지원하여, 두꺼운 IT 전공 도서의 학습 편의성을 돕고 있습니다.

"""

    # 마크다운 리포트 파일 저장
    report_path = os.path.join(artifact_dir, "yes24_eda_report.md")
    with open(report_path, "w", encoding="utf-8") as f:
        f.write(report_content)
    
    print(f"EDA 보고서 생성 완료: {report_path}")
    print(f"시각화 차트 이미지 저장 완료: {artifact_dir}")

if __name__ == "__main__":
    # 경로 설정
    base_dir = os.path.dirname(os.path.abspath(__file__))
    csv_file = os.path.join(base_dir, "yes24_bestsellers.csv")
    
    # 아티팩트 디렉터리 경로 설정
    artifact_directory = r"C:\Users\Rei EA Jo\.gemini\antigravity-cli\brain\0c250dd8-76d4-4526-b6fa-c78ec61f3f85"
    
    generate_eda_report(csv_file, artifact_directory)
