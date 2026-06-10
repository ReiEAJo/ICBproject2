import requests
import json
import pandas as pd
from datetime import datetime

class NaverAPI:
    def __init__(self, client_id, client_secret):
        self.client_id = client_id
        self.client_secret = client_secret
        self.headers = {
            "X-Naver-Client-Id": self.client_id,
            "X-Naver-Client-Secret": self.client_secret
        }

    def get_datalab_search(self, keywords, start_date, end_date, time_unit="date"):
        """
        통합 검색어 트렌드 API
        keywords: list of strings (e.g., ["파이썬", "자바"])
        """
        url = "https://openapi.naver.com/v1/datalab/search"
        self.headers["Content-Type"] = "application/json"
        
        keyword_groups = [
            {"groupName": kw, "keywords": [kw]} for kw in keywords
        ]
        
        body = {
            "startDate": start_date,
            "endDate": end_date,
            "timeUnit": time_unit,
            "keywordGroups": keyword_groups
        }
        
        response = requests.post(url, headers=self.headers, data=json.dumps(body))
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error {response.status_code}: {response.text}")
            return None

    def search_general(self, search_type, query, display=100, sort="sim"):
        """
        일반 검색 API (블로그, 카페글, 뉴스, 쇼핑)
        search_type: "blog", "cafearticle", "news", "shop"
        """
        url = f"https://openapi.naver.com/v1/search/{search_type}.json"
        params = {
            "query": query,
            "display": display,
            "start": 1,
            "sort": sort
        }
        
        response = requests.get(url, headers=self.headers, params=params)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error {response.status_code}: {response.text}")
            return None

    def get_shopping_trend(self, keywords, start_date, end_date, time_unit="date", category="50000000"):
        """
        쇼핑 인사이트 (키워드 트렌드) - 기본 카테고리 (50000000: 패션의류 등 더미용, 실제로는 카테고리 코드가 필요함)
        참고: 쇼핑 인사이트 API는 category 코드가 필수입니다. 
        대시보드에서는 가장 넓은 범위인 '50000000' (패션의류) 혹은 '50000003' (디지털/가전)을 예시로 사용하거나, 통합 검색어 트렌드로 대체.
        """
        url = "https://openapi.naver.com/v1/datalab/shopping/category/keywords"
        self.headers["Content-Type"] = "application/json"
        
        # 키워드를 [{"name": kw, "param": [kw]}] 형식으로 변환
        keyword_args = [{"name": kw, "param": [kw]} for kw in keywords]
        
        body = {
            "startDate": start_date,
            "endDate": end_date,
            "timeUnit": time_unit,
            "category": category, 
            "keyword": keyword_args
        }
        
        response = requests.post(url, headers=self.headers, data=json.dumps(body))
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error {response.status_code}: {response.text}")
            return {"error": response.status_code, "message": response.text}
