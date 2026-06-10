Title: Cached Content

Description: Fetched from cache

Source: https://developers.naver.com/docs/serviceapi/search/shopping/shopping.md

---

<!doctype html>
<html lang=ko>
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width,initial-scale=1.0,maximum-scale=1.0,minimum-scale=1.0,user-scalable=no">
    <meta name="google-site-verification" content="f6fjgA4xpfKO1zPNp92lRU_PN8Z9oO4HE6QFptF3MCs" />
<title>검색 > 쇼핑 - Search API</title>
<meta name="description" content="검색 > 쇼핑 쇼핑 검색 개요 개요 사전 준비 사항 쇼핑 검색 API 레퍼런스 쇼핑 검색 결과 조회 오류 코드 검색 API 쇼핑 검색 구현 예제 쇼핑 검색 개요 개요 사전 준비 사항 개요 검색 API와 쇼핑 검색 개요 검색 API는 네이버 검색 결과를 뉴스, 백과"/>


    <link rel="stylesheet" href="/inc/devcenter/xeicon2.3.1/xeicon.min.css">
    <link rel="stylesheet" type="text/css" href="/inc/devcenter/dist/style.d8b74738635aed08dea2e49cf820091a.css"/>


    <link rel="stylesheet" type="text/css" href="/inc/devcenter/css/prettify.css"/>
    <script src="/inc/devcenter/js/static/lib/prettify.js" type="text/javascript"></script>

    <script type="text/javascript" src="/inc/devcenter/js/static/lib/jquery-3.1.1.min.js"></script>
    <script type="text/javascript" src="/inc/devcenter/dist/manifest.00d9f3ddce23e7b83961.js"></script>
    <script type="text/javascript" src="/inc/devcenter/dist/vendor.ca53fd37b61f12ed8c89.js"></script>
    <script type="text/javascript" src="/inc/devcenter/dist/common.df201560aee617cccac8.js"></script>

</head>


<body>
<div id="react-app"></div>
<div id="react-content" style="display:none">
<div id="ssrContent"><div class="h_page_area"><h1 id="검색-_-쇼핑">검색 &gt; 쇼핑 <a class="header-anchor" href="/docs/serviceapi/search/shopping/shopping.md#검색-_-쇼핑" aria-hidden="true"><i class="xi-link"></i></a></h1>
<div class="side_menu"></div></div><div class="table-of-contents">
<ul>
    <li><a href="/docs/serviceapi/search/shopping/shopping.md#&#xC1FC;&#xD551;-&#xAC80;&#xC0C9;-&#xAC1C;&#xC694;">&#xC1FC;&#xD551; &#xAC80;&#xC0C9; &#xAC1C;&#xC694;</a></li>
    <ul>
        <li><a href="/docs/serviceapi/search/shopping/shopping.md#&#xAC1C;&#xC694;">&#xAC1C;&#xC694;</a></li>
        <li><a href="/docs/serviceapi/search/shopping/shopping.md#&#xC0AC;&#xC804;-&#xC900;&#xBE44;-&#xC0AC;&#xD56D;">&#xC0AC;&#xC804; &#xC900;&#xBE44; &#xC0AC;&#xD56D;</a></li>
    </ul>
    <li><a href="/docs/serviceapi/search/shopping/shopping.md#&#xC1FC;&#xD551;-&#xAC80;&#xC0C9;-api-&#xB808;&#xD37C;&#xB7F0;&#xC2A4;">&#xC1FC;&#xD551; &#xAC80;&#xC0C9; API &#xB808;&#xD37C;&#xB7F0;&#xC2A4;</a></li>
    <ul>
        <li><a href="/docs/serviceapi/search/shopping/shopping.md#&#xC1FC;&#xD551;-&#xAC80;&#xC0C9;-&#xACB0;&#xACFC;-&#xC870;&#xD68C;">&#xC1FC;&#xD551; &#xAC80;&#xC0C9; &#xACB0;&#xACFC; &#xC870;&#xD68C;</a></li>
        <li><a href="/docs/serviceapi/search/shopping/shopping.md#&#xC624;&#xB958;-&#xCF54;&#xB4DC;">&#xC624;&#xB958; &#xCF54;&#xB4DC;</a></li>
    </ul>
    <li><a href="/docs/serviceapi/search/shopping/shopping.md#&#xAC80;&#xC0C9;-api-&#xC1FC;&#xD551;-&#xAC80;&#xC0C9;-&#xAD6C;&#xD604;-&#xC608;&#xC81C;">&#xAC80;&#xC0C9; API &#xC1FC;&#xD551; &#xAC80;&#xC0C9; &#xAD6C;&#xD604; &#xC608;&#xC81C;</a></li>
