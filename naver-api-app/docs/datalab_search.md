Title: Cached Content

Description: Fetched from cache

Source: https://developers.naver.com/docs/serviceapi/datalab/search/search.md

---

<!doctype html>
<html lang=ko>
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width,initial-scale=1.0,maximum-scale=1.0,minimum-scale=1.0,user-scalable=no">
    <meta name="google-site-verification" content="f6fjgA4xpfKO1zPNp92lRU_PN8Z9oO4HE6QFptF3MCs" />
<title>통합 검색어 트렌드 - Datalab</title>
<meta name="description" content="통합 검색어 트렌드 통합 검색어 트렌드 개요 개요 사전 준비 사항 통합 검색어 트렌드 API 레퍼런스 네이버 통합 검색어 트렌드 조회 오류 코드 통합 검색어 트렌드 API 구현 예제 Java PHP Node.js Python C# 통합 검색어 트렌드 개요 개요 사"/>


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
<div id="ssrContent"><h1 id="통합-검색어-트렌드">통합 검색어 트렌드 <a class="header-anchor" href="/docs/serviceapi/datalab/search/search.md#통합-검색어-트렌드" aria-hidden="true"><i class="xi-link"></i></a></h1>
<div class="table-of-contents">
<ul>
<li><a href="/docs/serviceapi/datalab/search/search.md#&#xD1B5;&#xD569;-&#xAC80;&#xC0C9;&#xC5B4;-&#xD2B8;&#xB80C;&#xB4DC;-&#xAC1C;&#xC694;">&#xD1B5;&#xD569; &#xAC80;&#xC0C9;&#xC5B4; &#xD2B8;&#xB80C;&#xB4DC; &#xAC1C;&#xC694;</a></li>
    <ul>
        <li><a href="/docs/serviceapi/datalab/search/search.md#&#xAC1C;&#xC694;">&#xAC1C;&#xC694;</a></li>
        <li><a href="/docs/serviceapi/datalab/search/search.md#&#xC0AC;&#xC804;-&#xC900;&#xBE44;-&#xC0AC;&#xD56D;">&#xC0AC;&#xC804; &#xC900;&#xBE44; &#xC0AC;&#xD56D;</a></li>
    </ul>
<li><a href="/docs/serviceapi/datalab/search/search.md#&#xD1B5;&#xD569;-&#xAC80;&#xC0C9;&#xC5B4;-&#xD2B8;&#xB80C;&#xB4DC;-api-&#xB808;&#xD37C;&#xB7F0;&#xC2A4;">&#xD1B5;&#xD569; &#xAC80;&#xC0C9;&#xC5B4; &#xD2B8;&#xB80C;&#xB4DC; API &#xB808;&#xD37C;&#xB7F0;&#xC2A4;</a></li>
    <ul>
        <li><a href="/docs/serviceapi/datalab/search/search.md#&#xB124;&#xC774;&#xBC84;-&#xD1B5;&#xD569;-&#xAC80;&#xC0C9;&#xC5B4;-&#xD2B8;&#xB80C;&#xB4DC;-&#xC870;&#xD68C;">&#xB124;&#xC774;&#xBC84; &#xD1B5;&#xD569; &#xAC80;&#xC0C9;&#xC5B4; &#xD2B8;&#xB80C;&#xB4DC; &#xC870;&#xD68C;</a></li>
        <li><a href="/docs/serviceapi/datalab/search/search.md#&#xC624;&#xB958;-&#xCF54;&#xB4DC;">&#xC624;&#xB958; &#xCF54;&#xB4DC;</a></li>
    </ul>
<li><a href="/docs/serviceapi/datalab/search/search.md#&#xD1B5;&#xD569;-&#xAC80;&#xC0C9;&#xC5B4;-&#xD2B8;&#xB80C;&#xB4DC;-api-&#xAD6C;&#xD604;-&#xC608;&#xC81C;">&#xD1B5;&#xD569; &#xAC80;&#xC0C9;&#xC5B4; &#xD2B8;&#xB80C;&#xB4DC; API &#xAD6C;&#xD604; &#xC608;&#xC81C;</a></li>
    <ul>
        <li><a href="/docs/serviceapi/datalab/search/search.md#java">Java</a></li>
        <li><a href="/docs/serviceapi/datalab/search/search.md#php">PHP</a></li>
        <li><a href="/docs/serviceapi/datalab/search/search.md#node-js">Node.js</a></li>
        <li><a href="/docs/serviceapi/datalab/search/search.md#python">Python</a></li>
        <li><a href="/docs/serviceapi/datalab/search/search.md#c">C#</a></li>
    </ul>
