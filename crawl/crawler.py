import time
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup


# 클러스터링된 뉴스의 url
URL_0304_0310 = "https://search.naver.com/search.naver?where=news&sm=tab_tnw&query=%EC%82%BC%EC%84%B1%EC%A0%84%EC%9E%90&sort=0&photo=0&field=0&pd=3&ds=2024.03.04&de=2024.03.10&mynews=0&office_type=0&office_section_code=0&news_office_checked=&related=1&docid=0010014553331&nso=so:r,p:from20240304to20240310,a:all"
URL_0311_0317 = None
URL_0318_0324 = None

# Define the URL
url = URL_0304_0310
# url에서 검색구간 날짜 추출
start_date = url[url.find('ds')+3:url.find('ds')+13]
end_date = url[url.find('de')+3:url.find('de')+13]

# Setup Selenium WebDriver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.get(url)

# Scroll to the bottom of the page to load all news items
last_height = driver.execute_script("return document.body.scrollHeight")
while True:
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)  # Wait for the page to load
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break
    last_height = new_height

# Parse the page content with BeautifulSoup
soup = BeautifulSoup(driver.page_source, 'html.parser')
driver.quit()

# Extract the relevant information
news_items = []
for item in soup.select('li.bx'):
    title_element = item.select_one('a.news_tit')
    description_element = item.select_one('div.news_dsc')
    url_element = item.select_one('a.news_tit')
    thumbnail_elements = item.select('img')
    date_elements = item.select('span.info')
    print(date_elements)

    title = title_element.get_text() if title_element else None
    description = description_element.get_text() if description_element else None
    url = url_element['href'] if url_element else None
    thumbnail = thumbnail_elements[1]['src'] if len(thumbnail_elements)>1 else None

    if len(date_elements) == 1:
        date = date_elements[0].get_text()
    elif len(date_elements) == 2:   # 3면 1단, 2면 TOP 와 같은게 함께 있을 때
        date_elements[1].get_text()
    else:
        date = None

    if title and description and url and date:  # thumnail은 없을 수 있다!
        # DB column명에 대응되도록 저장
        news_items.append({
            'date': date,
            'title': title,
            'summary': description,
            'url': url,
            'image_url': thumbnail,
        })

# Save the data to a JSON file
with open(f'./data/{start_date}_{end_date}.json', 'w', encoding='utf-8') as f:
    json.dump(news_items, f, ensure_ascii=False, indent=4)
