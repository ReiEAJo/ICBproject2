Title: Cached Content

Description: Fetched from cache

Source: https://developers.naver.com/docs/serviceapi/search/blog/blog.md

---

<!doctype html>
<html lang=ko>
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width,initial-scale=1.0,maximum-scale=1.0,minimum-scale=1.0,user-scalable=no">
    <meta name="google-site-verification" content="f6fjgA4xpfKO1zPNp92lRU_PN8Z9oO4HE6QFptF3MCs" />
<title>검색 > 블로그 - Search API</title>
<meta name="description" content="검색 > 블로그 블로그 검색 개요 개요 사전 준비 사항 블로그 검색 API 레퍼런스 블로그 검색 결과 조회 오류 코드 검색 API 블로그 검색 구현 예제 Java PHP Node.js Python C# 블로그 검색 개요 개요 사전 준비 사항 개요 검색 API와 블"/>


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
<div id="ssrContent"><div class="h_page_area"><h1 id="검색-_-블로그">검색 &gt; 블로그 <a class="header-anchor" href="/docs/serviceapi/search/blog/blog.md#검색-_-블로그" aria-hidden="true"><i class="xi-link"></i></a></h1>
<div class="side_menu"></div></div><div class="table-of-contents">
<ul>
    <li><a href="/docs/serviceapi/search/blog/blog.md#&#xBE14;&#xB85C;&#xADF8;-&#xAC80;&#xC0C9;-&#xAC1C;&#xC694;">&#xBE14;&#xB85C;&#xADF8; &#xAC80;&#xC0C9; &#xAC1C;&#xC694;</a></li>
    <ul>
        <li><a href="/docs/serviceapi/search/blog/blog.md#&#xAC1C;&#xC694;">&#xAC1C;&#xC694;</a></li>
        <li><a href="/docs/serviceapi/search/blog/blog.md#&#xC0AC;&#xC804;-&#xC900;&#xBE44;-&#xC0AC;&#xD56D;">&#xC0AC;&#xC804; &#xC900;&#xBE44; &#xC0AC;&#xD56D;</a></li>
    </ul>
    <li><a href="/docs/serviceapi/search/blog/blog.md#&#xBE14;&#xB85C;&#xADF8;-&#xAC80;&#xC0C9;-api-&#xB808;&#xD37C;&#xB7F0;&#xC2A4;">&#xBE14;&#xB85C;&#xADF8; &#xAC80;&#xC0C9; API &#xB808;&#xD37C;&#xB7F0;&#xC2A4;</a></li>
    <ul>
        <li><a href="/docs/serviceapi/search/blog/blog.md#&#xBE14;&#xB85C;&#xADF8;-&#xAC80;&#xC0C9;-&#xACB0;&#xACFC;-&#xC870;&#xD68C;">&#xBE14;&#xB85C;&#xADF8; &#xAC80;&#xC0C9; &#xACB0;&#xACFC; &#xC870;&#xD68C;</a></li>
        <li><a href="/docs/serviceapi/search/blog/blog.md#&#xC624;&#xB958;-&#xCF54;&#xB4DC;">&#xC624;&#xB958; &#xCF54;&#xB4DC;</a></li>
    </ul>
    <li><a href="/docs/serviceapi/search/blog/blog.md#&#xAC80;&#xC0C9;-api-&#xBE14;&#xB85C;&#xADF8;-&#xAC80;&#xC0C9;-&#xAD6C;&#xD604;-&#xC608;&#xC81C;">&#xAC80;&#xC0C9; API &#xBE14;&#xB85C;&#xADF8; &#xAC80;&#xC0C9; &#xAD6C;&#xD604; &#xC608;&#xC81C;</a></li>
    <ul>
        <li><a href="/docs/serviceapi/search/blog/blog.md#java">Java</a></li>
        <li><a href="/docs/serviceapi/search/blog/blog.md#php">PHP</a></li>
        <li><a href="/docs/serviceapi/search/blog/blog.md#node-js">Node.js</a></li>
        <li><a href="/docs/serviceapi/search/blog/blog.md#python">Python</a></li>
        <li><a href="/docs/serviceapi/search/blog/blog.md#c">C#</a></li>
    </ul>
