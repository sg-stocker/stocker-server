import requests
import json
from bs4 import BeautifulSoup

# 클러스터링된 뉴스의 url
URL_0304_0310 = "https://search.naver.com/search.naver?where=news&sm=tab_tnw&query=%EC%82%BC%EC%84%B1%EC%A0%84%EC%9E%90&sort=0&photo=0&field=0&pd=3&ds=2024.03.04&de=2024.03.10&mynews=0&office_type=0&office_section_code=0&news_office_checked=&related=1&docid=0010014553331&nso=so:r,p:from20240304to20240310,a:all"


# Define the URL
url = URL_0304_0310
# url에서 검색구간 날짜 추출
start_date = url[url.find('ds')+3:url.find('ds')+13]
end_date = url[url.find('de')+3:url.find('de')+13]

# Send a request to the URL
response = requests.get(url)
response.raise_for_status()  # Raise an exception for HTTP errors

# Parse the HTML content using BeautifulSoup
soup = BeautifulSoup(response.text, 'html.parser')

# Extract the relevant information
news_items = []
for item in soup.select('li.bx'):
    title_element = item.select_one('a.news_tit')
    description_element = item.select_one('div.news_dsc')
    url_element = item.select_one('a.news_tit')
    thumbnail_elements = item.select('img')
    date_element = item.select_one('span.info')

    title = title_element.get_text() if title_element else None
    description = description_element.get_text() if description_element else None
    url = url_element['href'] if url_element else None
    thumbnail = thumbnail_elements[1]['data-lazysrc'] if thumbnail_elements else None
    date = date_element.get_text() if date_element else None

    if title and description and url and thumbnail and date:
        news_items.append({
            'title': title,
            'description': description,
            'url': url,
            'thumbnail': thumbnail,
            'date': date
        })

with open(f'./data/{start_date}_{end_date}', 'w', encoding='utf-8') as f:
    json.dump(news_items, f, ensure_ascii=False, indent=4)
