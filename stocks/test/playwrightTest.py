import re
import sys
import os
import time
import pytest
import pandas
import matplotlib.pyplot as plt
import matplotlib
from matplotlib import font_manager





# 현재 파일의 디렉토리 경로를 구합니다.
current_dir = os.path.dirname(os.path.abspath(__file__))

# 상위 디렉토리의 경로를 추가합니다.
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)
import seaborn as sns
from view.logView import writeLog as log
from playwright.sync_api import Page, expect, sync_playwright
from bs4 import BeautifulSoup as bs

#jsGrid__finder_stkisu0_0 > tbody > tr:nth-child(1)
# url = "https://playwright.dev/"
# url = 'http://data.krx.co.kr/contents/MDC/MDI/mdiLoader/index.cmd?menuId=MDC0201020104' # 전체 종목
url = 'http://data.krx.co.kr/contents/MDC/MDI/mdiLoader/index.cmd?menuId=MDC0201020103' # 개별 종목
def test_has_title(page: Page):
    page.set_extra_http_headers({
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36'
    })
    page.goto(url)
    # time.sleep(5)
    # CSS 셀렉터로 특정 요소가 로드될 때까지 기다립니다.
    page.wait_for_selector('#jsMdiContent > div > div.CI-GRID-AREA.CI-GRID-ON-WINDOWS > div.CI-GRID-WRAPPER > div.CI-GRID-MAIN-WRAPPER > div.CI-GRID-BODY-WRAPPER > div > div > table > tbody', state='visible')
    # page.wait_for_selector("#jsMdiContent > div > div.CI-GRID-AREA.CI-GRID-ON-WINDOWS > div.CI-GRID-WRAPPER > div.CI-GRID-MAIN-WRAPPER > div.CI-GRID-BODY-WRAPPER > div > div > table", state='visible')
    # 지정된 위치로 가서 데이터 추출

    # log.writeLog(f"title ? {response.body}")
    # response = page.content()
    response = page.locator("#jsMdiContent > div > div.CI-GRID-AREA.CI-GRID-ON-WINDOWS > div.CI-GRID-WRAPPER > div.CI-GRID-MAIN-WRAPPER > div.CI-GRID-BODY-WRAPPER > div > div > table > tbody").all_inner_texts()
    response = page.locator("#jsMdiContent > div > div.CI-GRID-AREA.CI-GRID-ON-WINDOWS > div.CI-GRID-WRAPPER > div.CI-GRID-MAIN-WRAPPER > div.CI-GRID-BODY-WRAPPER > div > div > table").all_inner_texts()
    for item in response:
        log(item)
    # 인코딩을 확인한 후 디코딩합니다.
    # 예를 들어, UTF-8로 디코딩
    # response = response.encode('utf-8').decode('utf-8')
    # HTML 내용 확인
    if response:
        log("HTML content retrieved successfully.")
    else:
        log("Failed to retrieve HTML content.")

    log("res2 "+response)
    beau = bs(response, "html.parser")
    log(beau)
    # beauParser = beau.select_one("#jsMdiContent > div.CI-MDI-CONTENT.active")
    
    # beauParser = beau.select_one("#jsMdiContent > div.CI-MDI-CONTENT.active")
    
    # log(f"{beauParser}")
    log("-----")
    # for item in beauParser:
    #     log(f" item ? {item}")
    # log("====") 
    # log(print(beau))

    # 페이지 제목을 추출합니다.
    # title = beau.title.string if beau.title else 'No title found'
    # log(f"Title of the page: {title}")

    # # 모든 링크를 추출합니다.
    # for link in beau.find_all('a'):
    #     href = link.get('href')
    #     text = link.get_text()
    #     log(f"Link text: {text}, URL: {href}")
    return
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