</ul>
</div>
<h2 id="블로그-검색-개요">블로그 검색 개요 <a class="header-anchor" href="/docs/serviceapi/search/blog/blog.md#블로그-검색-개요" aria-hidden="true"><i class="xi-link"></i></a></h2>
<ul>
<li><a href="/docs/serviceapi/search/blog/blog.md#%EA%B0%9C%EC%9A%94">개요</a></li>
<li><a href="/docs/serviceapi/search/blog/blog.md#%EC%82%AC%EC%A0%84-%EC%A4%80%EB%B9%84-%EC%82%AC%ED%95%AD">사전 준비 사항</a></li>
</ul>
<h3 id="개요">개요 <a class="header-anchor" href="/docs/serviceapi/search/blog/blog.md#개요" aria-hidden="true"><i class="xi-link"></i></a></h3>
<h4 id="검색-api와-블로그-검색-개요">검색 API와 블로그 검색 개요 <a class="header-anchor" href="/docs/serviceapi/search/blog/blog.md#검색-api와-블로그-검색-개요" aria-hidden="true"><i class="xi-link"></i></a></h4>
<p>검색 API는 네이버 검색 결과를 뉴스, 백과사전, 블로그, 쇼핑, 웹 문서, 전문정보, 지식iN, 책, 카페글 등 분야별로 볼 수 있는 API입니다. 그 외에 지역 검색 결과와 성인 검색어 판별 기능, 오타 변환 기능을 제공합니다.</p>
<p>블로그 검색은 검색 API를 사용해 네이버 검색의 블로그 검색 결과를 반환하는 RESTful API입니다. 블로그 검색 결과를 XML 형식 또는 JSON 형식으로 반환합니다. API를 호출할 때는 검색어와 검색 조건을 쿼리 스트링(Query String) 형식의 데이터로 전달합니다.</p>
<p>블로그 검색은 검색 API를 사용하며, 검색 API의 하루 호출 한도는 25,000회입니다.</p>
<h4 id="검색-api-특징">검색 API 특징 <a class="header-anchor" href="/docs/serviceapi/search/blog/blog.md#검색-api-특징" aria-hidden="true"><i class="xi-link"></i></a></h4>
<p>검색 API는 비로그인 방식 오픈 API입니다.</p>
<p>비로그인 방식 오픈 API는 네이버 오픈API를 호출할 때 HTTP 요청 헤더에 클라이언트 아이디와 클라이언트 시크릿 값만 전송해 사용할 수 있는 오픈 API입니다. 클라이언트 아이디와 클라이언트 시크릿은 네이버 오픈API에서 인증된 사용자인지 확인하는 수단입니다. <a href="https://developers.naver.com/">네이버 개발자 센터</a>에서 애플리케이션을 등록하면 클라이언트 아이디와 클라이언트 시크릿이 발급됩니다.</p>
<blockquote>
<p><strong>참고</strong><br>
네이버 오픈API의 종류와 클라이언트 아이디, 클라이언트 시크릿에 관한 자세한 내용은 &quot;<a href="https://developers.naver.com/docs/common/openapiguide/">API 공통 가이드</a>&quot;를 참고하십시오.</p>
</blockquote>
<h3 id="사전-준비-사항">사전 준비 사항 <a class="header-anchor" href="/docs/serviceapi/search/blog/blog.md#사전-준비-사항" aria-hidden="true"><i class="xi-link"></i></a></h3>
<p>검색 API를 사용해 블로그 검색을 실행하려면 먼저 <a href="https://developers.naver.com/">네이버 개발자 센터</a>에서 애플리케이션을 등록하고 클라이언트 아이디와 클라이언트 시크릿을 발급받아야 합니다.</p>
<p>클라이언트 아이디와 클라이언트 시크릿은 인증된 사용자인지를 확인하는 수단이며, 애플리케이션이 등록되면 발급됩니다. 클라이언트 아이디와 클라이언트 시크릿을 네이버 오픈API를 호출할 때 HTTP 헤더에 포함해서 전송해야 API를 호출할 수 있습니다. API 사용량은 클라이언트 아이디별로 합산됩니다.</p>
<p>블로그 검색을 실행하기 위해 발급받은 클라이언트 아이디와 클라이언트 시크릿은 검색 API의 다른 작업을 실행할 때에도 사용할 수 있습니다.</p>
<blockquote>
<p><strong>주의</strong><br>
네이버에 로그인한 사용자 계정으로 애플리케이션이 등록됩니다. 애플리케이션을 등록한 네이버 아이디는 '관리자' 권한을 가지게 되므로 네이버 계정의 보안에 각별히 주의해야 합니다.<br>
회사나 단체에서 애플리케이션을 등록할 때는 추후 키 관리 등이 용이하도록 네이버 단체 회원으로 로그인해 이용할 것을 권장합니다.</p>
<ul>
<li><a href="https://nid.naver.com/group/commonAction.nhn?m=viewTerms">네이버 단체 회원 가입하기</a></li>
</ul>
</blockquote>
<h4 id="애플리케이션-등록">애플리케이션 등록 <a class="header-anchor" href="/docs/serviceapi/search/blog/blog.md#애플리케이션-등록" aria-hidden="true"><i class="xi-link"></i></a></h4>
<p>네이버 개발자 센터에서 애플리케이션을 등록하는 방법은 다음과 같습니다.</p>
<ol>
<li>네이버 개발자 센터의 메뉴에서 <a href="https://developers.naver.com/apps/#/register"><strong>Application &gt; 애플리케이션 등록</strong></a>을 선택합니다.</li>
<li><strong>이용약관 동의</strong> 단계에서 <strong>이용약관에 동의합니다.</strong><!-- -->를 선택한 다음 <strong>확인</strong>을 클릭합니다.</li>
<li><strong>계정 정보 등록</strong> 단계에서 휴대폰 인증을 완료하고 회사 이름을 입력한 다음 <strong>확인</strong>을 클릭합니다. 휴대폰 인증은 담당자 연락처 확인을 위해 필요한 과정이며, 애플리케이션을 처음 등록할 때 한 번만 인증받으면 됩니다.</li>
<li><strong>애플리케이션 등록 (API이용신청)</strong> 페이지에서 <a href="/docs/serviceapi/search/blog/blog.md#%EC%95%A0%ED%94%8C%EB%A6%AC%EC%BC%80%EC%9D%B4%EC%85%98-%EB%93%B1%EB%A1%9D-%EC%84%B8%EB%B6%80-%EC%A0%95%EB%B3%B4">애플리케이션 등록 세부 정보</a>를 입력한 다음 <strong>등록하기</strong><!-- -->를 클릭합니다.</li>
</ol>
<h4 id="애플리케이션-등록-세부-정보">애플리케이션 등록 세부 정보 <a class="header-anchor" href="/docs/serviceapi/search/blog/blog.md#애플리케이션-등록-세부-정보" aria-hidden="true"><i class="xi-link"></i></a></h4>
<p><strong>애플리케이션 등록 (API이용신청)</strong> 페이지에서 애플리케이션 세부 정보를 입력하는 방법은 다음과 같습니다.</p>
<ol>
<li>등록하려는 애플리케이션의 이름을 <strong>애플리케이션 이름</strong>에 입력합니다. 최대 40자까지 입력할 수 있습니다.</li>
<li><strong>사용 API</strong>에서 <strong>검색</strong><!-- -->을 선택해 추가합니다.</li>
<li><a href="https://developers.naver.com/docs/common/openapiguide/appregister.md#%EB%B9%84%EB%A1%9C%EA%B7%B8%EC%9D%B8-%EC%98%A4%ED%94%88-api-%EC%84%9C%EB%B9%84%EC%8A%A4-%ED%99%98%EA%B2%BD"><strong>비로그인 오픈 API 서비스 환경</strong></a>에서 애플리케이션을 서비스할 환경을 추가하고 필요한 상세 정보를 입력합니다.</li>
</ol>
<p><img src="/proxyapi/rawgit/naver/naver-openapi-guide/master/ko/service-apis/search/blog/images/search-blog-01.png" alt=""></p>
<h4 id="애플리케이션-등록-확인">애플리케이션 등록 확인 <a class="header-anchor" href="/docs/serviceapi/search/blog/blog.md#애플리케이션-등록-확인" aria-hidden="true"><i class="xi-link"></i></a></h4>
<p>애플리케이션이 정상적으로 등록되면 네이버 개발자 센터의 <strong><a href="https://developers.naver.com/apps/#/list">Application &gt; 내 애플리케이션</a></strong> 메뉴의 아래에 등록한 애플리케이션 이름으로 하위 메뉴가 생깁니다.</p>
<p>애플리케이션 이름을 클릭하면 <strong>개요</strong> 탭에서 애플리케이션에 부여된 클라이언트 아이디와 클라이언트 시크릿을 확인할 수 있습니다.</p>
<p><img src="/proxyapi/rawgit/naver/naver-openapi-guide/master/ko/service-apis/search/blog/images/search-blog-02.png" alt=""></p>
<h2 id="블로그-검색-api-레퍼런스">블로그 검색 API 레퍼런스 <a class="header-anchor" href="/docs/serviceapi/search/blog/blog.md#블로그-검색-api-레퍼런스" aria-hidden="true"><i class="xi-link"></i></a></h2>
<ul>
<li><a href="/docs/serviceapi/search/blog/blog.md#%EB%B8%94%EB%A1%9C%EA%B7%B8-%EA%B2%80%EC%83%89-%EA%B2%B0%EA%B3%BC-%EC%A1%B0%ED%9A%8C">블로그 검색 결과 조회</a></li>
</ul>
<h3 id="블로그-검색-결과-조회">블로그 검색 결과 조회 <a class="header-anchor" href="/docs/serviceapi/search/blog/blog.md#블로그-검색-결과-조회" aria-hidden="true"><i class="xi-link"></i></a></h3>
<h4 id="설명">설명 <a class="header-anchor" href="/docs/serviceapi/search/blog/blog.md#설명" aria-hidden="true"><i class="xi-link"></i></a></h4>
<p>네이버 검색의 블로그 검색 결과를 XML 형식 또는 JSON 형식으로 반환합니다.</p>
<h4 id="요청-url">요청 URL <a class="header-anchor" href="/docs/serviceapi/search/blog/blog.md#요청-url" aria-hidden="true"><i class="xi-link"></i></a></h4>
<table>
<thead>
<tr>
<th style="width: 75%">요청 URL</th>
<th style="width: 25%">결괏값 반환 형식</th>
</tr>
</thead>
<tbody>
<tr>
<td><code>https://openapi.naver.com/v1/search/blog.xml</code></td>
<td style="text-align:center">XML</td>
</tr>
<tr>
<td><code>https://openapi.naver.com/v1/search/blog.json</code></td>
<td style="text-align:center">JSON</td>
</tr>
</tbody>
</table>
<h4 id="프로토콜">프로토콜 <a class="header-anchor" href="/docs/serviceapi/search/blog/blog.md#프로토콜" aria-hidden="true"><i class="xi-link"></i></a></h4>
<p>HTTPS</p>
<h4 id="http-메서드">HTTP 메서드 <a class="header-anchor" href="/docs/serviceapi/search/blog/blog.md#http-메서드" aria-hidden="true"><i class="xi-link"></i></a></h4>
<p>GET</p>
<h4 id="파라미터">파라미터 <a class="header-anchor" href="/docs/serviceapi/search/blog/blog.md#파라미터" aria-hidden="true"><i class="xi-link"></i></a></h4>
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
<td>검색 결과 정렬 방법<br/>- <code>sim</code>: 정확도순으로 내림차순 정렬(기본값)<br/>- <code>date</code>: 날짜순으로 내림차순 정렬</td>
</tr>
</tbody>
</table>
<h4 id="참고-사항">참고 사항 <a class="header-anchor" href="/docs/serviceapi/search/blog/blog.md#참고-사항" aria-hidden="true"><i class="xi-link"></i></a></h4>
<p>API를 요청할 때 다음 예와 같이 HTTP 요청 헤더에 <a href="https://developers.naver.com/docs/common/openapiguide/appregister.md#%ED%81%B4%EB%9D%BC%EC%9D%B4%EC%96%B8%ED%8A%B8-%EC%95%84%EC%9D%B4%EB%94%94%EC%99%80-%ED%81%B4%EB%9D%BC%EC%9D%B4%EC%96%B8%ED%8A%B8-%EC%8B%9C%ED%81%AC%EB%A6%BF-%ED%99%95%EC%9D%B8">클라이언트 아이디와 클라이언트 시크릿</a>을 추가해야 합니다.</p>
<pre class="prettyprint"><code class="language-sh">&gt; GET /v1/search/blog.xml?query=%EB%A6%AC%EB%B7%B0&amp;display=10&amp;start=1&amp;sort=sim HTTP/1.1
&gt; Host: openapi.naver.com
&gt; User-Agent: curl/7.49.1
&gt; Accept: */*
&gt; X-Naver-Client-Id: {애플리케이션 등록 시 발급받은 클라이언트 아이디 값}
&gt; X-Naver-Client-Secret: {애플리케이션 등록 시 발급받은 클라이언트 시크릿 값}
&gt;
</code></pre>
<h4 id="요청-예">요청 예 <a class="header-anchor" href="/docs/serviceapi/search/blog/blog.md#요청-예" aria-hidden="true"><i class="xi-link"></i></a></h4>
<pre class="prettyprint"><code class="language-sh">curl  &quot;https://openapi.naver.com/v1/search/blog.xml?query=%EB%A6%AC%EB%B7%B0&amp;display=10&amp;start=1&amp;sort=sim&quot; \
    -H &quot;X-Naver-Client-Id: {애플리케이션 등록 시 발급받은 클라이언트 아이디 값}&quot; \
    -H &quot;X-Naver-Client-Secret: {애플리케이션 등록 시 발급받은 클라이언트 시크릿 값}&quot; -v
</code></pre>
<h4 id="응답">응답 <a class="header-anchor" href="/docs/serviceapi/search/blog/blog.md#응답" aria-hidden="true"><i class="xi-link"></i></a></h4>
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
<td>블로그 포스트의 제목. 제목에서 검색어와 일치하는 부분은 <code>&lt;b&gt;</code> 태그로 감싸져 있습니다.</td>
</tr>
<tr>
<td>rss/channel/item/link</td>
<td style="text-align:center">String</td>
<td>블로그 포스트의 URL</td>
</tr>
<tr>
<td>rss/channel/item/description</td>
<td style="text-align:center">String</td>
<td>블로그 포스트의 내용을 요약한 패시지 정보. 패시지 정보에서 검색어와 일치하는 부분은 <code>&lt;b&gt;</code> 태그로 감싸져 있습니다.</td>
</tr>
<tr>
<td>rss/channel/item/bloggername</td>
<td style="text-align:center">String</td>
<td>블로그 포스트가 있는 블로그의 이름</td>
</tr>
<tr>
<td>rss/channel/item/bloggerlink</td>
<td style="text-align:center">String</td>
<td>블로그 포스트가 있는 블로그의 주소</td>
</tr>
<tr>
<td>rss/channel/item/postdate</td>
<td style="text-align:center">dateTime</td>
<td>블로그 포스트가 작성된 날짜</td>
</tr>
</tbody>
</table>
<h4 id="응답-예">응답 예 <a class="header-anchor" href="/docs/serviceapi/search/blog/blog.md#응답-예" aria-hidden="true"><i class="xi-link"></i></a></h4>
<pre class="prettyprint"><code class="language-xml">&lt; HTTP/1.1 200 OK
&lt; Server: nginx
&lt; Date: Mon, 26 Sep 2016 01:39:37 GMT
&lt; Content-Type: text/xml;charset=utf-8
&lt; Transfer-Encoding: chunked
&lt; Connection: keep-alive
&lt; Keep-Alive: timeout=5
&lt; Vary: Accept-Encoding
&lt; X-Powered-By: Naver
&lt; Cache-Control: no-cache, no-store, must-revalidate
&lt; Pragma: no-cache
&lt;
&lt;?xml version=&quot;1.0&quot; encoding=&quot;UTF-8&quot;?&gt;
&lt;rss version=&quot;2.0&quot;&gt;
    &lt;channel&gt;
        &lt;title&gt;Naver Open API - blog ::&#39;리뷰&#39;&lt;/title&gt;
        &lt;link&gt;http://search.naver.com&lt;/link&gt;
        &lt;description&gt;Naver Search Result&lt;/description&gt;
        &lt;lastBuildDate&gt;Mon, 26 Sep 2016 10:39:37 +0900&lt;/lastBuildDate&gt;
        &lt;total&gt;8714891&lt;/total&gt;
        &lt;start&gt;1&lt;/start&gt;&lt;display&gt;10&lt;/display&gt;
        &lt;item&gt;
            &lt;title&gt;명예훼손 없이 &lt;b&gt;리뷰&lt;/b&gt;쓰기&lt;/title&gt;
            &lt;link&gt;http://openapi.naver.com/l?AAABWLyw6CMBREv+ayNJe2UrrogvJwg8aYKGvACiSUalNR/t6azGLO5Mzrrd0moVSQJZDl/6I4KIxGpx9y9P4JNANShXSzHXZLu2q3660Jw2bt0k1+aF1rgFYXfZ+c7j3QorYDkCT4JxuIEEyRUYGcxpGXMeMs3VPBOUEWGXntynUW03k7ohBYfG+mOdRqbPL6E84/apnqgaEAAAA=&lt;/link&gt;
            &lt;description&gt;명예훼손 없이 &lt;b&gt;리뷰&lt;/b&gt;쓰기 우리 블로그하시는 분들께는 꽤 중요한 내용일 수도 있습니다 그것도 주로 &lt;b&gt;리뷰&lt;/b&gt; 위주로 블로그를 진행하신 분이라면 더욱 더 말이죠
                오늘 포스팅은, 어떻게 하면 객관적이고 좋은 &lt;b&gt;리뷰&lt;/b&gt;를... &lt;/description&gt;
            &lt;bloggername&gt;건짱의 Best Drawing World2&lt;/bloggername&gt;
            &lt;bloggerlink&gt;http://blog.naver.com/yoonbitgaram&lt;/bloggerlink&gt;
            &lt;postdate&gt;20161208&lt;/postdate&gt;
        &lt;/item&gt;
        ...
    &lt;/channel&gt;
&lt;/rss&gt;
</code></pre>
<h3 id="오류-코드">오류 코드 <a class="header-anchor" href="/docs/serviceapi/search/blog/blog.md#오류-코드" aria-hidden="true"><i class="xi-link"></i></a></h3>
<p>검색 API 블로그 검색의 주요 오류 코드는 다음과 같습니다.</p>
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
<td style="text-align:center">400</td>
<td>Incorrect query request (잘못된 쿼리요청입니다.)</td>
<td>API 요청 URL의 프로토콜, 파라미터 등에 오류가 있는지 확인합니다.</td>
</tr>
<tr>
<td style="text-align:center">SE02</td>
<td style="text-align:center">400</td>
<td>Invalid display value (부적절한 display 값입니다.)</td>
<td><code>display</code> 파라미터의 값이 허용 범위의 값(1~100)인지 확인합니다.</td>
</tr>
<tr>
<td style="text-align:center">SE03</td>
<td style="text-align:center">400</td>
<td>Invalid start value (부적절한 start 값입니다.)</td>
<td><code>start</code> 파라미터의 값이 허용 범위의 값(1~1000)인지 확인합니다.</td>
</tr>
<tr>
<td style="text-align:center">SE04</td>
<td style="text-align:center">400</td>
<td>Invalid sort value (부적절한 sort 값입니다.)</td>
<td><code>sort</code> 파라미터의 값에 오타가 있는지 확인합니다.</td>
</tr>
<tr>
<td style="text-align:center">SE06</td>
<td style="text-align:center">400</td>
<td>Malformed encoding (잘못된 형식의 인코딩입니다.)</td>
<td>검색어를 UTF-8로 인코딩합니다.</td>
</tr>
<tr>
<td style="text-align:center">SE05</td>
<td style="text-align:center">404</td>
<td>Invalid search api (존재하지 않는 검색 api 입니다.)</td>
<td>API 요청 URL에 오타가 있는지 확인합니다.</td>
</tr>
<tr>
<td style="text-align:center">SE99</td>
<td style="text-align:center">500</td>
<td>System Error (시스템 에러)</td>
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
<h2 id="검색-api-블로그-검색-구현-예제">검색 API 블로그 검색 구현 예제 <a class="header-anchor" href="/docs/serviceapi/search/blog/blog.md#검색-api-블로그-검색-구현-예제" aria-hidden="true"><i class="xi-link"></i></a></h2>
<p>다음은 검색 API로 블로그 검색 결과를 조회하는 구현 예제입니다. 검색 API의 다른 작업을 구현하는 방법도 이 구현 예제와 유사하기 때문에 이 구현 예제를 참고하면 검색 API를 구현할 수 있습니다.</p>
<ul>
<li><a href="/docs/serviceapi/search/blog/blog.md#java">Java</a></li>
<li><a href="/docs/serviceapi/search/blog/blog.md#php">PHP</a></li>
<li><a href="/docs/serviceapi/search/blog/blog.md#node-js">Node.js</a></li>
<li><a href="/docs/serviceapi/search/blog/blog.md#python">Python</a></li>
<li><a href="/docs/serviceapi/search/blog/blog.md#c">C#</a></li>
</ul>
<blockquote>
<p><strong>참고</strong></p>
<ul>
<li>샘플 코드에서 <code>YOUR_CLIENT_ID</code> 또는 <code>YOUR-CLIENT-ID</code>에는 애플리케이션을 등록하고 발급받은 클라이언트 아이디 값을 입력합니다.</li>
<li>샘플 코드에서 <code>YOUR_CLIENT_SECRET</code> 또는 <code>YOUR-CLIENT-SECRET</code>에는 애플리케이션을 등록하고 발급받은 클라이언트 시크릿 값을 입력합니다.</li>
</ul>
</blockquote>
<h3 id="java">Java <a class="header-anchor" href="/docs/serviceapi/search/blog/blog.md#java" aria-hidden="true"><i class="xi-link"></i></a></h3>
<pre class="prettyprint"><code class="language-java">// 네이버 검색 API 예제 - 블로그 검색
import java.io.*;
import java.net.HttpURLConnection;
import java.net.MalformedURLException;
import java.net.URL;
import java.net.URLEncoder;
import java.util.HashMap;
import java.util.Map;


public class ApiExamSearchBlog {


    public static void main(String[] args) {
        String clientId = &quot;YOUR_CLIENT_ID&quot;; //애플리케이션 클라이언트 아이디
        String clientSecret = &quot;YOUR_CLIENT_SECRET&quot;; //애플리케이션 클라이언트 시크릿


        String text = null;
        try {
            text = URLEncoder.encode(&quot;그린팩토리&quot;, &quot;UTF-8&quot;);
        } catch (UnsupportedEncodingException e) {
            throw new RuntimeException(&quot;검색어 인코딩 실패&quot;,e);
        }


        String apiURL = &quot;https://openapi.naver.com/v1/search/blog?query=&quot; + text;    // JSON 결과
        //String apiURL = &quot;https://openapi.naver.com/v1/search/blog.xml?query=&quot;+ text; // XML 결과


        Map&lt;String, String&gt; requestHeaders = new HashMap&lt;&gt;();
        requestHeaders.put(&quot;X-Naver-Client-Id&quot;, clientId);
        requestHeaders.put(&quot;X-Naver-Client-Secret&quot;, clientSecret);
        String responseBody = get(apiURL,requestHeaders);


        System.out.println(responseBody);
    }


    private static String get(String apiUrl, Map&lt;String, String&gt; requestHeaders){
        HttpURLConnection con = connect(apiUrl);
        try {
            con.setRequestMethod(&quot;GET&quot;);
            for(Map.Entry&lt;String, String&gt; header :requestHeaders.entrySet()) {
                con.setRequestProperty(header.getKey(), header.getValue());
            }


            int responseCode = con.getResponseCode();
            if (responseCode == HttpURLConnection.HTTP_OK) { // 정상 호출
                return readBody(con.getInputStream());
            } else { // 오류 발생
                return readBody(con.getErrorStream());
            }
        } catch (IOException e) {
            throw new RuntimeException(&quot;API 요청과 응답 실패&quot;, e);
        } finally {
            con.disconnect();
        }
    }


    private static HttpURLConnection connect(String apiUrl){
        try {
            URL url = new URL(apiUrl);
            return (HttpURLConnection)url.openConnection();
        } catch (MalformedURLException e) {
            throw new RuntimeException(&quot;API URL이 잘못되었습니다. : &quot; + apiUrl, e);
        } catch (IOException e) {
            throw new RuntimeException(&quot;연결이 실패했습니다. : &quot; + apiUrl, e);
        }
    }


    private static String readBody(InputStream body){
        InputStreamReader streamReader = new InputStreamReader(body);


        try (BufferedReader lineReader = new BufferedReader(streamReader)) {
            StringBuilder responseBody = new StringBuilder();


            String line;
            while ((line = lineReader.readLine()) != null) {
                responseBody.append(line);
            }


            return responseBody.toString();
        } catch (IOException e) {
            throw new RuntimeException(&quot;API 응답을 읽는 데 실패했습니다.&quot;, e);
        }
    }
}
</code></pre>
<h3 id="php">PHP <a class="header-anchor" href="/docs/serviceapi/search/blog/blog.md#php" aria-hidden="true"><i class="xi-link"></i></a></h3>
<pre class="prettyprint"><code class="language-php">// SSL 사용에 문제가 있으면 curl_setopt($ch, CURLOPT_SSL_VERIFYPEER, false); 를 추가해 보시기 바랍니다.
// 네이버 검색 API 예제 - 블로그 검색
&lt;?php
  $client_id = &quot;YOUR_CLIENT_ID&quot;;
  $client_secret = &quot;YOUR_CLIENT_SECRET&quot;;
  $encText = urlencode(&quot;네이버오픈API&quot;);
  $url = &quot;https://openapi.naver.com/v1/search/blog?query=&quot;.$encText; // json 결과
//  $url = &quot;https://openapi.naver.com/v1/search/blog.xml?query=&quot;.$encText; // xml 결과
  $is_post = false;
  $ch = curl_init();
  curl_setopt($ch, CURLOPT_URL, $url);
  curl_setopt($ch, CURLOPT_POST, $is_post);
  curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
  $headers = array();
  $headers[] = &quot;X-Naver-Client-Id: &quot;.$client_id;
  $headers[] = &quot;X-Naver-Client-Secret: &quot;.$client_secret;
  curl_setopt($ch, CURLOPT_HTTPHEADER, $headers);
  curl_setopt($ch, CURLOPT_SSL_VERIFYPEER, 0);
  $response = curl_exec ($ch);
  $status_code = curl_getinfo($ch, CURLINFO_HTTP_CODE);
  echo &quot;status_code:&quot;.$status_code.&quot;
&quot;;
  curl_close ($ch);
  if($status_code == 200) {
    echo $response;
  } else {
    echo &quot;Error 내용:&quot;.$response;
  }
?&gt;
</code></pre>
<h3 id="node-js">Node.js <a class="header-anchor" href="/docs/serviceapi/search/blog/blog.md#node-js" aria-hidden="true"><i class="xi-link"></i></a></h3>
<pre class="prettyprint"><code class="language-js">// 네이버 검색 API 예제 - 블로그 검색
var express = require(&#39;express&#39;);
var app = express();
var client_id = &#39;YOUR_CLIENT_ID&#39;;
var client_secret = &#39;YOUR_CLIENT_SECRET&#39;;
app.get(&#39;/search/blog&#39;, function (req, res) {
   var api_url = &#39;https://openapi.naver.com/v1/search/blog?query=&#39; + encodeURI(req.query.query); // JSON 결과
//   var api_url = &#39;https://openapi.naver.com/v1/search/blog.xml?query=&#39; + encodeURI(req.query.query); // XML 결과
   var request = require(&#39;request&#39;);
   var options = {
       url: api_url,
       headers: {&#39;X-Naver-Client-Id&#39;:client_id, &#39;X-Naver-Client-Secret&#39;: client_secret}
    };
   request.get(options, function (error, response, body) {
     if (!error &amp;&amp; response.statusCode == 200) {
       res.writeHead(200, {&#39;Content-Type&#39;: &#39;text/json;charset=utf-8&#39;});
       res.end(body);
     } else {
       res.status(response.statusCode).end();
       console.log(&#39;error = &#39; + response.statusCode);
     }
   });
 });
 app.listen(3000, function () {
   console.log(&#39;http://127.0.0.1:3000/search/blog?query=검색어 app listening on port 3000!&#39;);
 });
</code></pre>
<h3 id="python">Python <a class="header-anchor" href="/docs/serviceapi/search/blog/blog.md#python" aria-hidden="true"><i class="xi-link"></i></a></h3>
<pre class="prettyprint"><code class="language-python"># 네이버 검색 API 예제 - 블로그 검색
import os
import sys
import urllib.request
client_id = &quot;YOUR_CLIENT_ID&quot;
client_secret = &quot;YOUR_CLIENT_SECRET&quot;
encText = urllib.parse.quote(&quot;검색할 단어&quot;)
url = &quot;https://openapi.naver.com/v1/search/blog?query=&quot; + encText # JSON 결과
# url = &quot;https://openapi.naver.com/v1/search/blog.xml?query=&quot; + encText # XML 결과
request = urllib.request.Request(url)
request.add_header(&quot;X-Naver-Client-Id&quot;,client_id)
request.add_header(&quot;X-Naver-Client-Secret&quot;,client_secret)
response = urllib.request.urlopen(request)
rescode = response.getcode()
if(rescode==200):
    response_body = response.read()
    print(response_body.decode(&#39;utf-8&#39;))
else:
    print(&quot;Error Code:&quot; + rescode)
</code></pre>
<h3 id="c">C# <a class="header-anchor" href="/docs/serviceapi/search/blog/blog.md#c" aria-hidden="true"><i class="xi-link"></i></a></h3>
<pre class="prettyprint"><code class="language-csharp">using System;
using System.Net;
using System.Text;
using System.IO;


namespace NaverAPI_Guide
{
    public class APIExamSearchBlog
    {
        static void Main(string[] args)
        {
            string query = &quot;네이버 Open API&quot;; // 검색할 문자열
            string url = &quot;https://openapi.naver.com/v1/search/blog?query=&quot; + query; // JSON 결과
            // string url = &quot;https://openapi.naver.com/v1/search/blog.xml?query=&quot; + query;  // XML 결과
            HttpWebRequest request = (HttpWebRequest)WebRequest.Create(url);
            request.Headers.Add(&quot;X-Naver-Client-Id&quot;, &quot;YOUR-CLIENT-ID&quot;); // 클라이언트 아이디
            request.Headers.Add(&quot;X-Naver-Client-Secret&quot;, &quot;YOUR-CLIENT-SECRET&quot;);       // 클라이언트 시크릿
            HttpWebResponse response = (HttpWebResponse)request.GetResponse();
            string status = response.StatusCode.ToString();
            if(status == &quot;OK&quot;)
            {
                Stream stream = response.GetResponseStream();
                StreamReader reader = new StreamReader(stream, Encoding.UTF8);
                string text = reader.ReadToEnd();
                Console.WriteLine(text);
            }
            else
            {
                Console.WriteLine(&quot;Error 발생=&quot; + status);
            }
        }
    }
}
</code></pre>
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


