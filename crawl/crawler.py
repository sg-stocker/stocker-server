import time
import json
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
from datetime import datetime, timedelta


# 클러스터링된 주별 대표 뉴스들의 url
SA_URL_0304_0310 = "https://search.naver.com/search.naver?where=news&sm=tab_tnw&query=%EC%82%BC%EC%84%B1%EC%A0%84%EC%9E%90&sort=0&photo=0&field=0&pd=3&ds=2024.03.04&de=2024.03.10&mynews=0&office_type=0&office_section_code=0&news_office_checked=&related=1&docid=0010014553331&nso=so:r,p:from20240304to20240310,a:all"
SA_URL_0311_0317 = "https://search.naver.com/search.naver?where=news&sm=tab_tnw&query=%EC%82%BC%EC%84%B1%EC%A0%84%EC%9E%90&sort=0&photo=0&field=0&pd=3&ds=2024.03.11&de=2024.03.17&mynews=0&office_type=0&office_section_code=0&news_office_checked=&related=1&docid=0090005273401&nso=so:r,p:from20240311to20240317,a:all"
SA_URL_0318_0324 = "https://search.naver.com/search.naver?where=news&sm=tab_tnw&query=%EC%82%BC%EC%84%B1%EC%A0%84%EC%9E%90&sort=0&photo=0&field=0&pd=3&ds=2024.03.18&de=2024.03.24&mynews=0&office_type=0&office_section_code=0&news_office_checked=&related=1&docid=0150004963698&nso=so:r,p:from20240318to20240324,a:all"
SA_URL_0325_0331 = "https://search.naver.com/search.naver?where=news&sm=tab_tnw&query=%EC%82%BC%EC%84%B1%EC%A0%84%EC%9E%90&sort=0&photo=0&field=0&pd=3&ds=2024.03.25&de=2024.03.31&mynews=0&office_type=0&office_section_code=0&news_office_checked=&related=1&docid=0180005702954&nso=so:r,p:from20240325to20240331,a:all"
SA_URL_0401_0407 = "https://search.naver.com/search.naver?where=news&sm=tab_tnw&query=%EC%82%BC%EC%84%B1%EC%A0%84%EC%9E%90&sort=0&photo=0&field=0&pd=3&ds=2024.04.01&de=2024.04.07&mynews=0&office_type=0&office_section_code=0&news_office_checked=&related=1&docid=0920002327159&nso=so:r,p:from20240401to20240407,a:all"
SA_URL_0408_0414 = "https://search.naver.com/search.naver?where=news&sm=tab_tnw&query=%EC%82%BC%EC%84%B1%EC%A0%84%EC%9E%90&sort=0&photo=0&field=0&pd=3&ds=2024.04.08&de=2024.04.14&mynews=0&office_type=0&office_section_code=0&news_office_checked=&related=1&docid=0030012490112&nso=so:r,p:from20240408to20240414,a:all"
SA_URL_0415_0421 = "https://search.naver.com/search.naver?where=news&sm=tab_tnw&query=%EC%82%BC%EC%84%B1%EC%A0%84%EC%9E%90&sort=0&photo=0&field=0&pd=3&ds=2024.04.15&de=2024.04.21&mynews=0&office_type=0&office_section_code=0&news_office_checked=&related=1&docid=0150004975205&nso=so:r,p:from20240415to20240421,a:all"
SA_URL_0422_0428 = "https://search.naver.com/search.naver?where=news&sm=tab_tnw&query=%EC%82%BC%EC%84%B1%EC%A0%84%EC%9E%90&sort=0&photo=0&field=0&pd=3&ds=2024.04.22&de=2024.04.28&mynews=0&office_type=0&office_section_code=0&news_office_checked=&related=1&docid=0150004978196&nso=so:r,p:from20240422to20240428,a:all"
SA_URL_0429_0505 = "https://search.naver.com/search.naver?where=news&sm=tab_tnw&query=%EC%82%BC%EC%84%B1%EC%A0%84%EC%9E%90&sort=0&photo=0&field=0&pd=3&ds=2024.04.29&de=2024.05.05&mynews=0&office_type=0&office_section_code=0&news_office_checked=&related=1&docid=0030012525158&nso=so:r,p:from20240429to20240505,a:all"
SA_URL_0506_0512 = "https://search.naver.com/search.naver?where=news&sm=tab_tnw&query=%EC%82%BC%EC%84%B1%EC%A0%84%EC%9E%90&sort=0&photo=0&field=0&pd=3&ds=2024.05.06&de=2024.05.12&mynews=0&office_type=0&office_section_code=0&news_office_checked=&related=1&docid=1190002829053&nso=so:r,p:from20240506to20240512,a:all"
SA_URL_0513_0519 = "https://search.naver.com/search.naver?where=news&sm=tab_tnw&query=%EC%82%BC%EC%84%B1%EC%A0%84%EC%9E%90&sort=0&photo=0&field=0&pd=3&ds=2024.05.13&de=2024.05.19&mynews=0&office_type=0&office_section_code=0&news_office_checked=&related=1&docid=0310000837374&nso=so:r,p:from20240513to20240519,a:all"
SA_URL_0520_0526 = "https://search.naver.com/search.naver?where=news&sm=tab_tnw&query=%EC%82%BC%EC%84%B1%EC%A0%84%EC%9E%90&sort=0&photo=0&field=0&pd=3&ds=2024.05.20&de=2024.05.26&mynews=0&office_type=0&office_section_code=0&news_office_checked=&related=1&docid=0010014705455&nso=so:r,p:from20240520to20240526,a:all"

