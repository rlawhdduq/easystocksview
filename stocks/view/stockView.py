import sys
import os
import matplotlib.pyplot as plt
import time
import pytest
import pandas
import matplotlib.pyplot as plt
import matplotlib

from matplotlib import font_manager

from django.http import HttpResponse
from io import BytesIO
from playwright.sync_api import Page, expect, sync_playwright
from bs4 import BeautifulSoup as bs
from django.shortcuts import render

# 현재 파일의 디렉토리 경로를 구합니다.
current_dir = os.path.dirname(os.path.abspath(__file__))

# 상위 디렉토리의 경로를 추가합니다.
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)
from view.logView import writeLog as log

# 스크래핑 대상 사이트 url / 개별종목
url = 'http://data.krx.co.kr/contents/MDC/MDI/mdiLoader/index.cmd?menuId=MDC0201020103'
searchTxt = ""
def divMethod(request):
    if request.method == "GET":
        return searchTemplate(request)
    elif request.method == "POST":
        return getStockInfo(request)
    else: # 추후 Put, Delete 등 추가 된다면 분기처리 추가
        return
def searchTemplate(request):
    return render(request, 'stock/search.html')

# page 객체 설정
@pytest.fixture
def page():
    with sync_playwright() as p:
        # 브라우저를 headless 모드로 실행
        browser = p.chromium.launch()  # 백단실행
        # browser = p.chromium.launch(headless=False)  # UI를 볼 수 있도록 설정
        context = browser.new_context()
        page = context.new_page()
        yield page
        browser.close()
# request
#   searchTxt       검색 종목명
#   standardPrice   구매가격(평단가)
def getStockInfo(request):
    global searchTxt 
    searchTxt = request.POST.get("searchTxt")
    stockDate, stockPrice = getScraping() # 스크래핑 데이터 호출
     
    resBody = {"resCode":"N", "resData":""}
    if stockDate or stockPrice:
        standardPrice = request.POST.get('standardPrice')
        resBody["resData"] = drawScapringData(stockDate=stockDate, stockPrice=stockPrice, standardPrice=standardPrice)
        resBody["resMsg"]  = "Y"
    return resBody

def getScraping():
    with sync_playwright() as p:
        # 브라우저를 headless 모드로 실행
        # browser = p.chromium.launch()  # 백단실행
        browser = p.chromium.launch(headless=False)  # UI를 볼 수 있도록 설정
        context = browser.new_context()
        page = context.new_page()
        
        page.set_extra_http_headers({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36'
        })
        page.goto(url)

        # 해당 페이지가 로드 될 때 까지 대기
        page.wait_for_selector('#jsMdiContent > div > div.CI-GRID-AREA.CI-GRID-ON-WINDOWS > div.CI-GRID-WRAPPER > div.CI-GRID-MAIN-WRAPPER > div.CI-GRID-BODY-WRAPPER > div > div > table > tbody', state='visible')
        # 페이지가 로드되고 네트워크 요청이 완료될 때까지 대기
        page.wait_for_load_state('networkidle')

        # 페이지 로드 완료 후 검색어를 미리 지정해놓고 검색버튼 클릭
        global searchTxt
        page.fill("#tboxisuCd_finder_stkisu0_0", searchTxt)
        page.click("#btnisuCd_finder_stkisu0_0")

        # 모달창에 데이터 로드 되기 전 까지 대기
        page.wait_for_selector("#jsGrid_div__finder_stkisu0_0 > div > div > div.CI-TBODY-WRAPPER .jsRow, #jsGrid_div__finder_stkisu0_0 > div > div > div.CI-TBODY-WRAPPER .CI-EMPTY-ROW", state='visible', timeout=60000)

        # 모달의 내용 추출
        pageLocator = page.locator("#jsGrid__finder_stkisu0_0 > tbody")
        modal_content = pageLocator.inner_text()
        if not modal_content:
            log("데이터가 존재하지 않습니다.")
            return
        else:
            # 있으면 최소 1줄이라는거니까 첫 번째 tr에 클릭이벤트 실행하면 될듯?
            page.locator("#jsGrid__finder_stkisu0_0 > tbody > tr:nth-child(1)").click()

            # 조회버튼 클릭 후 최초 데이터 출력페이지가 로드 되고, 네트워크 요청이 완료될 때까지 다시 대기
            page.locator("#jsSearchButton").click()
            page.wait_for_load_state('networkidle')
            time.sleep(2)
            page.wait_for_selector('#jsMdiContent > div > div.CI-GRID-AREA.CI-GRID-ON-WINDOWS > div.CI-GRID-WRAPPER > div.CI-GRID-MAIN-WRAPPER > div.CI-GRID-BODY-WRAPPER > div > div > table > tbody > tr', state='visible')
            stocksData = page.locator("#jsMdiContent > div > div.CI-GRID-AREA.CI-GRID-ON-WINDOWS > div.CI-GRID-WRAPPER > div.CI-GRID-MAIN-WRAPPER > div.CI-GRID-BODY-WRAPPER > div > div > table > tbody > tr")
            stockDataCount = stocksData.count()
            scrapingDatas = {"data":stocksData, "count":stockDataCount}
            stockDate, stockPrice = scrapingDataProcess(scrapingDatas)
        return stockDate, stockPrice

