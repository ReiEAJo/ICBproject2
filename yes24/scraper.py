# -*- coding: utf-8 -*-
import sys
import os
import time
import json
import re
import csv
from scrapling.fetchers import Fetcher
import pandas as pd

# 콘솔 출력 시 유니코드/한글 인코딩 에러 방지 (Windows 환경)
if sys.platform.startswith('win'):
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

def parse_number(text):
    """텍스트에서 숫자만 추출하는 헬퍼 함수"""
    if not text:
        return 0
    numbers = re.findall(r'\d+', text.replace(',', ''))
    if numbers:
        return int(''.join(numbers))
    return 0

def scrape_yes24_bestsellers(category_number="001001003", max_pages=100):
    url = "https://www.yes24.com/product/category/BestSellerContents"
    
    headers = {
        "Host": "www.yes24.com",
        "Referer": f"https://www.yes24.com/product/category/bestseller?categoryNumber={category_number}&pageNumber=1&pageSize=24",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36",
        "Accept": "*/*",
        "Accept-Language": "ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7",
        "X-Requested-With": "XMLHttpRequest"
    }

    all_books = []
    page = 1

    print(f"카테고리 {category_number} 베스트셀러 데이터 수집 시작...")

    while page <= max_pages:
        params = {
            "categoryNumber": category_number,
            "sumGb": "06",
            "sex": "A",
            "age": "255",
            "goodsTp": "0",
            "addOptionTp": "0",
            "excludeTp": "2",
            "pageNumber": str(page),
            "pageSize": "24",
            "goodsStatGb": "06",
            "eBookTp": "0",
            "bestType": "YES24_BESTSELLER",
            "type": "",
            "saleYear": "0",
            "saleMonth": "0",
            "weekNo": "0",
            "saleDts": "",
            "viewMode": "",
            "freeYn": ""
        }

        print(f"페이지 {page} 요청 중...")
        try:
            # scrapling Fetcher를 사용하여 HTTP 요청
            response = Fetcher.get(url, params=params, headers=headers, timeout=10)
            if response.status != 200:
                print(f"페이지 {page} 요청 실패: Status Code {response.status}")
                break

            # response 자체가 scrapling.Adaptor의 기능을 상속받아 .css() 사용 가능
            items = response.css("li[data-goods-no]")

            if not items:
                print(f"페이지 {page}에 상품이 없습니다. 수집을 종료합니다.")
                break

            print(f"페이지 {page}에서 {len(items)}개의 상품을 발견했습니다.")

            for idx, item in enumerate(items, 1):
                book_data = {}

                # 1. 태그 내의 기본 속성
                book_data['goods_no'] = item.attrib.get("data-goods-no")
                book_data['partbook_no'] = item.attrib.get("data-partbook-no")
                book_data['statgb'] = item.attrib.get("data-statgb")
                book_data['iy_no'] = item.attrib.get("data-iy-no")

                # 2. 순위
                book_data['rank'] = item.css("em.rank::text").get("").strip()

                # 3. 이미지 정보 및 상세 URL
                img_tag = item.css("img.lazy")
                if img_tag:
                    book_data['image_url'] = img_tag.attrib.get("data-original") or img_tag.attrib.get("src") or ""
                    book_data['goods_name_html'] = img_tag.attrib.get("alt") or ""
                else:
                    book_data['image_url'] = ""
                    book_data['goods_name_html'] = ""

                href = item.css("a.lnk_img::attr(href)").get()
                book_data['detail_url'] = "https://www.yes24.com" + href if href else ""

                # 4. 상품명 영역 (구분, 제목, 부제, 특징)
                info_name_div = item.css("div.info_name")
                if info_name_div:
                    book_data['goods_type'] = info_name_div.css("span.gd_res::text").get("").strip()
                    book_data['goods_name'] = info_name_div.css("a.gd_name::text").get(book_data['goods_name_html']).strip()
                    book_data['goods_sub_name'] = info_name_div.css("span.gd_nameE::text").get("").strip()

                    # 특징 목록 파싱
                    features = [f.strip() for f in info_name_div.css("span.gd_feature span.feature::text").getall()]
                    book_data['features'] = " | ".join(features)
                else:
                    book_data['goods_type'] = ""
                    book_data['goods_name'] = book_data['goods_name_html']
                    book_data['goods_sub_name'] = ""
                    book_data['features'] = ""

                # 5. 출판 정보 (저자, 출판사, 출판일)
                info_pub_div = item.css("div.info_pubGrp")
                if info_pub_div:
                    book_data['author'] = info_pub_div.css("span.info_auth::text").get("").strip()
                    if book_data['author'].endswith(" 저"):
                        book_data['author'] = book_data['author'][:-2].strip()

                    book_data['publisher'] = info_pub_div.css("span.info_pub::text").get("").strip()
                    book_data['publish_date'] = info_pub_div.css("span.info_date::text").get("").strip()
                else:
                    book_data['author'] = ""
                    book_data['publisher'] = ""
                    book_data['publish_date'] = ""

                # 6. 구매 혜택
                book_data['benefits'] = item.css("dl.info_present dd::text").get("").strip()

                # 7. 가격 정보
                info_price_div = item.css("div.info_price")
                if info_price_div:
                    book_data['discount_rate'] = info_price_div.css("span.txt_sale::text").get("").strip()
                    book_data['price_sale'] = info_price_div.css("strong.txt_num::text").get("").strip()

                    price_original = info_price_div.css('span[class*="dash"]::text').get()
                    if not price_original:
                        price_original = info_price_div.css('span.dash::text').get()
                    book_data['price_original'] = price_original.strip() if price_original else ""

                    book_data['point'] = info_price_div.css("span.yPoint::text").get("").strip()
                else:
                    book_data['discount_rate'] = ""
                    book_data['price_sale'] = ""
                    book_data['price_original'] = ""
                    book_data['point'] = ""

                # 8. 평점 및 판매지수
                info_rating_div = item.css("div.info_rating")
                if info_rating_div:
                    book_data['sale_index_text'] = info_rating_div.css("span.saleNum::text").get("").strip()
                    book_data['sale_index'] = parse_number(book_data['sale_index_text'])

                    book_data['review_count_text'] = info_rating_div.css("span.rating_rvCount::text").get("").strip()
                    book_data['review_count'] = parse_number(book_data['review_count_text'])

                    book_data['rating'] = info_rating_div.css("span.rating_grade em.yes_b::text").get("").strip()
                else:
                    book_data['sale_index_text'] = ""
                    book_data['sale_index'] = 0
                    book_data['review_count_text'] = ""
                    book_data['review_count'] = 0
                    book_data['rating'] = ""

                # 9. 배송 정보
                book_data['delivery_info'] = item.css("div.info_deli::text").get("").strip()

                # 10. 분철 서비스 여부
                info_spring_div = item.css("div.info_spring")
                keynote_spring = item.css('span[class*="spring"]')
                book_data['is_spring_service'] = "Y" if (info_spring_div or keynote_spring) else "N"

                # 11. 태그 정보
                tags = [t.strip() for t in item.css("div.info_tag span.tag::text").getall()]
                book_data['tags'] = ", ".join(tags)

                # 12. 관련 상품
                rel_text = item.css("div.info_relG::text").get("")
                book_data['relation_goods'] = rel_text.replace("관련상품 :", "").strip() if rel_text else ""

                # 13. ORD_GOODS_OPT JSON 데이터 추가 파싱
                opt_val = item.css('input[name="ORD_GOODS_OPT"]::attr(value)').get()
                if opt_val:
                    try:
                        opt_json = json.loads(opt_val)
                        book_data['opt_goods_no'] = opt_json.get("goods_no")
                        book_data['opt_goods_seq'] = opt_json.get("goods_seq")
                        book_data['opt_order_limit_yn'] = opt_json.get("order_limit_yn")
                        book_data['opt_order_remain_count'] = opt_json.get("order_remain_count")
                        book_data['opt_event_no'] = opt_json.get("event_no")
                        book_data['opt_add_cart_yn'] = opt_json.get("add_cart_yn")
                        book_data['opt_goods_state'] = opt_json.get("goods_state")
                        book_data['opt_order_limit_count'] = opt_json.get("order_limit_count")
                        book_data['opt_resource_key'] = opt_json.get("resource_key")
                        book_data['opt_limit_age_yn'] = opt_json.get("limit_age_yn")
                        book_data['opt_limit_age'] = opt_json.get("limit_age")
                        book_data['opt_member_age'] = opt_json.get("member_age")
                        book_data['opt_noint_quotamonth'] = opt_json.get("noint_quotamonth")
                        book_data['opt_min_cnt'] = opt_json.get("min_cnt")
                        book_data['opt_max_cnt'] = opt_json.get("max_cnt")
                        book_data['opt_salepr'] = opt_json.get("opt_salepr")
                        book_data['opt_yn'] = opt_json.get("opt_yn")
                        book_data['opt_inst_yn'] = opt_json.get("opt_inst_yn")
                        book_data['opt_flat_rate_yn'] = opt_json.get("flat_rate_yn")
                        book_data['opt_rent_goods_yn'] = opt_json.get("rent_goods_yn")
                        book_data['opt_bookclue_yn'] = opt_json.get("bookclue_yn")
                        book_data['opt_goods_gb'] = opt_json.get("goods_gb")
                        book_data['opt_goodsSortNo'] = opt_json.get("goodsSortNo")
                        book_data['opt_goodsSortNm'] = opt_json.get("goodsSortNm")
                        book_data['opt_goodsAuth'] = opt_json.get("goodsAuth")
                        book_data['opt_shopPrice'] = opt_json.get("shopPrice")
                        book_data['opt_salePrice'] = opt_json.get("salePrice")
                        book_data['opt_discountShopPrice'] = opt_json.get("discountShopPrice")
                    except Exception as json_err:
                        print(f"JSON 파싱 에러 (상품번호: {book_data['goods_no']}): {json_err}")

                all_books.append(book_data)

            # 서버 부하를 줄이기 위한 딜레이
            time.sleep(1.0)
            page += 1

        except Exception as e:
            print(f"페이지 {page} 수집 중 에러 발생: {e}")
            break

    print(f"데이터 수집 완료! 총 {len(all_books)}개의 상품을 수집했습니다.")
    
    if all_books:
        # 데이터프레임으로 변환
        df = pd.DataFrame(all_books)
        
        # 1페이지 테스트 결과 CSV로 저장
        output_dir = os.path.dirname(os.path.abspath(__file__))
        csv_path = os.path.join(output_dir, "yes24_bestsellers.csv")
        
        # 인코딩은 엑셀 등에서 한글이 깨지지 않도록 utf-8-sig 사용
        df.to_csv(csv_path, index=False, encoding="utf-8-sig")
        print(f"데이터를 CSV 파일로 저장 완료: {csv_path}")
        return True
    else:
        print("수집된 데이터가 없습니다.")
        return False

if __name__ == "__main__":
    # 먼저 1페이지가 성공적으로 수집되는지 확인하기 위해 max_pages=1로 테스트 진행
    # 테스트가 성공하면 전체 페이지를 수집하는 코드를 가동하도록 구성할 수 있음.
    # 명령줄 인자로 'all'을 주면 전체 수집, 기본값은 1페이지 테스트
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == 'all':
        scrape_yes24_bestsellers(max_pages=100)
    else:
        print("--- 1페이지 테스트 수집을 시작합니다 ---")
        success = scrape_yes24_bestsellers(max_pages=1)
        if success:
            print("1페이지 수집 테스트 완료! 전체 페이지 수집을 하려면 스크립트 인자로 'all'을 주어 다시 실행하세요.")
        else:
            print("1페이지 수집 테스트 실패.")