SK_URL_0304_0310 = "https://search.naver.com/search.naver?where=news&sm=tab_tnw&query=SK%ED%95%98%EC%9D%B4%EB%8B%89%EC%8A%A4&sort=0&photo=0&field=0&pd=3&ds=2024.03.04&de=2024.03.10&mynews=0&office_type=0&office_section_code=0&news_office_checked=&related=1&docid=0810003435900&nso=so:r,p:from20240304to20240310,a:all"
SK_URL_0311_0317 = "https://search.naver.com/search.naver?where=news&sm=tab_tnw&query=SK%ED%95%98%EC%9D%B4%EB%8B%89%EC%8A%A4&sort=0&photo=0&field=0&pd=3&ds=2024.03.11&de=2024.03.17&mynews=0&office_type=0&office_section_code=0&news_office_checked=&related=1&docid=0010014557547&nso=so:r,p:from20240311to20240317,a:all"
SK_URL_0318_0324 = "https://search.naver.com/search.naver?where=news&sm=tab_tnw&query=SK%ED%95%98%EC%9D%B4%EB%8B%89%EC%8A%A4&sort=0&photo=0&field=0&pd=3&ds=2024.03.18&de=2024.03.24&mynews=0&office_type=0&office_section_code=0&news_office_checked=&related=1&docid=0090005276683&nso=so:r,p:from20240318to20240324,a:all"
SK_URL_0325_0331 = "https://search.naver.com/search.naver?where=news&sm=tab_tnw&query=SK%ED%95%98%EC%9D%B4%EB%8B%89%EC%8A%A4&sort=0&photo=0&field=0&pd=3&ds=2024.03.25&de=2024.03.31&mynews=0&office_type=0&office_section_code=0&news_office_checked=&related=1&docid=3660000981160&nso=so:r,p:from20240325to20240331,a:all"
SK_URL_0401_0407 = "https://search.naver.com/search.naver?where=news&sm=tab_tnw&query=SK%ED%95%98%EC%9D%B4%EB%8B%89%EC%8A%A4&sort=0&photo=0&field=0&pd=3&ds=2024.04.01&de=2024.04.07&mynews=0&office_type=0&office_section_code=0&news_office_checked=&related=1&docid=0010014609278&nso=so:r,p:from20240401to20240407,a:all"
SK_URL_0408_0414 = "https://search.naver.com/search.naver?where=news&sm=tab_tnw&query=SK%ED%95%98%EC%9D%B4%EB%8B%89%EC%8A%A4&sort=0&photo=0&field=0&pd=3&ds=2024.04.08&de=2024.04.14&mynews=0&office_type=0&office_section_code=0&news_office_checked=&related=1&docid=0010014624919&nso=so:r,p:from20240408to20240414,a:all"
SK_URL_0415_0421 = "https://search.naver.com/search.naver?where=news&sm=tab_tnw&query=SK%ED%95%98%EC%9D%B4%EB%8B%89%EC%8A%A4&sort=0&photo=0&field=0&pd=3&ds=2024.04.15&de=2024.04.21&mynews=0&office_type=0&office_section_code=0&news_office_checked=&related=1&docid=0230003829308&nso=so:r,p:from20240415to20240421,a:all"
SK_URL_0422_0428 = "https://search.naver.com/search.naver?where=news&sm=tab_tnw&query=SK%ED%95%98%EC%9D%B4%EB%8B%89%EC%8A%A4&sort=0&photo=0&field=0&pd=3&ds=2024.04.22&de=2024.04.28&mynews=0&office_type=0&office_section_code=0&news_office_checked=&related=1&docid=0230003830437&nso=so:r,p:from20240422to20240428,a:all"
SK_URL_0429_0505 = "https://search.naver.com/search.naver?where=news&sm=tab_tnw&query=SK%ED%95%98%EC%9D%B4%EB%8B%89%EC%8A%A4&sort=0&photo=0&field=0&pd=3&ds=2024.04.29&de=2024.05.05&mynews=0&office_type=0&office_section_code=0&news_office_checked=&related=1&docid=0230003831887&nso=so:r,p:from20240429to20240505,a:all"
SK_URL_0506_0512 = "https://search.naver.com/search.naver?where=news&sm=tab_tnw&query=SK%ED%95%98%EC%9D%B4%EB%8B%89%EC%8A%A4&sort=0&photo=0&field=0&pd=3&ds=2024.05.06&de=2024.05.12&mynews=0&office_type=0&office_section_code=0&news_office_checked=&related=1&docid=0150004982795&nso=so:r,p:from20240506to20240512,a:all"
SK_URL_0513_0519 = "https://search.naver.com/search.naver?where=news&sm=tab_tnw&query=SK%ED%95%98%EC%9D%B4%EB%8B%89%EC%8A%A4&sort=0&photo=0&field=0&pd=3&ds=2024.05.13&de=2024.05.19&mynews=0&office_type=0&office_section_code=0&news_office_checked=&related=1&docid=0300003205753&nso=so:r,p:from20240513to20240519,a:all"
SK_URL_0520_0526 = "https://search.naver.com/search.naver?where=news&sm=tab_tnw&query=SK%ED%95%98%EC%9D%B4%EB%8B%89%EC%8A%A4&sort=0&photo=0&field=0&pd=3&ds=2024.05.20&de=2024.05.26&mynews=0&office_type=0&office_section_code=0&news_office_checked=&related=1&docid=3660000994067&nso=so:r,p:from20240520to20240526,a:all"