def test_modalEvent(page):
    page.set_extra_http_headers({
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36'
    })
    # page.on("console", lambda msg: log("Console log:"+msg.text))
    page.goto(url)

    # 해당 페이지가 로드 될 때 까지 대기
    page.wait_for_selector('#jsMdiContent > div > div.CI-GRID-AREA.CI-GRID-ON-WINDOWS > div.CI-GRID-WRAPPER > div.CI-GRID-MAIN-WRAPPER > div.CI-GRID-BODY-WRAPPER > div > div > table > tbody', state='visible')
    # response = page.locator("#jsMdiContent > div > div.CI-GRID-AREA.CI-GRID-ON-WINDOWS > div.CI-GRID-WRAPPER > div.CI-GRID-MAIN-WRAPPER > div.CI-GRID-BODY-WRAPPER > div > div > table > tbody")
    # 페이지가 로드되고 네트워크 요청이 완료될 때까지 대기
    page.wait_for_load_state('networkidle')

    log("checkPoint3")

    # 페이지 로드 완료 후 검색어를 미리 지정해놓고 검색버튼 클릭
    searchTxt = "KG모빌리티"
    standardPrice = 8700
    page.fill("#tboxisuCd_finder_stkisu0_0", searchTxt)
    page.click("#btnisuCd_finder_stkisu0_0")

    log("checkPoint4")
    # 모달창에 데이터 로드 되기 전 까지 대기
    page.wait_for_selector("#jsGrid_div__finder_stkisu0_0 > div > div > div.CI-TBODY-WRAPPER .jsRow, #jsGrid_div__finder_stkisu0_0 > div > div > div.CI-TBODY-WRAPPER .CI-EMPTY-ROW", state='visible', timeout=60000)

    # 검색 데이터 채운 후 검색버튼 실행
    # page.click("#searchBtn__finder_stkisu0_0")

    # 모달의 내용 추출
    pageLocator = page.locator("#jsGrid__finder_stkisu0_0 > tbody")
    modal_content = pageLocator.inner_text()
    if not modal_content:
        log("데이터가 존재하지 않습니다.")
        return
    else:
        # 있으면 최소 1줄이라는거니까 첫 번째 tr에 클릭이벤트 실행하면 될듯?
        page.locator("#jsGrid__finder_stkisu0_0 > tbody > tr:nth-child(1)").click()
        # log(modal_content) # 데이터 출력

        # 조회버튼 클릭 후 최초 데이터 출력페이지가 로드 되고, 네트워크 요청이 완료될 때까지 다시 대기
        page.locator("#jsSearchButton").click()
        page.wait_for_load_state('networkidle')
        time.sleep(2)
        page.wait_for_selector('#jsMdiContent > div > div.CI-GRID-AREA.CI-GRID-ON-WINDOWS > div.CI-GRID-WRAPPER > div.CI-GRID-MAIN-WRAPPER > div.CI-GRID-BODY-WRAPPER > div > div > table > tbody > tr', state='visible')
        stocksData = page.locator("#jsMdiContent > div > div.CI-GRID-AREA.CI-GRID-ON-WINDOWS > div.CI-GRID-WRAPPER > div.CI-GRID-MAIN-WRAPPER > div.CI-GRID-BODY-WRAPPER > div > div > table > tbody > tr")
        stockDataCount = stocksData.count()

        stockDate = []
        stockPrice = []
        for i in range(stockDataCount):
            item = stocksData.nth(i)
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
        stockSeries = pandas.Series(stockPrice, index=stockDate)
        stockDataFrame = pandas.DataFrame()
        stockDataFrame["일자"] = pandas.to_datetime(stockDate, format="%Y/%m/%d")
        stockDataFrame["종가"] = stockPrice
        stockDataFrame.sort_values(['일자','종가'], ascending=False)
        # stockDataFrame.sort_values(['일자'], ascending=True)
        # log(stockSeries)
        # log(stockDataFrame)
        plt.figure(figsize=(12, 6))
        standardLine = plt.axhline(y=standardPrice, color='r', linestyle='-', label='Horizontal Line')
        priceLine, = plt.plot(stockDataFrame['일자'], stockDataFrame['종가'], marker='o')
        plt.legend(handles=[standardLine, priceLine], labels=['구매가격', '현재가'])
        plt.show()
        # sns.boxplot(x='일자', y='종가', data = stockDataFrame) # seaborn
        # stockDataFrame.plot()
    return
def test_sys():
    
    for item in font_manager.fontManager.ttflist:
        log(item.name)