def scrapingDataProcess(scrapingDatas):
    stockDate = []
    stockPrice = []
    for i in range(scrapingDatas["count"]):
        item = scrapingDatas["data"].nth(i)
        stockDate.append(item.locator("td[data-name='TRD_DD']").inner_text())
        stockPrice.append(int(item.locator("td[data-name='TDD_CLSPRC']").inner_text().replace(",", "")))
        # log(item.locator("td[data-name='TRD_DD']").inner_text()) # 일자
        # log(item.locator("td[data-name='TDD_CLSPRC']").inner_text()) # 가격
        # log(item.locator("td[data-name='CMPPREVDD_PRC'] > span").inner_text()) # 등락가
        # log(item.locator("td[data-name='FLUC_RT'] > span").inner_text()) # 등락폭
        # log(item.locator("td[data-name='TDD_OPNPRC']").inner_text()) # 시가
        # log(item.locator("td[data-name='TDD_HGPRC']").inner_text()) # 고가
        # log(item.locator("td[data-name='TDD_LWPRC']").inner_text()) # 저가
        # log(item.locator("td[data-name='ACC_TRDVOL']").inner_text()) # 거래량
        # log(item.locator("td[data-name='ACC_TRDVAL']").inner_text()) # 거래대금
        # log(item.locator("td[data-name='MKTCAP']").inner_text()) # 시가총액
        # log(item.locator("td[data-name='LIST_SHRS']").inner_text()) # 상장주식수
    return stockDate, stockPrice

def drawScapringData(stockDate, stockPrice, standardPrice):
    # stockSeries = pandas.Series(stockPrice, index=stockDate)
    stockDataFrame = pandas.DataFrame()
    stockDataFrame["일자"] = pandas.to_datetime(stockDate, format="%Y/%m/%d")
    stockDataFrame["종가"] = stockPrice
    stockDataFrame.sort_values(['일자','종가'], ascending=False)
    # stockDataFrame.sort_values(['일자'], ascending=True)
    # log(stockSeries)
    log(stockDataFrame)
    plt.figure(figsize=(12, 6))
    global searchTxt
    plt.title(searchTxt)
    standardLine = plt.axhline(y=int(standardPrice), color='r', linestyle='-', label='Horizontal Line')
    priceLine, = plt.plot(stockDataFrame['일자'], stockDataFrame['종가'], marker='o')
    plt.legend(handles=[standardLine, priceLine], labels=['구매가격', '종가'])
    plt.show()
    # sns.boxplot(x='일자', y='종가', data = stockDataFrame) # seaborn
    # stockDataFrame.plot()

    buf = BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)

    return HttpResponse(buf.read(), content_type='image/png')