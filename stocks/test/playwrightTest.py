import re
import sys
import os
import time
# 현재 파일의 디렉토리 경로를 구합니다.
current_dir = os.path.dirname(os.path.abspath(__file__))

# 상위 디렉토리의 경로를 추가합니다.
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from view.logView import writeLog as log
from playwright.sync_api import Page, expect
from bs4 import BeautifulSoup as bs

# url = "https://playwright.dev/"
url = 'http://data.krx.co.kr/contents/MDC/MDI/mdiLoader/index.cmd?menuId=MDC0201020104'
def test_has_title(page: Page):
    page.set_extra_http_headers({
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36'
    })
    page.goto(url)
    # time.sleep(5)
    # CSS 셀렉터로 특정 요소가 로드될 때까지 기다립니다.
    page.wait_for_selector('#jsMdiContent > div > div.CI-GRID-AREA.CI-GRID-ON-WINDOWS > div.CI-GRID-WRAPPER > div.CI-GRID-MAIN-WRAPPER > div.CI-GRID-BODY-WRAPPER > div > div > table > tbody', state='visible')

    # log.writeLog(f"title ? {response.body}")
    response = page.content()

    # 인코딩을 확인한 후 디코딩합니다.
    # 예를 들어, UTF-8로 디코딩
    response = response.encode('utf-8').decode('utf-8')

    # HTML 내용 확인
    # if response:
    #     log("HTML content retrieved successfully.")
    # else:
    #     log("Failed to retrieve HTML content.")

    beau = bs(response, "html.parser")
    beauParser = beau.select_one("#jsMdiContent > div.CI-MDI-CONTENT.active")
    # log(f"{beauParser.text}")
    log("-----")
    for item in beauParser:
        log(f" item ? {item.text}")
    log("====") 
    # log(print(beau))

    # 페이지 제목을 추출합니다.
    # title = beau.title.string if beau.title else 'No title found'
    # log(f"Title of the page: {title}")

    # # 모든 링크를 추출합니다.
    # for link in beau.find_all('a'):
    #     href = link.get('href')
    #     text = link.get_text()
    #     log(f"Link text: {text}, URL: {href}")