</ul>
</div>
<h2 id="쇼핑-검색-개요">쇼핑 검색 개요 <a class="header-anchor" href="/docs/serviceapi/search/shopping/shopping.md#쇼핑-검색-개요" aria-hidden="true"><i class="xi-link"></i></a></h2>
<ul>
<li><a href="/docs/serviceapi/search/shopping/shopping.md#%EA%B0%9C%EC%9A%94">개요</a></li>
<li><a href="/docs/serviceapi/search/shopping/shopping.md#%EC%82%AC%EC%A0%84-%EC%A4%80%EB%B9%84-%EC%82%AC%ED%95%AD">사전 준비 사항</a></li>
</ul>
<h3 id="개요">개요 <a class="header-anchor" href="/docs/serviceapi/search/shopping/shopping.md#개요" aria-hidden="true"><i class="xi-link"></i></a></h3>
<h4 id="검색-api와-쇼핑-검색-개요">검색 API와 쇼핑 검색 개요 <a class="header-anchor" href="/docs/serviceapi/search/shopping/shopping.md#검색-api와-쇼핑-검색-개요" aria-hidden="true"><i class="xi-link"></i></a></h4>
<p>검색 API는 네이버 검색 결과를 뉴스, 백과사전, 블로그, 쇼핑, 웹 문서, 전문정보, 지식iN, 책, 카페글 등 분야별로 볼 수 있는 API입니다. 그 외에 지역 검색 결과와 성인 검색어 판별 기능, 오타 변환 기능을 제공합니다.</p>
<p>쇼핑 검색은 검색 API를 사용해 네이버 검색의 쇼핑 검색 결과를 반환하는 RESTful API입니다. 쇼핑 검색 결과를 XML 형식 또는 JSON 형식으로 반환합니다. API를 호출할 때는 검색어와 검색 조건을 쿼리 스트링(Query String) 형식의 데이터로 전달합니다.</p>
<p>쇼핑 검색은 검색 API를 사용하며, 검색 API의 하루 호출 한도는 25,000회입니다.</p>
<h4 id="검색-api-특징">검색 API 특징 <a class="header-anchor" href="/docs/serviceapi/search/shopping/shopping.md#검색-api-특징" aria-hidden="true"><i class="xi-link"></i></a></h4>
<p>검색 API는 비로그인 방식 오픈 API입니다.</p>
<p>비로그인 방식 오픈 API는 네이버 오픈API를 호출할 때 HTTP 요청 헤더에 클라이언트 아이디와 클라이언트 시크릿 값만 전송해 사용할 수 있는 오픈 API입니다. 클라이언트 아이디와 클라이언트 시크릿은 네이버 오픈API에서 인증된 사용자인지 확인하는 수단입니다. <a href="https://developers.naver.com/">네이버 개발자 센터</a>에서 애플리케이션을 등록하면 클라이언트 아이디와 클라이언트 시크릿이 발급됩니다.</p>
<blockquote>
<p><strong>참고</strong><br>
네이버 오픈API의 종류와 클라이언트 아이디, 클라이언트 시크릿에 관한 자세한 내용은 &quot;<a href="https://developers.naver.com/docs/common/openapiguide/">API 공통 가이드</a>&quot;를 참고하십시오.</p>
</blockquote>
<h3 id="사전-준비-사항">사전 준비 사항 <a class="header-anchor" href="/docs/serviceapi/search/shopping/shopping.md#사전-준비-사항" aria-hidden="true"><i class="xi-link"></i></a></h3>
<p>검색 API를 사용해 쇼핑 검색을 실행하려면 먼저 <a href="https://developers.naver.com/">네이버 개발자 센터</a>에서 애플리케이션을 등록하고 클라이언트 아이디와 클라이언트 시크릿을 발급받아야 합니다.</p>
<p>클라이언트 아이디와 클라이언트 시크릿은 인증된 사용자인지를 확인하는 수단이며, 애플리케이션이 등록되면 발급됩니다. 클라이언트 아이디와 클라이언트 시크릿을 네이버 오픈API를 호출할 때 HTTP 헤더에 포함해서 전송해야 API를 호출할 수 있습니다. API 사용량은 클라이언트 아이디별로 합산됩니다.</p>
<p>쇼핑 검색을 실행하기 위해 발급받은 클라이언트 아이디와 클라이언트 시크릿은 검색 API의 다른 작업을 실행할 때에도 사용할 수 있습니다. 애플리케이션을 등록하고 클라이언트 아이디와 클라이언트 시크릿을 발급받는 방법은 <a href="/docs/serviceapi/search/shopping/../blog/blog.md#%EC%82%AC%EC%A0%84-%EC%A4%80%EB%B9%84-%EC%82%AC%ED%95%AD">블로그 검색의 사전 준비 사항</a>을 참고합니다.</p>
<blockquote>
<p><strong>주의</strong><br>
네이버에 로그인한 사용자 계정으로 애플리케이션이 등록됩니다. 애플리케이션을 등록한 네이버 아이디는 '관리자' 권한을 가지게 되므로 네이버 계정의 보안에 각별히 주의해야 합니다.<br>
회사나 단체에서 애플리케이션을 등록할 때는 추후 키 관리 등이 용이하도록 네이버 단체 회원으로 로그인해 이용할 것을 권장합니다.</p>
<ul>
<li><a href="https://nid.naver.com/group/commonAction.nhn?m=viewTerms">네이버 단체 회원 가입하기</a></li>
</ul>
</blockquote>
<h2 id="쇼핑-검색-api-레퍼런스">쇼핑 검색 API 레퍼런스 <a class="header-anchor" href="/docs/serviceapi/search/shopping/shopping.md#쇼핑-검색-api-레퍼런스" aria-hidden="true"><i class="xi-link"></i></a></h2>
<ul>
<li><a href="/docs/serviceapi/search/shopping/shopping.md#%EC%87%BC%ED%95%91-%EA%B2%80%EC%83%89-%EA%B2%B0%EA%B3%BC-%EC%A1%B0%ED%9A%8C">쇼핑 검색 결과 조회</a></li>
</ul>
<h3 id="쇼핑-검색-결과-조회">쇼핑 검색 결과 조회 <a class="header-anchor" href="/docs/serviceapi/search/shopping/shopping.md#쇼핑-검색-결과-조회" aria-hidden="true"><i class="xi-link"></i></a></h3>
<h4 id="설명">설명 <a class="header-anchor" href="/docs/serviceapi/search/shopping/shopping.md#설명" aria-hidden="true"><i class="xi-link"></i></a></h4>
<p>네이버 검색의 쇼핑 검색 결과를 XML 형식 또는 JSON 형식으로 반환합니다.</p>
<h4 id="요청-url">요청 URL <a class="header-anchor" href="/docs/serviceapi/search/shopping/shopping.md#요청-url" aria-hidden="true"><i class="xi-link"></i></a></h4>
<table>
<thead>
<tr>
<th style="width: 75%">요청 URL</th>
<th style="width: 25%">반환 형식</th>
</tr>
</thead>
<tbody>
<tr>
<td><code>https://openapi.naver.com/v1/search/shop.xml</code></td>
<td style="text-align:center">XML</td>
</tr>
<tr>
<td><code>https://openapi.naver.com/v1/search/shop.json</code></td>
<td style="text-align:center">JSON</td>
</tr>
</tbody>
</table>
<h4 id="프로토콜">프로토콜 <a class="header-anchor" href="/docs/serviceapi/search/shopping/shopping.md#프로토콜" aria-hidden="true"><i class="xi-link"></i></a></h4>
<p>HTTPS</p>
<h4 id="http-메서드">HTTP 메서드 <a class="header-anchor" href="/docs/serviceapi/search/shopping/shopping.md#http-메서드" aria-hidden="true"><i class="xi-link"></i></a></h4>
<p>GET</p>
<h4 id="파라미터">파라미터 <a class="header-anchor" href="/docs/serviceapi/search/shopping/shopping.md#파라미터" aria-hidden="true"><i class="xi-link"></i></a></h4>
<p>파라미터를 쿼리 스트링 형식으로 전달합니다.</p>
<table>
<thead>
<tr>
<th style="width: 30%">파라미터</th>
<th style="width: 30%">타입</th>
<th style="width: 10%">필수 여부</th>
<th style="width: 30%">설명</th>
</tr>
</thead>
<tbody>
<tr>
<td>query</td>
<td>String</td>
<td style="text-align:center">Y</td>
<td>검색어. UTF-8로 인코딩되어야 합니다.</td>
</tr>
<tr>
<td>display</td>
<td>Integer</td>
<td style="text-align:center">N</td>
<td>한 번에 표시할 검색 결과 개수(기본값: 10, 최댓값: 100)</td>
</tr>
<tr>
<td>start</td>
<td>Integer</td>
<td style="text-align:center">N</td>
<td>검색 시작 위치(기본값: 1, 최댓값: 1000)</td>
</tr>
<tr>
<td>sort</td>
<td>String</td>
<td style="text-align:center">N</td>
<td>검색 결과 정렬 방법<br/>- <code>sim</code>: 정확도순으로 내림차순 정렬(기본값)<br/>- <code>date</code>: 날짜순으로 내림차순 정렬<br/>- <code>asc</code>: 가격순으로 오름차순 정렬<br/>- <code>dsc</code>: 가격순으로 내림차순 정렬</td>
</tr>
<tr>
<td>filter</td>
<td>String</td>
<td style="text-align:center">N</td>
<td>검색 결과에 포함할 상품 유형<br/>- 설정 안 함: 모든 상품(기본값)<br/>- <code>naverpay</code>: 네이버페이 연동 상품</td>
</tr>
<tr>
<td>exclude</td>
<td>String</td>
<td style="text-align:center">N</td>
<td>검색 결과에서 제외할 상품 유형. <code>exclude={option}:{option}:{option}</code> 형태로 설정합니다(예: <code>exclude=used:cbshop</code>).<br/>- <code>used</code>: 중고<br/>- <code>rental</code>: 렌탈<br/>- <code>cbshop</code>: 해외직구, 구매대행</td>
</tr>
</tbody>
</table>
<h4 id="참고-사항">참고 사항 <a class="header-anchor" href="/docs/serviceapi/search/shopping/shopping.md#참고-사항" aria-hidden="true"><i class="xi-link"></i></a></h4>
<p>API를 요청할 때 다음 예와 같이 HTTP 요청 헤더에 <a href="https://developers.naver.com/docs/common/openapiguide/appregister.md#%ED%81%B4%EB%9D%BC%EC%9D%B4%EC%96%B8%ED%8A%B8-%EC%95%84%EC%9D%B4%EB%94%94%EC%99%80-%ED%81%B4%EB%9D%BC%EC%9D%B4%EC%96%B8%ED%8A%B8-%EC%8B%9C%ED%81%AC%EB%A6%BF-%ED%99%95%EC%9D%B8">클라이언트 아이디와 클라이언트 시크릿</a>을 추가해야 합니다.</p>
<pre class="prettyprint"><code class="language-sh">&gt; GET /v1/search/shop.xml?query=%EC%A3%BC%EC%8B%9D&amp;display=10&amp;start=1&amp;sort=sim HTTP/1.1
&gt; Host: openapi.naver.com
&gt; User-Agent: curl/7.49.1
&gt; Accept: */*
&gt; X-Naver-Client-Id: {애플리케이션 등록 시 발급받은 클라이언트 아이디 값}
&gt; X-Naver-Client-Secret: {애플리케이션 등록 시 발급받은 클라이언트 시크릿 값}
</code></pre>
<h4 id="요청-예">요청 예 <a class="header-anchor" href="/docs/serviceapi/search/shopping/shopping.md#요청-예" aria-hidden="true"><i class="xi-link"></i></a></h4>
<pre class="prettyprint"><code class="language-sh">curl &quot;https://openapi.naver.com/v1/search/shop.xml?query=%EC%A3%BC%EC%8B%9D&amp;display=10&amp;start=1&amp;sort=sim&quot; \
    -H &quot;X-Naver-Client-Id: {애플리케이션 등록 시 발급받은 클라이언트 아이디 값}&quot; \
    -H &quot;X-Naver-Client-Secret: {애플리케이션 등록 시 발급받은 클라이언트 시크릿 값}&quot; -v
</code></pre>
<h4 id="응답">응답 <a class="header-anchor" href="/docs/serviceapi/search/shopping/shopping.md#응답" aria-hidden="true"><i class="xi-link"></i></a></h4>
<p>응답에 성공하면 결괏값을 XML 형식 또는 JSON 형식으로 반환합니다. XML 형식의 결괏값은 다음과 같습니다.</p>
<table>
<thead>
<tr>
<th style="width: 42.857142857142854%">요소</th>
<th style="width: 14.285714285714285%">타입</th>
<th style="width: 42.857142857142854%">설명</th>
</tr>
</thead>
<tbody>
<tr>
<td>rss</td>
<td style="text-align:center">-</td>
<td>RSS 컨테이너. RSS 리더기를 사용해 검색 결과를 확인할 수 있습니다.</td>
</tr>
<tr>
<td>rss/channel</td>
<td style="text-align:center">-</td>
<td>검색 결과를 포함하는 컨테이너. <code>channel</code> 요소의 하위 요소인 <code>title</code>, <code>link</code>, <code>description</code>은 RSS에서 사용하는 정보이며, 검색 결과와는 상관이 없습니다.</td>
</tr>
<tr>
<td>rss/channel/lastBuildDate</td>
<td style="text-align:center">dateTime</td>
<td>검색 결과를 생성한 시간</td>
</tr>
<tr>
<td>rss/channel/total</td>
<td style="text-align:center">Integer</td>
<td>총 검색 결과 개수</td>
</tr>
<tr>
<td>rss/channel/start</td>
<td style="text-align:center">Integer</td>
<td>검색 시작 위치</td>
</tr>
<tr>
<td>rss/channel/display</td>
<td style="text-align:center">Integer</td>
<td>한 번에 표시할 검색 결과 개수</td>
</tr>
<tr>
<td>rss/channel/item</td>
<td style="text-align:center">-</td>
<td>개별 검색 결과. JSON 형식의 결괏값에서는 <code>items</code> 속성의 JSON 배열로 개별 검색 결과를 반환합니다.</td>
</tr>
<tr>
<td>rss/channel/item/title</td>
<td style="text-align:center">String</td>
<td>상품 이름. 이름에서 검색어와 일치하는 부분은 <code>&lt;b&gt;</code> 태그로 감싸져 있습니다.</td>
</tr>
<tr>
<td>rss/channel/item/link</td>
<td style="text-align:center">String</td>
<td>상품 정보 URL</td>
</tr>
<tr>
<td>rss/channel/item/image</td>
<td style="text-align:center">String</td>
<td>섬네일 이미지의 URL</td>
</tr>
<tr>
<td>rss/channel/item/lprice</td>
<td style="text-align:center">Integer</td>
<td>최저가. 최저가 정보가 없으면 <code>0</code>을 반환합니다. 가격 비교 데이터가 없으면 상품 가격을 의미합니다.</td>
</tr>
<tr>
<td>rss/channel/item/hprice</td>
<td style="text-align:center">Integer</td>
<td>최고가. 최고가 정보가 없거나 가격 비교 데이터가 없으면 <code>0</code>을 반환합니다.</td>
</tr>
<tr>
<td>rss/channel/item/mallName</td>
<td style="text-align:center">String</td>
<td>상품을 판매하는 쇼핑몰. 쇼핑몰 정보가 없으면 <code>네이버</code>를 반환합니다.</td>
</tr>
<tr>
<td>rss/channel/item/productId</td>
<td style="text-align:center">Integer</td>
<td>네이버 쇼핑의 상품 ID</td>
</tr>
<tr>
<td>rss/channel/item/productType</td>
<td style="text-align:center">Integer</td>
<td>상품군과 상품 종류에 따른 상품 타입. 상품군과 상품 종류에 따른 상품 타입은 <a href="/docs/serviceapi/search/shopping/shopping.md#%EC%83%81%ED%92%88%EA%B5%B0-%ED%83%80%EC%9E%85">상품군 타입</a>의 표를 참고합니다.<br/>- 상품군: 일반상품, 중고상품, 단종상품, 판매예정상품<br/>- 상품 종류: 가격비교 상품, 가격비교 비매칭 일반상품, 가격비교 매칭 일반상품</td>
</tr>
<tr>
<td>rss/channel/item/maker</td>
<td style="text-align:center">String</td>
<td>제조사</td>
</tr>
<tr>
<td>rss/channel/item/brand</td>
<td style="text-align:center">String</td>
<td>브랜드</td>
</tr>
<tr>
<td>rss/channel/item/category1</td>
<td style="text-align:center">String</td>
<td>상품의 카테고리(대분류)</td>
</tr>
<tr>
<td>rss/channel/item/category2</td>
<td style="text-align:center">String</td>
<td>상품의 카테고리(중분류)</td>
</tr>
<tr>
<td>rss/channel/item/category3</td>
<td style="text-align:center">String</td>
<td>상품의 카테고리(소분류)</td>
</tr>
<tr>
<td>rss/channel/item/category4</td>
<td style="text-align:center">String</td>
<td>상품의 카테고리(세분류)</td>
</tr>
</tbody>
</table>
<h4 id="상품군-타입">상품군 타입 <a class="header-anchor" href="/docs/serviceapi/search/shopping/shopping.md#상품군-타입" aria-hidden="true"><i class="xi-link"></i></a></h4>
<table>
<thead>
<tr>
<th style="width: 33.33333333333333%">상품군</th>
<th style="width: 33.33333333333333%">상품 종류</th>
<th style="width: 33.33333333333333%">타입</th>
</tr>
</thead>
<tbody>
<tr>
<td>일반상품</td>
<td>가격비교 상품</td>
<td>1</td>
</tr>
<tr>
<td>일반상품</td>
<td>가격비교 비매칭 일반상품</td>
<td>2</td>
</tr>
<tr>
<td>일반상품</td>
<td>가격비교 매칭 일반상품</td>
<td>3</td>
</tr>
<tr>
<td>중고상품</td>
<td>가격비교 상품</td>
<td>4</td>
</tr>
<tr>
<td>중고상품</td>
<td>가격비교 비매칭 일반상품</td>
<td>5</td>
</tr>
<tr>
<td>중고상품</td>
<td>가격비교 매칭 일반상품</td>
<td>6</td>
</tr>
<tr>
<td>단종상품</td>
<td>가격비교 상품</td>
<td>7</td>
</tr>
<tr>
<td>단종상품</td>
<td>가격비교 비매칭 일반상품</td>
<td>8</td>
</tr>
<tr>
<td>단종상품</td>
<td>가격비교 매칭 일반상품</td>
<td>9</td>
</tr>
<tr>
<td>판매예정상품</td>
<td>가격비교 상품</td>
<td>10</td>
</tr>
<tr>
<td>판매예정상품</td>
<td>가격비교 비매칭 일반상품</td>
<td>11</td>
</tr>
<tr>
<td>판매예정상품</td>
<td>가격비교 매칭 일반상품</td>
<td>12</td>
</tr>
</tbody>
</table>
<h4 id="응답-예">응답 예 <a class="header-anchor" href="/docs/serviceapi/search/shopping/shopping.md#응답-예" aria-hidden="true"><i class="xi-link"></i></a></h4>
<pre class="prettyprint"><code class="language-xml">&lt; HTTP/1.1 200 OK
&lt; Server: nginx
&lt; Date: Mon, 26 Sep 2016 09:04:44 GMT
&lt; Content-Type: text/xml;charset=utf-8
&lt; Transfer-Encoding: chunked
&lt; Connection: keep-alive
&lt; Keep-Alive: timeout=5
&lt; Vary: Accept-Encoding
&lt; X-Powered-By: Naver
&lt; Cache-Control: no-cache, no-store, must-revalidate
&lt; Pragma: no-cache
&lt;
&lt;rss version=&quot;2.0&quot;&gt;
    &lt;channel&gt;
        &lt;title&gt;Naver Open API - shop ::&#39;가방&#39;&lt;/title&gt;
        &lt;link&gt;http://search.naver.com&lt;/link&gt;
        &lt;description&gt;Naver Search Result&lt;/description&gt;
        &lt;lastBuildDate&gt;Tue, 04 Oct 2016 13:23:58 +0900&lt;/lastBuildDate&gt;
        &lt;total&gt;17161390&lt;/total&gt;
        &lt;start&gt;1&lt;/start&gt;
        &lt;display&gt;10&lt;/display&gt;
        &lt;item&gt;
            &lt;title&gt;허니트립 보스턴백&lt;/title&gt;
            &lt;link&gt;http://openapi.naver.com/l?AAABWLsQ7CIBRFv+Z1JLzSShkYqLajRmPcG6TQRCgiNunfizdnODnJfX9N2iUMCnoKHYWh/4sSlUtmli7nCExBPRY+bo1xCZaEaTOJ6NWXaKdsSHAB2Lg8gZ2QMmybA0cuqiyx4W0ZZR2KrvJyx2CPV3RQ95fbnDT3r+Fh2kbfz5su7x8wIs7ZjgAAAA==&lt;/link&gt;
            &lt;image&gt;http://shopping.phinf.naver.net/main_1031546/10315467179.jpg&lt;/image&gt;
            &lt;lprice&gt;6700&lt;/lprice&gt;
            &lt;hprice&gt;0&lt;/hprice&gt;
            &lt;mallName&gt;허니트립&lt;/mallName&gt;
            &lt;productId&gt;10315467179&lt;/productId&gt;
            &lt;productType&gt;2&lt;/productType&gt;
            &lt;brand&gt;&lt;/brand&gt;
            &lt;maker&gt;허니트립&lt;/maker&gt;
            &lt;category1&gt;패션잡화&lt;/category1&gt;
            &lt;category2&gt;여행용가방/소품&lt;/category2&gt;
            &lt;category3&gt;보스턴백&lt;/category3&gt;
            &lt;category4&gt;&lt;/category4&gt;
        &lt;/item&gt;
        ...
    &lt;/channel&gt;
&lt;/rss&gt;
</code></pre>
<h3 id="오류-코드">오류 코드 <a class="header-anchor" href="/docs/serviceapi/search/shopping/shopping.md#오류-코드" aria-hidden="true"><i class="xi-link"></i></a></h3>
<p>검색 API 쇼핑 검색의 주요 오류 코드는 다음과 같습니다.</p>
<table>
<thead>
<tr>
<th style="width: 12.5%">오류 코드</th>
<th style="width: 12.5%">HTTP 상태 코드</th>
<th style="width: 37.5%">오류 메시지</th>
<th style="width: 37.5%">설명</th>
</tr>
</thead>
<tbody>
<tr>
<td style="text-align:center">SE01</td>
<td style="text-align:center"></td>
<td>400Incorrect query request (잘못된 쿼리요청입니다.)</td>
<td>API 요청 URL의 프로토콜, 파라미터 등에 오류가 있는지 확인합니다.</td>
</tr>
<tr>
<td style="text-align:center">SE02</td>
<td style="text-align:center"></td>
<td>400Invalid display value (부적절한 display 값입니다.)</td>
<td><code>display</code> 파라미터의 값이 허용 범위의 값(1~100)인지 확인합니다.</td>
</tr>
<tr>
<td style="text-align:center">SE03</td>
<td style="text-align:center"></td>
<td>400Invalid start value (부적절한 start 값입니다.)</td>
<td><code>start</code> 파라미터의 값이 허용 범위의 값(1~1000)인지 확인합니다.</td>
</tr>
<tr>
<td style="text-align:center">SE04</td>
<td style="text-align:center"></td>
<td>400Invalid sort value (부적절한 sort 값입니다.)</td>
<td><code>sort</code> 파라미터의 값에 오타가 있는지 확인합니다.</td>
</tr>
<tr>
<td style="text-align:center">SE06</td>
<td style="text-align:center"></td>
<td>400Malformed encoding (잘못된 형식의 인코딩입니다.)</td>
<td>검색어를 UTF-8로 인코딩합니다.</td>
</tr>
<tr>
<td style="text-align:center">SE05</td>
<td style="text-align:center"></td>
<td>404Invalid search api (존재하지 않는 검색 api 입니다.)</td>
<td>API 요청 URL에 오타가 있는지 확인합니다.</td>
</tr>
<tr>
<td style="text-align:center">SE99</td>
<td style="text-align:center"></td>
<td>500System Error (시스템 에러)</td>
<td>서버 내부에 오류가 발생했습니다. &quot;<a href="https://developers.naver.com/forum">개발자 포럼</a>&quot;에 오류를 신고해 주십시오.</td>
</tr>
</tbody>
</table>
<blockquote>
<p><strong>403 오류</strong><br>
개발자 센터에 등록한 애플리케이션에서 검색 API를 사용하도록 설정하지 않았다면 'API 권한 없음'을 의미하는 403 오류가 발생할 수 있습니다. 403 오류가 발생했다면 네이버 개발자 센터의 <a href="https://developers.naver.com/apps/#/list"><strong>Application &gt; 내 애플리케이션</strong></a> 메뉴에서 오류가 발생한 애플리케이션의 <strong>API 설정</strong> 탭을 클릭한 다음 <strong>검색</strong><!-- -->이 선택돼 있는지 확인해 보십시오.</p>
</blockquote>
<blockquote>
<p><strong>참고</strong><br>
네이버 오픈API 공통 오류 코드는 &quot;<a href="https://developers.naver.com/docs/common/openapiguide/">API 공통 가이드</a>&quot;의 '<a href="https://developers.naver.com/docs/common/openapiguide/errorcode.md">오류 코드</a>'를 참고하십시오.</p>
</blockquote>
<h2 id="검색-api-쇼핑-검색-구현-예제">검색 API 쇼핑 검색 구현 예제 <a class="header-anchor" href="/docs/serviceapi/search/shopping/shopping.md#검색-api-쇼핑-검색-구현-예제" aria-hidden="true"><i class="xi-link"></i></a></h2>
<p>검색 API로 쇼핑 검색 결과를 조회하는 방법은 블로그 검색 결과를 조회하는 방법과 유사합니다. 쇼핑 검색 결과 조회를 구현하는 방법은 <a href="/docs/serviceapi/search/shopping/../blog/blog.md#%EA%B2%80%EC%83%89-api-%EB%B8%94%EB%A1%9C%EA%B7%B8-%EA%B2%80%EC%83%89-%EA%B5%AC%ED%98%84-%EC%98%88%EC%A0%9C">검색 API 블로그 검색 구현 예제</a>를 참고합니다.</p>
</div>
</div>
<div id="react-footer" style="display:none">
    


</div>
<script type="text/javascript" src="/inc/devcenter/dist/docs-serviceapi-search.4ba00308ddb6d2df4cb6.js" ></script>
<script type="text/javascript">
addEventListener('load', function (event) { PR.prettyPrint() }, false);
</script>

</body>
</html>