SAMSUNG_TICKER = "005930"
SAMSUNG_URLS= [SA_URL_0304_0310, SA_URL_0311_0317, SA_URL_0318_0324, SA_URL_0325_0331,
        SA_URL_0401_0407, SA_URL_0408_0414, SA_URL_0415_0421, SA_URL_0422_0428,
        SA_URL_0429_0505, SA_URL_0506_0512, SA_URL_0513_0519, SA_URL_0520_0526]

SK_TICKER = "000660"
SK_URLS= [SK_URL_0304_0310, SK_URL_0311_0317, SK_URL_0318_0324, SK_URL_0325_0331,
        SK_URL_0401_0407, SK_URL_0408_0414, SK_URL_0415_0421, SK_URL_0422_0428,
        SK_URL_0429_0505, SK_URL_0506_0512, SK_URL_0513_0519, SK_URL_0520_0526]

# TODO 여기서 조작
ticker = SK_TICKER
urls = SK_URLS

for url in urls:
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

        title = title_element.get_text() if title_element else None
        description = description_element.get_text() if description_element else None
        url = url_element['href'] if url_element else None

        if len(thumbnail_elements) <= 1:  # 뉴스회사 로고가 항상 1개 존재
            thumbnail = None
        else:
            element = thumbnail_elements[1]
            if 'data-lazysrc' in element.attrs:
                thumbnail = element['data-lazysrc']
            elif 'src' in element.attrs:
                thumbnail = element['src']
            else:
                thumbnail = None

        if len(date_elements) == 1:
            date = date_elements[0].get_text()
        elif len(date_elements) == 2:   # "3면 1단", "2면 TOP" 와 같은게 함께 있을 때 처리
            date = date_elements[1].get_text()
        else:
            date = None

        # 최근기사들은 날짜가 아닌 x일전으로 되어 있어서 처리 필요 ex.7일전
        if date and date[-1] == "전":
            if "일" in date:
                num = int(date[:date.find('일')])
                d = datetime.today() - timedelta(days=num)
                date = d.strftime('%Y.%m.%d.')
            elif "주" in date: # 그냥 end_date로 하는 수 밖에 없다
                date = end_date[:4]+ "." + end_date[5:7]+"."+end_date[8:]+"."

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
    with open(f'./data/{ticker}/{start_date}_{end_date}.json', 'w', encoding='utf-8') as f:
        json.dump(news_items, f, ensure_ascii=False, indent=4)