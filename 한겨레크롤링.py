#[한겨례의 경우]

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
import pandas as pd
import time

# 크롬 드라이버 경로 설정
path = "C:/Users/crazn/OneDrive/바탕 화면/크롬드라이버/chromedriver-win64/chromedriver.exe"

# 크롤링할 주소
base_url = "https://news.naver.com/main/list.naver?mode=LPOD&mid=sec&oid=028&date=20240410&page={}"

# 크롬 드라이버 사용
service = Service(executable_path=path)
options = webdriver.ChromeOptions()
driver = webdriver.Chrome(service=service)

# 페이지별로 크롤링한 정보를 저장할 리스트 생성
title_list = []
time_list = []

# 페이지별로 크롤링
start_page = 1
end_page = 1  # 예시로 1페이지까지만 크롤링

for page in range(start_page, end_page + 1):
    url = base_url.format(page)
    driver.get(url)
    driver.implicitly_wait(10)
    
    # 페이지 소스 가져오기
    page_source = driver.page_source
    
    # BeautifulSoup으로 페이지 소스 파싱
    soup = BeautifulSoup(page_source, 'html.parser')
    
    # 모든 <a> 태그 찾기
    links = soup.find_all('a', class_='nclicks(cnt_flashart)')
    
    # 각 링크의 주소에 접속하여 제목과 시간 가져오기
    for link in links:
        link_url = link['href']
        driver.get(link_url)
        driver.implicitly_wait(10)
        link_source = driver.page_source
        link_soup = BeautifulSoup(link_source, 'html.parser')
        
        # 제목 추출
        title_element = link_soup.find('h2', class_='media_end_head_headline')
        if title_element:
            title = title_element.span.get_text(strip=True)
            title_list.append(title)
        else:
            title_list.append("제목 정보 없음")
        
        # 시간 추출
        time_element = link_soup.find('span', class_='media_end_head_info_datestamp_time _ARTICLE_DATE_TIME')
        if time_element:
            time = time_element['data-date-time']
            time_list.append(time)
        else:
            time_list.append("시간 정보 없음")

# DataFrame 생성
df = pd.DataFrame({"제목": title_list, "시간": time_list})

# DataFrame을 엑셀 파일로 저장
df.to_excel("news_data.xlsx", index=False)

# 결과 출력
print("DataFrame을 엑셀 파일로 저장했습니다.")

# 웹 드라이버 종료
driver.quit()

import pandas as pd

# 엑셀 파일 경로
excel_file_path = "news_data.xlsx"

# 엑셀 파일 열기
df = pd.read_excel(excel_file_path)

# DataFrame 출력
print(df)