</ul>
</div>
<h2 id="통합-검색어-트렌드-개요">통합 검색어 트렌드 개요 <a class="header-anchor" href="/docs/serviceapi/datalab/search/search.md#통합-검색어-트렌드-개요" aria-hidden="true"><i class="xi-link"></i></a></h2>
<ul>
<li><a href="/docs/serviceapi/datalab/search/search.md#%EA%B0%9C%EC%9A%94">개요</a></li>
<li><a href="/docs/serviceapi/datalab/search/search.md#%EC%82%AC%EC%A0%84-%EC%A4%80%EB%B9%84-%EC%82%AC%ED%95%AD">사전 준비 사항</a></li>
</ul>
<h3 id="개요">개요 <a class="header-anchor" href="/docs/serviceapi/datalab/search/search.md#개요" aria-hidden="true"><i class="xi-link"></i></a></h3>
<h4 id="통합-검색어-트렌드-api-개요">통합 검색어 트렌드 API 개요 <a class="header-anchor" href="/docs/serviceapi/datalab/search/search.md#통합-검색어-트렌드-api-개요" aria-hidden="true"><i class="xi-link"></i></a></h4>
<p>통합 검색어 트렌드 API는 <a href="http://datalab.naver.com/">네이버 데이터랩</a>의 <a href="http://datalab.naver.com/keyword/trendSearch.naver"><strong>검색어 트렌드</strong></a>를 API로 실행할 수 있게하는 RESTful API입니다. 주제어로 묶은 검색어들에 대한 네이버 통합검색에서의 검색 추이 데이터를 JSON 형식으로 반환합니다. API를 호출할 때는 주제어와 검색어, 검색 조건을 JSON 형식의 데이터로 전달합니다.</p>
<p>통합 검색어 트렌드 API의 하루 호출 한도는 1,000회입니다.</p>
<h4 id="통합-검색어-트렌드-api-특징">통합 검색어 트렌드 API 특징 <a class="header-anchor" href="/docs/serviceapi/datalab/search/search.md#통합-검색어-트렌드-api-특징" aria-hidden="true"><i class="xi-link"></i></a></h4>
<p>통합 검색어 트렌드 API는 비로그인 방식 오픈 API입니다.</p>
<p>비로그인 방식 오픈 API는 네이버 오픈API를 호출할 때 HTTP 요청 헤더에 클라이언트 아이디와 클라이언트 시크릿 값만 전송해 사용할 수 있는 오픈 API입니다. 클라이언트 아이디와 클라이언트 시크릿은 네이버 오픈API에서 인증된 사용자인지 확인하는 수단입니다. <a href="https://developers.naver.com/">네이버 개발자 센터</a>에서 애플리케이션을 등록하면 클라이언트 아이디와 클라이언트 시크릿이 발급됩니다.</p>
<blockquote>
<p><strong>참고</strong><br>
네이버 오픈API의 종류와 클라이언트 아이디, 클라이언트 시크릿에 관한 자세한 내용은 &quot;<a href="https://developers.naver.com/docs/common/openapiguide/">API 공통 가이드</a>&quot;를 참고하십시오.</p>
</blockquote>
<h3 id="사전-준비-사항">사전 준비 사항 <a class="header-anchor" href="/docs/serviceapi/datalab/search/search.md#사전-준비-사항" aria-hidden="true"><i class="xi-link"></i></a></h3>
<p>통합 검색어 트렌드 API를 사용하려면 먼저 <a href="https://developers.naver.com/">네이버 개발자 센터</a>에서 애플리케이션을 등록하고 클라이언트 아이디와 클라이언트 시크릿을 발급받아야 합니다.</p>
<p>클라이언트 아이디와 클라이언트 시크릿은 인증된 사용자인지를 확인하는 수단이며, 애플리케이션이 등록되면 발급됩니다. 클라이언트 아이디와 클라이언트 시크릿을 네이버 오픈API를 호출할 때 HTTP 헤더에 포함해서 전송해야 API를 호출할 수 있습니다. API 사용량은 클라이언트 아이디별로 합산됩니다.</p>
<blockquote>
<p><strong>주의</strong><br>
네이버에 로그인한 사용자 계정으로 애플리케이션이 등록됩니다. 애플리케이션을 등록한 네이버 아이디는 '관리자' 권한을 가지게 되므로 네이버 계정의 보안에 각별히 주의해야 합니다.<br>
회사나 단체에서 애플리케이션을 등록할 때는 추후 키 관리 등이 용이하도록 네이버 단체 회원으로 로그인해 이용할 것을 권장합니다.</p>
<ul>
<li><a href="https://nid.naver.com/group/commonAction.nhn?m=viewTerms">네이버 단체 회원 가입하기</a></li>
</ul>
</blockquote>
<h4 id="애플리케이션-등록">애플리케이션 등록 <a class="header-anchor" href="/docs/serviceapi/datalab/search/search.md#애플리케이션-등록" aria-hidden="true"><i class="xi-link"></i></a></h4>
<p>네이버 개발자 센터에서 애플리케이션을 등록하는 방법은 다음과 같습니다.</p>
<ol>
<li>네이버 개발자 센터의 메뉴에서 <a href="https://developers.naver.com/apps/#/wizard/register"><strong>Application &gt; 애플리케이션 등록</strong></a>을 선택합니다.</li>
<li><strong>이용약관 동의</strong> 단계에서 <strong>이용약관에 동의합니다.</strong><!-- -->를 선택한 다음 <strong>확인</strong>을 클릭합니다.</li>
<li><strong>계정 정보 등록</strong> 단계에서 휴대폰 인증을 완료하고 회사 이름을 입력한 다음 <strong>확인</strong>을 클릭합니다. 휴대폰 인증은 담당자 연락처 확인을 위해 필요한 과정이며, 애플리케이션을 처음 등록할 때 한 번만 인증받으면 됩니다.</li>
<li><strong>애플리케이션 등록 (API이용신청)</strong> 페이지에서 <a href="/docs/serviceapi/datalab/search/search.md#%EC%95%A0%ED%94%8C%EB%A6%AC%EC%BC%80%EC%9D%B4%EC%85%98-%EB%93%B1%EB%A1%9D-%EC%84%B8%EB%B6%80-%EC%A0%95%EB%B3%B4">애플리케이션 등록 세부 정보</a>를 입력한 다음 <strong>등록하기</strong><!-- -->를 클릭합니다.</li>
</ol>
<h4 id="애플리케이션-등록-세부-정보">애플리케이션 등록 세부 정보 <a class="header-anchor" href="/docs/serviceapi/datalab/search/search.md#애플리케이션-등록-세부-정보" aria-hidden="true"><i class="xi-link"></i></a></h4>
<p><strong>애플리케이션 등록 (API이용신청)</strong> 페이지에서 애플리케이션 세부 정보를 입력하는 방법은 다음과 같습니다.</p>
<ol>
<li>등록하려는 애플리케이션의 이름을 <strong>애플리케이션 이름</strong><!-- -->에 입력합니다. 최대 40자까지 입력할 수 있습니다.</li>
<li><strong>사용 API</strong>에서 <strong>데이터랩 (검색어트렌드)</strong><!-- -->를 선택해 추가합니다.</li>
<li><a href="https://developers.naver.com/docs/common/openapiguide/appregister.md#%EB%B9%84%EB%A1%9C%EA%B7%B8%EC%9D%B8-%EC%98%A4%ED%94%88-api-%EC%84%9C%EB%B9%84%EC%8A%A4-%ED%99%98%EA%B2%BD"><strong>비로그인 오픈 API 서비스 환경</strong></a>에서 애플리케이션을 서비스할 환경을 추가하고 필요한 상세 정보를 입력합니다.</li>
</ol>
<p><img src="/proxyapi/rawgit/naver/naver-openapi-guide/master/ko/service-apis/datalab/search/images/datalab-01.png" alt=""></p>
<h4 id="애플리케이션-등록-확인">애플리케이션 등록 확인 <a class="header-anchor" href="/docs/serviceapi/datalab/search/search.md#애플리케이션-등록-확인" aria-hidden="true"><i class="xi-link"></i></a></h4>
<p>애플리케이션이 정상적으로 등록되면 네이버 개발자 센터의 <strong><a href="https://developers.naver.com/apps/#/list">Application &gt; 내 애플리케이션</a></strong> 메뉴의 아래에 등록한 애플리케이션 이름으로 하위 메뉴가 생깁니다.</p>
<p>애플리케이션 이름을 클릭하면 <strong>개요</strong> 탭에서 애플리케이션에 부여된 클라이언트 아이디와 클라이언트 시크릿을 확인할 수 있습니다.</p>
<p><img src="/proxyapi/rawgit/naver/naver-openapi-guide/master/ko/service-apis/datalab/search/images/datalab-02.png" alt=""></p>
<h2 id="통합-검색어-트렌드-api-레퍼런스">통합 검색어 트렌드 API 레퍼런스 <a class="header-anchor" href="/docs/serviceapi/datalab/search/search.md#통합-검색어-트렌드-api-레퍼런스" aria-hidden="true"><i class="xi-link"></i></a></h2>
<ul>
<li><a href="/docs/serviceapi/datalab/search/search.md#%EB%84%A4%EC%9D%B4%EB%B2%84-%ED%86%B5%ED%95%A9-%EA%B2%80%EC%83%89%EC%96%B4-%ED%8A%B8%EB%A0%8C%EB%93%9C-%EC%A1%B0%ED%9A%8C">네이버 통합 검색어 트렌드 조회</a></li>
<li><a href="/docs/serviceapi/datalab/search/search.md#%EC%98%A4%EB%A5%98-%EC%BD%94%EB%93%9C">오류 코드</a></li>
</ul>
<h3 id="네이버-통합-검색어-트렌드-조회">네이버 통합 검색어 트렌드 조회 <a class="header-anchor" href="/docs/serviceapi/datalab/search/search.md#네이버-통합-검색어-트렌드-조회" aria-hidden="true"><i class="xi-link"></i></a></h3>
<h4 id="설명">설명 <a class="header-anchor" href="/docs/serviceapi/datalab/search/search.md#설명" aria-hidden="true"><i class="xi-link"></i></a></h4>
<p>그룹으로 묶은 검색어에 대한 네이버 통합검색에서 검색 추이 데이터를 JSON 형식으로 반환합니다.</p>
<h4 id="요청-url">요청 URL <a class="header-anchor" href="/docs/serviceapi/datalab/search/search.md#요청-url" aria-hidden="true"><i class="xi-link"></i></a></h4>
<pre class="prettyprint"><code class="language-sh">https://openapi.naver.com/v1/datalab/search
</code></pre>
<h4 id="프로토콜">프로토콜 <a class="header-anchor" href="/docs/serviceapi/datalab/search/search.md#프로토콜" aria-hidden="true"><i class="xi-link"></i></a></h4>
<p>HTTPS</p>
<h4 id="http-메서드">HTTP 메서드 <a class="header-anchor" href="/docs/serviceapi/datalab/search/search.md#http-메서드" aria-hidden="true"><i class="xi-link"></i></a></h4>
<p>POST</p>
<h4 id="파라미터">파라미터 <a class="header-anchor" href="/docs/serviceapi/datalab/search/search.md#파라미터" aria-hidden="true"><i class="xi-link"></i></a></h4>
<p>파라미터를 JSON 형식으로 전달합니다.</p>
<table>
<thead>
<tr>
<th style="width: 27.27272727272727%">파라미터</th>
<th style="width: 27.27272727272727%">타입</th>
<th style="width: 9.090909090909092%">필수 여부</th>
<th style="width: 36.36363636363637%">설명</th>
</tr>
</thead>
<tbody>
<tr>
<td>startDate</td>
<td>string</td>
<td style="text-align:center">Y</td>
<td>조회 기간 시작 날짜(<code>yyyy-mm-dd</code> 형식). 2016년 1월 1일부터 조회할 수 있습니다.</td>
</tr>
<tr>
<td>endDate</td>
<td>string</td>
<td style="text-align:center">Y</td>
<td>조회 기간 종료 날짜(<code>yyyy-mm-dd</code> 형식)</td>
</tr>
<tr>
<td>timeUnit</td>
<td>string</td>
<td style="text-align:center">Y</td>
<td>구간 단위<br/>- <code>date</code>: 일간<br/>- <code>week</code>: 주간<br/>- <code>month</code>: 월간</td>
</tr>
<tr>
<td>keywordGroups</td>
<td>array(JSON)</td>
<td style="text-align:center">Y</td>
<td>주제어와 주제어에 해당하는 검색어 묶음 쌍의 배열. 최대 5개의 쌍을 배열로 설정할 수 있습니다.</td>
</tr>
<tr>
<td>keywordGroups.groupName</td>
<td>string</td>
<td style="text-align:center">Y</td>
<td>주제어. 검색어 묶음을 대표하는 이름입니다.</td>
</tr>
<tr>
<td>keywordGroups.keywords</td>
<td>array(string)</td>
<td style="text-align:center">Y</td>
<td>주제어에 해당하는 검색어. 최대 20개의 검색어를 배열로 설정할 수 있습니다.</td>
</tr>
<tr>
<td>device</td>
<td>string</td>
<td style="text-align:center">N</td>
<td>범위. 검색 환경에 따른 조건입니다.<br/>- 설정 안 함: 모든 환경<br/>- <code>pc</code>: PC에서 검색 추이<br/>- <code>mo</code>: 모바일에서 검색 추이</td>
</tr>
<tr>
<td>gender</td>
<td>string</td>
<td style="text-align:center">N</td>
<td>성별. 검색 사용자의 성별에 따른 조건입니다.<br/>- 설정 안 함: 모든 성별<br/>- <code>m</code>: 남성<br/>- <code>f</code>: 여성</td>
</tr>
<tr>
<td>ages</td>
<td>array(string)</td>
<td style="text-align:center">N</td>
<td>연령. 검색 사용자의 연령에 따른 조건입니다. <br>- 설정 안 함: 모든 연령<br>- <code>1</code>: 0∼12세<br>- <code>2</code>: 13∼18세<br>- <code>3</code>: 19∼24세<br>- <code>4</code>: 25∼29세<br>- <code>5</code>: 30∼34세<br>- <code>6</code>: 35∼39세<br>- <code>7</code>: 40∼44세<br>- <code>8</code>: 45∼49세<br>- <code>9</code>: 50∼54세<br>- <code>10</code>: 55∼59세<br>- <code>11</code>: 60세 이상</td>
</tr>
</tbody>
</table>
<h4 id="참고-사항">참고 사항 <a class="header-anchor" href="/docs/serviceapi/datalab/search/search.md#참고-사항" aria-hidden="true"><i class="xi-link"></i></a></h4>
<p>API를 요청할 때 다음 예와 같이 HTTP 요청 헤더에 <a href="https://developers.naver.com/docs/common/openapiguide/appregister.md#%ED%81%B4%EB%9D%BC%EC%9D%B4%EC%96%B8%ED%8A%B8-%EC%95%84%EC%9D%B4%EB%94%94%EC%99%80-%ED%81%B4%EB%9D%BC%EC%9D%B4%EC%96%B8%ED%8A%B8-%EC%8B%9C%ED%81%AC%EB%A6%BF-%ED%99%95%EC%9D%B8">클라이언트 아이디와 클라이언트 시크릿</a>을 추가해야 합니다.</p>
<pre class="prettyprint"><code class="language-sh">&gt; POST /v1/datalab/search HTTP/1.1
&gt; Host: openapi.naver.com
&gt; User-Agent: curl/7.49.1
&gt; Accept: */*
&gt; Content-Type: application/x-www-form-urlencoded; charset=UTF-8
&gt; X-Naver-Client-Id: {애플리케이션 등록 시 발급받은 클라이언트 아이디 값}
&gt; X-Naver-Client-Secret: {애플리케이션 등록 시 발급받은 클라이언트 시크릿 값}
&gt; Content-Length: 360
</code></pre>
<h4 id="요청-예">요청 예 <a class="header-anchor" href="/docs/serviceapi/datalab/search/search.md#요청-예" aria-hidden="true"><i class="xi-link"></i></a></h4>
<pre class="prettyprint"><code class="language-sh">curl https://openapi.naver.com/v1/datalab/search \
--header &quot;X-Naver-Client-Id: YOUR_CLIENT_ID&quot; \
--header &quot;X-Naver-Client-Secret: YOUR_CLIENT_SECRET&quot; \
--header &quot;Content-Type: application/json&quot; \
-d @&lt;(cat &lt;&lt;EOF
{
  &quot;startDate&quot;: &quot;2017-01-01&quot;,
  &quot;endDate&quot;: &quot;2017-04-30&quot;,
  &quot;timeUnit&quot;: &quot;month&quot;,
  &quot;keywordGroups&quot;: [
    {
      &quot;groupName&quot;: &quot;한글&quot;,
      &quot;keywords&quot;: [
        &quot;한글&quot;,
        &quot;korean&quot;
      ]
    },
    {
      &quot;groupName&quot;: &quot;영어&quot;,
      &quot;keywords&quot;: [
        &quot;영어&quot;,
        &quot;english&quot;
      ]
    }
  ],
  &quot;device&quot;: &quot;pc&quot;,
  &quot;ages&quot;: [
    &quot;1&quot;,
    &quot;2&quot;
  ],
  &quot;gender&quot;: &quot;f&quot;
}
EOF
)
</code></pre>
<h4 id="응답">응답 <a class="header-anchor" href="/docs/serviceapi/datalab/search/search.md#응답" aria-hidden="true"><i class="xi-link"></i></a></h4>
<p>응답에 성공하면 결괏값을 JSON 형식으로 반환합니다.</p>
<table>
<thead>
<tr>
<th style="width: 30%">속성</th>
<th style="width: 30%">타입</th>
<th style="width: 40%">설명</th>
</tr>
</thead>
<tbody>
<tr>
<td>startDate</td>
<td>string</td>
<td>조회 기간 시작 날짜(<code>yyyy-mm-dd</code> 형식).</td>
</tr>
<tr>
<td>endDate</td>
<td>string</td>
<td>조회 기간 종료 날짜(<code>yyyy-mm-dd</code> 형식)</td>
</tr>
<tr>
<td>timeUnit</td>
<td>string</td>
<td>구간 단위</td>
</tr>
<tr>
<td>results.title</td>
<td>string</td>
<td>주제어</td>
</tr>
<tr>
<td>results.keywords</td>
<td>array</td>
<td>주제어에 해당하는 검색어</td>
</tr>
<tr>
<td>results.data.period</td>
<td>string</td>
<td>구간별 시작 날짜(<code>yyyy-mm-dd</code> 형식)</td>
</tr>
<tr>
<td>results.data.ratio</td>
<td>string</td>
<td>구간별 검색량의 상대적 비율. 구간별 결과에서 가장 큰 값을 100으로 설정한 상댓값입니다.</td>
</tr>
</tbody>
</table>
<h4 id="응답-예">응답 예 <a class="header-anchor" href="/docs/serviceapi/datalab/search/search.md#응답-예" aria-hidden="true"><i class="xi-link"></i></a></h4>
<pre class="prettyprint"><code class="language-json">{
  &quot;startDate&quot;: &quot;2017-01-01&quot;,
  &quot;endDate&quot;: &quot;2017-04-30&quot;,
  &quot;timeUnit&quot;: &quot;month&quot;,
  &quot;results&quot;: [
    {
      &quot;title&quot;: &quot;한글&quot;,
      &quot;keywords&quot;: [
        &quot;한글&quot;,
        &quot;korean&quot;
      ],
      &quot;data&quot;: [
        {
          &quot;period&quot;: &quot;2017-01-01&quot;,
          &quot;ratio&quot;: 47.0
        },
        {
          &quot;period&quot;: &quot;2017-02-01&quot;,
          &quot;ratio&quot;: 53.23
        },
        {
          &quot;period&quot;: &quot;2017-03-01&quot;,
          &quot;ratio&quot;: 100.0
        },
        {
          &quot;period&quot;: &quot;2017-04-01&quot;,
          &quot;ratio&quot;: 85.32
        }
      ]
    },
    {
      &quot;title&quot;: &quot;영어&quot;,
      &quot;keywords&quot;: [
        &quot;영어&quot;,
        &quot;english&quot;
      ],
      &quot;data&quot;: [
        {
          &quot;period&quot;: &quot;2017-01-01&quot;,
          &quot;ratio&quot;: 40.08
        },
        {
          &quot;period&quot;: &quot;2017-02-01&quot;,
          &quot;ratio&quot;: 36.69
        },
        {
          &quot;period&quot;: &quot;2017-03-01&quot;,
          &quot;ratio&quot;: 52.11
        },
        {
          &quot;period&quot;: &quot;2017-04-01&quot;,
          &quot;ratio&quot;: 44.45
        }
      ]
    }
  ]
}
</code></pre>
<h3 id="오류-코드">오류 코드 <a class="header-anchor" href="/docs/serviceapi/datalab/search/search.md#오류-코드" aria-hidden="true"><i class="xi-link"></i></a></h3>
<p>통합 검색어 트렌드 API의 주요 오류 코드는 다음과 같습니다.</p>
<table>
<thead>
<tr>
<th style="width: 21.428571428571427%">오류 코드</th>
<th style="width: 21.428571428571427%">HTTP 상태 코드</th>
<th style="width: 28.57142857142857%">오류 메세지</th>
<th style="width: 28.57142857142857%">설명</th>
</tr>
</thead>
<tbody>
<tr>
<td>400</td>
<td>400</td>
<td>잘못된 요청</td>
<td>API 요청 URL의 프로토콜, 파라미터 등에 오류가 있는지 확인합니다.</td>
</tr>
<tr>
<td>500</td>
<td>500</td>
<td>서버 내부 오류</td>
<td>서버 내부에 오류가 발생했습니다. &quot;<a href="https://developers.naver.com/forum">개발자 포럼</a>&quot;에 오류를 신고해 주십시오.</td>
</tr>
</tbody>
</table>
<blockquote>
<p><strong>403 오류</strong><br>
개발자 센터에 등록한 애플리케이션에서 통합 검색어 트렌드 API를 사용하도록 설정하지 않았다면 'API 권한 없음'을 의미하는 403 오류가 발생할 수 있습니다. 403 오류가 발생했다면 네이버 개발자 센터의 <a href="https://developers.naver.com/apps/#/list"><strong>Application &gt; 내 애플리케이션</strong></a> 메뉴에서 오류가 발생한 애플리케이션의 <strong>API 설정</strong> 탭을 클릭한 다음 <strong>데이터랩 (검색어트렌드)</strong><!-- -->가 선택돼 있는지 확인해 보십시오.</p>
</blockquote>
<blockquote>
<p><strong>참고</strong><br>
네이버 오픈API 공통 오류 코드는 &quot;<a href="https://developers.naver.com/docs/common/openapiguide/">API 공통 가이드</a>&quot;의 '<a href="https://developers.naver.com/docs/common/openapiguide/errorcode.md">오류 코드</a>'를 참고하십시오.</p>
</blockquote>
<h2 id="통합-검색어-트렌드-api-구현-예제">통합 검색어 트렌드 API 구현 예제 <a class="header-anchor" href="/docs/serviceapi/datalab/search/search.md#통합-검색어-트렌드-api-구현-예제" aria-hidden="true"><i class="xi-link"></i></a></h2>
<p>다음은 각 언어별 통합 검색어 트렌드 API 구현 예제입니다.</p>
<ul>
<li><a href="/docs/serviceapi/datalab/search/search.md#java">Java</a></li>
<li><a href="/docs/serviceapi/datalab/search/search.md#php">PHP</a></li>
<li><a href="/docs/serviceapi/datalab/search/search.md#node-js">Node.js</a></li>
<li><a href="/docs/serviceapi/datalab/search/search.md#python">Python</a></li>
<li><a href="/docs/serviceapi/datalab/search/search.md#c">C#</a></li>
</ul>
<blockquote>
<p><strong>참고</strong></p>
<ul>
<li>샘플 코드에서 <code>YOUR_CLIENT_ID</code> 또는 <code>YOUR-CLIENT-ID</code>에는 애플리케이션을 등록하고 발급받은 클라이언트 아이디 값을 입력합니다.</li>
<li>샘플 코드에서 <code>YOUR_CLIENT_SECRET</code> 또는 <code>YOUR-CLIENT-SECRET</code>에는 애플리케이션을 등록하고 발급받은 클라이언트 시크릿 값을 입력합니다.</li>
</ul>
</blockquote>
<h3 id="java">Java <a class="header-anchor" href="/docs/serviceapi/datalab/search/search.md#java" aria-hidden="true"><i class="xi-link"></i></a></h3>
<pre class="prettyprint"><code class="language-java">import java.io.*;
import java.net.HttpURLConnection;
import java.net.MalformedURLException;
import java.net.URL;
import java.nio.charset.StandardCharsets;
import java.util.HashMap;
import java.util.Map;

public class ApiExamDatalabTrend {

    public static void main(String[] args) {
        String clientId = &quot;YOUR_CLIENT_ID&quot;; // 애플리케이션 클라이언트 아이디
        String clientSecret = &quot;YOUR_CLIENT_SECRET&quot;; // 애플리케이션 클라이언트 시크릿

        String apiUrl = &quot;https://openapi.naver.com/v1/datalab/search&quot;;

        Map&lt;String, String&gt; requestHeaders = new HashMap&lt;&gt;();
        requestHeaders.put(&quot;X-Naver-Client-Id&quot;, clientId);
        requestHeaders.put(&quot;X-Naver-Client-Secret&quot;, clientSecret);
        requestHeaders.put(&quot;Content-Type&quot;, &quot;application/json&quot;);

        String requestBody = &quot;{\&quot;startDate\&quot;:\&quot;2017-01-01\&quot;,&quot; +
                &quot;\&quot;endDate\&quot;:\&quot;2017-04-30\&quot;,&quot; +
                &quot;\&quot;timeUnit\&quot;:\&quot;month\&quot;,&quot; +
                &quot;\&quot;keywordGroups\&quot;:[{\&quot;groupName\&quot;:\&quot;한글\&quot;,&quot; + &quot;\&quot;keywords\&quot;:[\&quot;한글\&quot;,\&quot;korean\&quot;]},&quot; +
                &quot;{\&quot;groupName\&quot;:\&quot;영어\&quot;,&quot; + &quot;\&quot;keywords\&quot;:[\&quot;영어\&quot;,\&quot;english\&quot;]}],&quot; +
                &quot;\&quot;device\&quot;:\&quot;pc\&quot;,&quot; +
                &quot;\&quot;ages\&quot;:[\&quot;1\&quot;,\&quot;2\&quot;],&quot; +
                &quot;\&quot;gender\&quot;:\&quot;f\&quot;}&quot;;

        String responseBody = post(apiUrl, requestHeaders, requestBody);
        System.out.println(responseBody);
    }

    private static String post(String apiUrl, Map&lt;String, String&gt; requestHeaders, String requestBody) {
        HttpURLConnection con = connect(apiUrl);

        try {
            con.setRequestMethod(&quot;POST&quot;);
            for(Map.Entry&lt;String, String&gt; header :requestHeaders.entrySet()) {
                con.setRequestProperty(header.getKey(), header.getValue());
            }

            con.setDoOutput(true);
            try (DataOutputStream wr = new DataOutputStream(con.getOutputStream())) {
                wr.write(requestBody.getBytes());
                wr.flush();
            }

            int responseCode = con.getResponseCode();
            if (responseCode == HttpURLConnection.HTTP_OK) { // 정상 응답
                return readBody(con.getInputStream());
            } else {  // 에러 응답
                return readBody(con.getErrorStream());
            }
        } catch (IOException e) {
            throw new RuntimeException(&quot;API 요청과 응답 실패&quot;, e);
        } finally {
            con.disconnect(); // Connection을 재활용할 필요가 없는 프로세스일 경우
        }
    }

    private static HttpURLConnection connect(String apiUrl) {
        try {
            URL url = new URL(apiUrl);
            return (HttpURLConnection) url.openConnection();
        } catch (MalformedURLException e) {
            throw new RuntimeException(&quot;API URL이 잘못되었습니다. : &quot; + apiUrl, e);
        } catch (IOException e) {
            throw new RuntimeException(&quot;연결이 실패했습니다. : &quot; + apiUrl, e);
        }
    }

    private static String readBody(InputStream body) {
        InputStreamReader streamReader = new InputStreamReader(body, StandardCharsets.UTF_8);

        try (BufferedReader lineReader = new BufferedReader(streamReader)) {
            StringBuilder responseBody = new StringBuilder();

            String line;
            while ((line = lineReader.readLine()) != null) {
                responseBody.append(line);
            }

            return responseBody.toString();
        } catch (IOException e) {
            throw new RuntimeException(&quot;API 응답을 읽는데 실패했습니다.&quot;, e);
        }
    }
}

</code></pre>
<ul>
<li><a href="https://github.com/naver/naver-openapi-guide/blob/master/sample/java/APIExamDatalabTrend.java">GitHub에서 보기</a></li>
</ul>
<h3 id="php">PHP <a class="header-anchor" href="/docs/serviceapi/datalab/search/search.md#php" aria-hidden="true"><i class="xi-link"></i></a></h3>
<pre class="prettyprint"><code class="language-php">&lt;?php
  // 네이버 데이터랩 통합검색어 트렌드 Open API 예제
  $client_id = &quot;YOUR_CLIENT_ID&quot;; // 네이버 개발자센터에서 발급받은 CLIENT ID
  $client_secret = &quot;YOUR_CLIENT_SECRET&quot;;// 네이버 개발자센터에서 발급받은 CLIENT SECRET
  $url = &quot;https://openapi.naver.com/v1/datalab/search&quot;;
  $body = &quot;{\&quot;startDate\&quot;:\&quot;2017-01-01\&quot;,\&quot;endDate\&quot;:\&quot;2017-04-30\&quot;,\&quot;timeUnit\&quot;:\&quot;month\&quot;,\&quot;keywordGroups\&quot;:[{\&quot;groupName\&quot;:\&quot;한글\&quot;,\&quot;keywords\&quot;:[\&quot;한글\&quot;,\&quot;korean\&quot;]},{\&quot;groupName\&quot;:\&quot;영어\&quot;,\&quot;keywords\&quot;:[\&quot;영어\&quot;,\&quot;english\&quot;]}],\&quot;device\&quot;:\&quot;pc\&quot;,\&quot;ages\&quot;:[\&quot;1\&quot;,\&quot;2\&quot;],\&quot;gender\&quot;:\&quot;f\&quot;}&quot;;
  $ch = curl_init();
  curl_setopt($ch, CURLOPT_URL, $url);
  curl_setopt($ch, CURLOPT_POST, true);
  curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
  $headers = array();
  $headers[] = &quot;X-Naver-Client-Id: &quot;.$client_id;
  $headers[] = &quot;X-Naver-Client-Secret: &quot;.$client_secret;
  $headers[] = &quot;Content-Type: application/json&quot;;
  curl_setopt($ch, CURLOPT_HTTPHEADER, $headers);
  // SSL 이슈가 있을 경우, 아래 코드 주석 해제
  // curl_setopt($ch, CURLOPT_SSL_VERIFYPEER, 0);
  curl_setopt($ch, CURLOPT_POSTFIELDS, $body);
  $response = curl_exec ($ch);
  $status_code = curl_getinfo($ch, CURLINFO_HTTP_CODE);
  echo &quot;status_code:&quot;.$status_code.&quot; &quot;;
  curl_close ($ch);
  if($status_code == 200) {
      echo $response;
  } else {
      echo &quot;Error 내용:&quot;.$response;
  }
?&gt;
</code></pre>
<ul>
<li><a href="https://github.com/naver/naver-openapi-guide/blob/master/sample/php/APIExamDatalabTrend.php">GitHub에서 보기</a></li>
</ul>
<h3 id="node-js">Node.js <a class="header-anchor" href="/docs/serviceapi/datalab/search/search.md#node-js" aria-hidden="true"><i class="xi-link"></i></a></h3>
<pre class="prettyprint"><code class="language-js">var request = require(&#39;request&#39;);
var client_id = &#39;YOUR_CLIENT_ID&#39;;
var client_secret = &#39;YOUR_CLIENT_SECRET&#39;;
var api_url = &#39;https://openapi.naver.com/v1/datalab/search&#39;;
var request_body = {
    &quot;startDate&quot;: &quot;2017-01-01&quot;,
    &quot;endDate&quot;: &quot;2017-04-30&quot;,
    &quot;timeUnit&quot;: &quot;month&quot;,
    &quot;keywordGroups&quot;: [
        {
            &quot;groupName&quot;: &quot;한글&quot;,
            &quot;keywords&quot;: [
                &quot;한글&quot;,
                &quot;korean&quot;
            ]
        },
        {
            &quot;groupName&quot;: &quot;영어&quot;,
            &quot;keywords&quot;: [
                &quot;영어&quot;,
                &quot;english&quot;
            ]
        }
    ],
    &quot;device&quot;: &quot;pc&quot;,
    &quot;ages&quot;: [
        &quot;1&quot;,
        &quot;2&quot;
    ],
    &quot;gender&quot;: &quot;f&quot;
};

request.post({
        url: api_url,
        body: JSON.stringify(request_body),
        headers: {
            &#39;X-Naver-Client-Id&#39;: client_id,
            &#39;X-Naver-Client-Secret&#39;: client_secret,
            &#39;Content-Type&#39;: &#39;application/json&#39;
        }
    },
    function (error, response, body) {
        console.log(response.statusCode);
        console.log(body);
    });
</code></pre>
<ul>
<li><a href="https://github.com/naver/naver-openapi-guide/blob/master/sample/nodejs/APIExamDatalabTrend.js">GitHub에서 보기</a></li>
</ul>
<h3 id="python">Python <a class="header-anchor" href="/docs/serviceapi/datalab/search/search.md#python" aria-hidden="true"><i class="xi-link"></i></a></h3>
<pre class="prettyprint"><code class="language-python">#-*- coding: utf-8 -*-
import os
import sys
import urllib.request
client_id = &quot;YOUR_CLIENT_ID&quot;
client_secret = &quot;YOUR_CLIENT_SECRET&quot;
url = &quot;https://openapi.naver.com/v1/datalab/search&quot;;
body = &quot;{\&quot;startDate\&quot;:\&quot;2017-01-01\&quot;,\&quot;endDate\&quot;:\&quot;2017-04-30\&quot;,\&quot;timeUnit\&quot;:\&quot;month\&quot;,\&quot;keywordGroups\&quot;:[{\&quot;groupName\&quot;:\&quot;한글\&quot;,\&quot;keywords\&quot;:[\&quot;한글\&quot;,\&quot;korean\&quot;]},{\&quot;groupName\&quot;:\&quot;영어\&quot;,\&quot;keywords\&quot;:[\&quot;영어\&quot;,\&quot;english\&quot;]}],\&quot;device\&quot;:\&quot;pc\&quot;,\&quot;ages\&quot;:[\&quot;1\&quot;,\&quot;2\&quot;],\&quot;gender\&quot;:\&quot;f\&quot;}&quot;;

request = urllib.request.Request(url)
request.add_header(&quot;X-Naver-Client-Id&quot;,client_id)
request.add_header(&quot;X-Naver-Client-Secret&quot;,client_secret)
request.add_header(&quot;Content-Type&quot;,&quot;application/json&quot;)
response = urllib.request.urlopen(request, data=body.encode(&quot;utf-8&quot;))
rescode = response.getcode()
if(rescode==200):
    response_body = response.read()
    print(response_body.decode(&#39;utf-8&#39;))
else:
    print(&quot;Error Code:&quot; + rescode)
</code></pre>
<ul>
<li><a href="https://github.com/naver/naver-openapi-guide/blob/master/sample/python/APIExamDatalabTrend.py">GitHub에서 보기</a></li>
</ul>
<h3 id="c">C# <a class="header-anchor" href="/docs/serviceapi/datalab/search/search.md#c" aria-hidden="true"><i class="xi-link"></i></a></h3>
<pre class="prettyprint"><code class="language-csharp">using System;
using System.Net;
using System.Text;
using System.IO;

namespace NaverAPI_Guide
{
    public class APIExamDatalabTrend
    {
        static void Main(string[] args)
        {
            string url = &quot;https://openapi.naver.com/v1/datalab/search&quot;;
            HttpWebRequest request = (HttpWebRequest)WebRequest.Create(url);
            request.Headers.Add(&quot;X-Naver-Client-Id&quot;, &quot;YOUR-CLIENT-ID&quot;);
            request.Headers.Add(&quot;X-Naver-Client-Secret&quot;, &quot;YOUR-CLIENT-SECRET&quot;);
            request.ContentType = &quot;application/json&quot;;
            request.Method = &quot;POST&quot;;
            string body = &quot;{\&quot;startDate\&quot;:\&quot;2017-01-01\&quot;,\&quot;endDate\&quot;:\&quot;2017-04-30\&quot;,\&quot;timeUnit\&quot;:\&quot;month\&quot;,\&quot;keywordGroups\&quot;:[{\&quot;groupName\&quot;:\&quot;한글\&quot;,\&quot;keywords\&quot;:[\&quot;한글\&quot;,\&quot;korean\&quot;]},{\&quot;groupName\&quot;:\&quot;영어\&quot;,\&quot;keywords\&quot;:[\&quot;영어\&quot;,\&quot;english\&quot;]}],\&quot;device\&quot;:\&quot;pc\&quot;,\&quot;ages\&quot;:[\&quot;1\&quot;,\&quot;2\&quot;],\&quot;gender\&quot;:\&quot;f\&quot;}&quot;;
            byte[] byteDataParams = Encoding.UTF8.GetBytes(body);
            request.ContentLength = byteDataParams.Length;
            Stream st = request.GetRequestStream();
            st.Write(byteDataParams, 0, byteDataParams.Length);
            st.Close();
            HttpWebResponse response = (HttpWebResponse)request.GetResponse();
            Stream stream = response.GetResponseStream();
            StreamReader reader = new StreamReader(stream, Encoding.UTF8);
            string text = reader.ReadToEnd();
            stream.Close();
            response.Close();
            reader.Close();
            Console.WriteLine(text);
        }
    }
}
</code></pre>
<ul>
<li><a href="https://github.com/naver/naver-openapi-guide/blob/master/sample/c%23-asp.net/APIExamDatalabTren.cs">GitHub에서 보기</a></li>
</ul>
</div>
</div>
<div id="react-footer" style="display:none">
    


</div>
<script type="text/javascript" src="/inc/devcenter/dist/docs-serviceapi-datalab.fe8afb07cd7200cb634a.js" ></script>
<script type="text/javascript">
addEventListener('load', function (event) { PR.prettyPrint() }, false);
</script>

</body>
</html>


